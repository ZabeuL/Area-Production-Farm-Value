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
from src.business.search_engine import SearchEngine, SearchCondition, ComparisonOperator, BooleanOperator
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
    
    def test_sort_records_by_geo(self, service):
        """Test sorting records by geographic location."""
        # Add records in random order
        service.add_record(FarmDataRecord(geo="Zebra Province", value="100"))
        service.add_record(FarmDataRecord(geo="Alpha Province", value="200"))
        service.add_record(FarmDataRecord(geo="Beta Province", value="300"))
        
        # Sort by geo ascending
        success = service.sort_records('geo', ascending=True)
        assert success == True
        
        # Verify order
        all_records = service.get_all_records()
        assert all_records[0].geo == "Alpha Province"
        assert all_records[1].geo == "Beta Province"
        assert all_records[2].geo == "Zebra Province"
    
    def test_sort_records_by_value_descending(self, service):
        """Test sorting records by numeric value in descending order."""
        # Add records with numeric values
        service.add_record(FarmDataRecord(geo="Location A", value="100"))
        service.add_record(FarmDataRecord(geo="Location B", value="500"))
        service.add_record(FarmDataRecord(geo="Location C", value="250"))
        
        # Sort by value descending
        success = service.sort_records('value', ascending=False)
        assert success == True
        
        # Verify order (highest first)
        all_records = service.get_all_records()
        assert all_records[0].value == "500"
        assert all_records[1].value == "250"
        assert all_records[2].value == "100"
    
    def test_sort_records_invalid_field(self, service, sample_record):
        """Test sorting with invalid field name."""
        service.add_record(sample_record)
        success = service.sort_records('invalid_field')
        assert success == False
    
    def test_get_top_n_records(self, service):
        """Test getting top N records."""
        # Add records
        for i in range(10):
            service.add_record(FarmDataRecord(geo=f"Location {i}", value=str(i * 100)))
        
        # Get top 3 by value
        top_records = service.get_top_n_records(3, 'value', ascending=False)
        
        assert len(top_records) == 3
        assert top_records[0].value == "900"
        assert top_records[1].value == "800"
        assert top_records[2].value == "700"
    
    def test_get_unique_values(self, service):
        """Test getting unique values using set data structure."""
        # Add records with some duplicate locations
        service.add_record(FarmDataRecord(geo="Ontario", value="100"))
        service.add_record(FarmDataRecord(geo="Quebec", value="200"))
        service.add_record(FarmDataRecord(geo="Ontario", value="300"))
        service.add_record(FarmDataRecord(geo="Alberta", value="400"))
        
        # Get unique locations
        unique_geos = service.get_unique_values('geo')
        
        assert isinstance(unique_geos, set)
        assert len(unique_geos) == 3
        assert "Ontario" in unique_geos
        assert "Quebec" in unique_geos
        assert "Alberta" in unique_geos


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


class TestSearchEngine:
    """Test cases for the SearchEngine class."""
    
    @pytest.fixture
    def sample_records(self):
        """Create sample records for search testing."""
        records = [
            FarmDataRecord(
                ref_date="2020", geo="Canada", dguid="123", 
                area_production_farm_value="Wheat", uom="Bushels", uom_id="1",
                scalar_factor="thousands", scalar_id="3", vector="v001",
                coordinate="1.1", value="1000", status="", symbol="", 
                terminated="", decimals="0"
            ),
            FarmDataRecord(
                ref_date="2020", geo="Ontario", dguid="124",
                area_production_farm_value="Corn", uom="Bushels", uom_id="1",
                scalar_factor="thousands", scalar_id="3", vector="v002",
                coordinate="1.2", value="2000", status="", symbol="",
                terminated="", decimals="0"
            ),
            FarmDataRecord(
                ref_date="2021", geo="Quebec", dguid="125",
                area_production_farm_value="Barley", uom="Bushels", uom_id="1",
                scalar_factor="thousands", scalar_id="3", vector="v003",
                coordinate="1.3", value="1500", status="", symbol="",
                terminated="", decimals="0"
            ),
            FarmDataRecord(
                ref_date="2021", geo="Alberta", dguid="126",
                area_production_farm_value="Wheat", uom="Acres", uom_id="28",
                scalar_factor="units", scalar_id="0", vector="v004",
                coordinate="1.4", value="500", status="", symbol="",
                terminated="", decimals="0"
            ),
        ]
        return records
    
    @pytest.fixture
    def search_engine(self, sample_records):
        """Create a SearchEngine instance with sample data."""
        return SearchEngine.from_records(sample_records)
    
    def test_get_available_columns(self, search_engine):
        """Test retrieving available column names."""
        columns = list(search_engine._df.columns)
        assert len(columns) > 0
        assert 'GEO' in columns
        assert 'VALUE' in columns
        assert 'REF_DATE' in columns
    
    def test_simple_equality_search(self, search_engine):
        """Test simple equality comparison."""
        condition = SearchCondition(
            column='GEO',
            operator=ComparisonOperator.EQUALS,
            value='Ontario'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 1
        assert results_df.iloc[0]['GEO'] == 'Ontario'
    
    def test_numeric_comparison_greater_than(self, search_engine):
        """Test numeric greater than comparison."""
        condition = SearchCondition(
            column='VALUE',
            operator=ComparisonOperator.GREATER_THAN,
            value='1000'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 2  # 2000 and 1500
        for _, row in results_df.iterrows():
            assert float(row['VALUE']) > 1000
    
    def test_numeric_comparison_less_than_or_equal(self, search_engine):
        """Test numeric less than or equal comparison."""
        condition = SearchCondition(
            column='VALUE',
            operator=ComparisonOperator.LESS_EQUAL,
            value='1000'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 2  # 1000 and 500
        for _, row in results_df.iterrows():
            assert float(row['VALUE']) <= 1000
    
    def test_text_contains(self, search_engine):
        """Test text contains operator."""
        condition = SearchCondition(
            column='Area, production and farm value of potatoes',
            operator=ComparisonOperator.CONTAINS,
            value='Wheat'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 2
        for _, row in results_df.iterrows():
            assert 'Wheat' in row['Area, production and farm value of potatoes']
    
    def test_text_startswith(self, search_engine):
        """Test text startswith operator."""
        condition = SearchCondition(
            column='Area, production and farm value of potatoes',
            operator=ComparisonOperator.STARTSWITH,
            value='W'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 2
        for _, row in results_df.iterrows():
            assert row['Area, production and farm value of potatoes'].startswith('W')
    
    def test_text_endswith(self, search_engine):
        """Test text endswith operator."""
        condition = SearchCondition(
            column='UOM',
            operator=ComparisonOperator.ENDSWITH,
            value='s'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) >= 1
        for _, row in results_df.iterrows():
            assert row['UOM'].endswith('s')
    
    def test_multiple_conditions_and(self, search_engine):
        """Test multiple conditions with AND logic."""
        conditions = [
            SearchCondition(
                column='REF_DATE',
                operator=ComparisonOperator.EQUALS,
                value='2020'
            ),
            SearchCondition(
                column='GEO',
                operator=ComparisonOperator.CONTAINS,
                value='a'
            )
        ]
        results_df = search_engine.search(
            conditions, 
            boolean_op=BooleanOperator.AND
        )
        assert len(results_df) == 2  # Canada and Ontario in 2020
        for _, row in results_df.iterrows():
            assert row['REF_DATE'] == '2020'
            assert 'a' in row['GEO'].lower()
    
    def test_multiple_conditions_or(self, search_engine):
        """Test multiple conditions with OR logic."""
        conditions = [
            SearchCondition(
                column='GEO',
                operator=ComparisonOperator.EQUALS,
                value='Canada'
            ),
            SearchCondition(
                column='GEO',
                operator=ComparisonOperator.EQUALS,
                value='Quebec'
            )
        ]
        results_df = search_engine.search(
            conditions,
            boolean_op=BooleanOperator.OR
        )
        assert len(results_df) == 2  # Canada or Quebec
        geos = {row['GEO'] for _, row in results_df.iterrows()}
        assert geos == {'Canada', 'Quebec'}
    
    def test_not_equals(self, search_engine):
        """Test not equals comparison."""
        condition = SearchCondition(
            column='UOM',
            operator=ComparisonOperator.NOT_EQUALS,
            value='Bushels'
        )
        results_df = search_engine.search([condition])
        for _, row in results_df.iterrows():
            assert row['UOM'] != 'Bushels'
    
    def test_empty_results(self, search_engine):
        """Test search that returns no results."""
        condition = SearchCondition(
            column='GEO',
            operator=ComparisonOperator.EQUALS,
            value='NonexistentLocation'
        )
        results_df = search_engine.search([condition])
        assert len(results_df) == 0
    
    def test_get_summary_statistics(self, search_engine):
        """Test getting summary statistics."""
        condition = SearchCondition(
            column='REF_DATE',
            operator=ComparisonOperator.EQUALS,
            value='2020'
        )
        results_df = search_engine.search([condition])
        stats = results_df.describe()
        assert len(stats) > 0  # Should have count, mean, std, etc.
    
    def test_export_to_csv(self, search_engine):
        """Test exporting search results to CSV."""
        condition = SearchCondition(
            column='GEO',
            operator=ComparisonOperator.CONTAINS,
            value='a'
        )
        results_df = search_engine.search([condition])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            results_df.to_csv(temp_filename, index=False)
            assert os.path.exists(temp_filename)
            
            # Verify file has content
            with open(temp_filename, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert 'GEO' in content
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


# Pytest will automatically discover and run tests when you run: pytest
# You can also run specific test classes or methods:
# pytest tests/test_farm_analyzer.py::TestFarmDataRecord::test_accessors
# pytest tests/test_farm_analyzer.py::TestFarmDataService -v
# pytest tests/test_farm_analyzer.py::TestIntegration::test_end_to_end_workflow -v