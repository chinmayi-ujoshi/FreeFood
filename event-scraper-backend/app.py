from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from scraper import scrape_events_with_food  # Import your scraper function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/scrape', methods=['GET'])
def scrape_events():
    main_url = "https://calendar.syracuse.edu/events/"
    events = scrape_events_with_food(main_url)
    return jsonify({"food_events": events})

if __name__ == "__main__":
    app.run(debug=True)
