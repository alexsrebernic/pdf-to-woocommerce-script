import logging
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
import pdf2image

# Configure OpenAI client
client = OpenAI()

def extract_text_and_tables_from_pdf(pdf_path, sku):
    logging.info(f"Processing PDF: {pdf_path}")

    try:
        images = pdf2image.convert_from_path(pdf_path)
        logging.info(f"Found {len(images)} pages in the PDF.")

        extracted_text = ""
        full_table_data = []

        for idx, image in enumerate(images):
            logging.info(f"Processing page {idx + 1}...")

            with BytesIO() as img_bytes:
                image.save(img_bytes, format="PNG")
                img_content = img_bytes.getvalue()

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": (
                            "You are a text extraction assistant for PDFs. Your role is to accurately extract all readable text "
                            "from provided images. If the image contains tabular data, retain the structure of tables in their raw form. "
                            "Provide the text content in a concise yet comprehensive manner, ensuring no data is omitted or altered." 
                        )},
                        {"role": "user", "content": [
                            {"type": "text", "text": "Extract and summarize the text content from this image, including tables if present."},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64.b64encode(img_content).decode()}"}}
                        ]}
                    ],
                    timeout=30
                )
                response_text = response.choices[0].message.content
                cleaned_text, extracted_tables = clean_and_process_text(response_text)
                extracted_text += cleaned_text + " "
                if extracted_tables:
                    full_table_data.extend(extracted_tables)

            except Exception as e:
                logging.error(f"Error in OpenAI request: {e}")
                continue

    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path}: {e}")

    return format_product_description(extracted_text, sku, pdf_path), full_table_data

def clean_and_process_text(response_text):
    lines = response_text.split("\n")
    cleaned_lines = [line for line in lines if not line.startswith("Here is")]
    cleaned_text = " ".join([line.replace("###", "").replace("**", "").strip() for line in cleaned_lines if '|' not in line])
    table_data = [line.split('|') for line in cleaned_lines if '|' in line]
    return cleaned_text, table_data

def format_product_description(text, sku, pdf_path):
    pdf_url = upload_media_to_wordpress(pdf_path, 'pdf')
    return (
        f"<h2 style='text-align: left;'>Product Title</h2>"
        f"<p style='text-align: left;'>{text.strip()}</p>"
        f"<p style='text-align: left;'>DOWNLOAD {sku} CATALOGUE:</p>"
        f"<a href='{pdf_url}'>"
        f"<img class='alignleft wp-image-2641' src='https://lighting.superluce.com.au/wp-content/uploads/2021/01/pdf.jpg' alt='download catalogue' width='50' height='51' /></a>"
    )
