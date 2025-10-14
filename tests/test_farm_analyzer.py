#!/usr/bin/env python3
"""
Test script for the Farm Data Analyzer application with layered architecture.

This script validates the functionality of the layered components:
- FarmDataRecord (Entity layer)
- FarmDataRepository (Persistence layer)
- FarmDataService (Business layer)
- FarmDataUI (Presentation layer)

Uses pytest for testing framework.

Author: Lucas Zabeu
"""

import pytest
import os
import tempfile
from src.entities.farm_data_record import FarmDataRecord
from src.persistence.farm_data_repository import FarmDataRepository
from src.business.farm_data_service import FarmDataService
from src.presentation.farm_data_ui import FarmDataUI


class TestFarmDataRecord:
    """Test cases for the FarmDataRecord entity class."""
    
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
        assert sample_record.uom == "Acres"
        assert sample_record.vector == "v47140"
    
    def test_mutators(self, sample_record):
        """Test setter methods."""
        sample_record.ref_date = "1909"
        sample_record.geo = "United States"
        sample_record.value = "600000"
        
        assert sample_record.ref_date == "1909"
        assert sample_record.geo == "United States"
        assert sample_record.value == "600000"
    
    def test_string_representation(self, sample_record):
        """Test string representation."""
        str_repr = str(sample_record)
        assert "Farm Data Record:" in str_repr
        assert "1908" in str_repr
        assert "Canada" in str_repr
        assert "Seeded area, potatoes" in str_repr
    
    def test_to_csv_row(self, sample_record):
        """Test CSV row conversion."""
        csv_row = sample_record.to_csv_row()
        assert csv_row["REF_DATE"] == "1908"
        assert csv_row["GEO"] == "Canada"
        assert csv_row["VALUE"] == "503600"
        assert "Area, production and farm value of potatoes" in csv_row


class TestFarmDataRepository:
    """Test cases for the FarmDataRepository persistence layer."""
    
    @pytest.fixture
    def repository(self):
        """Create a FarmDataRepository instance for testing."""
        return FarmDataRepository()
    
    @pytest.fixture
    def csv_filename(self):
        """CSV filename for testing."""
        return "data/CST8333-Area, production  farm value (32100358).csv"
    
    @pytest.fixture
    def sample_records(self):
        """Create sample records for testing."""
        return [
            FarmDataRecord(
                ref_date="1908",
                geo="Canada",
                dguid="2016A000011124",
                area_production_farm_value="Seeded area, potatoes",
                uom="Acres",
                value="503600"
            ),
            FarmDataRecord(
                ref_date="1909",
                geo="Ontario",
                dguid="2016A000011125",
                area_production_farm_value="Production, potatoes",
                uom="Hundredweight",
                value="44200"
            )
        ]
    
    def test_load_records_from_csv(self, repository, csv_filename):
        """Test loading records from CSV file."""
        if os.path.exists(csv_filename):
            records = repository.load_records_from_csv(csv_filename, max_records=10)
            assert len(records) > 0
            assert len(records) <= 10
            assert isinstance(records[0], FarmDataRecord)
    
    def test_load_records_file_not_found(self, repository):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            repository.load_records_from_csv("nonexistent.csv")
    
    def test_save_records_to_csv(self, repository, sample_records):
        """Test saving records to CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            success = repository.save_records_to_csv(sample_records, temp_filename)
            assert success == True
            assert os.path.exists(temp_filename)
            
            # Verify content was written
            with open(temp_filename, 'r') as f:
                content = f.read()
                assert "REF_DATE" in content  # Header
                assert "1908" in content     # Data
                assert "Canada" in content   # Data
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_save_empty_records(self, repository):
        """Test saving empty records list."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            success = repository.save_records_to_csv([], temp_filename)
            assert success == False
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_constants(self, repository):
        """Test repository constants."""
        assert repository.REF_DATE == "REF_DATE"
        assert repository.GEO == "GEO"
        assert repository.VALUE == "VALUE"


class TestFarmDataService:
    """Test cases for the FarmDataService business layer."""
    
    @pytest.fixture
    def service(self):
        """Create a FarmDataService instance for testing."""
        return FarmDataService()
    
    @pytest.fixture
    def csv_filename(self):
        """CSV filename for testing."""
        return "data/CST8333-Area, production  farm value (32100358).csv"
    
    @pytest.fixture
    def sample_record(self):
        """Create a sample record for testing."""
        return FarmDataRecord(
            ref_date="2024",
            geo="Test Location",
            area_production_farm_value="Test Data",
            value="1000"
        )
    
    def test_initialization(self, service):
        """Test service initialization."""
        assert service.record_count == 0
        assert service.source_filename is None
    
    def test_load_data_from_file(self, service, csv_filename):
        """Test loading data through service."""
        if os.path.exists(csv_filename):
            success = service.load_data_from_file(csv_filename, max_records=5)
            assert success == True
            assert service.record_count > 0
            assert service.record_count <= 5
            assert service.source_filename == csv_filename
    
    def test_add_record(self, service, sample_record):
        """Test adding a record."""
        initial_count = service.record_count
        success = service.add_record(sample_record)
        
        assert success == True
        assert service.record_count == initial_count + 1
    
    def test_get_record_by_index(self, service, sample_record):
        """Test retrieving record by index."""
        service.add_record(sample_record)
        
        retrieved_record = service.get_record_by_index(0)
        assert retrieved_record is not None
        assert retrieved_record.geo == "Test Location"
        
        # Test invalid index
        invalid_record = service.get_record_by_index(999)
        assert invalid_record is None
    
    def test_update_record(self, service, sample_record):
        """Test updating a record."""
        service.add_record(sample_record)
        
        updated_record = FarmDataRecord(
            ref_date="2025",
            geo="Updated Location",
            area_production_farm_value="Updated Data",
            value="2000"
        )
        
        success = service.update_record(0, updated_record)
        assert success == True
        
        retrieved = service.get_record_by_index(0)
        assert retrieved.geo == "Updated Location"
        assert retrieved.value == "2000"
    
    def test_delete_record(self, service, sample_record):
        """Test deleting a record."""
        service.add_record(sample_record)
        initial_count = service.record_count
        
        success = service.delete_record(0)
        assert success == True
        assert service.record_count == initial_count - 1
        
        # Test invalid index
        invalid_delete = service.delete_record(999)
        assert invalid_delete == False
    
    def test_search_records(self, service):
        """Test searching records."""
        # Add test records
        service.add_record(FarmDataRecord(geo="Canada", value="1000"))
        service.add_record(FarmDataRecord(geo="Ontario", value="2000"))
        service.add_record(FarmDataRecord(geo="Quebec", value="3000"))
        
        # Search for records
        results = service.search_records("canada")
        assert len(results) == 1
        assert results[0][1].geo == "Canada"
        
        results = service.search_records("000")
        assert len(results) == 3  # All have "000" in value
    
    def test_get_records_by_range(self, service):
        """Test getting records by range."""
        # Add test records
        for i in range(5):
            service.add_record(FarmDataRecord(geo=f"Location {i}", value=str(i * 100)))
        
        results = service.get_records_by_range(1, 3)
        assert len(results) == 3
        assert results[0][0] == 1  # First result should have index 1
        assert results[2][0] == 3  # Last result should have index 3
    
    def test_get_all_records(self, service, sample_record):
        """Test getting all records."""
        service.add_record(sample_record)
        all_records = service.get_all_records()
        
        assert len(all_records) == 1
        assert all_records[0].geo == "Test Location"


class TestFarmDataUI:
    """Test cases for the FarmDataUI presentation layer."""
    
    @pytest.fixture
    def ui(self):
        """Create a FarmDataUI instance for testing."""
        return FarmDataUI()
    
    def test_initialization(self, ui):
        """Test UI initialization."""
        assert ui._author_name == "Lucas Zabeu"
        assert ui._service.record_count == 0


# Integration tests
class TestIntegration:
    """Integration tests for the layered architecture."""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from UI to persistence."""
        service = FarmDataService()
        
        # Create a test record
        test_record = FarmDataRecord(
            ref_date="2024",
            geo="Test Province",
            area_production_farm_value="Test Production",
            uom="Test Units",
            value="12345"
        )
        
        # Add record through service
        service.add_record(test_record)
        assert service.record_count == 1
        
        # Retrieve and verify
        retrieved = service.get_record_by_index(0)
        assert retrieved.geo == "Test Province"
        assert retrieved.value == "12345"
        
        # Test save functionality with temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            success = service.save_data_to_file(temp_filename)
            assert success == True
            assert os.path.exists(temp_filename)
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


# Pytest will automatically discover and run tests when you run: pytest
# You can also run specific test classes or methods:
# pytest tests/test_farm_analyzer.py::TestFarmDataRecord::test_accessors
# pytest tests/test_farm_analyzer.py::TestFarmDataService -v
# pytest tests/test_farm_analyzer.py::TestIntegration::test_end_to_end_workflow -v