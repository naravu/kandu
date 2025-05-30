from flask import Flask, request, render_template
import subprocess
import re
import sys

app = Flask(__name__)

def get_ttl(ip: str) -> int:
    """Runs ping and extracts TTL value."""
    ping_cmd = ["ping", "-n", "1", ip] if sys.platform.startswith("win") else ["ping", "-c", "1", ip]
    try:
        output = subprocess.run(ping_cmd, capture_output=True, text=True, check=True).stdout
        if ttl_match := re.search(r"TTL=(\d+)", output, re.IGNORECASE):
            return int(ttl_match.group(1))
    except subprocess.CalledProcessError:
        pass
    return None

def detect_os(ip: str) -> str:
    """Determines OS based on TTL value."""
    ttl = get_ttl(ip)
    if ttl is None:
        return f"❌ Unable to determine OS for IP **{ip}** (Host unreachable)"
    os_type = "Windows" if 100 <= ttl <= 128 else "Linux" if 50 <= ttl <= 64 else "Unknown/Network"
    return f"✅ IP {ip} is running {os_type} OS (TTL: {ttl})"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ip = None
    if request.method == "POST":
        ip = request.form.get("ip")
        if ip:
            result = detect_os(ip)
    return render_template("index.html", result=result, ip=ip)

if __name__ == "__main__":
    app.run(debug=True)
