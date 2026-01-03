from flask import Flask, request, jsonify
from openai import OpenAI
import re
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/zillow", methods=["POST"])
def zillow():
    address = request.json.get("address", "")

    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=f"{address} Zillow Zestimate and Market Value numeric values only"
    )

    text = response.output_text or ""

    zestimate = ""
    market = ""

    for line in text.splitlines():
        if "zestimate" in line.lower():
            zestimate = extract_price(line)
        if "market" in line.lower() or "listing" in line.lower():
            market = extract_price(line)

    return jsonify({
        "zestimate": zestimate,
        "market": market
    })

def extract_price(text):
    m = re.search(r"\$\s*\d{3}(?:,\d{3})+", text)
    return m.group(0) if m else ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
