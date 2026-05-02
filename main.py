import logging
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Memulai ETL Pipeline Fashion Studio...")
    
    df_raw = extract_data()
    
    if not df_raw.empty:
        df_clean = transform_data(df_raw)
        
        load_to_csv(df_clean)
        load_to_postgres(df_clean)
        load_to_gsheets(df_clean)
        
        logging.info("Seluruh proses ETL selesai!")
    else:
        logging.warning("Data kosong, ETL dihentikan.")

if __name__ == "__main__":
    main()