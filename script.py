import os
import csv
import logging
from dotenv import load_dotenv
from pathlib import Path
from modules.wordpress import upload_media_to_wordpress, upload_additional_images
from modules.pdf_processing import extract_text_and_tables_from_pdf
from modules.file_management import save_tables_to_csv_and_zip

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Directory for additional images and tables
ADDITIONAL_IMAGES_DIR = "./additional-images"
TABLES_DIR = "./extracted_tables"


def main():
    pdf_folder = "./pdfs"
    consolidated_products_csv = "all_products.csv"

    product_headers = [
        "ID", "Type", "SKU", "GTIN, UPC, EAN, or ISBN", "Name", "Published", "Is featured?", "Visibility in catalog", 
        "Short description", "Description", "Date sale price starts", "Date sale price ends", "Tax status", "Tax class",
        "In stock?", "Stock", "Low stock amount", "Backorders allowed?", "Sold individually?", "Weight (kg)", 
        "Length (cm)", "Width (cm)", "Height (cm)", "Allow customer reviews?", "Purchase note", "Sale price", 
        "Regular price", "Categories", "Tags", "Shipping class", "Images", "Download limit", 
        "Download expiry days", "Parent", "Grouped products", "Upsells", "Cross-sells", "External URL", 
        "Button text", "Position", "Brands"
    ]

    Path(ADDITIONAL_IMAGES_DIR).mkdir(parents=True, exist_ok=True)
    Path(TABLES_DIR).mkdir(parents=True, exist_ok=True)

    # Dictionary to hold table data for each SKU
    product_tables_map = {}

    try:
        with open(consolidated_products_csv, mode='w', newline='', encoding='utf-8') as product_file:
            product_writer = csv.writer(product_file)
            product_writer.writerow(product_headers)

            for filename in os.listdir(pdf_folder):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(pdf_folder, filename)
                    sku = os.path.splitext(filename)[0]
                    description, table_data = extract_text_and_tables_from_pdf(pdf_path, sku)

                    # Collect table data for this SKU
                    product_tables_map[sku] = table_data

                    # Upload additional images associated with the product
                    main_image_url, gallery_image_urls = upload_additional_images(sku)
                    image_urls = [main_image_url] + gallery_image_urls if main_image_url else gallery_image_urls

                    short_description = f"[table_id={sku}]"
                    product_data = [
                        "", "simple", sku, "", sku , "1", "1", "visible", short_description, 
                        description, "", "", "taxable", "", "1", "", "", "0", "0","", "", "", "", "1", "", "", "", 
                        "Category", "Tag", "", ", ".join(filter(None, image_urls)), "", "", "", "", "", "", "", "0", ""
                    ]

                    product_writer.writerow(product_data)

        # Save all tables into a single ZIP file
        save_tables_to_csv_and_zip(product_tables_map)
        
        logging.info(f"Process completed successfully. Products have been stored in {consolidated_products_csv}")
    
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
