"""
farm_data_repository.py

Persistence layer for farm data operations. Handles all file I/O operations
including reading from CSV files and writing data back to disk.

Classes:
    FarmDataRepository: Handles file operations for farm data records.

Author: Lucas Zabeu
"""

import csv
import os
from typing import List, Optional
from ..entities.farm_data_record import FarmDataRecord


class FarmDataRepository:
    """
    Repository class for farm data persistence operations.
    
    This class handles all file I/O operations including:
    - Reading farm data from CSV files
    - Writing farm data to CSV files
    - Exception handling for file operations
    """
    
    # Constants for column names (using dataset column names)
    REF_DATE = "REF_DATE"
    GEO = "GEO"
    DGUID = "DGUID"
    AREA_PRODUCTION_FARM_VALUE = "Area, production and farm value of potatoes"
    UOM = "UOM"
    UOM_ID = "UOM_ID"
    SCALAR_FACTOR = "SCALAR_FACTOR"
    SCALAR_ID = "SCALAR_ID"
    VECTOR = "VECTOR"
    COORDINATE = "COORDINATE"
    VALUE = "VALUE"
    STATUS = "STATUS"
    SYMBOL = "SYMBOL"
    TERMINATED = "TERMINATED"
    DECIMALS = "DECIMALS"
    
    def __init__(self):
        """Initialize the repository."""
        pass
    
    def load_records_from_csv(self, csv_filename: str, max_records: int = 100) -> List[FarmDataRecord]:
        """
        Load farm data records from a CSV file.
        
        Args:
            csv_filename: Path to the CSV file containing farm data.
            max_records: Maximum number of records to load (default: 100).
        
        Returns:
            List of FarmDataRecord objects loaded from the file.
            
        Raises:
            FileNotFoundError: If the specified CSV file does not exist.
            PermissionError: If the program lacks permission to read the file.
            csv.Error: If there is an error parsing the CSV file.
            Exception: For any other unexpected errors during file processing.
        """
        records = []
        
        try:
            # Check if file exists
            if not os.path.exists(csv_filename):
                raise FileNotFoundError(f"CSV file not found: {csv_filename}")
            
            # Open and read the CSV file using the csv API library
            with open(csv_filename, 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)
                
                # Variables to track records processed
                records_processed = 0
                
                # Loop through CSV rows and create record objects
                for row in csv_reader:
                    if records_processed >= max_records:
                        break
                    
                    # Create a new FarmDataRecord with data from CSV row
                    farm_record = FarmDataRecord(
                        ref_date=row.get(self.REF_DATE, ""),
                        geo=row.get(self.GEO, ""),
                        dguid=row.get(self.DGUID, ""),
                        area_production_farm_value=row.get(self.AREA_PRODUCTION_FARM_VALUE, ""),
                        uom=row.get(self.UOM, ""),
                        uom_id=row.get(self.UOM_ID, ""),
                        scalar_factor=row.get(self.SCALAR_FACTOR, ""),
                        scalar_id=row.get(self.SCALAR_ID, ""),
                        vector=row.get(self.VECTOR, ""),
                        coordinate=row.get(self.COORDINATE, ""),
                        value=row.get(self.VALUE, ""),
                        status=row.get(self.STATUS, ""),
                        symbol=row.get(self.SYMBOL, ""),
                        terminated=row.get(self.TERMINATED, ""),
                        decimals=row.get(self.DECIMALS, "")
                    )
                    
                    # Store record in the list
                    records.append(farm_record)
                    records_processed += 1
                    
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please ensure the CSV file exists in the correct location.")
            raise
        except PermissionError:
            print("Error: Permission denied when trying to read the CSV file.")
            raise
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error occurred while reading CSV: {e}")
            raise
            
        return records
    
    def save_records_to_csv(self, records: List[FarmDataRecord], csv_filename: str) -> bool:
        """
        Save farm data records to a CSV file.
        
        Args:
            records: List of FarmDataRecord objects to save.
            csv_filename: Path to the output CSV file.
            
        Returns:
            True if the file was saved successfully, False otherwise.
            
        Raises:
            PermissionError: If the program lacks permission to write the file.
            Exception: For any other unexpected errors during file writing.
        """
        try:
            if not records:
                print("No records to save.")
                return False
                
            # Define fieldnames in the order they appear in the original CSV
            fieldnames = [
                self.REF_DATE, self.GEO, self.DGUID, self.AREA_PRODUCTION_FARM_VALUE,
                self.UOM, self.UOM_ID, self.SCALAR_FACTOR, self.SCALAR_ID,
                self.VECTOR, self.COORDINATE, self.VALUE, self.STATUS,
                self.SYMBOL, self.TERMINATED, self.DECIMALS
            ]
            
            with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for record in records:
                    writer.writerow(record.to_csv_row())
                    
            return True
            
        except PermissionError:
            print("Error: Permission denied when trying to write the CSV file.")
            raise
        except Exception as e:
            print(f"Unexpected error occurred while writing CSV: {e}")
            raise