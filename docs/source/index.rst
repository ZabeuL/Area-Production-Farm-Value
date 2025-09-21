.. Farm Data Analyzer documentation master file, created by
   sphinx-quickstart on Sat Sep 20 23:14:07 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Farm Data Analyzer Documentation
===============================

Welcome to the Farm Data Analyzer documentation!

This application analyzes farm production data from CSV files and provides comprehensive data analysis capabilities.

**Author:** Lucas Zabeu

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Getting Started
===============

The Farm Data Analyzer consists of two main classes:

- **FarmDataRecord**: Represents individual farm data records
- **FarmDataAnalyzer**: Main analyzer class for processing CSV data

Quick Example
=============

.. code-block:: python

   from farm_data_analyzer import FarmDataAnalyzer
   
   # Create analyzer instance
   analyzer = FarmDataAnalyzer("your_data.csv")
   
   # Run the complete application
   analyzer.run_application()

API Reference
=============

.. automodule:: farm_data_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

Classes
=======

FarmDataRecord
--------------
.. autoclass:: farm_data_analyzer.FarmDataRecord
   :members:
   :undoc-members:
   :show-inheritance:

FarmDataAnalyzer
----------------
.. autoclass:: farm_data_analyzer.FarmDataAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

