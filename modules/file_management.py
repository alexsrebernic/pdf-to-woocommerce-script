import os
import csv
import logging
import zipfile

def save_tables_to_csv_and_zip(table_data_map, tables_dir, zip_filename='all_products_tables.zip'):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for sku, tables in table_data_map.items():
            csv_filename = f'{sku}_tables.csv'
            csv_path = os.path.join(tables_dir, csv_filename)
            
            # Write the table data for the current product to a CSV file
            with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(tables)
                logging.info(f"Saved complete table for {sku} to {csv_path}")
            
            # Add the CSV file to the ZIP archive with the filename, ensuring it's at the root
            zipf.write(csv_path, arcname=csv_filename)
            logging.info(f"CSV for {sku} added to zip as {csv_filename}")

    logging.info(f"All product CSVs have been zipped into {zip_filename}")
