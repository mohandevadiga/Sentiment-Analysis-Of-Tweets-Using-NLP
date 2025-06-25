#!/usr/bin/env python3
"""
Test script to verify NLTK tokenization is working
"""

import pandas as pd
from nltk.tokenize import word_tokenize

def test_tokenization():
    """Test the tokenization function that was failing"""
    print("Testing NLTK tokenization...")
    
    # Test with sample text
    sample_texts = [
        "Produk bagus, pengiriman cepat!",
        "Kualitas sesuai harga, recommended.",
        "Pelayanan kurang memuaskan.",
        "Barang sesuai deskripsi, terima kasih."
    ]
    
    def word_tokenize_wrapper(text):
        return word_tokenize(text)
    
    print("Testing individual texts:")
    for i, text in enumerate(sample_texts, 1):
        try:
            tokens = word_tokenize_wrapper(text)
            print(f"✓ Text {i}: '{text}' -> {tokens}")
        except Exception as e:
            print(f"✗ Text {i} failed: {e}")
            return False
    
    # Test with pandas Series (like in the notebook)
    print("\nTesting with pandas Series:")
    try:
        df = pd.DataFrame({'Review': sample_texts})
        df['Tokens'] = df['Review'].apply(word_tokenize_wrapper)
        print("✓ Pandas apply with tokenization works!")
        print(df[['Review', 'Tokens']].head())
        return True
    except Exception as e:
        print(f"✗ Pandas apply failed: {e}")
        return False

def test_with_actual_data():
    """Test with the actual Shopee dataset"""
    print("\n" + "="*50)
    print("Testing with actual Shopee dataset...")
    
    import os
    
    # Change to the project directory
    if os.path.exists("Sentiment-Analysis-NLP-with-Python"):
        os.chdir("Sentiment-Analysis-NLP-with-Python")
    
    try:
        # Load the dataset
        data = pd.read_csv("dataset_shopee2.csv", sep=',', encoding='latin1')
        print(f"✓ Dataset loaded: {data.shape}")
        
        # Test tokenization on first few rows
        print("\nTesting tokenization on first 3 reviews:")
        
        def word_tokenize_wrapper(text):
            return word_tokenize(str(text))  # Convert to string to handle any NaN values
        
        # Test on first 3 rows only
        sample_data = data.head(3).copy()
        sample_data['Tokens'] = sample_data['Review'].apply(word_tokenize_wrapper)
        
        print("✓ Tokenization successful on sample data!")
        
        for idx, row in sample_data.iterrows():
            print(f"Review {idx}: {row['Review'][:50]}...")
            print(f"Tokens: {row['Tokens'][:10]}...")  # Show first 10 tokens
            print()
        
        return True
        
    except Exception as e:
        print(f"✗ Error with actual data: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("NLTK TOKENIZATION TEST")
    print("=" * 60)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Test basic tokenization
        basic_ok = test_tokenization()
        
        # Test with actual data
        if basic_ok:
            actual_ok = test_with_actual_data()
        else:
            actual_ok = False
        
        print("\n" + "=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        print(f"Basic tokenization: {'✓ PASS' if basic_ok else '✗ FAIL'}")
        print(f"Actual data test: {'✓ PASS' if actual_ok else '✗ FAIL'}")
        
        if basic_ok and actual_ok:
            print("\n🎉 All tokenization tests passed!")
            print("You can now run the notebook cell that was failing.")
        else:
            print("\n❌ Some tests failed.")
            
    finally:
        # Restore original directory
        os.chdir(original_dir)
