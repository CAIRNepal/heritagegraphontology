/* ontoreview client: theme, copy, search, filters, figure (Cytoscape). Works from file://. */
(function () {
  "use strict";
  var DATA = window.ONTOREVIEW || { search: [], graph: null, i18n: {}, ui: {} };
  var T = DATA.i18n || {};
  var UI = DATA.ui || {};
  var root = document.documentElement;
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function fmt(s, o) { return String(s || "").replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  var liveEl = document.getElementById("a11y-status"), liveTimer = null;
  function announce(msg) {
    if (!liveEl) return;
    liveEl.textContent = "";
    clearTimeout(liveTimer);
    liveTimer = setTimeout(function () { liveEl.textContent = msg; }, 60);
  }
  var reduceMotion = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- theme ---------- */
  function isDark() {
    var t = root.dataset.theme;
    if (t) return t === "dark";
    return !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
  }
  function labelTheme() {
    $$('[data-action="theme"]').forEach(function (b) {
      b.textContent = isDark() ? (b.dataset.light || "Light") : (b.dataset.dark || "Dark");
      b.setAttribute("aria-pressed", isDark() ? "true" : "false");
    });
  }
  labelTheme();

  /* ---------- text size ---------- */
  var SIZES = ["100", "115", "130"];
  function labelSize() {
    var z = root.dataset.textsize || "100";
    $$('[data-action="textsize"] .textsize-val').forEach(function (v) { v.textContent = z + "%"; });
  }
  labelSize();

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-action]");
    if (!btn) return;
    var a = btn.dataset.action;
    if (a === "theme") {
      root.dataset.theme = isDark() ? "light" : "dark"; store("ontoreview-theme", root.dataset.theme);
      labelTheme();
      if (graph) graph.restyle();
    } else if (a === "menu") {
      setNav(!document.body.classList.contains("nav-open"));
    } else if (a === "textsize") {
      var cur = SIZES.indexOf(root.dataset.textsize || "100");
      var next = SIZES[(cur + 1) % SIZES.length];
      if (next === "100") delete root.dataset.textsize; else root.dataset.textsize = next;
      store("ontoreview-textsize", next);
      labelSize();
      announce((btn.getAttribute("aria-label") || "Text size") + " " + next + "%");
    } else if (a === "search") {
      openSearch();
    } else if (a === "close-search") {
      closeSearch();
    }
  });
  var menuBtns = $$('[data-action="menu"]'), sidebar = $("#sidebar");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    menuBtns.forEach(function (b) { b.setAttribute("aria-expanded", open ? "true" : "false"); });
    if (open && sidebar) { var f = $("a, button, input, select", sidebar); if (f) f.focus(); }
  }
  var lang = $("#lang-select");
  if (lang) lang.addEventListener("change", function () { location.href = lang.value; });
  $$(".toc a").forEach(function (a) { a.addEventListener("click", function () { if (!a.closest(".toc-kind summary")) setNav(false); }); });
  // A link inside <summary> navigates but would not expand the list: open it as well.
  $$(".toc-kind summary > a").forEach(function (a) {
    a.addEventListener("click", function () { var d = a.closest("details"); if (d) d.open = true; });
  });

  /* ---------- copy ---------- */
  function copyText(text, btn) {
    function done() { var old = btn.textContent; btn.classList.add("done"); btn.textContent = (T.copied || "copied").toLowerCase(); announce(T.copied || "Copied"); setTimeout(function () { btn.classList.remove("done"); btn.textContent = old; }, 1200); }
    function fallback() { var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) {} document.body.removeChild(ta); }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".copy");
    if (!b) return;
    var text = b.dataset.copy;
    if (!text && b.dataset.copyHref) { try { text = new URL(b.dataset.copyHref, location.href).href; } catch (err) { text = b.dataset.copyHref; } }
    if (!text && b.dataset.copyTarget) { var el = document.getElementById(b.dataset.copyTarget); text = el ? el.innerText.trim() : ""; }
    if (text) copyText(text, b);
  });

  /* ---------- filters ---------- */
  $$(".term-filter").forEach(function (input) {
    var cards = $$(".term", input.closest("section"));
    var texts = cards.map(function (c) { return c.innerText.toLowerCase(); });
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c, i) { c.hidden = !!q && texts[i].indexOf(q) === -1; if (!c.hidden) shown++; });
      announce(fmt(T.filter_count || "{shown} of {total} terms shown", { shown: shown, total: cards.length }));
    });
  });
  $$(".index-filter").forEach(function (input) {
    var items = $$("li", input.parentNode);
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (li) { var ok = !q || li.textContent.toLowerCase().indexOf(q) !== -1; li.style.display = ok ? "" : "none"; if (ok) shown++; });
      announce(fmt(T.filter_count || "{shown} of {total} terms shown", { shown: shown, total: items.length }));
    });
  });

  /* ---------- search ---------- */
  var modal = $("#search-modal"), input = $("#search-input"), list = $("#search-results");
  var mini = null, sel = 0;
  function ensureIndex() {
    if (mini || !window.MiniSearch) return;
    mini = new MiniSearch({
      fields: ["label", "curie", "alt", "def"], storeFields: ["label", "curie", "def", "kind", "href", "dep"],
      searchOptions: { boost: { label: 4, curie: 3, alt: 2 }, prefix: true, fuzzy: 0.2 }
    });
    mini.addAll(DATA.search || []);
  }
  var countEl = $("#search-count"), opener = null;
  function openSearch() {
    if (!modal) return;
    if (modal.hidden) opener = document.activeElement;
    ensureIndex(); modal.hidden = false; input.value = ""; list.innerHTML = "";
    input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant");
    setTimeout(function () { input.focus(); }, 10);
  }
  function closeSearch() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    if (opener && opener.focus && document.contains(opener)) opener.focus();
    opener = null;
  }
  function select(lis, i) {
    lis.forEach(function (li, j) { li.classList.toggle("sel", j === i); li.setAttribute("aria-selected", j === i ? "true" : "false"); });
    if (lis[i]) { input.setAttribute("aria-activedescendant", lis[i].id); lis[i].scrollIntoView({ block: "nearest" }); }
    else input.removeAttribute("aria-activedescendant");
  }
  function hl(text, q) {
    var t = esc(text); if (!q) return t;
    var words = q.split(/\s+/).filter(function (w) { return w.length > 1; }).map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); });
    return words.length ? t.replace(new RegExp("(" + words.join("|") + ")", "ig"), "<mark>$1</mark>") : t;
  }
  function render(items, q) {
    sel = 0;
    input.removeAttribute("aria-activedescendant");
    if (!q) { list.innerHTML = ""; input.setAttribute("aria-expanded", "false"); if (countEl) countEl.textContent = ""; return; }
    if (!items.length) {
      list.innerHTML = '<li class="search-empty" role="presentation">' + esc(T.no_results || "No results") + "</li>";
      input.setAttribute("aria-expanded", "false");
      if (countEl) countEl.textContent = T.no_results || "No results";
      return;
    }
    input.setAttribute("aria-expanded", "true");
    if (countEl) countEl.textContent = fmt(T.results_count || "{n} results", { n: Math.min(items.length, 40) });
    list.innerHTML = items.slice(0, 40).map(function (r, i) {
      return '<li id="sr-' + i + '" role="option" aria-selected="' + (i === 0 ? "true" : "false") + '" class="' + (i === 0 ? "sel" : "") + '"><a tabindex="-1" href="' + esc(r.href) + '"><span class="sr-top"><span class="sr-label">' + hl(r.label, q) + '</span>' +
        '<span class="sr-kind">' + esc(r.kind) + "</span>" + (r.curie ? '<span class="sr-curie">' + esc(r.curie) + "</span>" : "") + "</span>" +
        (r.def ? '<span class="sr-def">' + hl(r.def, q) + "</span>" : "") + "</a></li>";
    }).join("");
  }
  if (input) {
    input.addEventListener("input", function () {
      var q = input.value.trim();
      ensureIndex();
      render(q && mini ? mini.search(q) : [], q);
      if ($("#sr-0")) input.setAttribute("aria-activedescendant", "sr-0");
    });
    input.addEventListener("keydown", function (e) {
      var lis = $$("li", list).filter(function (li) { return li.querySelector("a"); });
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!lis.length) return;
        sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + lis.length) % lis.length;
        select(lis, sel);
      } else if (e.key === "Enter") {
        var a = lis[sel] && lis[sel].querySelector("a");
        if (a) { e.preventDefault(); opener = null; closeSearch(); location.href = a.getAttribute("href"); }
      } else if (e.key === "Tab") {
        e.preventDefault(); // keep focus inside the dialog; results are reached with the arrow keys
      }
    });
    list.addEventListener("click", function (e) { if (e.target.closest("a")) { opener = null; closeSearch(); } });
  }
  document.addEventListener("keydown", function (e) {
    var typing = /input|textarea|select/i.test(e.target.tagName || "") || e.target.isContentEditable;
    if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing)) { e.preventDefault(); openSearch(); }
    else if (e.key === "Escape") {
      if (modal && !modal.hidden) { closeSearch(); return; }
      if (document.body.classList.contains("nav-open")) { setNav(false); if (menuBtns[0]) menuBtns[0].focus(); return; }
      if (graph) graph.collapse();
    }
  });

  /* ---------- table of contents: scroll-spy ---------- */
  var navLinks = $$(".toc-list a[data-section]").filter(function (a) { return a.getAttribute("href").charAt(0) === "#"; });
  if (navLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    navLinks.forEach(function (a) { (byId[a.dataset.section] = byId[a.dataset.section] || []).push(a); });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && byId[en.target.id]) {
          navLinks.forEach(function (a) { a.classList.remove("current"); });
          byId[en.target.id].forEach(function (a) { a.classList.add("current"); });
        }
      });
    }, { rootMargin: "-10% 0px -75% 0px" });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) obs.observe(s); });
  }

  /* ---------- figure ---------- */
  var graph = null;
  var cyEl = document.getElementById("cy");
  if (cyEl && window.cytoscape && DATA.graph) graph = makeGraph(cyEl, DATA.graph);

  // "Show in figure" links
  document.addEventListener("click", function (e) {
    var a = e.target.closest(".graph-link");
    if (!a || !graph) return;
    e.preventDefault();
    var fig = $("#figure-graph");
    if (fig) fig.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    graph.focus(a.dataset.focus);
  });
  if (graph) {
    var params = new URLSearchParams(location.search);
    if (params.get("focus")) graph.focus(params.get("focus"));
  }

  // Display label: allow line breaks inside camelCase / snake_case names (zero-width spaces).
  function breakable(s) {
    s = String(s || "");
    if (s.indexOf(" ") !== -1 || s.length <= 12) return s;
    return s.replace(/([a-z0-9])([A-Z])/g, "$1​$2").replace(/([_\-\/.:])/g, "$1​");
  }

  // Turn the shared graph data into WebVOWL-style elements: classes are circles; every property is a
  // labelled node sitting between its domain and range; datatype properties point at literal boxes.
  function toVowl(g) {
    var els = [], subs = {};
    g.edges.forEach(function (e) { if (e.data.type === "sub") subs[e.data.source] = (subs[e.data.source] || 0) + 1; });
    g.nodes.forEach(function (n) {
      var d = Object.assign({}, n.data);
      d.cls = true;
      d.show = breakable(d.label);
      var weight = (subs[d.id] || 0) + (d.inst || 0);
      var len = Math.min(String(d.label).length, 22);
      d.size = Math.round(Math.min(160, Math.max(72, 40 + len * 4.6) + 8 * Math.log2(1 + weight)));
      els.push({ data: d });
      (n.data.dprops || []).forEach(function (p, i) {
        var pid = "dp|" + d.id + "|" + i, lid = "lit|" + d.id + "|" + i;
        els.push({ data: { id: pid, label: p.l, show: breakable(p.l), href: p.h, kind: "dprop", pel: true } });
        var lit = String(p.r || "Literal").replace(/^xsd:/, "").replace(/^rdfs:/, "");
        els.push({ data: { id: lid, label: lit, show: lit, kind: "literal", pel: true, generic: lit === "Literal" } });
        els.push({ data: { id: pid + "|a", source: d.id, target: pid, type: "pa", pel: true } });
        els.push({ data: { id: pid + "|b", source: pid, target: lid, type: "pb", pel: true } });
      });
    });
    var byKey = {};
    g.edges.forEach(function (e) {
      var x = e.data;
      if (x.type !== "prop") { els.push({ data: Object.assign({}, x) }); return; }
      // an inverse pair (p: A→B, inverse q: B→A) becomes one node with both names, as in WebVOWL
      var twin = x.inv && byKey[x.inv + "|" + x.target + "|" + x.source];
      if (twin) {
        twin.label = twin.label + "\n" + x.label;
        twin.show = twin.label;
        twin.both = true;
        return;
      }
      var pid = "op|" + x.id;
      var node = { id: pid, label: x.label, show: breakable(x.label), href: x.href, kind: "oprop", pel: true, self: x.source === x.target };
      byKey[(x.prop || x.id) + "|" + x.source + "|" + x.target] = node;
      els.push({ data: node });
      els.push({ data: { id: pid + "|a", source: x.source, target: pid, type: "pa", pel: true, owner: pid } });
      els.push({ data: { id: pid + "|b", source: pid, target: x.target, type: "pb", pel: true } });
    });
    var owners = {};
    Object.keys(byKey).forEach(function (k) { owners[byKey[k].id] = byKey[k]; });
    els.forEach(function (el) { if (el.data.owner && owners[el.data.owner]) el.data.both = !!owners[el.data.owner].both; });
    return els;
  }

  function makeGraph(el, g) {
    function css(n) { return getComputedStyle(root).getPropertyValue(n).trim(); }
    var notation = store("ontoreview-notation") || (UI.notation === "uml" ? "uml" : "vowl");
    if (notation !== "uml") notation = "vowl";
    var vowl = notation === "vowl";
    var figEl = $("#figure-graph");
    if (figEl) figEl.setAttribute("data-notation", notation);
    g.nodes.forEach(function (n) { n.data.full = n.data.attrs ? n.data.label + "\n───\n" + n.data.attrs : n.data.label; });
    // members of a class (enum values, named individuals): small nodes tied to their class by rdf:type
    var vals = (g.values || []).map(function (n) {
      return { data: Object.assign({}, n.data, { full: n.data.label, show: breakable(n.data.label) }) };
    });
    var cy = window.cytoscape({ container: el, elements: vowl ? toVowl(g).concat(vals) : g.nodes.concat(vals, g.edges), minZoom: 0.05, maxZoom: 3, wheelSensitivity: 0.3 });
    var status = $("#g-status");
    var classCount = g.nodes.length;
    var propCount = g.edges.filter(function (e) { return e.data.type === "prop"; }).length;
    var pelCount = vowl ? cy.nodes("[kind = 'oprop'], [kind = 'dprop']").length : propCount;
    // "auto": draw properties only while the figure stays legible; otherwise they appear on focus
    var showProps = UI.props === "auto"
      ? (vowl ? classCount <= 60 && pelCount <= 45 : classCount <= 40 && propCount <= 20)
      : !!UI.props;
    var layoutName = UI.layout && UI.layout !== "auto" ? UI.layout : (vowl ? "force" : "hierarchy");
    if (layoutName === "force") layoutName = "cose";
    var mode = "hierarchy";
    var focused = null;
    function isClass(n) { return !n.data("pel") && !n.data("val"); }
    var TREE = "[type = 'sub'], [type = 'eq'], [type = 'inst']";

    // UML: fan out property edges that leave the same class so their labels do not overlap
    var fan = {};
    cy.edges("[type = 'prop']").forEach(function (e) {
      var k = e.data("source");
      fan[k] = (fan[k] || 0) + 1;
      e.data("fan", fan[k]);
    });
    function spread(e) {
      var i = e.data("fan") || 1;
      var d = 28 + 26 * Math.floor((i - 1) / 2);
      return [i % 2 ? d : -d];
    }
    cy.edges("[type = 'sub']").forEach(function (ed) { ed.data("name", ed.data("rel") || "subclass of"); });
    cy.edges("[type = 'inst']").forEach(function (ed) { ed.data("name", "instance of (rdf:type)"); });
    cy.edges("[type = 'eq']").forEach(function (ed) { ed.data("name", "equivalent to (part of)"); });

    function umlStyle(ink, muted, rule, paper, link) {
      return [
        { selector: "node", style: {
          "label": showProps ? "data(full)" : "data(label)", "font-size": 12, "font-family": css("--serif") || "Georgia, serif", "color": ink,
          "text-valign": "center", "text-halign": "center", "shape": "rectangle", "padding": "7px",
          "width": "label", "height": "label", "background-color": paper, "border-width": 1, "border-color": ink,
          "text-wrap": "wrap", "text-max-width": 220, "line-height": 1.35 } },
        { selector: "node[kind = 'external']", style: { "border-style": "dashed", "color": muted, "border-color": muted } },
        { selector: "node[?dep]", style: { "color": muted, "border-color": muted } },
        { selector: "node[?val]", style: { "shape": "round-rectangle", "font-size": 11, "font-family": css("--sans"), "padding": "4px",
          "border-color": muted, "color": ink, "text-max-width": 160 } },
        { selector: "node[kind = 'concept_scheme']", style: { "border-style": "double", "border-width": 3 } },
        { selector: "edge", style: { "width": 1, "curve-style": "bezier", "line-color": rule } },
        { selector: "edge[type = 'inst']", style: { "line-style": "dashed", "line-dash-pattern": [2, 3], "line-color": muted, "width": 1,
          "target-arrow-shape": "circle", "target-arrow-color": muted, "arrow-scale": 0.6 } },
        { selector: "edge[type = 'sub']", style: { "source-arrow-shape": "triangle", "source-arrow-fill": "hollow", "source-arrow-color": ink, "line-color": ink, "arrow-scale": 1.45, "width": 1.4 } },
        { selector: "edge[type = 'eq']", style: { "line-style": "dotted", "line-color": muted, "source-arrow-shape": "triangle", "source-arrow-fill": "hollow", "source-arrow-color": muted, "width": 1.2 } },
        { selector: "edge[type = 'prop']", style: { "text-margin-y": -7, "line-style": "dashed", "line-dash-pattern": [5, 3], "target-arrow-shape": "vee", "target-arrow-color": link, "line-color": link,
          "curve-style": "unbundled-bezier", "control-point-distances": spread, "control-point-weights": [0.5], "width": 1.1,
          "label": "data(label)", "font-size": 10, "font-family": css("--sans"), "color": link, "text-rotation": "autorotate",
          "text-background-color": paper, "text-background-opacity": 1, "text-background-padding": 2, "loop-direction": "-45deg", "loop-sweep": "-90deg" } },
        { selector: ".hl", style: { "border-width": 2.5, "border-color": link, "color": link, "font-weight": "bold" } },
        { selector: "node.path", style: { "border-color": link, "border-width": 2, "color": link } },
        { selector: "edge.path[type = 'sub'], edge.path[type = 'eq']", style: { "line-color": link, "source-arrow-color": link, "width": 2.4, "z-index": 9 } }
      ];
    }
    function vowlStyle(ink, muted, rule, paper, link) {
      var text = "#15171a", stroke = css("--vowl-stroke") || "#30343a", sans = css("--sans");
      return [
        { selector: "node", style: { "label": "data(show)", "font-family": sans, "color": text, "text-valign": "center", "text-halign": "center",
          "text-wrap": "wrap", "line-height": 1.2, "overlay-opacity": 0 } },
        { selector: "node[?cls]", style: { "shape": "ellipse", "width": "data(size)", "height": "data(size)",
          "background-color": css("--vowl-class"), "border-width": 1.5, "border-color": stroke, "font-size": 13, "font-weight": 600,
          "text-max-width": function (n) { return Math.round(n.data("size") * 0.78) + "px"; } } },
        { selector: "node[?defined]", style: { "border-style": "double", "border-width": 5 } },
        { selector: "node[kind = 'external']", style: { "background-color": css("--vowl-external"), "color": "#ffffff" } },
        { selector: "node[?dep]", style: { "background-color": css("--vowl-deprecated"), "color": "#3b3b3b" } },
        { selector: "node[kind = 'oprop'], node[kind = 'dprop']", style: { "shape": "round-rectangle", "width": "label", "height": "label",
          "padding": "4px", "font-size": 11.5, "text-max-width": "140px", "background-color": css("--vowl-oprop"), "border-width": 0 } },
        { selector: "node[kind = 'dprop']", style: { "background-color": css("--vowl-dprop") } },
        { selector: "node[kind = 'literal']", style: { "shape": "rectangle", "width": "label", "height": "label", "padding": "4px",
          "font-size": 11, "background-color": css("--vowl-literal"), "border-width": 1, "border-color": stroke } },
        { selector: "node[?generic]", style: { "border-style": "dashed" } },
        { selector: "node[?val]", style: { "shape": "round-rectangle", "width": "label", "height": "label", "padding": "4px",
          "font-size": 11, "text-max-width": "120px", "background-color": css("--vowl-value") || "#f3e3c3", "border-width": 1, "border-color": stroke } },
        { selector: "node[kind = 'concept_scheme']", style: { "border-style": "double", "border-width": 5 } },
        { selector: "edge[type = 'inst']", style: { "line-style": "dashed", "line-dash-pattern": [2, 3], "width": 1, "line-color": stroke,
          "target-arrow-shape": "circle", "target-arrow-color": stroke, "arrow-scale": 0.6 } },
        { selector: "edge", style: { "width": 1.2, "curve-style": "bezier", "line-color": stroke, "arrow-scale": 1.05 } },
        { selector: "edge[type = 'pb']", style: { "target-arrow-shape": "triangle", "target-arrow-color": stroke } },
        { selector: "edge[?both]", style: { "source-arrow-shape": "triangle", "source-arrow-color": stroke } },
        { selector: "edge[type = 'sub']", style: { "line-style": "dashed", "line-dash-pattern": [6, 4], "source-arrow-shape": "triangle",
          "source-arrow-fill": "hollow", "source-arrow-color": stroke, "arrow-scale": 1.35, "width": 1.4 } },
        { selector: "edge[type = 'sub'].sublabel", style: { "label": "data(name)", "font-size": 10, "font-family": sans, "color": muted,
          "text-background-color": paper, "text-background-opacity": 1, "text-background-padding": 2, "text-rotation": "autorotate" } },
        { selector: "edge[type = 'eq']", style: { "line-style": "dotted", "source-arrow-shape": "triangle", "source-arrow-fill": "hollow",
          "source-arrow-color": stroke, "width": 1.3 } },
        { selector: ".hl", style: { "border-width": 3.5, "border-color": link, "border-style": "solid" } },
        { selector: "node.path[?cls]", style: { "border-color": link, "border-width": 3 } },
        { selector: "node.path[?pel], node.path[?val]", style: { "border-width": 1.5, "border-color": link } },
        { selector: "edge.path", style: { "line-color": link, "source-arrow-color": link, "target-arrow-color": link, "width": 2.4, "z-index": 9 } }
      ];
    }
    function style() {
      var ink = css("--ink"), muted = css("--muted"), rule = css("--rule-strong"), paper = css("--paper"), link = css("--link");
      var s = (vowl ? vowlStyle : umlStyle)(ink, muted, rule, paper, link);
      cy.style(s.concat([
        { selector: "edge.named", style: { "label": "data(name)", "font-size": 10, "font-family": css("--sans"), "color": link,
          "text-background-color": paper, "text-background-opacity": 1, "text-background-padding": 2, "text-rotation": "autorotate" } },
        { selector: ".dim", style: { "opacity": 0.22 } },
        { selector: ".hidden", style: { "display": "none" } }
      ]));
    }
    style();

    // depth of every class in the subclass hierarchy (roots = no superclass edge)
    var depth = {};
    var roots = cy.nodes().filter(function (n) { return isClass(n) && n.incomers("edge[type = 'sub']").length === 0; });
    var queue = roots.map(function (n) { depth[n.id()] = 0; return n; });
    while (queue.length) {
      var n = queue.shift();
      n.outgoers("edge[type = 'sub']").targets().forEach(function (c) {
        if (depth[c.id()] === undefined) { depth[c.id()] = depth[n.id()] + 1; queue.push(c); }
      });
    }
    cy.nodes("[?val]").forEach(function (v) {
      var up = v.incomers("edge[type = 'inst']").sources().map(function (c) { return depth[c.id()] || 0; });
      depth[v.id()] = (up.length ? Math.max.apply(null, up) : 0) + 1;
    });
    var large = classCount > 150;

    // show/hide property elements; a property is visible only when the classes it joins are
    function syncProps() {
      cy.nodes("[?pel][kind != 'literal']").forEach(function (p) {
        var ends = p.neighborhood("node").filter(isClass);
        p.toggleClass("hidden", !showProps || ends.some(function (c) { return c.hasClass("hidden"); }));
      });
      cy.nodes("[kind = 'literal']").forEach(function (l) { l.toggleClass("hidden", l.neighborhood("node").some(function (x) { return x.hasClass("hidden"); })); });
      cy.edges("[?pel]").forEach(function (e) { e.toggleClass("hidden", e.source().hasClass("hidden") || e.target().hasClass("hidden")); });
    }
    // a value is visible whenever one of its classes is
    function syncValues() {
      cy.nodes("[?val]").forEach(function (v) {
        var cls = v.incomers("edge[type = 'inst']").sources();
        v.toggleClass("hidden", !cls.length || cls.every(function (c) { return c.hasClass("hidden"); }));
      });
      cy.edges("[type = 'inst']").forEach(function (e) { e.toggleClass("hidden", e.source().hasClass("hidden") || e.target().hasClass("hidden")); });
    }
    function applyEdges() {
      if (vowl) { syncProps(); syncValues(); return; }
      cy.edges("[type = 'prop']").toggleClass("hidden", !showProps);
      cy.nodes().forEach(function (n) { n.style("label", showProps ? n.data("full") : n.data("label")); });
      syncValues();
    }
    function visible() { return cy.elements().not(".hidden"); }
    var hasDagre = (function () { try { return !!cy.layout({ name: "dagre", eles: cy.collection() }); } catch (e) { return false; } })();
    function widestLevel(nodes) {
      var count = {};
      nodes.filter(isClass).forEach(function (n) { var d = depth[n.id()] || 0; count[d] = (count[d] || 0) + 1; });
      return Math.max.apply(null, Object.keys(count).map(function (k) { return count[k]; }).concat([1]));
    }
    function run() {
      var all = visible();
      var tree = vowl ? all : all.nodes().union(all.edges(TREE));
      var opts, horizontal = false;
      cy.edges("[type = 'sub']").toggleClass("sublabel", vowl && all.nodes().filter(isClass).length <= 20);
      if (layoutName === "hierarchy") {
        horizontal = widestLevel(all.nodes()) > 7;  // many siblings: left-to-right keeps labels readable
        if (hasDagre) {
          opts = { name: "dagre", rankDir: horizontal ? "LR" : "TB", nodeSep: horizontal ? 14 : 28, rankSep: horizontal ? 70 : 56,
            edgeSep: 10, ranker: "network-simplex", padding: 30, nodeDimensionsIncludeLabels: true };
        } else {
          var r = tree.nodes().filter(function (n) { return n.incomers(TREE).not(".hidden").length === 0; });
          opts = { name: "breadthfirst", directed: true, roots: r, padding: 30, avoidOverlap: true, nodeDimensionsIncludeLabels: true };
        }
        if (!vowl) cy.edges("[type = 'sub']").style({ "curve-style": "taxi", "taxi-direction": horizontal ? "horizontal" : "vertical", "taxi-turn": "50%" });
        tree.layout(opts).run();
      } else {
        if (!vowl) cy.edges("[type = 'sub']").style({ "curve-style": "bezier" });
        if (layoutName === "concentric") {
          opts = { name: "concentric", padding: 24, minNodeSpacing: 24, nodeDimensionsIncludeLabels: true,
            concentric: function (n) { return 10 - (depth[n.id()] || 0); }, levelWidth: function () { return 1; } };
        } else if (vowl) {
          // WebVOWL-like force layout: property nodes stay close to their classes, classes push apart
          opts = { name: "cose", animate: false, randomize: true, padding: 30, nodeDimensionsIncludeLabels: true,
            nodeRepulsion: function (n) { return isClass(n) ? 900000 : 120000; },
            idealEdgeLength: function (e) { var t = e.data("type"); return t === "sub" || t === "eq" ? 95 : t === "inst" ? 46 : 34; },
            edgeElasticity: function (e) { return e.data("pel") || e.data("type") === "inst" ? 260 : 110; },
            nodeOverlap: 24, gravity: 0.6, componentSpacing: 60, numIter: 3000, coolingFactor: 0.97, minTemp: 1 };
        } else {
          opts = { name: "cose", animate: false, nodeRepulsion: 400000, idealEdgeLength: 110, nodeOverlap: 40, gravity: 0.4,
            padding: 30, nodeDimensionsIncludeLabels: true, numIter: 1500 };
        }
        all.layout(opts).run();
      }
      cy.fit(all, 30);
      if (cy.zoom() > 1.25) { cy.zoom(1.25); cy.center(all); }
      var floor = vowl && layoutName !== "hierarchy" ? 0.62 : 0.72;
      if (cy.zoom() < floor) {  // keep labels readable; the reader pans to see the rest
        if (layoutName !== "hierarchy") { cy.zoom(floor); cy.center(all); return; }
        var anchor = all.nodes().filter(function (n) { return isClass(n) && (depth[n.id()] || 0) === 0; });
        var bb = (anchor.length ? anchor : all.nodes()).boundingBox();
        cy.zoom(floor);
        cy.pan(horizontal ? { x: 30 - bb.x1 * floor, y: 30 - bb.y1 * floor }
                          : { x: el.clientWidth / 2 - ((bb.x1 + bb.x2) / 2) * floor, y: 30 - bb.y1 * floor });
      }
    }
    function say(key) { if (status) status.textContent = T[key] || ""; }

    function showHierarchy() {
      mode = "hierarchy"; focused = null;
      cy.elements().removeClass("hl hidden");
      if (large) {
        var top = UI.topLevels || 2;
        cy.nodes().filter(isClass).forEach(function (n) { if ((depth[n.id()] || 0) >= top) n.addClass("hidden"); });
        if (!vowl) cy.edges().forEach(function (e) { if (e.source().hasClass("hidden") || e.target().hasClass("hidden")) e.addClass("hidden"); });
        say("graph_showing_top");
      } else {
        say("graph_showing_all");
      }
      applyEdges();
      if (vowl) cy.edges("[type = 'sub'], [type = 'eq']").forEach(function (e) { e.toggleClass("hidden", e.source().hasClass("hidden") || e.target().hasClass("hidden")); });
      run();
    }
    function focus(iri) {
      var node = cy.getElementById(iri);
      if (!node || !node.length) return;
      mode = "focus"; focused = iri;
      cy.elements().removeClass("hl").addClass("hidden");
      var hierEdges = "edge[type = 'sub'], edge[type = 'eq']";
      var keep = node.union(node.connectedEdges(hierEdges).connectedNodes());
      keep = keep.union(walk(node, "up").nodes());
      if (vowl) {
        node.neighborhood("node[kind = 'oprop']").forEach(function (p) { keep = keep.union(p.neighborhood("node").filter(isClass)); });
      } else {
        keep = keep.union(keep.closedNeighborhood("edge[type = 'sub']").connectedNodes());
      }
      keep.removeClass("hidden");
      keep.edgesWith(keep).filter("[type = 'sub'], [type = 'eq']").removeClass("hidden");
      if (!vowl) keep.edgesWith(keep).filter("[type = 'prop']").removeClass("hidden");
      node.addClass("hl");
      var was = showProps;
      if (vowl) { showProps = true; syncProps(); showProps = was; syncValues(); }
      else {
        applyEdges();
        if (!showProps) node.connectedEdges("[type = 'prop']").removeClass("hidden").connectedNodes().removeClass("hidden");
      }
      run();
      say("graph_showing_focus");
      var f = $("#g-focus"); if (f) f.value = node.data("label");
    }
    // superclasses up to the root ("up") or all subclasses below ("down"), through hierarchy edges only
    function walk(node, dir) {
      var out = cy.collection(), q = [node], sel = "edge[type = 'sub'], edge[type = 'eq']";
      while (q.length) {
        var x = q.pop();
        (dir === "up" ? x.incomers(sel) : x.outgoers(sel)).forEach(function (e) {
          if (out.contains(e)) return;
          var m = dir === "up" ? e.source() : e.target();
          out = out.union(e).union(m);
          q.push(m);
        });
      }
      return out;
    }

    cy.on("tap", "node", function (e) {
      var d = e.target.data();
      if (d.kind === "literal") return;
      if (d.pel || d.val) { if (d.href) location.href = d.href; return; }
      if (mode === "focus" && focused === d.id && d.href) { location.href = d.href; return; }
      if (d.kind === "external") { if (d.href) window.open(d.href, "_blank", "noopener"); return; }
      focus(d.id);
    });
    cy.on("dbltap", "node", function (e) { var h = e.target.data("href"); if (h) location.href = h; });
    cy.on("mouseover", "node", function (e) {
      var t = e.target, c;
      if (isClass(t)) {
        c = t.union(walk(t, "up")).union(walk(t, "down"));
        var props = t.neighborhood("node[?pel]");
        var around = props.union(props.neighborhood()).union(t.connectedEdges("[type = 'prop']")).union(t.connectedEdges("[type = 'prop']").connectedNodes())
          .union(t.connectedEdges("[type = 'inst']")).union(t.connectedEdges("[type = 'inst']").connectedNodes());
        c.addClass("path");
        cy.elements().not(c).not(around).addClass("dim");
      } else {
        c = t.union(t.neighborhood());
        c.neighborhood("node[kind = 'literal']").forEach(function (l) { c = c.union(l).union(l.connectedEdges()); });
        c.addClass("path");
        cy.elements().not(c).addClass("dim");
      }
      el.style.cursor = t.data("kind") === "literal" ? "" : "pointer";
    });
    cy.on("mouseout", "node", function () { cy.elements().removeClass("path dim"); el.style.cursor = ""; });
    cy.on("mouseover", "edge[type = 'sub'], edge[type = 'eq'], edge[type = 'inst']", function (e) { e.target.addClass("named path"); e.target.connectedNodes().addClass("path"); });
    cy.on("mouseout", "edge", function (e) { e.target.removeClass("named path"); e.target.connectedNodes().removeClass("path"); });
    cy.on("tap", "edge[type = 'prop']", function (e) { var h = e.target.data("href"); if (h) location.href = h; });

    var fig = figEl;
    var expandBtn = $("#g-expand");
    function collapse() {
      if (!fig || !fig.classList.contains("is-expanded")) return;
      fig.classList.remove("is-expanded"); document.body.classList.remove("figure-open");
      if (expandBtn) expandBtn.textContent = expandBtn.dataset.expand;
      cy.resize(); run();
    }
    if (expandBtn) expandBtn.addEventListener("click", function () {
      if (fig.classList.contains("is-expanded")) { collapse(); return; }
      fig.classList.add("is-expanded"); document.body.classList.add("figure-open");
      expandBtn.textContent = expandBtn.dataset.collapse;
      cy.resize(); run();
    });
    var propBox = $("#g-prop");
    if (propBox) { propBox.checked = showProps; propBox.addEventListener("change", function () { showProps = propBox.checked; if (mode === "focus") focus(focused); else { applyEdges(); run(); } }); }
    var notSel = $("#g-notation");
    if (notSel) {
      notSel.value = notation;
      notSel.addEventListener("change", function () { store("ontoreview-notation", notSel.value); location.reload(); });
    }
    var layoutSel = $("#g-layout");
    if (layoutSel) {
      layoutSel.value = layoutName;
      layoutSel.addEventListener("change", function () { layoutName = layoutSel.value; run(); });
    }
    $("#g-reset") && $("#g-reset").addEventListener("click", function () { var f = $("#g-focus"); if (f) f.value = ""; showHierarchy(); });
    $("#g-png") && $("#g-png").addEventListener("click", function () {
      var a = document.createElement("a");
      a.href = cy.png({ full: true, scale: 2, bg: css("--paper") });
      a.download = "figure-1.png"; a.click();
    });
    var dl = $("#g-terms");
    if (dl) dl.innerHTML = g.nodes.filter(function (n) { return n.data.kind !== "external"; }).map(function (n) { return '<option value="' + esc(n.data.label) + '">'; }).join("");
    var focusInput = $("#g-focus");
    if (focusInput) focusInput.addEventListener("change", function () {
      var v = focusInput.value.trim().toLowerCase();
      if (!v) { showHierarchy(); return; }
      var cls = cy.nodes().filter(isClass);
      var m = cls.filter(function (x) { return (x.data("label") || "").toLowerCase() === v; });
      if (!m.length) m = cls.filter(function (x) { return (x.data("label") || "").toLowerCase().indexOf(v) !== -1; });
      if (m.length) focus(m[0].id());
    });

    showHierarchy();
    return { focus: focus, collapse: collapse, restyle: style };
  }
})();
