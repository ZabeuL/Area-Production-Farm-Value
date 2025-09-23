import os
import csv
import sys
from typing import List, Optional
from .farm_data_record import FarmDataRecord

"""
farm_data_analyzer.py

This module provides the FarmDataAnalyzer class for reading, analyzing,
and displaying farm data records from a CSV file. It handles file I/O,
parses CSV data into FarmDataRecord objects, and provides methods for
displaying the data in a user-friendly format.

Classes:
    FarmDataAnalyzer: Main application class for analyzing farm data.

Example:
    analyzer = FarmDataAnalyzer("data/dataset.csv")
    analyzer.run_application(max_records=10)

Attributes:
    None

Raises:
    FileNotFoundError: If the specified CSV file does not exist.
    PermissionError: If the program lacks permission to read the file.
    csv.Error: If there is an error parsing the CSV file.
"""
class FarmDataAnalyzer:
    """
    Main application class for analyzing farm data from CSV files.

    The FarmDataAnalyzer class provides functionality to:
      - Read and parse farm data from a CSV file
      - Store each record as a FarmDataRecord object
      - Display the loaded records in a formatted manner
      - Handle file I/O and CSV parsing exceptions gracefully

    Attributes:
        csv_filename (str): Path to the CSV file containing farm data.
        farm_records (List[FarmDataRecord]): List of loaded farm data records.
        author_name (str): Name of the application author.

    Methods:
        display_header(): Prints the application header and author information.
        read_csv_data(max_records): Reads and parses farm data from the CSV file.
        display_records(): Displays all loaded farm data records.
        run_application(max_records): Runs the application workflow.
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
    
    def __init__(self, csv_filename: str):
        """
        Initialize the FarmDataAnalyzer with a CSV filename.
        
        Args:
            csv_filename: Path to the CSV file containing farm data.
                Can be relative or absolute path.
        
        Attributes:
            csv_filename: Stored path to the CSV file.
            farm_records: Empty list to store FarmDataRecord objects.
            author_name: Author identifier for the application.
        """
        self.csv_filename = csv_filename
        self.farm_records: List[FarmDataRecord] = []
        self.author_name = "Lucas Zabeu"  
    
    def display_header(self) -> None:
        """
        Display the application header with author name and dataset info.
        
        Prints a formatted header that remains visible throughout the application
        execution, including author name and dataset filename.
        """
        print("=" * 80)
        print(f"FARM DATA ANALYZER APPLICATION")
        print(f"Author: {self.author_name}")
        print(f"Dataset: {os.path.basename(self.csv_filename)}")
        print("=" * 80)
        print()
    
    def read_csv_data(self, max_records: Optional[int] = None) -> bool:
        """
        Read and parse CSV data with comprehensive exception handling.

        Opens the specified CSV file, reads its contents using the csv API,
        and creates FarmDataRecord objects for each row. Records are stored
        in the farm_records list.

        Args:
            max_records: Maximum number of records to read from the file.
                If None, all records are read.

        Returns:
            bool: True if records are loaded successfully, False if an error occurs.

        Raises:
            FileNotFoundError: If the specified CSV file does not exist.
            PermissionError: If the program lacks permission to read the file.
            csv.Error: If there is an error parsing the CSV file.
            Exception: For any other unexpected errors during file processing.
        """
        try:
            # Check if file exists
            if not os.path.exists(self.csv_filename):
                raise FileNotFoundError(f"CSV file not found: {self.csv_filename}")
            
            # Open and read the CSV file using the csv API library
            with open(self.csv_filename, 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)
                
                # Variables to track records processed
                records_processed = 0
                
                # Loop through CSV rows and create record objects
                for row in csv_reader:
                    if max_records is not None and records_processed >= max_records:
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
                    
                    # Store record in the array/list data structure
                    self.farm_records.append(farm_record)
                    records_processed += 1
                
                print(f"Successfully loaded {len(self.farm_records)} farm data records.")
                return True
                
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please ensure the CSV file exists in the correct location.")
            return False
        except PermissionError:
            print("Error: Permission denied when trying to read the CSV file.")
            return False
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error occurred while reading CSV: {e}")
            return False
    
    def display_records(self) -> None:
        """
        Loop over the data structure and output record data on screen.
        
        Uses a loop structure to iterate through the farm records array
        and display each record's information.
        """
        if not self.farm_records:
            print("No farm data records to display.")
            return
        
        print(f"Displaying {len(self.farm_records)} Farm Data Records:")
        print("-" * 60)
        
        # Loop structure to iterate through the array/list data structure
        for index, record in enumerate(self.farm_records, 1):
            print(f"\nRecord #{index}:")
            print(record)
    
    def run_application(self, max_records: Optional[int] = None) -> None:
        """
        Main method to run the entire application.
        
        This method orchestrates the application flow: displaying header,
        reading data, and displaying results.
        
        Args:
            max_records: Maximum number of records to process. If None, 
                processes all records in the CSV file.
        
        Raises:
            SystemExit: If data loading fails, the application exits with code 1.
        """
        # Display header with full name (remains visible)
        self.display_header()
        
        # Use File-IO with exception handling to read data
        if self.read_csv_data(max_records):
            print()
            # Loop over data structure and output records
            self.display_records()
        else:
            print("Application failed to load data. Exiting...")
            sys.exit(1)
        
        print(f"\n{'-' * 60}")
        print(f"Application completed successfully by {self.author_name}")