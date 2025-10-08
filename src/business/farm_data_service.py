"""
farm_data_service.py

Business layer for farm data operations. Manages in-memory data operations
and coordinates between the presentation and persistence layers.

Classes:
    FarmDataService: Business logic for farm data management.

Author: Lucas Zabeu
"""

from typing import List, Optional
from ..entities.farm_data_record import FarmDataRecord
from ..persistence.farm_data_repository import FarmDataRepository


class FarmDataService:
    """
    Business service class for farm data operations.
    
    This class manages the in-memory data structure and provides business logic
    for CRUD operations on farm data records.
    """
    
    def __init__(self):
        """Initialize the service with an empty data structure and repository."""
        self._farm_records: List[FarmDataRecord] = []
        self._repository = FarmDataRepository()
        self._source_filename: Optional[str] = None
    
    @property
    def record_count(self) -> int:
        """Get the number of records currently in memory."""
        return len(self._farm_records)
    
    @property
    def source_filename(self) -> Optional[str]:
        """Get the filename of the currently loaded dataset."""
        return self._source_filename
    
    def load_data_from_file(self, csv_filename: str, max_records: int = 100) -> bool:
        """
        Load farm data from a CSV file into memory.
        
        Args:
            csv_filename: Path to the CSV file containing farm data.
            max_records: Maximum number of records to load (default: 100).
            
        Returns:
            True if data was loaded successfully, False otherwise.
        """
        try:
            records = self._repository.load_records_from_csv(csv_filename, max_records)
            self._farm_records = records
            self._source_filename = csv_filename
            return True
        except Exception as e:
            print(f"Failed to load data: {e}")
            return False
    
    def save_data_to_file(self, csv_filename: str) -> bool:
        """
        Save current in-memory data to a CSV file.
        
        Args:
            csv_filename: Path to the output CSV file.
            
        Returns:
            True if data was saved successfully, False otherwise.
        """
        try:
            return self._repository.save_records_to_csv(self._farm_records, csv_filename)
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False
    
    def get_all_records(self) -> List[FarmDataRecord]:
        """
        Get all records currently in memory.
        
        Returns:
            List of all FarmDataRecord objects in memory.
        """
        return self._farm_records.copy()
    
    def get_record_by_index(self, index: int) -> Optional[FarmDataRecord]:
        """
        Get a specific record by its index.
        
        Args:
            index: Zero-based index of the record to retrieve.
            
        Returns:
            FarmDataRecord object if found, None otherwise.
        """
        if 0 <= index < len(self._farm_records):
            return self._farm_records[index]
        return None
    
    def add_record(self, record: FarmDataRecord) -> bool:
        """
        Add a new record to the in-memory data structure.
        
        Args:
            record: FarmDataRecord object to add.
            
        Returns:
            True if the record was added successfully.
        """
        self._farm_records.append(record)
        return True
    
    def update_record(self, index: int, record: FarmDataRecord) -> bool:
        """
        Update an existing record at the specified index.
        
        Args:
            index: Zero-based index of the record to update.
            record: New FarmDataRecord object to replace the existing one.
            
        Returns:
            True if the record was updated successfully, False if index is invalid.
        """
        if 0 <= index < len(self._farm_records):
            self._farm_records[index] = record
            return True
        return False
    
    def delete_record(self, index: int) -> bool:
        """
        Delete a record from the in-memory data structure.
        
        Args:
            index: Zero-based index of the record to delete.
            
        Returns:
            True if the record was deleted successfully, False if index is invalid.
        """
        if 0 <= index < len(self._farm_records):
            del self._farm_records[index]
            return True
        return False
    
    def search_records(self, search_term: str) -> List[tuple[int, FarmDataRecord]]:
        """
        Search for records containing the specified term in any field.
        
        Args:
            search_term: Term to search for in record fields.
            
        Returns:
            List of tuples containing (index, record) for matching records.
        """
        results = []
        search_term_lower = search_term.lower()
        
        for index, record in enumerate(self._farm_records):
            # Search in key fields
            if (search_term_lower in record.geo.lower() or
                search_term_lower in record.ref_date.lower() or
                search_term_lower in record.area_production_farm_value.lower() or
                search_term_lower in record.value.lower()):
                results.append((index, record))
                
        return results
    
    def get_records_by_range(self, start_index: int, end_index: int) -> List[tuple[int, FarmDataRecord]]:
        """
        Get records within a specified index range.
        
        Args:
            start_index: Starting index (inclusive).
            end_index: Ending index (inclusive).
            
        Returns:
            List of tuples containing (index, record) for records in the range.
        """
        results = []
        start = max(0, start_index)
        end = min(len(self._farm_records) - 1, end_index)
        
        for index in range(start, end + 1):
            if index < len(self._farm_records):
                results.append((index, self._farm_records[index]))
                
        return results