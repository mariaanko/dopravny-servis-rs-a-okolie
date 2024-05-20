from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import scraper
from flask_caching import Cache

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:8000"}})


@app.route("/api/reportsRS", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@cache.cached(timeout=30)
def get_reports():
    response = jsonify(scraper.scraper())
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
