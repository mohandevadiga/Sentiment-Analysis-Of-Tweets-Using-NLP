#!/usr/bin/env python3
"""
Test script to detect the correct encoding for CSV files
"""

import pandas as pd
import chardet
import os

def detect_encoding(file_path):
    """Detect the encoding of a file"""
    print(f"Detecting encoding for: {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            print(f"Detected encoding: {result}")
            return result['encoding']
    except Exception as e:
        print(f"Error detecting encoding: {e}")
        return None

def test_csv_loading():
    """Test loading CSV files with different encodings"""
    
    # Change to project directory
    if os.path.exists("Sentiment-Analysis-NLP-with-Python"):
        os.chdir("Sentiment-Analysis-NLP-with-Python")
    
    files_to_test = [
        "dataset_shopee2.csv",
        "normalisasi.csv",
        "stopwords.csv"
    ]
    
    for file_name in files_to_test:
        if not os.path.exists(file_name):
            print(f"! {file_name} not found")
            continue
            
        print(f"\n{'='*50}")
        print(f"Testing: {file_name}")
        print('='*50)
        
        # Detect encoding
        detected_encoding = detect_encoding(file_name)
        
        # Try different encodings
        encodings_to_try = [
            'utf-8',
            'latin1', 
            'iso-8859-1',
            'cp1252',
            'utf-8-sig',
            detected_encoding
        ]
        
        # Remove None and duplicates
        encodings_to_try = list(set([enc for enc in encodings_to_try if enc]))
        
        success = False
        for encoding in encodings_to_try:
            try:
                print(f"Trying encoding: {encoding}")
                df = pd.read_csv(file_name, encoding=encoding)
                print(f"✓ Success with {encoding}!")
                print(f"  Shape: {df.shape}")
                print(f"  Columns: {list(df.columns)}")
                if len(df) > 0:
                    print(f"  First row: {df.iloc[0].to_dict()}")
                success = True
                break
            except Exception as e:
                print(f"✗ Failed with {encoding}: {str(e)[:100]}...")
        
        if not success:
            print(f"❌ Could not read {file_name} with any encoding")

if __name__ == "__main__":
    print("CSV ENCODING TEST")
    print("="*60)
    
    original_dir = os.getcwd()
    try:
        test_csv_loading()
    finally:
        os.chdir(original_dir)
