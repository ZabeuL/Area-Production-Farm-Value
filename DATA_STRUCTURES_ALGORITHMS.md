# Data Structures & Algorithms Implementation

**Author: Lucas Zabeu**  
**Project: Farm Data Analyzer**

## Overview

This document describes the implementation of Data Structures and Algorithms in the Farm Data Analyzer project, fulfilling the assignment requirement to use containers beyond simple arrays and implement sorting algorithms.

## Implementation Details

### 1. Data Structures (Containers)

#### **Primary Container: List**
- **Location**: `src/business/farm_data_service.py` - `_farm_records: List[FarmDataRecord]`
- **Purpose**: Main in-memory storage for farm data records
- **Features**:
  - Stores up to 100 strongly-typed `FarmDataRecord` objects
  - Supports all CRUD operations (Create, Read, Update, Delete)
  - Maintains order (insertion or sorted)
  - Efficient sequential access

#### **Supporting Container: Set**
- **Location**: `src/business/farm_data_service.py` - `get_unique_values()` method
- **Purpose**: Fast duplicate detection and unique value extraction
- **Features**:
  - O(1) average-case duplicate detection
  - Used for data hygiene checks
  - Provides unique geographic locations, measurement types, etc.
- **Code Example**:
```python
def get_unique_values(self, field: str) -> set:
    unique_values = set()
    for record in self._farm_records:
        value = getattr(record, field)
        if value:
            unique_values.add(value)
    return unique_values
```

### 2. Sorting Algorithm

#### **Algorithm: Timsort**
- **Implementation**: Python's built-in `sorted()` function
- **Complexity**: O(n log n) time complexity
- **Characteristics**:
  - Hybrid algorithm combining merge sort and insertion sort
  - Stable sorting (maintains relative order of equal elements)
  - Optimized for real-world data patterns

#### **Sorting Features**
- **Location**: `src/business/farm_data_service.py` - `sort_records()` method
- **Sortable Fields**:
  1. `ref_date` - Reference date/year (string)
  2. `geo` - Geographic location (string)
  3. `area_production_farm_value` - Measurement type (string)
  4. `value` - Data value (numeric conversion)
  5. `uom` - Unit of measurement (string)
  6. `vector` - Vector identifier (string)
  7. `coordinate` - Coordinate value (numeric conversion)

- **Sort Orders**: Ascending or Descending
- **Stability**: Multi-key sorting with secondary key (ref_date) for deterministic ties

#### **Implementation Code**:
```python
def sort_records(self, sort_by: str, ascending: bool = True) -> bool:
    """
    Sort records in-memory by specified field using Timsort (O(n log n)).
    """
    valid_fields = {
        'ref_date', 'geo', 'area_production_farm_value', 
        'value', 'uom', 'vector', 'coordinate'
    }
    
    if sort_by not in valid_fields:
        return False
    
    if sort_by == 'value':
        # Numeric sorting with fallback
        self._farm_records = sorted(
            self._farm_records,
            key=lambda record: (
                self._safe_numeric_convert(record.value),
                record.ref_date  # Secondary key for stability
            ),
            reverse=not ascending
        )
    else:
        # String sorting (case-insensitive)
        self._farm_records = sorted(
            self._farm_records,
            key=lambda record: (
                getattr(record, sort_by).lower(),
                record.ref_date
            ),
            reverse=not ascending
        )
    
    return True
```

### 3. Type Conversion for Numeric Sorting

```python
def _safe_numeric_convert(self, value: str) -> float:
    """
    Safely convert string to float for numeric sorting.
    Handles missing/invalid values gracefully.
    """
    try:
        return float(value.strip()) if value.strip() else 0.0
    except (ValueError, AttributeError):
        return 0.0  # Fallback for invalid values
```

### 4. Analytical Features

#### **Top N Records**
- **Method**: `get_top_n_records(n, sort_by, ascending)`
- **Purpose**: Analytical queries without modifying main structure
- **Use Cases**:
  - "Show top 10 by farm value"
  - "Display highest production areas"
  - "List regions by area"

```python
def get_top_n_records(self, n: int, sort_by: str = 'value', 
                     ascending: bool = False) -> List[FarmDataRecord]:
    temp_records = self._farm_records.copy()
    temp_records = sorted(
        temp_records,
        key=lambda record: self._safe_numeric_convert(record.value),
        reverse=not ascending
    )
    return temp_records[:min(n, len(temp_records))]
```

## User Interface Integration

### Menu Options
- **Option 9**: Sort records (Data Structures & Algorithms)
- **Option 10**: View top N records

### User Workflow
1. User selects field to sort by from menu
2. User chooses ascending or descending order
3. System sorts records in-place using Timsort
4. Optional preview of first 5 records
5. Main data structure is now sorted for all subsequent operations

## Benefits & Use Cases

### Direct User Benefits
1. **Quick Scanning**: Sorted views make it easy to scan and compare data
2. **Analytical Queries**: "Top 10" queries help identify patterns
3. **Regional Comparisons**: Sort by location to group regions together
4. **Value Analysis**: Sort by farm value to identify highest/lowest producers
5. **Temporal Analysis**: Sort by date to see chronological trends

### Technical Benefits
1. **Performance**: O(n log n) complexity ensures fast sorting even with 100+ records
2. **Stability**: Deterministic results with secondary sorting keys
3. **Type Safety**: Handles both numeric and string fields appropriately
4. **Error Handling**: Graceful handling of invalid/missing data
5. **In-Memory**: No database dependencies, pure Python implementation

## Implementation Compliance

### Assignment Requirements Met

✅ **Use List rather than simple array**
   - Implementation: `List[FarmDataRecord]` in business service layer
   - Location: `src/business/farm_data_service.py`

✅ **Use Set for additional functionality**
   - Implementation: `set` for unique value extraction
   - Location: `get_unique_values()` method

✅ **Sort records by column from dataset**
   - Implementation: `sort_records()` method with 7 sortable fields
   - Algorithm: Python's Timsort (O(n log n))

✅ **Use built-in API libraries**
   - `sorted()` function (Timsort)
   - `operator.attrgetter` for efficient attribute access
   - Lambda functions for key-based comparators

✅ **Offer user the option**
   - Menu options 9 and 10 in interactive UI
   - User selects field, order, and preview options

✅ **Sorting via programming code (not SQL)**
   - Pure Python implementation
   - No database or SQL statements used
   - In-memory operations only

## Testing

### Test Coverage (25 Total Tests)
- `test_sort_records_by_geo()` - String field sorting
- `test_sort_records_by_value_descending()` - Numeric sorting
- `test_sort_records_invalid_field()` - Error handling
- `test_get_top_n_records()` - Top N analytical queries
- `test_get_unique_values()` - Set-based unique extraction

### Test Results
```
tests/test_farm_analyzer.py::TestFarmDataService::test_sort_records_by_geo PASSED
tests/test_farm_analyzer.py::TestFarmDataService::test_sort_records_by_value_descending PASSED
tests/test_farm_analyzer.py::TestFarmDataService::test_sort_records_invalid_field PASSED
tests/test_farm_analyzer.py::TestFarmDataService::test_get_top_n_records PASSED
tests/test_farm_analyzer.py::TestFarmDataService::test_get_unique_values PASSED
```

## Code Organization

```
src/business/farm_data_service.py
├── Data Structures
│   ├── _farm_records: List[FarmDataRecord]  (Primary container)
│   └── get_unique_values() -> set            (Set for duplicates)
├── Sorting Algorithms
│   ├── sort_records()                        (Main sorting method)
│   ├── _safe_numeric_convert()               (Type conversion)
│   └── get_top_n_records()                   (Top N queries)

src/presentation/farm_data_ui.py
├── handle_sort_records()                     (User interface for sorting)
└── handle_top_n_records()                    (User interface for top N)
```

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Sort (Timsort) | O(n log n) | Worst and average case |
| Top N records | O(n log n) | Creates copy, sorts, returns top N |
| Unique values (Set) | O(n) | Single pass through records |
| Add to Set | O(1) | Average case for duplicate check |

## Future Extensions

The architecture supports easy extension:
1. **heapq** for more efficient top-k queries (O(n log k))
2. Additional sort keys (multi-field sorting)
3. Custom comparators for domain-specific sorting
4. Caching sorted results for repeated queries
5. Sort result persistence across sessions

---

**Implementation Date**: November 2025  
**Author**: Lucas Zabeu  
**Project**: Farm Data Analyzer - Layered Architecture  
**Course**: Programming Language Research Project, Algonquin College
