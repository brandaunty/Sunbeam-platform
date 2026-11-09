"""Sunbeam field-officer service (Task 1 placeholder).

Deliberately tiny: it proves the same code runs under Docker and Dokku.
It serves only feeder-level aggregates, never customer-level data.
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Synthetic, feeder-level only. Replaced by the real data platform in Task 3.
FEEDERS = [
    {"feeder": i, "area": "urban" if i < 5 else "rural", "suspected_loss_pct": None}
    for i in range(10)
]


@app.get("/health")
def health():
    return jsonify(status="ok", service="sunbeam-field")


@app.get("/feeders")
def feeders():
    return jsonify(FEEDERS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
