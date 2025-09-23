#!/usr/bin/env python3
"""
Farm Data Analyzer Application Demo

This script runs the complete Farm Data Analyzer application.
Author: Lucas Zabeu
"""

# Import the main analyzer class from the src package
from src.farm_data_analyzer import FarmDataAnalyzer


def main():
    """
    Run the complete Farm Data Analyzer application.
    """
    # Specify the path to the CSV dataset
    csv_file = "data/CST8333-Area, production  farm value (32100358).csv"
    
    # Create an instance of FarmDataAnalyzer with the CSV file
    analyzer = FarmDataAnalyzer(csv_file)
    
    # Run the application, displaying the first 5 records
    analyzer.run_application(5)
    
    # Print completion message
    print("\n" + "=" * 60)
    print("APPLICATION EXECUTION COMPLETE")
    print("=" * 60)

# Entry point for the script
if __name__ == "__main__":
    main()