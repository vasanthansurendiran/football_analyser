import unittest
from pathlib import Path
import sys

# Dynamically add the 'src' directory to the system path so we can import our modules
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from ingest import stream_player_data
from processor import build_tactical_roster

class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        # Resolve the absolute path to our dataset for integration testing
        self.dataset_path = Path(__file__).parent.parent / "data" / "players.csv"
        
    def test_file_not_found_exception(self):
        """TDD: Ensure our custom exception handling works for bad paths."""
        with self.assertRaises(FileNotFoundError):
            # We wrap it in list() to force the generator to evaluate immediately
            list(stream_player_data("fake_path_that_does_not_exist.csv"))
            
    def test_roster_data_integrity(self):
        """TDD: Verify the processor outputs the correct data structures and types."""
        # Note: To demonstrate pdb debugging for your assignment report, 
        # uncomment the two lines below, run the test, and take a screenshot of your terminal.
        import pdb
        pdb.set_trace() 
        
        roster = build_tactical_roster(self.dataset_path)
        
        # Verify it returns a dictionary-like object (defaultdict)
        self.assertIsInstance(roster, dict)
        
        # Verify our 4-1-2-3 key positions exist in the filtered output
        self.assertIn('ST', roster)
        self.assertIn('CB', roster)
        self.assertIn('CDM', roster)
        
        # Verify our dictionary comprehension correctly cast the stats to integers
        if len(roster['ST']) > 0:
            first_striker = roster['ST'][0]
            self.assertIsInstance(first_striker['overall'], int)
            self.assertIsInstance(first_striker['short_name'], str)

if __name__ == '__main__':
    unittest.main(verbosity=2)