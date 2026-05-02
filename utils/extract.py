import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Setup logging dasar
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_data(base_url="https://fashion-studio.dicoding.dev"):
    """
    Mengekstrak data produk dari halaman 1 hingga 50.
    Mengembalikan data mentah dalam bentuk DataFrame pandas.
    """
    raw_data = []
    
    for page in range(1, 51):
        # Perbaikan URL agar sesuai dengan arsitektur web target
        if page == 1:
            url = f"{base_url}/"
        else:
            url = f"{base_url}/page{page}" 
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Menggunakan 'collection-card'
            product_cards = soup.find_all('div', class_='collection-card') 
            
            for card in product_cards:
                try:
                    # 1. Mengambil Judul (Title)
                    title_tag = card.find('h3', class_='product-title')
                    title = title_tag.text.strip() if title_tag else None
                    
                    # 2. Mengambil Harga (Price)
                    price_tag = card.find(class_='price')
                    price = price_tag.text.strip() if price_tag else "Price Unavailable"
                    
                    # 3. Mengambil Atribut Lainnya (Rating, Colors, Size, Gender)
                    rating, colors, size, gender = None, None, None, None
                    
                    # Cari semua tag <p> di dalam kartu produk ini
                    p_tags = card.find_all('p')
                    for p in p_tags:
                        text = p.text.strip()
                        
                        # Lewati jika tag <p> ini ternyata adalah tag harga (Price Unavailable)
                        if p.get('class') and 'price' in p.get('class'):
                            continue
                        
                        # Kategorisasi berdasarkan isi teks
                        if "Rating" in text:
                            rating = text
                        elif "Color" in text:
                            colors = text
                        elif "Size" in text:
                            size = text
                        elif "Gender" in text:
                            gender = text
                    
                    raw_data.append({
                        'Title': title,
                        'Price': price,
                        'Rating': rating,
                        'Colors': colors,
                        'Size': size,
                        'Gender': gender
                    })
                    
                except Exception as inner_e:
                    logging.warning(f"Gagal mengekstrak atribut produk di halaman {page}: {inner_e}")
                    continue
                    
        # Error handling
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error terjadi pada halaman {page}: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Gagal terhubung ke halaman {page}: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Request timeout pada halaman {page}: {timeout_err}")
        except Exception as err:
            logging.error(f"Error tidak terduga pada halaman {page}: {err}")
            
    logging.info(f"Proses ekstraksi selesai. Total data terkumpul: {len(raw_data)} dari target 1000.")
    
    return pd.DataFrame(raw_data)