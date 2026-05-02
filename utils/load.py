import pandas as pd
import logging
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_to_csv(df, file_path="products.csv"):
    try:
        logging.info("Memulai proses simpan ke CSV...")
        # Menyimpan DataFrame ke CSV
        df.to_csv(file_path, index=False)
        logging.info(f"Berhasil! Data telah disimpan ke {file_path}")
    except Exception as e:
        logging.error(f"Gagal menyimpan data ke CSV: {e}")
        raise

def load_to_postgres(df, db_url="postgresql://postgres:wawid300305@localhost:5432/produk_Fashion_Studio", table_name="competitor_products"):
    """Menyimpan data ke dalam database PostgreSQL"""
    try:
        logging.info("Memulai proses simpan ke PostgreSQL...")
        # Membuat engine koneksi SQLAlchemy
        engine = create_engine(db_url)
        
        # Menyimpan data
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Berhasil! Data telah disimpan ke tabel '{table_name}' di PostgreSQL.")
    except Exception as e:
        logging.error(f"Gagal menyimpan data ke PostgreSQL: {e}")
        raise

def load_to_gsheets(df, spreadsheet_id="1JeoMs4DYsd3Q52fFPAcpggBIo528KsHpavGRkQvABco", range_name="Sheet1!A1", credentials_file="google-sheets-api.json"):
    """Menyimpan data ke dalam Google Sheets menggunakan API"""
    try:
        logging.info("Memulai proses simpan ke Google Sheets...")
        
        # Setup scope dan kredensial API
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Menyiapkan data
        df_string = df.astype(str) 
        values = [df_string.columns.tolist()] + df_string.values.tolist()
        body = {'values': values}
        
        # Membersihkan sheet terlebih dahulu
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range="Sheet1"
        ).execute()
        
        # Menulis data ke Google Sheets
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body
        ).execute()
        
        logging.info(f"Berhasil! {result.get('updatedCells')} sel telah diperbarui di Google Sheets.")
    except Exception as e:
        logging.error(f"Gagal menyimpan data ke Google Sheets: {e}")
        raise

# Blok pengujian lokal
if __name__ == "__main__":
    # Mengimpor modul extract dan transform untuk mendapatkan data bersih
    from extract import extract_data
    from transform import transform_data
    
    print("Menjalankan pipeline mini untuk testing load...")
    df_raw = extract_data()
    if not df_raw.empty:
        df_clean = transform_data(df_raw)
        
        # Jalankan ketiga fungsi load
        load_to_csv(df_clean)
        load_to_postgres(df_clean)
        load_to_gsheets(df_clean)