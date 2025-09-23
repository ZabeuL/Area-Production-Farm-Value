#!/usr/bin/env python3
"""
Farm Data Analyzer Application

This Python application analyzes farm data from a CSV file containing area,
production, and farm value information for potatoes across different regions.

Author: Lucas Zabeu
Date: 2025-09-20
Course: CST8333
"""

import csv
import os
import sys
from typing import List, Optional


class FarmDataRecord:
    """
    Record object (entity/data-transfer object) representing a single farm data entry.
    
    This class uses column names from the dataset as attribute names and provides
    accessors and mutators for each field.
    """
    
    def __init__(self, ref_date: str = "", geo: str = "", dguid: str = "", 
                 area_production_farm_value: str = "", uom: str = "", 
                 uom_id: str = "", scalar_factor: str = "", scalar_id: str = "",
                 vector: str = "", coordinate: str = "", value: str = "",
                 status: str = "", symbol: str = "", terminated: str = "",
                 decimals: str = ""):
        """
        Initialize a FarmDataRecord with data from CSV columns.
        
        Args:
            ref_date: Reference date for the data
            geo: Geographic location
            dguid: Geographic unique identifier
            area_production_farm_value: Description of the measurement type
            uom: Unit of measurement
            uom_id: Unit of measurement ID
            scalar_factor: Scalar factor for the value
            scalar_id: Scalar ID
            vector: Vector identifier
            coordinate: Coordinate value
            value: The actual data value
            status: Data status
            symbol: Symbol indicator
            terminated: Termination flag
            decimals: Number of decimal places
        """
        self._ref_date = ref_date
        self._geo = geo
        self._dguid = dguid
        self._area_production_farm_value = area_production_farm_value
        self._uom = uom
        self._uom_id = uom_id
        self._scalar_factor = scalar_factor
        self._scalar_id = scalar_id
        self._vector = vector
        self._coordinate = coordinate
        self._value = value
        self._status = status
        self._symbol = symbol
        self._terminated = terminated
        self._decimals = decimals
    
    # Accessors (getters)
    @property
    def ref_date(self) -> str:
        """Get reference date."""
        return self._ref_date
    
    @property
    def geo(self) -> str:
        """Get geographic location."""
        return self._geo
    
    @property
    def dguid(self) -> str:
        """Get geographic unique identifier."""
        return self._dguid
    
    @property
    def area_production_farm_value(self) -> str:
        """Get area, production and farm value description."""
        return self._area_production_farm_value
    
    @property
    def uom(self) -> str:
        """Get unit of measurement."""
        return self._uom
    
    @property
    def uom_id(self) -> str:
        """Get unit of measurement ID."""
        return self._uom_id
    
    @property
    def scalar_factor(self) -> str:
        """Get scalar factor."""
        return self._scalar_factor
    
    @property
    def scalar_id(self) -> str:
        """Get scalar ID."""
        return self._scalar_id
    
    @property
    def vector(self) -> str:
        """Get vector identifier."""
        return self._vector
    
    @property
    def coordinate(self) -> str:
        """Get coordinate value."""
        return self._coordinate
    
    @property
    def value(self) -> str:
        """Get the data value."""
        return self._value
    
    @property
    def status(self) -> str:
        """Get data status."""
        return self._status
    
    @property
    def symbol(self) -> str:
        """Get symbol indicator."""
        return self._symbol
    
    @property
    def terminated(self) -> str:
        """Get termination flag."""
        return self._terminated
    
    @property
    def decimals(self) -> str:
        """Get number of decimal places."""
        return self._decimals
    
    # Mutators (setters)
    @ref_date.setter
    def ref_date(self, value: str) -> None:
        """Set reference date."""
        self._ref_date = value
    
    @geo.setter
    def geo(self, value: str) -> None:
        """Set geographic location."""
        self._geo = value
    
    @dguid.setter
    def dguid(self, value: str) -> None:
        """Set geographic unique identifier."""
        self._dguid = value
    
    @area_production_farm_value.setter
    def area_production_farm_value(self, value: str) -> None:
        """Set area, production and farm value description."""
        self._area_production_farm_value = value
    
    @uom.setter
    def uom(self, value: str) -> None:
        """Set unit of measurement."""
        self._uom = value
    
    @uom_id.setter
    def uom_id(self, value: str) -> None:
        """Set unit of measurement ID."""
        self._uom_id = value
    
    @scalar_factor.setter
    def scalar_factor(self, value: str) -> None:
        """Set scalar factor."""
        self._scalar_factor = value
    
    @scalar_id.setter
    def scalar_id(self, value: str) -> None:
        """Set scalar ID."""
        self._scalar_id = value
    
    @vector.setter
    def vector(self, value: str) -> None:
        """Set vector identifier."""
        self._vector = value
    
    @coordinate.setter
    def coordinate(self, value: str) -> None:
        """Set coordinate value."""
        self._coordinate = value
    
    @value.setter
    def value(self, value: str) -> None:
        """Set the data value."""
        self._value = value
    
    @status.setter
    def status(self, value: str) -> None:
        """Set data status."""
        self._status = value
    
    @symbol.setter
    def symbol(self, value: str) -> None:
        """Set symbol indicator."""
        self._symbol = value
    
    @terminated.setter
    def terminated(self, value: str) -> None:
        """Set termination flag."""
        self._terminated = value
    
    @decimals.setter
    def decimals(self, value: str) -> None:
        """Set number of decimal places."""
        self._decimals = value
    
    def __str__(self) -> str:
        """
        String representation of the farm data record.
        
        Returns:
            Formatted string showing key information from the record
        """
        return (f"Farm Data Record:\n"
                f"  Year: {self._ref_date}\n"
                f"  Location: {self._geo}\n"
                f"  Type: {self._area_production_farm_value}\n"
                f"  Value: {self._value} {self._uom}\n"
                f"  Vector: {self._vector}")


class FarmDataAnalyzer:
    """
    Main application class for analyzing farm data from CSV files.
    
    This class handles file I/O operations, data parsing, and display functionality
    with proper exception handling.
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
            csv_filename: Path to the CSV file containing farm data
        """
        self.csv_filename = csv_filename
        self.farm_records: List[FarmDataRecord] = []
        self.author_name = "Your Full Name Here"  # TODO: Replace with actual name
    
    def display_header(self) -> None:
        """
        Display the application header with author name (remains visible).
        """
        print("=" * 80)
        print(f"FARM DATA ANALYZER APPLICATION")
        print(f"Author: {self.author_name}")
        print(f"Dataset: {os.path.basename(self.csv_filename)}")
        print("=" * 80)
        print()
    
    def read_csv_data(self, max_records: int = 5) -> bool:
        """
        Read and parse CSV data with exception handling.
        
        Uses File-IO to open and read the dataset, initializing record objects
        with data parsed from the first few records in the CSV file.
        
        Args:
            max_records: Maximum number of records to read from the file
            
        Returns:
            True if successful, False if failed
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
            print(f"  Year: {record.ref_date}")
            print(f"  Location: {record.geo}")
            print(f"  Measurement Type: {record.area_production_farm_value}")
            print(f"  Value: {record.value} {record.uom}")
            print(f"  Vector ID: {record.vector}")
            print(f"  Coordinate: {record.coordinate}")
    
    def run_application(self) -> None:
        """
        Main method to run the entire application.
        
        This method orchestrates the application flow: displaying header,
        reading data, and displaying results.
        """
        # Display header with full name (remains visible)
        self.display_header()
        
        # Use File-IO with exception handling to read data
        if self.read_csv_data():
            print()
            # Loop over data structure and output records
            self.display_records()
        else:
            print("Application failed to load data. Exiting...")
            sys.exit(1)
        
        print(f"\n{'-' * 60}")
        print(f"Application completed successfully by {self.author_name}")

def main() -> None:
    """
    Main function to initialize and run the Farm Data Analyzer application.
    
    This function demonstrates all required programming concepts:
    - Variables (csv_filename, analyzer)
    - Methods (various class methods)
    - Loop structure (in display_records and read_csv_data)
    - File-IO (reading CSV dataset)
    - Exception handling (try-catch blocks)
    - API library usage (csv module)
    - Array/data structure (list of FarmDataRecord objects)
    """
    # Variable definition - CSV filename
    csv_filename = "CST8333-Area, production  farm value (32100358).csv"
    
    # Create analyzer instance (using variables and methods)
    analyzer = FarmDataAnalyzer(csv_filename)
    
    # Run the application
    analyzer.run_application()


# Entry point - execute main function when script is run directly
if __name__ == "__main__":
    main()