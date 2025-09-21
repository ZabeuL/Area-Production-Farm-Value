# Farm Data Analyzer

A Python application that analyzes farm data from a CSV file containing area, production, and farm value information for potatoes across different regions.

## Author
**Your Full Name Here** - [Replace with your actual name]

## Overview
This project demonstrates various programming concepts including:
- Object-oriented programming with record/entity objects
- File I/O operations with exception handling
- Data parsing and manipulation
- Loop structures and data display
- API library usage (csv module)
- Comprehensive documentation

## Features

### 1. Record Object (FarmDataRecord)
- Uses column names from the dataset as variable names and attributes
- Implements accessors (getters) and mutators (setters) for all fields
- Provides string representation for easy data display

### 2. File I/O with Exception Handling
- Reads CSV data using Python's built-in csv module
- Handles various file-related exceptions:
  - FileNotFoundError
  - PermissionError
  - csv.Error
  - General exceptions

### 3. Data Structure
- Stores parsed records in a Python list (array-like structure)
- Initializes records with data from the first few CSV rows
- Maintains data integrity and structure

### 4. Display Functionality
- Shows author name prominently (remains visible)
- Loops through data structure to display record information
- Formats output for readability

## Programming Concepts Demonstrated

1. **Variables**: Used throughout for data storage (csv_filename, records_processed, etc.)
2. **Methods**: Multiple class methods including accessors, mutators, and utility functions
3. **Loop Structure**: for loops for iterating through CSV data and displaying records
4. **File-IO**: Reading from the CSV dataset using file operations
5. **Exception Handling**: Comprehensive try-catch blocks for error management
6. **API Library**: Usage of Python's csv module for data parsing
7. **Array/Data Structure**: List containing FarmDataRecord objects

## Dataset
The application processes the file: `CST8333-Area, production  farm value (32100358).csv`

This dataset contains the following columns:
- REF_DATE: Reference date
- GEO: Geographic location
- DGUID: Geographic unique identifier
- Area, production and farm value of potatoes: Measurement description
- UOM: Unit of measurement
- UOM_ID: Unit of measurement ID
- SCALAR_FACTOR: Scalar factor
- SCALAR_ID: Scalar ID
- VECTOR: Vector identifier
- COORDINATE: Coordinate value
- VALUE: Actual data value
- STATUS: Data status
- SYMBOL: Symbol indicator
- TERMINATED: Termination flag
- DECIMALS: Number of decimal places

## Usage

To run the application:

```bash
python3 farm_data_analyzer.py
```

## Output Example

```
================================================================================
FARM DATA ANALYZER APPLICATION
Author: Your Full Name Here
Dataset: CST8333-Area, production  farm value (32100358).csv
================================================================================

Successfully loaded 5 farm data records.

Displaying 5 Farm Data Records:
------------------------------------------------------------

Record #1:
  Year: 1908
  Location: Canada
  Measurement Type: Seeded area, potatoes
  Value: 503600 Acres
  Vector ID: v47140
  Coordinate: 1.1

Record #2:
  Year: 1908
  Location: Canada
  Measurement Type: Average yield, potatoes
  Value: 87.9 Hundredweight per harvested acres
  Vector ID: v47151
  Coordinate: 1.2

[... additional records ...]

------------------------------------------------------------
Application completed successfully by Your Full Name Here
```

## Code Structure

### FarmDataRecord Class
- **Purpose**: Record object representing individual farm data entries
- **Features**: Complete set of accessors and mutators, string representation
- **Data**: Uses actual column names from CSV as attribute names

### FarmDataAnalyzer Class
- **Purpose**: Main application logic for data processing and display
- **Features**: File I/O, exception handling, data display
- **Methods**:
  - `read_csv_data()`: Loads and parses CSV with exception handling
  - `display_records()`: Loops through data structure and displays records
  - `display_header()`: Shows application title and author name
  - `run_application()`: Main application flow orchestration

## Requirements Met

✅ **Record Object**: FarmDataRecord uses CSV column names as attributes  
✅ **File-IO**: Reads CSV dataset with exception handling  
✅ **Data Structure**: Stores records in Python list  
✅ **Loop Structure**: Iterates through records for display  
✅ **Full Name Display**: Author name remains visible throughout  
✅ **Documentation**: Comprehensive docstrings and comments  
✅ **Programming Concepts**: All required concepts implemented  
✅ **Exception Handling**: Multiple exception types handled  
✅ **API Library**: csv module usage  
✅ **Variables & Methods**: Extensive use throughout application  

## Error Handling

The application gracefully handles:
- Missing CSV files
- Permission errors
- CSV parsing errors
- General I/O exceptions

Example error output:
```
Error: CSV file not found: CST8333-Area, production  farm value (32100358).csv
Please ensure the CSV file exists in the correct location.
Application failed to load data. Exiting...
```