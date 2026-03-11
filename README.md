# AI Auto-Category & Tag Generator

## Overview

This project implements **Module 1: AI Auto-Category & Tag Generator** from the Rayeva AI Systems Assignment.

The purpose of this module is to reduce manual catalog effort in sustainable ecommerce platforms by automatically classifying products and generating metadata using AI.

The system analyzes a product description and automatically generates:

* Primary category
* Sub-category
* SEO tags
* Sustainability filters

The output is returned in **structured JSON format** and can be stored in a database for further processing.

---

# Features

## 1. Auto Assign Primary Category

The AI automatically selects the correct **primary category from a predefined list**.

Example categories:

* Personal Care
* Kitchen
* Office Supplies
* Packaging
* Clothing
* Home & Living
* Food & Beverage

This ensures consistent product classification.

---

## 2. Sub-category Suggestion

The AI suggests a **more specific sub-category** based on the product description.

Example:

Category: Personal Care
Sub-category: Oral Care

---

## 3. SEO Tag Generation

The system generates **5–10 SEO tags** automatically to improve product discoverability.

Example:

["bamboo toothbrush", "eco toothbrush", "plastic free toothbrush", "biodegradable toothbrush"]

---

## 4. Sustainability Filters

The AI identifies sustainability attributes such as:

* plastic-free
* compostable
* vegan
* recycled
* biodegradable
* eco-friendly

These filters help customers easily find environmentally friendly products.

---

## 5. Structured JSON Output

{
 "category": "Personal Care",
 "sub_category": "Oral Care",
 "seo_tags": [
  "bamboo toothbrush",
  "eco toothbrush",
  "plastic free toothbrush"
 ],
 "sustainability_filters": [
  "plastic-free",
  "biodegradable",
  "eco-friendly"
 ]
}

---

# Architecture Overview

The system separates **business logic** from **AI processing**.

User Input (Product Description)
↓
AI Prompt Processing
↓
Groq LLM
↓
Structured JSON Response
↓
Database Storage

This architecture ensures clean separation between:

* AI logic
* business rules
* application layer

---

# AI Prompt Design

The prompt instructs the AI model to:

1. Choose a category from a predefined list
2. Suggest a relevant sub-category
3. Generate 5–10 SEO tags
4. Identify sustainability filters
5. Return the result as structured JSON

Example prompt:

You are an AI assistant for a sustainable ecommerce platform.

Select the primary category ONLY from this list:

Personal Care
Kitchen
Office Supplies
Packaging
Clothing
Home & Living
Food & Beverage

Tasks:

1. Assign the correct category
2. Suggest a sub-category
3. Generate SEO tags
4. Suggest sustainability filters

Return only valid JSON.

---

# Technologies Used

* Python
* Flask
* Groq API (LLM)
* HTML / CSS (UI demo)
* JSON
* dotenv

---

# How to Run

Install dependencies:

pip install -r requirements.txt

Add environment variables:

GROQ_API_KEY=your_api_key

Run the application:

python app.py

Open in browser:

http://127.0.0.1:5000

---

# Example Input

Bamboo toothbrush biodegradable eco friendly plastic free handle

---

# Example Output

{
"category": "Personal Care",
"sub_category": "Oral Care",
"seo_tags": [
"bamboo toothbrush",
"eco toothbrush",
"plastic free toothbrush"
],
"sustainability_filters": [
"plastic-free",
"biodegradable",
"eco-friendly"
]
}

---

# Future Improvements

* Category confidence scoring
* Multi-language product classification
* AI assisted product description generation
* Advanced sustainability scoring

---

# Author

Dhruv Patil
AI Systems Assignment Submission
