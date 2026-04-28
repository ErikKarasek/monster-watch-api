from flask import Flask, jsonify
from flask_cors import CORS
from scraper import get_monster_deals
import os

app = Flask(__name__)
CORS(app) # Povolí frontendu stahovat data z tohoto API

@app.route('/api/deals')
def deals():
    try:
        data = get_monster_deals()
        return jsonify({
            "status": "success",
            "date": "2026-04-28",
            "deals": data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
