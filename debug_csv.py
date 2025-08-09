#!/usr/bin/env python3
"""
Debug script to test CSV parsing with different methods
"""

import pandas as pd

def test_direct_pandas():
    """Test direct pandas reading with different parameters"""
    print("🔍 Testing Direct Pandas Reading...")
    
    # Try different encodings
    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    delimiters = [';', ',', '\t', '|']
    
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                df = pd.read_csv('test_football_stats.csv', sep=delimiter, encoding=encoding)
                if len(df.columns) >= 10 and len(df) > 100:  # Reasonable results
                    print(f"✅ Success with encoding={encoding}, delimiter='{delimiter}'")
                    print(f"   Shape: {df.shape}")
                    print(f"   Columns: {list(df.columns[:5])}")
                    print(f"   First player: {df.iloc[0]['Player'] if 'Player' in df.columns else 'No Player column'}")
                    return df, encoding, delimiter
            except Exception as e:
                continue
    
    print("❌ No successful combination found")
    return None, None, None

def test_file_object():
    """Test file object based reading"""
    print("\n🔍 Testing File Object Reading...")
    
    try:
        with open('test_football_stats.csv', 'rb') as f:
            # Read first few bytes
            first_bytes = f.read(100)
            print(f"First 100 bytes: {first_bytes}")
            
            f.seek(0)
            # Try with latin-1 encoding and semicolon separator
            df = pd.read_csv(f, sep=';', encoding='latin-1')
            print(f"✅ File object reading successful")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns[:5])}")
            return df
            
    except Exception as e:
        print(f"❌ File object reading failed: {e}")
        return None

def test_mock_file():
    """Test with mock file similar to what validate_and_preview_data uses"""
    print("\n🔍 Testing Mock File Reading...")
    
    class MockFile:
        def __init__(self, filepath):
            self.filepath = filepath
            self.position = 0
            
        def seek(self, pos):
            self.position = pos
            
        def read(self):
            with open(self.filepath, 'rb') as f:
                f.seek(self.position)
                return f.read()
    
    try:
        mock_file = MockFile('test_football_stats.csv')
        
        # Try to read with pandas using the mock file
        mock_file.seek(0)
        df = pd.read_csv(mock_file, sep=';', encoding='latin-1')
        print(f"✅ Mock file reading successful")
        print(f"   Shape: {df.shape}")
        return df
        
    except Exception as e:
        print(f"❌ Mock file reading failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # Test 1: Direct pandas
    df1, enc, delim = test_direct_pandas()
    
    # Test 2: File object
    df2 = test_file_object()
    
    # Test 3: Mock file
    df3 = test_mock_file()
    
    print(f"\n📊 Summary:")
    print(f"Direct pandas: {'✅' if df1 is not None else '❌'}")
    print(f"File object: {'✅' if df2 is not None else '❌'}")
    print(f"Mock file: {'✅' if df3 is not None else '❌'}")
