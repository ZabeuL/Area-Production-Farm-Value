# Farm Data Analyzer - Layered Architecture

**Author: Lucas Zabeu**

An interactive Python application for analyzing farm production data with a layered architecture design.

## Architecture Overview

This project implements a three-layered architecture pattern:

### 🎨 **Presentation Layer** (`src/presentation/`)
- **Purpose**: Handles all user interactions and display logic
- **Components**:
  - `FarmDataUI`: Interactive menu-driven user interface
- **Responsibilities**:
  - Display menus and prompts
  - Process user input and validation
  - Format and display data to users
  - Coordinate with business layer for operations

### 🧠 **Business Layer** (`src/business/`)
- **Purpose**: Contains application logic and manages in-memory data
- **Components**:
  - `FarmDataService`: Core business logic and data management
- **Responsibilities**:
  - Manage the in-memory data structure (list of records)
  - Implement CRUD operations (Create, Read, Update, Delete)
  - Provide search and filtering functionality
  - Coordinate between presentation and persistence layers

### 💾 **Persistence Layer** (`src/persistence/`)
- **Purpose**: Handles all file I/O operations
- **Components**:
  - `FarmDataRepository`: File operations and data access
- **Responsibilities**:
  - Read data from CSV files with exception handling
  - Write data to CSV files
  - Handle file-related errors gracefully

### 📊 **Entity Layer** (`src/entities/`)
- **Purpose**: Data models and record objects
- **Components**:
  - `FarmDataRecord`: Represents a single farm data entry
- **Responsibilities**:
  - Encapsulate farm data with proper accessors/mutators
  - Provide data validation and formatting
  - Enable easy serialization to/from CSV format

## Features

### 🚀 **Interactive Functionality**
1. **Data Loading**: Load/reload data from CSV dataset (up to 100 records)
2. **Data Persistence**: Save in-memory data to new CSV files
3. **Data Display**: 
   - Display single records by index
   - Display multiple records (all, by range, or first N)
4. **Data Management**:
   - Create new records with full field input
   - Edit existing records with current value defaults
   - Delete records with confirmation
   - Search records across key fields

### 🛡️ **Error Handling**
- Comprehensive exception handling for file operations
- Input validation for user interactions
- Graceful handling of missing files or permissions
- User-friendly error messages throughout

### 👤 **Author Attribution**
- "Lucas Zabeu" displayed prominently in all interfaces
- Author name visible in headers, menus, and prompts
- Consistent branding throughout the application

## Usage

### Running the Application
```bash
python main.py
```

### Default Dataset
The application automatically loads the default dataset on startup:
```
data/CST8333-Area, production  farm value (32100358).csv
```

### Interactive Menu Options
1. **Load/Reload data** - Load fresh data from CSV file
2. **Save data** - Export current data to new CSV file
3. **Display single record** - View one record by index
4. **Display multiple records** - View records with various options
5. **Create new record** - Add new farm data entry
6. **Edit existing record** - Modify record fields
7. **Delete record** - Remove record with confirmation
8. **Search records** - Find records by term matching
9. **Exit application** - Close the program

## Project Structure

```
📁 Area-Production-Farm-Value/
├── 📁 src/
│   ├── 📁 presentation/          # UI Layer
│   │   ├── __init__.py
│   │   └── farm_data_ui.py       # Interactive user interface
│   ├── 📁 business/              # Business Logic Layer
│   │   ├── __init__.py
│   │   └── farm_data_service.py  # Data management & operations
│   ├── 📁 persistence/           # Data Access Layer
│   │   ├── __init__.py
│   │   └── farm_data_repository.py # File I/O operations
│   ├── 📁 entities/              # Data Models
│   │   ├── __init__.py
│   │   └── farm_data_record.py   # Farm record entity
│   └── __init__.py
├── 📁 tests/                     # Unit tests
│   ├── __init__.py
│   └── test_farm_analyzer.py
├── 📁 data/                      # Dataset files
│   └── CST8333-Area, production  farm value (32100358).csv
├── 📁 docs/                      # Generated documentation
│   ├── index.html               # Documentation index
│   └── *.html                   # Module documentation
├── main.py                      # Application entry point
├── generate_docs.py             # Documentation generator
└── README.md                    # This file
```

## Technical Implementation

### Data Management
- **In-Memory Storage**: Uses Python list for storing up to 100 `FarmDataRecord` objects
- **CSV Processing**: Leverages Python's `csv` module for reliable file operations
- **Exception Handling**: Comprehensive error handling for file operations and user input

### Design Patterns
- **Layered Architecture**: Clear separation of concerns across layers
- **Repository Pattern**: Centralized data access through `FarmDataRepository`
- **Service Layer Pattern**: Business logic encapsulated in `FarmDataService`
- **Entity Pattern**: Data encapsulation with `FarmDataRecord`

### Key Benefits
- **Maintainability**: Clear separation of responsibilities
- **Testability**: Each layer can be tested independently
- **Scalability**: Easy to extend with new features
- **Reusability**: Components can be reused across different interfaces

## Requirements Met

✅ **Layered Design**: Presentation, Business, and Persistence layers implemented  
✅ **File I/O on Startup**: Loads 100 records from CSV with exception handling  
✅ **Author Display**: "Lucas Zabeu" prominently displayed throughout interface  
✅ **Interactive Options**: All requested functionality implemented:
  - ✅ Reload data from dataset
  - ✅ Persist data to new CSV file
  - ✅ Display single or multiple records
  - ✅ Create new records
  - ✅ Edit existing records
  - ✅ Delete records from memory

## Documentation

Generated HTML documentation is available in the `docs/` folder:
- Open `docs/index.html` in a web browser for module documentation
- Documentation includes all layers and their components

## Author

**Lucas Zabeu**  
Programming Language Research Project  
Algonquin College

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