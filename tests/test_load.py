import pytest
import os
import pandas as pd
from unittest.mock import patch
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

df_dummy = pd.DataFrame({'Title': ['Tes'], 'Price': [160000.0]})

def test_load_csv(tmp_path):
    file_path = tmp_path / "test.csv"
    load_to_csv(df_dummy, str(file_path))
    assert os.path.exists(file_path)

def test_load_csv_error():
    with pytest.raises(Exception):
        load_to_csv(df_dummy, "/folder_tidak_ada/test.csv")

@patch('utils.load.create_engine')
@patch('pandas.DataFrame.to_sql')
def test_load_postgres(mock_to_sql, mock_create_engine):
    load_to_postgres(df_dummy, db_url="sqlite:///:memory:")
    mock_to_sql.assert_called_once()

def test_load_postgres_error():
    with pytest.raises(Exception):
        load_to_postgres("Data Error")

@patch('utils.load.build')
@patch('utils.load.Credentials.from_service_account_file')
def test_load_gsheets(mock_creds, mock_build):
    load_to_gsheets(df_dummy, credentials_file="dummy.json")
    mock_build.assert_called_once()

def test_load_gsheets_error():
    with pytest.raises(Exception):
        load_to_gsheets("Data Error")