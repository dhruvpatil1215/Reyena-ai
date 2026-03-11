import sqlite3
import json
from datetime import datetime

DB_PATH = "rayeva.db"


def get_connection():
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the products table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_description TEXT NOT NULL,
            category TEXT,
            sub_category TEXT,
            seo_tags TEXT,
            sustainability_filters TEXT,
            raw_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_product(description, ai_result):
    """Save a product and its AI-generated data to the database.
    
    Args:
        description: The original product description
        ai_result: The parsed AI result dict
    
    Returns:
        The ID of the inserted row
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (product_description, category, sub_category, seo_tags, sustainability_filters, raw_response)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        description,
        ai_result.get("category", ""),
        ai_result.get("sub_category", ""),
        json.dumps(ai_result.get("seo_tags", [])),
        json.dumps(ai_result.get("sustainability_filters", [])),
        json.dumps(ai_result)
    ))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


def get_all_products():
    """Fetch all stored products, newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = dict(row)
        # Parse JSON fields back to lists
        try:
            product["seo_tags"] = json.loads(product["seo_tags"]) if product["seo_tags"] else []
        except json.JSONDecodeError:
            product["seo_tags"] = []
        try:
            product["sustainability_filters"] = json.loads(product["sustainability_filters"]) if product["sustainability_filters"] else []
        except json.JSONDecodeError:
            product["sustainability_filters"] = []
        products.append(product)

    return products


def get_product_by_id(product_id):
    """Fetch a single product by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        product = dict(row)
        try:
            product["seo_tags"] = json.loads(product["seo_tags"]) if product["seo_tags"] else []
        except json.JSONDecodeError:
            product["seo_tags"] = []
        try:
            product["sustainability_filters"] = json.loads(product["sustainability_filters"]) if product["sustainability_filters"] else []
        except json.JSONDecodeError:
            product["sustainability_filters"] = []
        return product

    return None
