"""
farm_data_record.py

This module defines the FarmDataRecord class, which represents a single
row of farm data from a CSV file. The class provides accessors and mutators
for each field, allowing for encapsulated data management and easy integration
with data analysis workflows.

Classes:
    FarmDataRecord: Represents a single farm data entry with fields for
        reference date, location, measurement type, value, and more.

Example:
    record = FarmDataRecord(ref_date="2024", geo="Ontario", value="1000")
    print(record.ref_date)
    record.value = "1200"

Attributes:
    None

Raises:
    None
"""

#!/usr/bin/env python3

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
                f"  Vector: {self._vector}\n"
                f"  Coordinate: {self._coordinate}")