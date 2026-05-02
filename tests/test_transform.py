import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform_success():
    df_raw = pd.DataFrame({
        'Title': ['Baju Tes', 'Unknown Product'],
        'Price': ['$10.00', 'Price Unavailable'],
        'Rating': ['Rating: 4.5 / 5', 'Invalid Rating'],
        'Colors': ['3 Colors', '0 Colors'],
        'Size': ['Size: M', 'Size: S'],
        'Gender': ['Gender: Men', 'Gender: Women']
    })
    
    df_clean = transform_data(df_raw)
    assert len(df_clean) == 1
    assert df_clean.iloc[0]['Price'] == 160000.0

def test_transform_error():
    with pytest.raises(Exception):
        transform_data("Bukan DataFrame")