import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["medisynthia"]
collection = db["products"]

# Load Excel data
df = pd.read_excel("data.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Convert price column safely
df["productPrice"] = pd.to_numeric(df["productPrice"], errors="coerce").fillna(0)

products = []

for _, row in df.iterrows():
    # Skip rows where essential fields are missing
    if pd.isna(row["productName"]) or pd.isna(row["productGeneric"]) or pd.isna(row["Strength"]):
        continue  # skip this row

    product_name = str(row["productName"]).strip()
    product_generic = str(row["productGeneric"]).strip()
    strength = str(row["Strength"]).strip()
    price = float(row["productPrice"]) if not pd.isna(row["productPrice"]) else 0

    # Only set productImgUrl if missing
    img_url = str(row["productImgUrl"]).strip() if "productImgUrl" in row and pd.notna(row["productImgUrl"]) and str(row["productImgUrl"]).strip() != "" else "none image"

    product = {
        "productName": product_name,
        "productGeneric": product_generic,
        "strength": strength,
        "productImgUrl": img_url,
        "isAvailable": True,
        "productPrice": price
    }

    products.append(product)

if products:
    collection.insert_many(products)
    print(f"Data imported successfully! {len(products)} products added.")
else:
    print("No valid data to import.")