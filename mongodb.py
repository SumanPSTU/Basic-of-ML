import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["medisynthia"]
collection = db["products"]


df = pd.read_excel("data.xlsx")

# clean column names
df.columns = df.columns.str.strip()

# convert price column safely
df["productPrice"] = pd.to_numeric(df["productPrice"], errors="coerce").fillna(0)

products = []

for _, row in df.iterrows():
    product = {
        "productName": row["productName"],
        "productPrice": float(row["productPrice"]),  # now always valid
        "productImgUrl": "none image",
        "strength": row["Strength"],
    }
    products.append(product)

collection.insert_many(products)

print("Data imported successfully!")