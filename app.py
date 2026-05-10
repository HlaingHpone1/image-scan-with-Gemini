import sys
import json
from google import genai
from pydantic import BaseModel
from typing import List
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define Schema
class VoucherItem(BaseModel):
    product_name: str
    size: str
    qty: int
    unit_price: float
    total_unit_price: float

class VoucherAnalysis(BaseModel):
    date: str
    items: List[VoucherItem]
    delivery_fee: float
    grand_total_price: float

def main(image_path):
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print(json.dumps({"error": "API Key not found in .env file"}))
        return

    client = genai.Client(api_key=api_key)

    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=["Extract voucher data to JSON.", img],
        config={
            'response_mime_type': 'application/json',
            'response_schema': VoucherAnalysis,
        }
    )
    
    # Output only the JSON so n8n can catch it
    print(response.text)

if __name__ == "__main__":
    # Get image path from n8n command line argument
    img_path = sys.argv[1]

    
    main(img_path)