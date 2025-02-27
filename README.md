# PDF to WooCommerce Products Script

This script allows you to extract text and tables from PDF files, upload images and PDFs to a WordPress site, and generate a consolidated CSV file for WooCommerce products.

## Requirements

- Python 3.x
- Install the dependencies listed in `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

## Setup

1. **Configuration File (.env):**

   Create a `.env` file in the root directory of the project with the following variables:

   ```
   WP_SITE_URL=https://your-site.local
   WP_USERNAME=your_username
   WP_APP_PASSWORD=your_password
   ```

   Make sure to replace the values with your WordPress credentials.

2. **Directory Structure:**

   - `pdfs/`: Place the PDF files you want to process here.
   - `additional-images/`: Place additional images for each product here.


## Script Input and Output

### Input
- **PDF Files**: The script processes PDF files located in the `./pdfs` directory. Each PDF file should be named with the SKU of the product it represents.
- **Environment Variables**: The script uses environment variables loaded from a `.env` file. These variables are necessary for connecting to WordPress and other configurations.

### Output
- **CSV File**: The script generates a CSV file named `all_products.csv` in the current directory. This file contains product data extracted from the PDFs, formatted for WooCommerce import.
- **ZIP File**: A ZIP file containing CSVs of extracted tables is created. This file is useful for reviewing the extracted table data separately.
- **WordPress Uploads**: Additional images associated with each product are uploaded to WordPress. The URLs of these images are included in the `all_products.csv` file.
- 
## Usage

Run the main script:

```
python script.py
```

The script will process the PDFs in the `pdfs/` directory, extract text and tables, upload images and PDFs to WordPress, and generate a consolidated CSV file `all_products.csv`.

The script logs its progress and any errors encountered during execution.


## Modules

- `modules/wordpress.py`: Functions for uploading media to WordPress.
- `modules/pdf_processing.py`: Functions for extracting text and tables from PDFs.
- `modules/file_management.py`: Functions for managing CSV and ZIP files.

## Notes

- Ensure that the WordPress server is set up to accept application credentials.
- The script disables SSL verification for local environments. Make sure to enable it in production.

## Contributions

If you'd like to contribute to this project, please open an issue or send a pull request.

