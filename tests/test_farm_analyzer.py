#!/usr/bin/env python3
"""
Test script for the Farm Data Analyzer application.

This script validates the functionality of the FarmDataRecord and FarmDataAnalyzer classes.
Uses pytest for testing framework.

Author: Lucas Zabeu
"""

import pytest
import os
from src.farm_data_analyzer import FarmDataRecord, FarmDataAnalyzer


class TestFarmDataRecord:
    """Test cases for the FarmDataRecord class."""
    
    @pytest.fixture
    def sample_record(self):
        """Create a sample FarmDataRecord for testing."""
        return FarmDataRecord(
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
    
    def test_accessors(self, sample_record):
        """Test getter methods."""
        assert sample_record.ref_date == "1908"
        assert sample_record.geo == "Canada"
        assert sample_record.area_production_farm_value == "Seeded area, potatoes"
        assert sample_record.value == "503600"
    
    def test_mutators(self, sample_record):
        """Test setter methods."""
        sample_record.ref_date = "1909"
        sample_record.geo = "United States"
        assert sample_record.ref_date == "1909"
        assert sample_record.geo == "United States"
    
    def test_string_representation(self, sample_record):
        """Test string representation."""
        str_repr = str(sample_record)
        assert "Farm Data Record:" in str_repr
        assert "1908" in str_repr
        assert "Canada" in str_repr


class TestFarmDataAnalyzer:
    """Test cases for the FarmDataAnalyzer class."""
    
    @pytest.fixture
    def csv_filename(self):
        """CSV filename for testing."""
        return "data/CST8333-Area, production  farm value (32100358).csv"
    
    @pytest.fixture
    def analyzer(self, csv_filename):
        """Create a FarmDataAnalyzer instance for testing."""
        return FarmDataAnalyzer(csv_filename)
    
    def test_initialization(self, analyzer, csv_filename):
        """Test analyzer initialization."""
        assert analyzer.csv_filename == csv_filename
        assert len(analyzer.farm_records) == 0
        assert analyzer.author_name == "Your Full Name Here"
    
    def test_file_exists(self, csv_filename):
        """Test if the CSV file exists."""
        assert os.path.exists(csv_filename), f"CSV file {csv_filename} should exist"
    
    def test_constants(self):
        """Test class constants."""
        assert FarmDataAnalyzer.REF_DATE == "REF_DATE"
        assert FarmDataAnalyzer.GEO == "GEO"
        assert FarmDataAnalyzer.VALUE == "VALUE"


# Pytest will automatically discover and run tests when you run: pytest
# You can also run specific test classes or methods:
# pytest tests/test_farm_analyzer.py::TestFarmDataRecord::test_accessors
# pytest tests/test_farm_analyzer.py::TestFarmDataAnalyzer -v