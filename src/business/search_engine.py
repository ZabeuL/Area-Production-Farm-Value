"""
search_engine.py

Business layer for advanced search and filtering operations using pandas.
Provides interactive search capabilities with multiple operators, boolean logic,
and type-aware filtering.

Classes:
    SearchEngine: Advanced search and filtering engine for farm data.
    SearchCondition: Represents a single search condition with operator and value.

Author: Lucas Zabeu
"""

import pandas as pd
import re
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ComparisonOperator(Enum):
    """Enumeration of supported comparison operators."""
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    CONTAINS = "contains"
    REGEX = "regex"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"


class BooleanOperator(Enum):
    """Enumeration of boolean logic operators."""
    AND = "AND"
    OR = "OR"


@dataclass
class SearchCondition:
    """
    Represents a single search condition.
    
    Attributes:
        column: Column name to search in
        operator: Comparison operator to use
        value: Value to compare against
        case_sensitive: Whether string comparisons are case-sensitive
    """
    column: str
    operator: ComparisonOperator
    value: Any
    case_sensitive: bool = False


class SearchEngine:
    """
    Advanced search engine for filtering farm data records.
    
    This class provides sophisticated filtering capabilities including:
    - Multiple comparison operators (==, !=, >, <, >=, <=)
    - Text-based operators (contains, regex, startswith, endswith)
    - Boolean logic (AND/OR) for combining conditions
    - Type-aware value conversion
    - Search refinement on previous results
    
    Uses pandas DataFrame for efficient filtering operations.
    """
    
    # Column name mappings from FarmDataRecord to CSV columns
    COLUMN_MAPPING = {
        'ref_date': 'REF_DATE',
        'geo': 'GEO',
        'dguid': 'DGUID',
        'area_production_farm_value': 'Area, production and farm value of potatoes',
        'uom': 'UOM',
        'uom_id': 'UOM_ID',
        'scalar_factor': 'SCALAR_FACTOR',
        'scalar_id': 'SCALAR_ID',
        'vector': 'VECTOR',
        'coordinate': 'COORDINATE',
        'value': 'VALUE',
        'status': 'STATUS',
        'symbol': 'SYMBOL',
        'terminated': 'TERMINATED',
        'decimals': 'DECIMALS'
    }
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize search engine with a pandas DataFrame.
        
        Args:
            dataframe: pandas DataFrame containing farm data records
        """
        self._df = dataframe.copy()
        self._last_results: Optional[pd.DataFrame] = None
        self._search_history: List[Tuple[List[SearchCondition], BooleanOperator]] = []
    
    @classmethod
    def from_records(cls, records: List) -> 'SearchEngine':
        """
        Create a SearchEngine from a list of FarmDataRecord objects.
        
        Args:
            records: List of FarmDataRecord objects
            
        Returns:
            SearchEngine instance initialized with records
        """
        data = []
        for record in records:
            data.append({
                'REF_DATE': record.ref_date,
                'GEO': record.geo,
                'DGUID': record.dguid,
                'Area, production and farm value of potatoes': record.area_production_farm_value,
                'UOM': record.uom,
                'UOM_ID': record.uom_id,
                'SCALAR_FACTOR': record.scalar_factor,
                'SCALAR_ID': record.scalar_id,
                'VECTOR': record.vector,
                'COORDINATE': record.coordinate,
                'VALUE': record.value,
                'STATUS': record.status,
                'SYMBOL': record.symbol,
                'TERMINATED': record.terminated,
                'DECIMALS': record.decimals
            })
        
        df = pd.DataFrame(data)
        return cls(df)
    
    def get_available_columns(self) -> List[str]:
        """
        Get list of available column names.
        
        Returns:
            List of column names in the DataFrame
        """
        return list(self._df.columns)
    
    def get_column_type(self, column: str) -> str:
        """
        Get the data type of a column.
        
        Args:
            column: Column name
            
        Returns:
            String representation of column data type
        """
        if column not in self._df.columns:
            return "unknown"
        
        dtype = self._df[column].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            return "numeric"
        else:
            return "text"
    
    def _convert_value(self, column: str, value: str) -> Any:
        """
        Convert user input value to match column data type.
        
        Args:
            column: Column name to match type for
            value: String value from user input
            
        Returns:
            Converted value matching column data type
        """
        if column not in self._df.columns:
            return value
        
        col_type = self.get_column_type(column)
        
        if col_type == "numeric":
            try:
                # Try integer first
                if '.' not in value:
                    return int(value)
                else:
                    return float(value)
            except ValueError:
                # Return as string if conversion fails
                return value
        
        return value
    
    def _apply_condition(self, df: pd.DataFrame, condition: SearchCondition) -> pd.Series:
        """
        Apply a single search condition to a DataFrame.
        
        Args:
            df: DataFrame to filter
            condition: Search condition to apply
            
        Returns:
            Boolean Series indicating which rows match the condition
        """
        if condition.column not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        column_data = df[condition.column]
        value = condition.value
        
        # Handle string operations
        if condition.operator == ComparisonOperator.CONTAINS:
            if not condition.case_sensitive:
                return column_data.astype(str).str.lower().str.contains(
                    str(value).lower(), regex=False, na=False
                )
            return column_data.astype(str).str.contains(str(value), regex=False, na=False)
        
        elif condition.operator == ComparisonOperator.REGEX:
            try:
                return column_data.astype(str).str.contains(
                    str(value), regex=True, na=False,
                    case=condition.case_sensitive
                )
            except re.error:
                # Invalid regex, return no matches
                return pd.Series([False] * len(df), index=df.index)
        
        elif condition.operator == ComparisonOperator.STARTSWITH:
            if not condition.case_sensitive:
                return column_data.astype(str).str.lower().str.startswith(str(value).lower())
            return column_data.astype(str).str.startswith(str(value))
        
        elif condition.operator == ComparisonOperator.ENDSWITH:
            if not condition.case_sensitive:
                return column_data.astype(str).str.lower().str.endswith(str(value).lower())
            return column_data.astype(str).str.endswith(str(value))
        
        # Handle comparison operations
        elif condition.operator == ComparisonOperator.EQUALS:
            return column_data == value
        
        elif condition.operator == ComparisonOperator.NOT_EQUALS:
            return column_data != value
        
        elif condition.operator == ComparisonOperator.GREATER_THAN:
            # Try numeric comparison
            try:
                return pd.to_numeric(column_data, errors='coerce') > float(value)
            except (ValueError, TypeError):
                return column_data > value
        
        elif condition.operator == ComparisonOperator.LESS_THAN:
            try:
                return pd.to_numeric(column_data, errors='coerce') < float(value)
            except (ValueError, TypeError):
                return column_data < value
        
        elif condition.operator == ComparisonOperator.GREATER_EQUAL:
            try:
                return pd.to_numeric(column_data, errors='coerce') >= float(value)
            except (ValueError, TypeError):
                return column_data >= value
        
        elif condition.operator == ComparisonOperator.LESS_EQUAL:
            try:
                return pd.to_numeric(column_data, errors='coerce') <= float(value)
            except (ValueError, TypeError):
                return column_data <= value
        
        return pd.Series([False] * len(df), index=df.index)
    
    def search(
        self,
        conditions: List[SearchCondition],
        boolean_op: BooleanOperator = BooleanOperator.AND,
        refine_previous: bool = False
    ) -> pd.DataFrame:
        """
        Execute a search with multiple conditions.
        
        Args:
            conditions: List of search conditions to apply
            boolean_op: Boolean operator to combine conditions (AND/OR)
            refine_previous: If True, search within previous results
            
        Returns:
            DataFrame containing matching records
        """
        # Start with full dataset or previous results
        if refine_previous and self._last_results is not None:
            df = self._last_results.copy()
        else:
            df = self._df.copy()
        
        if not conditions:
            self._last_results = df
            return df
        
        # Apply first condition
        mask = self._apply_condition(df, conditions[0])
        
        # Combine remaining conditions with boolean operator
        for condition in conditions[1:]:
            condition_mask = self._apply_condition(df, condition)
            
            if boolean_op == BooleanOperator.AND:
                mask = mask & condition_mask
            else:  # OR
                mask = mask | condition_mask
        
        # Filter DataFrame
        results = df[mask].copy()
        
        # Store results and history
        self._last_results = results
        self._search_history.append((conditions, boolean_op))
        
        return results
    
    def get_last_results(self) -> Optional[pd.DataFrame]:
        """
        Get the results from the last search.
        
        Returns:
            DataFrame of last search results, or None if no search performed
        """
        return self._last_results.copy() if self._last_results is not None else None
    
    def clear_results(self) -> None:
        """Clear last search results and history."""
        self._last_results = None
        self._search_history.clear()
    
    def get_summary_statistics(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Get summary statistics for numeric columns in the DataFrame.
        
        Args:
            df: DataFrame to analyze (uses last results if None)
            
        Returns:
            Dictionary containing summary statistics
        """
        if df is None:
            df = self._last_results if self._last_results is not None else self._df
        
        stats = {}
        
        # Overall statistics
        stats['total_records'] = len(df)
        
        # Numeric column statistics
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # Text column statistics
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            stats[f'{col}_unique_count'] = df[col].nunique()
            stats[f'{col}_most_common'] = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else None
        
        return stats
    
    def export_to_csv(self, filename: str, df: Optional[pd.DataFrame] = None) -> bool:
        """
        Export search results to CSV file.
        
        Args:
            filename: Output CSV filename
            df: DataFrame to export (uses last results if None)
            
        Returns:
            True if export successful, False otherwise
        """
        if df is None:
            df = self._last_results if self._last_results is not None else self._df
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def get_unique_values(self, column: str, df: Optional[pd.DataFrame] = None) -> List[Any]:
        """
        Get unique values from a column.
        
        Args:
            column: Column name
            df: DataFrame to analyze (uses last results if None)
            
        Returns:
            List of unique values sorted
        """
        if df is None:
            df = self._last_results if self._last_results is not None else self._df
        
        if column not in df.columns:
            return []
        
        unique_vals = df[column].dropna().unique()
        try:
            return sorted(unique_vals)
        except TypeError:
            # If values can't be sorted, return as list
            return list(unique_vals)
