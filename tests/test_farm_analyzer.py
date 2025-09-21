#!/usr/bin/env python3
"""
Test script for the Farm Data Analyzer application.

This script validates the functionality of the FarmDataRecord and FarmDataAnalyzer classes.
"""

import unittest
import os
import sys
from src.farm_data_analyzer import FarmDataRecord, FarmDataAnalyzer


class TestFarmDataRecord(unittest.TestCase):
    """Test cases for the FarmDataRecord class."""
    
    def setUp(self):
        """Set up test data."""
        self.record = FarmDataRecord(
            ref_date="1908",
            geo="Canada",
            dguid="2016A000011124",
            area_production_farm_value="Seeded area, potatoes",
            uom="Acres",
            uom_id="28",
            scalar_factor="units",
            scalar_id="0",
            vector="v47140",
            coordinate="1.1",
            value="503600",
            status="",
            symbol="",
            terminated="",
            decimals="0"
        )
    
    def test_accessors(self):
        """Test getter methods."""
        self.assertEqual(self.record.ref_date, "1908")
        self.assertEqual(self.record.geo, "Canada")
        self.assertEqual(self.record.area_production_farm_value, "Seeded area, potatoes")
        self.assertEqual(self.record.value, "503600")
    
    def test_mutators(self):
        """Test setter methods."""
        self.record.ref_date = "1909"
        self.record.geo = "United States"
        self.assertEqual(self.record.ref_date, "1909")
        self.assertEqual(self.record.geo, "United States")
    
    def test_string_representation(self):
        """Test string representation."""
        str_repr = str(self.record)
        self.assertIn("Farm Data Record:", str_repr)
        self.assertIn("1908", str_repr)
        self.assertIn("Canada", str_repr)


class TestFarmDataAnalyzer(unittest.TestCase):
    """Test cases for the FarmDataAnalyzer class."""
    
    def setUp(self):
        """Set up test data."""
        self.csv_filename = "CST8333-Area, production  farm value (32100358).csv"
        self.analyzer = FarmDataAnalyzer(self.csv_filename)
    
    def test_initialization(self):
        """Test analyzer initialization."""
        self.assertEqual(self.analyzer.csv_filename, self.csv_filename)
        self.assertEqual(len(self.analyzer.farm_records), 0)
        self.assertEqual(self.analyzer.author_name, "Your Full Name Here")
    
    def test_file_exists(self):
        """Test if the CSV file exists."""
        self.assertTrue(os.path.exists(self.csv_filename), 
                       f"CSV file {self.csv_filename} should exist")
    
    def test_constants(self):
        """Test class constants."""
        self.assertEqual(FarmDataAnalyzer.REF_DATE, "REF_DATE")
        self.assertEqual(FarmDataAnalyzer.GEO, "GEO")
        self.assertEqual(FarmDataAnalyzer.VALUE, "VALUE")


def run_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("RUNNING FARM DATA ANALYZER TESTS")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestFarmDataRecord))
    test_suite.addTest(unittest.makeSuite(TestFarmDataAnalyzer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("ALL TESTS PASSED!")
    else:
        print(f"TESTS FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the tests
    success = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)