#!/usr/bin/env python3
"""
Script to download all required NLTK data for sentiment analysis
"""

import nltk
import ssl

def download_nltk_data():
    """Download all required NLTK data"""
    print("Downloading NLTK data...")
    
    # Handle SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # List of required NLTK data
    required_data = [
        'punkt',           # For tokenization
        'stopwords',       # For stopword removal
        'wordnet',         # For lemmatization
        'averaged_perceptron_tagger',  # For POS tagging
        'vader_lexicon',   # For sentiment analysis
        'omw-1.4',         # For wordnet
        'punkt_tab'        # Additional tokenizer data
    ]
    
    print("Downloading required NLTK data packages...")
    
    for package in required_data:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=False)
            print(f"✓ {package} downloaded successfully")
        except Exception as e:
            print(f"✗ Failed to download {package}: {e}")
            # Try alternative download
            try:
                nltk.download(package, quiet=True)
                print(f"✓ {package} downloaded successfully (alternative method)")
            except:
                print(f"✗ {package} download failed completely")
    
    print("\nTesting NLTK functionality...")
    
    # Test tokenization
    try:
        from nltk.tokenize import word_tokenize
        test_text = "This is a test sentence."
        tokens = word_tokenize(test_text)
        print(f"✓ Tokenization works: {tokens}")
    except Exception as e:
        print(f"✗ Tokenization failed: {e}")
    
    # Test stopwords
    try:
        from nltk.corpus import stopwords
        stop_words = stopwords.words('english')
        print(f"✓ English stopwords loaded: {len(stop_words)} words")
        
        # Try Indonesian stopwords
        try:
            indo_stop_words = stopwords.words('indonesian')
            print(f"✓ Indonesian stopwords loaded: {len(indo_stop_words)} words")
        except:
            print("! Indonesian stopwords not available, will use custom list")
    except Exception as e:
        print(f"✗ Stopwords failed: {e}")
    
    print("\nNLTK setup complete!")

if __name__ == "__main__":
    download_nltk_data()
