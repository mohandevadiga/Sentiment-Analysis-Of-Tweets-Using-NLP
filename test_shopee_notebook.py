#!/usr/bin/env python3
"""
Test script to verify the Shopee sentiment analysis notebook can run
"""

import os
import sys

def test_environment():
    """Test if all required packages are available"""
    print("Testing environment...")
    
    try:
        import pandas as pd
        print(f"✓ pandas {pd.__version__}")
    except ImportError as e:
        print(f"✗ pandas failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ numpy {np.__version__}")
    except ImportError as e:
        print(f"✗ numpy failed: {e}")
        return False
    
    try:
        import sklearn
        print(f"✓ scikit-learn {sklearn.__version__}")
    except ImportError as e:
        print(f"✗ scikit-learn failed: {e}")
        return False
    
    return True

def test_data_files():
    """Test if all required data files exist"""
    print("\nTesting data files...")
    
    # Change to the Shopee project directory
    project_dir = "Sentiment-Analysis-NLP-with-Python"
    if not os.path.exists(project_dir):
        print(f"✗ Project directory {project_dir} not found")
        return False
    
    os.chdir(project_dir)
    
    required_files = [
        "dataset_shopee2.csv",
        "normalisasi.csv", 
        "stopwords.csv"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} not found")
            return False
    
    return True

def test_data_loading():
    """Test if the main dataset can be loaded"""
    print("\nTesting data loading...")
    
    try:
        import pandas as pd
        
        # Test loading the main dataset
        data = pd.read_csv("dataset_shopee2.csv", sep=',', encoding='latin1')
        print(f"✓ dataset_shopee2.csv loaded successfully - Shape: {data.shape}")
        print(f"  Columns: {list(data.columns)}")
        
        # Show first few rows
        print("\nFirst 3 rows:")
        print(data.head(3))
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return False

def test_normalization_files():
    """Test if normalization and stopwords files can be loaded"""
    print("\nTesting normalization files...")
    
    try:
        import pandas as pd
        
        # Test normalization file
        normalizad_word = pd.read_csv("normalisasi.csv")
        print(f"✓ normalisasi.csv loaded - Shape: {normalizad_word.shape}")
        
        # Test stopwords file
        sw = pd.read_csv("stopwords.csv")
        print(f"✓ stopwords.csv loaded - Shape: {sw.shape}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading normalization files: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("SHOPEE SENTIMENT ANALYSIS ENVIRONMENT TEST")
    print("=" * 60)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Test environment
        env_ok = test_environment()
        
        # Test data files
        files_ok = test_data_files()
        
        # Test data loading
        if env_ok and files_ok:
            loading_ok = test_data_loading()
            norm_ok = test_normalization_files()
        else:
            loading_ok = False
            norm_ok = False
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Environment: {'✓ PASS' if env_ok else '✗ FAIL'}")
        print(f"Data files: {'✓ PASS' if files_ok else '✗ FAIL'}")
        print(f"Data loading: {'✓ PASS' if loading_ok else '✗ FAIL'}")
        print(f"Normalization files: {'✓ PASS' if norm_ok else '✗ FAIL'}")
        
        if env_ok and files_ok and loading_ok and norm_ok:
            print("\n🎉 All tests passed! Your Shopee sentiment analysis environment is ready.")
            print("\nTo run the notebook:")
            print("1. Make sure VS Code is using the correct Python interpreter")
            print("2. Open: Sentiment-Analysis-NLP-with-Python/shopee2021.ipynb")
            print("3. Run the cells")
        else:
            print("\n❌ Some tests failed. Please check the error messages above.")
            
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
