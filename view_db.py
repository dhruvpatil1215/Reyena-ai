import sqlite3
import json

conn = sqlite3.connect("rayeva.db")
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()

for r in rows:
    tags = json.loads(r["seo_tags"]) if r["seo_tags"] else []
    filters = json.loads(r["sustainability_filters"]) if r["sustainability_filters"] else []
    print(f"""
--- Product #{r['id']} ---
Date:        {r['created_at']}
Description: {r['product_description'][:100]}
Category:    {r['category']}
Sub-cat:     {r['sub_category']}
SEO Tags:    {', '.join(tags)}
Filters:     {', '.join(filters)}""")

print(f"\n{'='*40}")
print(f"Total: {len(rows)} product(s) in database")
conn.close()
