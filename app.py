from flask import Flask, render_template, request, jsonify, redirect, url_for
from ai import generate_category
from database import init_db, save_product, get_all_products, get_product_by_id
import json

app = Flask(__name__)

# Initialize database on startup
init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    product_text = ""

    if request.method == "POST":
        product_text = request.form.get("product", "").strip()

        if not product_text:
            error = "Please enter a product description."
        else:
            ai_response = generate_category(product_text)

            if ai_response["success"]:
                result = ai_response["data"]
                # Save to database
                save_product(product_text, result)
            else:
                error = ai_response.get("error", "Something went wrong with the AI.")
                if ai_response.get("raw"):
                    error += f" | Raw response: {ai_response['raw']}"

    return render_template("index.html", result=result, error=error, product_text=product_text)


@app.route("/history")
def history():
    products = get_all_products()
    return render_template("history.html", products=products)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """JSON API endpoint for programmatic access."""
    data = request.get_json()
    if not data or not data.get("product"):
        return jsonify({"success": False, "error": "Missing 'product' field"}), 400

    ai_response = generate_category(data["product"])

    if ai_response["success"]:
        save_product(data["product"], ai_response["data"])

    return jsonify(ai_response)


if __name__ == "__main__":
    app.run(debug=True)