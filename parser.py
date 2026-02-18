import sys
import re
from pathlib import Path

from rdflib import Graph
from rdflib.exceptions import ParserError

# Some parsers raise more specific exceptions (e.g., BadSyntax for Turtle/N3).
try:
    from rdflib.plugins.parsers.notation3 import BadSyntax
except Exception:  # pragma: no cover
    BadSyntax = None

# Optional reasoning
try:
    from owlrl import DeductiveClosure, OWLRL_Semantics
    OWLRL_AVAILABLE = True
except ImportError:
    OWLRL_AVAILABLE = False


def read_text_best_effort(path: Path):
    """
    Read as bytes and decode best-effort into text.
    Prefer UTF-8; fall back to latin-1 (lossless mapping) if needed.
    """
    raw = path.read_bytes()
    try:
        txt = raw.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        txt = raw.decode("latin-1")
        enc = "latin-1"
    return raw, txt, enc


def print_error_with_location(path: Path, err: Exception, text: str, context_lines: int = 2):
    """
    Try to extract (line, column) from common rdflib exceptions and print context.
    """
    line = None
    col = None

    # Turtle/N3 often raises BadSyntax with .lines and .num, etc.
    if BadSyntax is not None and isinstance(err, BadSyntax):
        # BadSyntax typically has attributes:
        #   err.lines (list of lines), err.startLine, err.startColumn, err.message
        line = getattr(err, "startLine", None)
        col = getattr(err, "startColumn", None)

    # Many XML parsing errors embed "line X, column Y" in the message
    msg = str(err)
    m = re.search(r"line\s+(\d+)[^\d]+column\s+(\d+)", msg, flags=re.IGNORECASE)
    if m:
        line = line or int(m.group(1))
        col = col or int(m.group(2))

    # Some exceptions may expose .lineno / .offset
    line = line or getattr(err, "lineno", None)
    col = col or getattr(err, "offset", None)

    print("❌ Parse failed.")
    print(f"   File: {path}")
    print(f"   Error: {err.__class__.__name__}: {msg}")

    if line is None:
        print("\n⚠️  Could not reliably extract line/column from this error.")
        print("   Tip: try specifying the correct format explicitly, e.g. --format xml or --format turtle.\n")
        return None, None

    print(f"\n📍 Error location: line {line}" + (f", column {col}" if col is not None else ""))

    # Print a snippet around the error line
    lines = text.splitlines()
    idx = max(0, line - 1)  # 1-based -> 0-based
    start = max(0, idx - context_lines)
    end = min(len(lines), idx + context_lines + 1)

    print("\n--- Context ---")
    for i in range(start, end):
        prefix = ">>" if i == idx else "  "
        ln = i + 1
        print(f"{prefix} {ln:6d}: {lines[i]}")
        # caret under column if available and this is the error line
        if i == idx and col is not None and col > 0:
            # col is 1-based in many messages; normalize gently
            caret_pos = max(0, col - 1)
            print(" " * (10 + caret_pos) + "^")
    print("---------------\n")

    return line, col


def safe_auto_fix(text: str, assume_xml: bool):
    """
    Apply conservative fixes that commonly break parsers:
    - Remove UTF-8 BOM
    - Remove NUL bytes
    - Normalize smart quotes to ASCII quotes
    - Normalize line endings
    - (XML only, optional) Escape stray ampersands not part of an entity
    Returns (fixed_text, list_of_changes)
    """
    changes = []
    fixed = text

    # BOM (in text form)
    if fixed.startswith("\ufeff"):
        fixed = fixed.lstrip("\ufeff")
        changes.append("removed UTF-8 BOM")

    # NULs
    if "\x00" in fixed:
        fixed = fixed.replace("\x00", "")
        changes.append("removed NUL (\\x00) characters")

    # Normalize line endings
    if "\r\n" in fixed or "\r" in fixed:
        fixed = fixed.replace("\r\n", "\n").replace("\r", "\n")
        changes.append("normalized line endings to LF")

    # Smart quotes -> normal quotes
    smart_map = {
        "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
        "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
    }
    if any(ch in fixed for ch in smart_map):
        fixed = "".join(smart_map.get(ch, ch) for ch in fixed)
        changes.append("replaced smart quotes with ASCII quotes")

    # XML-specific: escape stray & (VERY common cause of RDF/XML parse failures)
    # Only do this if we assume XML, because in Turtle & is legal in some contexts.
    if assume_xml:
        # Replace & that is NOT part of &name; or &#123; or &#x1A;
        # This is still heuristic but usually safe for text nodes/attributes.
        stray_amp = re.compile(r"&(?!(?:[A-Za-z_][A-Za-z0-9._-]*|#[0-9]+|#x[0-9A-Fa-f]+);)")
        if stray_amp.search(fixed):
            fixed = stray_amp.sub("&amp;", fixed)
            changes.append("escaped stray '&' as '&amp;' (XML heuristic)")

    return fixed, changes


def parse_graph(path: Path, rdf_format: str | None):
    g = Graph()
    # If rdf_format is None, rdflib will try to guess from content / extension.
    g.parse(str(path), format=rdf_format)
    return g


def run_reasoning(g: Graph):
    if not OWLRL_AVAILABLE:
        print("⚠️  owlrl not installed — skipping reasoning (pip install owlrl)")
        return
    before = len(g)
    DeductiveClosure(OWLRL_Semantics).expand(g)
    after = len(g)
    print(f"🧠 OWL-RL reasoning added {after - before} inferred triples")


def summarize(g: Graph):
    from rdflib.namespace import RDF, OWL

    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    classes = set(g.subjects(RDF.type, OWL.Class))
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    individuals = set(g.subjects(RDF.type, OWL.NamedIndividual))

    print(f"✅ Parsed OK. Triples: {len(g)}")
    if ontologies:
        print("🦉 owl:Ontology:")
        for o in ontologies[:10]:
            print(f"  - {o}")
        if len(ontologies) > 10:
            print(f"  ... (+{len(ontologies)-10} more)")
    else:
        print("⚠️  No owl:Ontology declaration found")

    print(f"📦 Classes: {len(classes)}")
    print(f"🔗 Object properties: {len(obj_props)}")
    print(f"🔢 Datatype properties: {len(data_props)}")
    print(f"👤 Named individuals: {len(individuals)}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python check_owl_with_fix.py <file.owl> [--format xml|turtle|n3|nt] [--fix]")
        print("")
        print("Examples:")
        print("  python check_owl_with_fix.py ontology.owl --format xml --fix")
        print("  python check_owl_with_fix.py ontology.ttl --format turtle --fix")
        sys.exit(1)

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(2)

    rdf_format = None
    do_fix = False

    # Simple arg parse (kept dependency-free)
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            rdf_format = args[i + 1].strip().lower()
            i += 2
        elif args[i] == "--fix":
            do_fix = True
            i += 1
        else:
            print(f"⚠️  Unknown arg: {args[i]}")
            i += 1

    # First parse attempt
    print(f"\n📄 File: {path}")
    print(f"🔧 Format: {rdf_format or '(auto-detect)'}")
    print(f"🧽 Auto-fix enabled: {do_fix}\n")

    raw, text, enc = read_text_best_effort(path)
    print(f"📥 Read encoding (best-effort): {enc}")

    try:
        g = parse_graph(path, rdf_format)
        summarize(g)
        run_reasoning(g)
        print("\n🎉 Done.\n")
        return
    except Exception as e:
        # Show location/snippet if possible
        print_error_with_location(path, e, text)

        if not do_fix:
            print("Tip: re-run with --fix to try safe auto-fixes.")
            sys.exit(3)

    # Auto-fix and retry
    assume_xml = (rdf_format == "xml") or (rdf_format is None and path.suffix.lower() in [".owl", ".rdf", ".xml"])
    fixed_text, changes = safe_auto_fix(text, assume_xml=assume_xml)

    if not changes:
        print("🧽 No safe auto-fixes applicable (nothing changed).")
    else:
        print("🧽 Applied safe auto-fixes:")
        for c in changes:
            print(f"  - {c}")

    fixed_path = path.with_suffix(path.suffix + ".fixed")
    fixed_path.write_text(fixed_text, encoding="utf-8")
    print(f"\n💾 Wrote fixed copy: {fixed_path} (utf-8)\n")

    # Retry parse on fixed copy
    try:
        g2 = parse_graph(fixed_path, rdf_format)
        print("✅ Re-parse of fixed copy succeeded.")
        summarize(g2)
        run_reasoning(g2)
        print("\n🎉 Done.\n")
        return
    except Exception as e2:
        print_error_with_location(fixed_path, e2, fixed_text)
        print("❌ Still failing after safe auto-fix.")
        print("   At this point the file likely has structural RDF/XML or Turtle syntax errors.")
        sys.exit(4)


if __name__ == "__main__":
    main()
