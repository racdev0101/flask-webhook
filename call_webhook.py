from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 👇 Store this securely in Render → Settings → Environment Variables
GOOGLE_CHAT_WEBHOOK = os.environ.get("GOOGLE_CHAT_WEBHOOK")

@app.route("/elevenlabs-webhook", methods=["POST"])
def receive_webhook():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"status": "invalid json"}), 400

    analysis = (
        data.get("data", {})
            .get("analysis", {})
            .get("data_collection_results", {})
    )

    # Extract fields
    product_price     = analysis.get("product_price", {}).get("value")
    name_location     = analysis.get("name_location", {}).get("value")
    contact_details   = analysis.get("contact_details", {}).get("value")
    product_details   = analysis.get("product_details", {}).get("value")
    product_quantity  = analysis.get("product_quantity", {}).get("value")
    delivery_time     = analysis.get("delivery_time", {}).get("value")

    # Prepare message
    text = (
        f"📞 *New ElevenLabs Call Summary:*\n"
        f"• Product: {product_details}\n"
        f"• Price: {product_price}\n"
        f"• Quantity: {product_quantity}\n"
        f"• Delivery Time: {delivery_time}\n"
        f"• Buyer: {name_location}\n"
        f"• Contact: {contact_details}"
    )

    # Send to Google Chat
    if GOOGLE_CHAT_WEBHOOK:
        requests.post(GOOGLE_CHAT_WEBHOOK, json={"text": text})

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
