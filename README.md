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
5. **Data Structures & Algorithms**:
   - Sort records by any field using Timsort (O(n log n))
   - View top N records with analytical queries
   - Use set data structure for unique value extraction

### � **Data Structures & Algorithms Implementation**

The application demonstrates practical use of core Python data structures and algorithms:

#### **Sorting Algorithm (Timsort)**
- **Implementation**: Uses Python's built-in `sorted()` function (Timsort hybrid algorithm)
- **Complexity**: O(n log n) time complexity, stable sorting
- **Features**:
  - Sort by any field: date, location, value, measurement type, etc.
  - Ascending or descending order
  - Multi-key sorting with secondary key (ref_date) for deterministic ties
  - Smart numeric conversion for value-based sorting
  - Case-insensitive string sorting

#### **Data Structures**
- **List**: Primary in-memory container for farm records
  - Efficient sequential access
  - Supports all CRUD operations
  - Maintains insertion order (when not sorted)
  
- **Set**: Used for unique value extraction
  - O(1) average-case duplicate detection
  - Fast membership testing
  - Useful for data hygiene and filter options

#### **Analytical Features**
- **Top N Records**: Get top/bottom N records by any field without modifying main structure
- **Unique Values**: Extract unique geographic locations, measurement types, etc.
- **Stable Sorting**: Maintains relative order of equal elements

### �🛡️ **Error Handling**
- Comprehensive exception handling for file operations
- Input validation for user interactions
- Graceful handling of missing files or permissions
- Safe numeric conversion for sorting operations
- User-friendly error messages throughout

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
9. **Sort records** - Sort by any field using algorithms (Timsort O(n log n))
10. **View top N records** - Analytical queries without modifying data
11. **Exit application** - Close the program

### Example Use Cases

**Sorting Examples:**
- Sort by geographic location (alphabetically)
- Sort by farm value (highest to lowest)
- Sort by year/date (chronologically)
- Sort by measurement type

**Analytical Queries:**
- "Show me the top 10 records by farm value"
- "Display highest production areas"
- "List unique geographic regions in dataset"
- "Compare regions by sorted area values"

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

### Algorithms & Data Structures
- **Sorting Algorithm**: Python's Timsort (hybrid merge-insertion sort)
  - O(n log n) time complexity
  - Stable sorting preserves relative order of equal elements
  - Key-based comparators using `operator.attrgetter` and lambda functions
  - Multi-key sorting for deterministic results
- **Data Structures**:
  - **List**: Primary container for sequential record storage and manipulation
  - **Set**: Fast duplicate detection and unique value extraction (O(1) average case)
- **Type Conversion**: Safe numeric conversion with fallback handling for sorting
- **Performance**: In-memory operations, no database dependencies

### Design Patterns
- **Layered Architecture**: Clear separation of concerns across layers
- **Repository Pattern**: Centralized data access through `FarmDataRepository`
- **Service Layer Pattern**: Business logic encapsulated in `FarmDataService`
- **Entity Pattern**: Data encapsulation with `FarmDataRecord`

### Key Benefits
- **Maintainability**: Clear separation of responsibilities
- **Testability**: Each layer can be tested independently
- **Scalability**: Easy to extend with new features (e.g., heapq for top-k views)
- **Reusability**: Components can be reused across different interfaces
- **Performance**: Efficient O(n log n) sorting, O(1) set operations

## Requirements Met

✅ **Layered Design**: Presentation, Business, and Persistence layers implemented  
✅ **File I/O on Startup**: Loads 100 records from CSV with exception handling  
✅ **Author Display**: "Lucas Zabeu" prominently displayed throughout interface  
✅ **Data Structures & Algorithms**: 
  - ✅ List container for record storage (not simple array)
  - ✅ Set container for unique value extraction
  - ✅ Timsort algorithm for sorting by any column
  - ✅ User menu option for sorting functionality
  - ✅ Programming code/API calls (no SQL/database)
  - ✅ Ascending/descending sort order options
  - ✅ Multi-key sorting for stable results
✅ **Interactive Options**: All features implemented:
  - ✅ Reload data from dataset
  - ✅ Persist data to new CSV file
  - ✅ Display single or multiple records
  - ✅ Create new records
  - ✅ Edit existing records
  - ✅ Delete records from memory

## Testing

### Test Structure
The project includes comprehensive unit tests for all layers:

- **Entity Tests**: `TestFarmDataRecord` - Tests data model functionality
- **Persistence Tests**: `TestFarmDataRepository` - Tests file I/O operations
- **Business Tests**: `TestFarmDataService` - Tests business logic, CRUD operations, and algorithms
- **Presentation Tests**: `TestFarmDataUI` - Tests UI initialization
- **Integration Tests**: `TestIntegration` - Tests end-to-end workflows

### Running Tests
```bash
# Run all tests
python -m pytest tests/test_farm_analyzer.py -v

# Run specific test class
python -m pytest tests/test_farm_analyzer.py::TestFarmDataService -v

# Run specific test method
python -m pytest tests/test_farm_analyzer.py::TestFarmDataRecord::test_accessors -v
```

### Test Coverage
- ✅ Entity layer: Record creation, accessors, mutators, string representation, CSV conversion
- ✅ Persistence layer: File loading, saving, error handling, constants
- ✅ Business layer: CRUD operations, search, filtering, data management
- ✅ **Algorithms**: Sorting by different fields, ascending/descending order, invalid field handling
- ✅ **Data Structures**: Top N records, unique value extraction using sets
- ✅ Presentation layer: UI initialization and author attribution
- ✅ Integration: End-to-end workflow testing

### Test Results
All **25 tests** pass successfully, including:
- 5 new tests for sorting and data structure operations
- Validation of O(n log n) sorting algorithm behavior
- Set-based unique value extraction
- Top N analytical queries
# Run all tests
python -m pytest tests/test_farm_analyzer.py -v

# Run specific test class
python -m pytest tests/test_farm_analyzer.py::TestFarmDataService -v

# Run specific test method
python -m pytest tests/test_farm_analyzer.py::TestFarmDataRecord::test_accessors -v
```

### Test Coverage
- ✅ Entity layer: Record creation, accessors, mutators, string representation, CSV conversion
- ✅ Persistence layer: File loading, saving, error handling, constants
- ✅ Business layer: CRUD operations, search, filtering, data management
- ✅ Presentation layer: UI initialization and author attribution
- ✅ Integration: End-to-end workflow testing

## Documentation

### Generated HTML Documentation
The project includes comprehensive auto-generated documentation:

- **Main Index**: `docs/index.html` - Clean, organized documentation index
- **Module Documentation**: Individual HTML pages for each module
- **Layered Organization**: Documentation is organized by architectural layers:
  - 🔹 **Business Logic Layer**: Core application logic and data management
  - 🔹 **Entity/Data Models**: Farm data record objects and models  
  - 🔹 **Data Access Layer**: File I/O and persistence operations
  - 🔹 **User Interface Layer**: Interactive user interface components
  - 📦 **Test Modules**: Comprehensive unit and integration tests

### Documentation Features
- **Clean Design**: Professional styling with clear navigation
- **Modular Organization**: Only actual modules (no package-level pages)
- **Layer Descriptions**: Each architectural layer clearly identified
- **Auto-Generated**: Uses pydoc for simplicity and reliability

### Viewing Documentation
```bash
# Open the main documentation index
start docs/index.html    # Windows
open docs/index.html     # macOS  
xdg-open docs/index.html # Linux
```

### Regenerating Documentation
```bash
python generate_docs.py
```

## Author

**Lucas Zabeu**  
Programming Language Research Project  
Algonquin College @ CDI