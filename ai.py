from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

VALID_CATEGORIES = [
    "Personal Care",
    "Kitchen",
    "Office Supplies",
    "Packaging",
    "Clothing",
    "Home & Living",
    "Food & Beverage"
]

VALID_SUSTAINABILITY_FILTERS = [
    "plastic-free",
    "compostable",
    "vegan",
    "recycled",
    "biodegradable",
    "eco-friendly",
    "organic",
    "fair-trade",
    "zero-waste",
    "cruelty-free",
    "reusable",
    "carbon-neutral"
]


def parse_ai_response(raw_text):
    """Extract and validate JSON from AI response text."""
    # Try to extract JSON from markdown code fences
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', raw_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        # Try to find raw JSON object
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0).strip()
        else:
            return None

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None

    # Validate required keys
    required_keys = ["category", "sub_category", "seo_tags", "sustainability_filters"]
    for key in required_keys:
        if key not in data:
            return None

    # Validate category is from predefined list
    if data["category"] not in VALID_CATEGORIES:
        # Try to find closest match (case-insensitive)
        for cat in VALID_CATEGORIES:
            if cat.lower() == data["category"].lower():
                data["category"] = cat
                break

    # Ensure seo_tags is a list with 5-10 items
    if not isinstance(data["seo_tags"], list):
        data["seo_tags"] = [data["seo_tags"]]
    data["seo_tags"] = data["seo_tags"][:10]  # Cap at 10

    # Ensure sustainability_filters is a list
    if not isinstance(data["sustainability_filters"], list):
        data["sustainability_filters"] = [data["sustainability_filters"]]

    return data


def generate_category(product):
    """Generate AI category, tags, and filters for a product description."""
    prompt = f"""
You are an AI assistant for a sustainable ecommerce platform.

Select the PRIMARY category ONLY from this predefined list:

- Personal Care
- Kitchen
- Office Supplies
- Packaging
- Clothing
- Home & Living
- Food & Beverage

Tasks:
1. Auto-assign the primary category from the list above
2. Suggest a sub_category
3. Generate 5-10 SEO tags (lowercase, relevant for search engines)
4. Suggest sustainability filters from: plastic-free, compostable, vegan, recycled, biodegradable, eco-friendly, organic, fair-trade, zero-waste, cruelty-free, reusable, carbon-neutral

Product description:
{product}

Return ONLY valid JSON in this exact format, no other text:

{{
  "category": "",
  "sub_category": "",
  "seo_tags": [],
  "sustainability_filters": []
}}
"""

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only responder. Output ONLY valid JSON with no extra text or markdown."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=500
        )

        raw_text = response.choices[0].message.content
        parsed = parse_ai_response(raw_text)

        if parsed:
            parsed["_raw"] = raw_text
            return {"success": True, "data": parsed}
        else:
            return {
                "success": False,
                "error": "Failed to parse AI response",
                "raw": raw_text
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "raw": None
        }