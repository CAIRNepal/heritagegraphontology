"""HTTP helper using curl (macOS framework Python lacks root certs)."""
import subprocess, tempfile, os
from config import USER_AGENT


def post_form(url, fields, accept, timeout=300):
    """POST application/x-www-form-urlencoded; fields = {k: v}."""
    args = ["curl", "-sS", "-m", str(timeout), "-X", "POST", url,
            "-H", f"User-Agent: {USER_AGENT}", "-H", f"Accept: {accept}"]
    for k, v in fields.items():
        args += ["--data-urlencode", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, check=True)
    return out.stdout


def get(url, accept="application/json", timeout=120):
    args = ["curl", "-sSL", "-m", str(timeout), url,
            "-H", f"User-Agent: {USER_AGENT}", "-H", f"Accept: {accept}"]
    out = subprocess.run(args, capture_output=True, check=True)
    return out.stdout
