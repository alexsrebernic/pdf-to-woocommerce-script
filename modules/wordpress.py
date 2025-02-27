import os
import base64
import logging
import requests

# WordPress site credentials
WP_SITE_URL = os.getenv("WP_SITE_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def upload_media_to_wordpress(file_path, file_type):
    """Uploads an image or PDF to WordPress and returns the URL."""
    logging.info(f"Uploading {file_path} to WordPress...")
    
    file_name = os.path.basename(file_path)
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()}',
        'Content-Disposition': f'attachment; filename={file_name}',
    }
    url = f"{WP_SITE_URL}/wp-json/wp/v2/media"

    with open(file_path, 'rb') as file_content:
        if file_type == 'pdf':
            headers['Content-Type'] = 'application/pdf'
        else:
            headers['Content-Type'] = 'image/jpeg'
        
        # Disable SSL verification for the local environment
        response = requests.post(url, headers=headers, data=file_content, verify=False) 
    
    if response.status_code == 201:
        logging.info(f"Uploaded {file_name} successfully.")
        return response.json()['source_url']
    else:
        logging.error(f"Failed to upload {file_name}: {response.content}")
        return None

def upload_additional_images(product_name, additional_images_dir):
    """Upload additional images for a product and return URLs with the main image first."""
    main_image_url = None
    gallery_image_urls = []
    possible_main_images = [f"{product_name}_1.jpg", f"{product_name}_1.png", f"{product_name}_1.JPG", f"{product_name}_1.PNG"]

    for main_image_filename in possible_main_images:
        main_image_path = os.path.join(additional_images_dir, main_image_filename)
        if os.path.exists(main_image_path):
            main_image_url = upload_media_to_wordpress(main_image_path, 'image')
            break

    for filename in os.listdir(additional_images_dir):
        if filename.startswith(product_name) and filename not in possible_main_images and filename.lower().endswith(('.jpg', '.png')):
            file_path = os.path.join(additional_images_dir, filename)
            image_url = upload_media_to_wordpress(file_path, 'image')
            if image_url:
                gallery_image_urls.append(image_url)

    return main_image_url, gallery_image_urls
