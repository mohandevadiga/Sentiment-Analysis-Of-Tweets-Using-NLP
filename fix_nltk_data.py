#!/usr/bin/env python3
"""
Script to fix corrupted NLTK data by cleaning and re-downloading
"""

import os
import shutil
import nltk
import ssl

def clean_nltk_data():
    """Remove existing NLTK data directory"""
    print("Cleaning existing NLTK data...")
    
    # Get NLTK data path
    nltk_data_path = nltk.data.find('tokenizers/punkt')
    if nltk_data_path:
        # Go up to the main nltk_data directory
        nltk_data_dir = os.path.dirname(os.path.dirname(nltk_data_path))
        print(f"Found NLTK data directory: {nltk_data_dir}")
        
        try:
            # Remove the entire directory
            if os.path.exists(nltk_data_dir):
                shutil.rmtree(nltk_data_dir)
                print("✓ Existing NLTK data removed")
            else:
                print("! No existing NLTK data found")
        except Exception as e:
            print(f"! Could not remove NLTK data: {e}")
    else:
        print("! No existing NLTK data found")

def download_nltk_data_fresh():
    """Download NLTK data with proper error handling"""
    print("\nDownloading fresh NLTK data...")
    
    # Handle SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Essential packages only
    essential_packages = [
        'punkt',           # For tokenization
        'stopwords',       # For stopword removal
    ]
    
    success_count = 0
    
    for package in essential_packages:
        print(f"\nDownloading {package}...")
        try:
            # Try downloading with force=True to overwrite any corrupted files
            result = nltk.download(package, quiet=False, force=True)
            if result:
                print(f"✓ {package} downloaded successfully")
                success_count += 1
            else:
                print(f"✗ {package} download failed")
        except Exception as e:
            print(f"✗ {package} download error: {e}")
    
    return success_count == len(essential_packages)

def test_nltk_functionality():
    """Test if NLTK is working properly"""
    print("\nTesting NLTK functionality...")
    
    try:
        from nltk.tokenize import word_tokenize
        
        # Test with simple text
        test_text = "Hello world, this is a test."
        tokens = word_tokenize(test_text)
        print(f"✓ Tokenization works: {tokens}")
        return True
        
    except Exception as e:
        print(f"✗ Tokenization failed: {e}")
        return False

def alternative_tokenization():
    """Provide alternative tokenization method if NLTK fails"""
    print("\nSetting up alternative tokenization...")
    
    # Simple regex-based tokenization as fallback
    import re
    
    def simple_tokenize(text):
        """Simple tokenization using regex"""
        # Remove punctuation and split by whitespace
        text = re.sub(r'[^\w\s]', ' ', str(text))
        tokens = text.split()
        return [token.lower() for token in tokens if token.strip()]
    
    # Test the alternative method
    test_text = "Hello world, this is a test!"
    tokens = simple_tokenize(test_text)
    print(f"✓ Alternative tokenization works: {tokens}")
    
    return simple_tokenize

def main():
    """Main function to fix NLTK issues"""
    print("=" * 60)
    print("FIXING NLTK DATA CORRUPTION")
    print("=" * 60)
    
    # Step 1: Clean existing data
    clean_nltk_data()
    
    # Step 2: Download fresh data
    download_success = download_nltk_data_fresh()
    
    # Step 3: Test functionality
    if download_success:
        test_success = test_nltk_functionality()
        
        if test_success:
            print("\n🎉 NLTK is now working properly!")
            print("\nYou can now run your notebook cell again.")
        else:
            print("\n⚠️ NLTK download succeeded but testing failed.")
            print("Setting up alternative tokenization method...")
            alt_tokenize = alternative_tokenization()
            
            print("\nTo use alternative tokenization in your notebook, replace:")
            print("  from nltk.tokenize import word_tokenize")
            print("With:")
            print("  import re")
            print("  def word_tokenize(text):")
            print("      text = re.sub(r'[^\\w\\s]', ' ', str(text))")
            print("      return [token.lower() for token in text.split() if token.strip()]")
    else:
        print("\n❌ NLTK download failed.")
        print("Setting up alternative tokenization method...")
        alt_tokenize = alternative_tokenization()
        
        print("\nTo use alternative tokenization in your notebook, replace:")
        print("  from nltk.tokenize import word_tokenize")
        print("With:")
        print("  import re")
        print("  def word_tokenize(text):")
        print("      text = re.sub(r'[^\\w\\s]', ' ', str(text))")
        print("      return [token.lower() for token in text.split() if token.strip()]")

if __name__ == "__main__":
    main()
