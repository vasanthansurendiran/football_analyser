import unittest
import pandas as pd
from pathlib import Path
import sys

# Dynamically add the 'src' directory
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from ingest import load_and_clean_data

class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        self.dataset_path = Path(__file__).parent.parent / "data" / "players.csv"
        
    def test_file_not_found_exception(self):
        """TDD: Ensure Pandas correctly raises an error for bad paths."""
        with self.assertRaises(FileNotFoundError):
            load_and_clean_data("fake_path_that_does_not_exist.csv")
            
    def test_dataframe_integrity_and_scaling(self):
        """TDD: Verify Pandas drops nulls, encodes categoricals, and returns a DataFrame."""
        # UNCOMMENT THE TWO LINES BELOW FOR YOUR PDB DEBUGGING SCREENSHOT
        # import pdb
        # pdb.set_trace() 
        
        df = load_and_clean_data(self.dataset_path)
        
        # 1. Verify we successfully built a Pandas DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        
        # 2. Verify Missing Data Handling (Should be 0 nulls in critical columns)
        self.assertEqual(df['overall'].isnull().sum(), 0)
        
        # 3. Verify Categorical Encoding worked (Right=1, Left=0)
        self.assertIn(df['preferred_foot_encoded'].iloc[0], [0.0, 1.0])
        
        # 4. Verify Feature Scaling (Scaled values usually fall between -3 and 3, not 1-99)
        # We test the first player's pace to ensure it was transformed
        self.assertTrue(-4.0 <= df['pace'].iloc[0] <= 4.0)

if __name__ == '__main__':
    unittest.main(verbosity=2)