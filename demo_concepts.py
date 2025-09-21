#!/usr/bin/env python3
"""
Farm Data Analyzer Application Demo

This script runs the complete Farm Data Analyzer application.
Author: Lucas Zabeu
"""

from src.farm_data_analyzer import FarmDataAnalyzer


def main():
    """
    Run the complete Farm Data Analyzer application.
    """
    
    # CSV file path
    csv_file = "CST8333-Area, production  farm value (32100358).csv"
    
    # Create analyzer instance and run complete application
    analyzer = FarmDataAnalyzer(csv_file)
    analyzer.run_application()
    
    print("\n" + "=" * 60)
    print("APPLICATION EXECUTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()