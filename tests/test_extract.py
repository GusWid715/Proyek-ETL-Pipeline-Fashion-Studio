import pytest
import requests
from unittest.mock import patch, Mock
from utils.extract import extract_data

@patch('utils.extract.requests.get')
def test_extract_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    # Menyisipkan 1 data valid dan 1 data cacat untuk menguji error handling bagian dalam
    mock_response.content = b'''
    <div class="collection-card"><h3 class="product-title">Tes</h3><p class="price">$10</p></div>
    <div class="collection-card">Data HTML Rusak</div>
    '''
    mock_get.return_value = mock_response
    
    df = extract_data("http://dummy")
    assert not df.empty

@patch('utils.extract.requests.get')
def test_extract_errors(mock_get):
    # Mensimulasikan 4 jenis error berbeda secara berurutan untuk 50 halaman
    mock_get.side_effect = [
        requests.exceptions.HTTPError("HTTP Error"),
        requests.exceptions.ConnectionError("Conn Error"),
        requests.exceptions.Timeout("Timeout Error"),
        Exception("General Error")
    ] + [Exception()] * 46
    
    df = extract_data("http://dummy")
    assert df.empty