import pandas as pd
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def transform_data(df):
    """
    Melakukan pembersihan data, konversi tipe data, dan transformasi nilai 
    sesuai dengan kriteria tugas (Modular Code & Data Cleaning).
    """
    try:
        logging.info("Memulai proses transformasi data...")
        
        # 1. Copy data agar tidak mengubah dataframe asli
        df_clean = df.copy()

        # 2. Menghapus Data Invalid
        df_clean = df_clean[df_clean['Title'] != 'Unknown Product']
        df_clean = df_clean[df_clean['Price'] != 'Price Unavailable']
        df_clean = df_clean[~df_clean['Rating'].str.contains('Invalid Rating', na=False)]

        # 3. Transformasi Kolom 'Price'
        # Hapus simbol $ dan tanda koma (,), lalu konversi ke float dan kalikan 16.000
        df_clean['Price'] = df_clean['Price'].str.replace('$', '', regex=False)
        df_clean['Price'] = df_clean['Price'].str.replace(',', '', regex=False)
        df_clean['Price'] = df_clean['Price'].astype(float) * 16000

        # 4. Transformasi Kolom 'Rating'
        # Karena format dipastikan selalu desimal (misal 4.0 / 5)
        df_clean['Rating'] = df_clean['Rating'].str.extract(r'(\d+\.\d+)')[0].astype(float)

        # 5. Transformasi Kolom 'Colors'
        df_clean['Colors'] = df_clean['Colors'].str.extract(r'(\d+)')[0].astype(int)

        # 6. Transformasi Kolom 'Size' dan 'Gender'
        df_clean['Size'] = df_clean['Size'].str.replace('Size:', '', regex=False).str.strip()
        df_clean['Gender'] = df_clean['Gender'].str.replace('Gender:', '', regex=False).str.strip()

        # 7. Menghapus Duplikat
        df_clean = df_clean.drop_duplicates()

        # 8. Menghapus nilai null sisa
        df_clean = df_clean.dropna()

        # 9. Menambahkan kolom 'timestamp' 
        df_clean['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logging.info(f"Transformasi selesai. Total data bersih siap load: {len(df_clean)}")
        return df_clean

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat proses transformasi: {e}")
        raise 