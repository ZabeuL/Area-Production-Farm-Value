"""
Farm Data Analyzer - Layered Architecture Package

This package implements a three-layered architecture:
- Presentation Layer: User interface and interaction handling
- Business Layer: Application logic and in-memory data management  
- Persistence Layer: File I/O operations
- Entities: Data models and record objects

Author: Lucas Zabeu
"""

from .presentation import FarmDataUI
from .business import FarmDataService
from .persistence import FarmDataRepository
from .entities import FarmDataRecord

__all__ = ['FarmDataUI', 'FarmDataService', 'FarmDataRepository', 'FarmDataRecord']