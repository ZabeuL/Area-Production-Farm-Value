#!/usr/bin/env python3
"""
main.py

Main entry point for the Farm Data Analyzer application.
Demonstrates the layered architecture with Presentation, Business, and Persistence layers.

Author: Lucas Zabeu
"""

import sys
import os

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.farm_data_ui import FarmDataUI


def main():
    """
    Main function to start the Farm Data Analyzer application.
    """
    try:
        # Create and run the application
        app = FarmDataUI()
        app.run_application()
        
    except KeyboardInterrupt:
        print(f"\n\nApplication interrupted by user.")
        print("Thank you for using the Farm Data Analyzer by Lucas Zabeu!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Application terminated by Lucas Zabeu")
        sys.exit(1)


if __name__ == "__main__":
    main()