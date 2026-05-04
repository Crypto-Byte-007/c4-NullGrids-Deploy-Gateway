from flask import Flask, request, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)
FLAG = open("flag.txt").read().strip()

# ... (API endpoints remain the same) ...

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "uptime": "14d 3h 22m"})

@app.route("/api/version")
def version():
    return jsonify({
        "service": "nullgrids-deploy",
        "version": "3.1.4",
        "environment": "production",
        "debug": False
    })

@app.route("/api/deploy", methods=["POST"])
def deploy():
    api_key = request.headers.get("X-API-Key", "")
    if not api_key:
        return jsonify({"error": "API key required"}), 401
    # Uses key from environment (which leaks via /.env)
    expected = os.environ.get("DEPLOY_API_KEY", "unset")
    if api_key != expected:
        return jsonify({"error": "Invalid API key"}), 403
    return jsonify({"status": "Deploy triggered", "flag": FLAG})

# VULNERABILITY: .env file was committed and is served statically
# The /.env route simulates a misconfigured web server exposing dotenv
@app.route("/.env")
def env_file():
    # Serve the .env file contents (simulates nginx misconfiguration)
    try:
        with open(".env", "r") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/plain"}
    except FileNotFoundError:
        return "Not found", 404

# NOISE: .env.dev with fake data
@app.route("/.env.dev")
def env_dev_file():
    content = "APP_ENV=development\nDEPLOY_API_KEY=test-key-do-not-use\nFLAG=nullgrids{d3v_fl4gs_d0nt_c0unt}"
    return content, 200, {"Content-Type": "text/plain"}

# Bonus red herring: /config.php returns a 200 with fake data
@app.route("/config.php")
def config_php():
    return "<?php // Config loaded ?>", 200, {"Content-Type": "text/plain"}

# Red herring: /backup.zip returns 403
@app.route("/backup.zip")
def backup():
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
