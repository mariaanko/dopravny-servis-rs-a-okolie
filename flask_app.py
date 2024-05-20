from flask import Flask, jsonify
import scraper
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route("/reportsRS")
@cache.cached(timeout=15)
def get_reports():
    alerts = scraper.scraper()
    return jsonify(alerts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
