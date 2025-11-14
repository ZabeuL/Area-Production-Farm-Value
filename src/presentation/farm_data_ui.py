"""
farm_data_ui.py

Presentation layer for the farm data analyzer application. Handles all user
interactions and displays data in a user-friendly format.

Classes:
    FarmDataUI: User interface controller for the farm data application.

Author: Lucas Zabeu
"""

import os
import sys
from typing import Optional
from ..business.farm_data_service import FarmDataService
from ..entities.farm_data_record import FarmDataRecord


class FarmDataUI:
    """
    User interface controller for the farm data analyzer application.
    
    This class handles all user interactions including:
    - Displaying menus and prompts
    - Processing user input
    - Coordinating with the business layer
    - Displaying results and data
    """
    
    def __init__(self):
        """Initialize the UI with a business service."""
        self._service = FarmDataService()
        self._author_name = "Lucas Zabeu"
    
    def display_header(self) -> None:
        """
        Display the application header with author name.
        """
        print("\n" + "=" * 80)
        print(f"FARM DATA ANALYZER APPLICATION")
        print(f"Author: {self._author_name}")
        if self._service.source_filename:
            print(f"Dataset: {os.path.basename(self._service.source_filename)}")
        print(f"Records in memory: {self._service.record_count}")
        print("=" * 80)
    
    def display_main_menu(self) -> None:
        """
        Display the main menu options.
        """
        print(f"\n--- Main Menu (Author: {self._author_name}) ---")
        print("1. Load/Reload data from dataset")
        print("2. Save data to new CSV file")
        print("3. Display single record")
        print("4. Display multiple records")
        print("5. Create new record")
        print("6. Edit existing record")
        print("7. Delete record")
        print("8. Search records")
        print("9. Sort records (Data Structures & Algorithms)")
        print("10. View top N records")
        print("11. Exit application")
        print("-" * 50)
    
    def get_user_choice(self) -> str:
        """
        Get user menu choice with input validation.
        
        Returns:
            User's menu choice as a string.
        """
        while True:
            choice = input(f"Enter your choice (1-11) [{self._author_name}]: ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
                return choice
            print("Invalid choice. Please enter a number between 1 and 11.")
    
    def handle_load_data(self) -> None:
        """Handle loading/reloading data from a CSV file."""
        print(f"\n--- Load Data (by {self._author_name}) ---")
        filename = input("Enter CSV filename (or press Enter for default): ").strip()
        
        if not filename:
            filename = "data/CST8333-Area, production  farm value (32100358).csv"
        
        print(f"Loading data from: {filename}")
        
        if self._service.load_data_from_file(filename, max_records=100):
            print(f"Successfully loaded {self._service.record_count} records from {filename}")
        else:
            print("Failed to load data. Please check the file path and try again.")
    
    def handle_save_data(self) -> None:
        """Handle saving current data to a new CSV file."""
        print(f"\n--- Save Data (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory to save. Please load data first.")
            return
        
        filename = input("Enter output filename (e.g., 'output.csv'): ").strip()
        
        if not filename:
            print("Filename cannot be empty.")
            return
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        if self._service.save_data_to_file(filename):
            print(f"Successfully saved {self._service.record_count} records to {filename}")
        else:
            print("Failed to save data.")
    
    def handle_display_single_record(self) -> None:
        """Handle displaying a single record by index."""
        print(f"\n--- Display Single Record (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print(f"Available records: 0 to {self._service.record_count - 1}")
        
        try:
            index = int(input("Enter record index: "))
            record = self._service.get_record_by_index(index)
            
            if record:
                print(f"\nRecord #{index}:")
                print("-" * 40)
                print(record)
            else:
                print(f"Invalid index. Please enter a number between 0 and {self._service.record_count - 1}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def handle_display_multiple_records(self) -> None:
        """Handle displaying multiple records with options."""
        print(f"\n--- Display Multiple Records (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print("Display options:")
        print("1. Display all records")
        print("2. Display records by range")
        print("3. Display first N records")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            self._display_all_records()
        elif choice == '2':
            self._display_records_by_range()
        elif choice == '3':
            self._display_first_n_records()
        else:
            print("Invalid choice.")
    
    def _display_all_records(self) -> None:
        """Display all records in memory."""
        records = self._service.get_all_records()
        print(f"\nDisplaying all {len(records)} records:")
        print("-" * 60)
        
        for index, record in enumerate(records):
            print(f"\nRecord #{index}:")
            print(record)
    
    def _display_records_by_range(self) -> None:
        """Display records within a specified range."""
        try:
            start = int(input(f"Enter start index (0 to {self._service.record_count - 1}): "))
            end = int(input(f"Enter end index (0 to {self._service.record_count - 1}): "))
            
            records = self._service.get_records_by_range(start, end)
            
            if records:
                print(f"\nDisplaying records {start} to {end}:")
                print("-" * 60)
                
                for index, record in records:
                    print(f"\nRecord #{index}:")
                    print(record)
            else:
                print("No records found in the specified range.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
    
    def _display_first_n_records(self) -> None:
        """Display the first N records."""
        try:
            n = int(input(f"Enter number of records to display (max {self._service.record_count}): "))
            
            if n <= 0:
                print("Number must be greater than 0.")
                return
            
            records = self._service.get_records_by_range(0, n - 1)
            
            print(f"\nDisplaying first {len(records)} records:")
            print("-" * 60)
            
            for index, record in records:
                print(f"\nRecord #{index}:")
                print(record)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def handle_create_record(self) -> None:
        """Handle creating a new record."""
        print(f"\n--- Create New Record (by {self._author_name}) ---")
        
        print("Enter details for the new record:")
        
        ref_date = input("Reference Date (e.g., 2024): ").strip()
        geo = input("Geographic Location (e.g., Ontario): ").strip()
        dguid = input("Geographic Unique ID: ").strip()
        area_production_farm_value = input("Area/Production/Farm Value Description: ").strip()
        uom = input("Unit of Measurement: ").strip()
        uom_id = input("UOM ID: ").strip()
        scalar_factor = input("Scalar Factor: ").strip()
        scalar_id = input("Scalar ID: ").strip()
        vector = input("Vector: ").strip()
        coordinate = input("Coordinate: ").strip()
        value = input("Value: ").strip()
        status = input("Status: ").strip()
        symbol = input("Symbol: ").strip()
        terminated = input("Terminated: ").strip()
        decimals = input("Decimals: ").strip()
        
        new_record = FarmDataRecord(
            ref_date=ref_date,
            geo=geo,
            dguid=dguid,
            area_production_farm_value=area_production_farm_value,
            uom=uom,
            uom_id=uom_id,
            scalar_factor=scalar_factor,
            scalar_id=scalar_id,
            vector=vector,
            coordinate=coordinate,
            value=value,
            status=status,
            symbol=symbol,
            terminated=terminated,
            decimals=decimals
        )
        
        if self._service.add_record(new_record):
            print(f"Successfully created new record. Total records: {self._service.record_count}")
        else:
            print("Failed to create record.")
    
    def handle_edit_record(self) -> None:
        """Handle editing an existing record."""
        print(f"\n--- Edit Record (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print(f"Available records: 0 to {self._service.record_count - 1}")
        
        try:
            index = int(input("Enter record index to edit: "))
            record = self._service.get_record_by_index(index)
            
            if not record:
                print(f"Invalid index. Please enter a number between 0 and {self._service.record_count - 1}")
                return
            
            print(f"\nCurrent record #{index}:")
            print(record)
            print(f"\nEnter new values (press Enter to keep current value):")
            
            # Get new values with current values as defaults
            ref_date = input(f"Reference Date [{record.ref_date}]: ").strip() or record.ref_date
            geo = input(f"Geographic Location [{record.geo}]: ").strip() or record.geo
            dguid = input(f"Geographic Unique ID [{record.dguid}]: ").strip() or record.dguid
            area_production_farm_value = input(f"Area/Production/Farm Value [{record.area_production_farm_value}]: ").strip() or record.area_production_farm_value
            uom = input(f"Unit of Measurement [{record.uom}]: ").strip() or record.uom
            uom_id = input(f"UOM ID [{record.uom_id}]: ").strip() or record.uom_id
            scalar_factor = input(f"Scalar Factor [{record.scalar_factor}]: ").strip() or record.scalar_factor
            scalar_id = input(f"Scalar ID [{record.scalar_id}]: ").strip() or record.scalar_id
            vector = input(f"Vector [{record.vector}]: ").strip() or record.vector
            coordinate = input(f"Coordinate [{record.coordinate}]: ").strip() or record.coordinate
            value = input(f"Value [{record.value}]: ").strip() or record.value
            status = input(f"Status [{record.status}]: ").strip() or record.status
            symbol = input(f"Symbol [{record.symbol}]: ").strip() or record.symbol
            terminated = input(f"Terminated [{record.terminated}]: ").strip() or record.terminated
            decimals = input(f"Decimals [{record.decimals}]: ").strip() or record.decimals
            
            updated_record = FarmDataRecord(
                ref_date=ref_date,
                geo=geo,
                dguid=dguid,
                area_production_farm_value=area_production_farm_value,
                uom=uom,
                uom_id=uom_id,
                scalar_factor=scalar_factor,
                scalar_id=scalar_id,
                vector=vector,
                coordinate=coordinate,
                value=value,
                status=status,
                symbol=symbol,
                terminated=terminated,
                decimals=decimals
            )
            
            if self._service.update_record(index, updated_record):
                print(f"Successfully updated record #{index}")
            else:
                print("Failed to update record.")
                
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def handle_delete_record(self) -> None:
        """Handle deleting a record."""
        print(f"\n--- Delete Record (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print(f"Available records: 0 to {self._service.record_count - 1}")
        
        try:
            index = int(input("Enter record index to delete: "))
            record = self._service.get_record_by_index(index)
            
            if not record:
                print(f"Invalid index. Please enter a number between 0 and {self._service.record_count - 1}")
                return
            
            print(f"\nRecord to delete #{index}:")
            print(record)
            
            confirm = input("\nAre you sure you want to delete this record? (y/N): ").strip().lower()
            
            if confirm == 'y' or confirm == 'yes':
                if self._service.delete_record(index):
                    print(f"Successfully deleted record. Total records: {self._service.record_count}")
                else:
                    print("Failed to delete record.")
            else:
                print("Delete operation cancelled.")
                
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def handle_search_records(self) -> None:
        """Handle searching for records."""
        print(f"\n--- Search Records (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        search_term = input("Enter search term: ").strip()
        
        if not search_term:
            print("Search term cannot be empty.")
            return
        
        results = self._service.search_records(search_term)
        
        if results:
            print(f"\nFound {len(results)} matching records:")
            print("-" * 60)
            
            for index, record in results:
                print(f"\nRecord #{index}:")
                print(record)
        else:
            print(f"No records found matching '{search_term}'")
    
    def handle_sort_records(self) -> None:
        """Handle sorting records using data structures and algorithms."""
        print(f"\n--- Sort Records - Data Structures & Algorithms (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print("\nThis feature uses Python's Timsort algorithm (O(n log n) complexity)")
        print("to sort records in-memory by any field. Sorting is stable, meaning")
        print("records with equal keys maintain their relative order.\n")
        
        print("Available fields to sort by:")
        print("  1. ref_date          - Reference date/year")
        print("  2. geo               - Geographic location")
        print("  3. area_production_farm_value - Type of measurement")
        print("  4. value             - Data value (numeric)")
        print("  5. uom               - Unit of measurement")
        print("  6. vector            - Vector identifier")
        print("  7. coordinate        - Coordinate value (numeric)")
        
        # Map user choice to field name
        field_map = {
            '1': 'ref_date',
            '2': 'geo',
            '3': 'area_production_farm_value',
            '4': 'value',
            '5': 'uom',
            '6': 'vector',
            '7': 'coordinate'
        }
        
        choice = input("\nEnter field number to sort by (1-7): ").strip()
        
        if choice not in field_map:
            print("Invalid choice.")
            return
        
        sort_field = field_map[choice]
        
        # Get sort order
        order = input("Sort order - (A)scending or (D)escending? [A]: ").strip().upper()
        ascending = order != 'D'
        
        print(f"\nSorting records by '{sort_field}' in {'ascending' if ascending else 'descending'} order...")
        
        if self._service.sort_records(sort_field, ascending):
            print(f"Successfully sorted {self._service.record_count} records!")
            print(f"Order: {'Ascending' if ascending else 'Descending'}")
            
            # Show first few records as confirmation
            show_preview = input("\nDisplay first 5 records to confirm? (y/N): ").strip().lower()
            if show_preview == 'y' or show_preview == 'yes':
                records = self._service.get_records_by_range(0, 4)
                print("\nFirst 5 records after sorting:")
                print("-" * 60)
                for index, record in records:
                    print(f"\nRecord #{index}:")
                    print(record)
        else:
            print("Failed to sort records. Please try again.")
    
    def handle_top_n_records(self) -> None:
        """Handle displaying top N records by a specified field."""
        print(f"\n--- Top N Records (by {self._author_name}) ---")
        
        if self._service.record_count == 0:
            print("No data in memory. Please load data first.")
            return
        
        print("\nThis feature provides analytical queries like 'top 10 by farm value'")
        print("without modifying the main data structure order.\n")
        
        try:
            n = int(input(f"How many top records to display? (1-{self._service.record_count}): "))
            
            if n <= 0 or n > self._service.record_count:
                print(f"Please enter a number between 1 and {self._service.record_count}")
                return
            
            print("\nSort by:")
            print("  1. value      - Data value (most common)")
            print("  2. ref_date   - Reference date")
            print("  3. geo        - Geographic location")
            
            sort_choice = input("Enter choice (1-3) [1]: ").strip() or '1'
            
            sort_map = {'1': 'value', '2': 'ref_date', '3': 'geo'}
            sort_field = sort_map.get(sort_choice, 'value')
            
            # For numeric fields, default to descending (top values first)
            # For text fields, default to ascending
            default_desc = sort_field == 'value'
            
            order = input(f"Sort order - (A)scending or (D)escending? [{'D' if default_desc else 'A'}]: ").strip().upper()
            
            if not order:
                ascending = not default_desc
            else:
                ascending = order != 'D'
            
            print(f"\nGetting top {n} records sorted by '{sort_field}'...")
            
            top_records = self._service.get_top_n_records(n, sort_field, ascending)
            
            if top_records:
                print(f"\nTop {len(top_records)} records by {sort_field} ({'ascending' if ascending else 'descending'}):")
                print("=" * 60)
                
                for index, record in enumerate(top_records, 1):
                    print(f"\n#{index}:")
                    print(record)
            else:
                print("No records found.")
                
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def run_application(self) -> None:
        """
        Main method to run the interactive application.
        """
        print(f"Welcome to the Farm Data Analyzer by {self._author_name}!")
        
        # Try to load default data on startup
        default_file = "data/CST8333-Area, production  farm value (32100358).csv"
        if os.path.exists(default_file):
            print(f"Loading default dataset: {default_file}")
            self._service.load_data_from_file(default_file, max_records=100)
        
        while True:
            self.display_header()
            self.display_main_menu()
            
            choice = self.get_user_choice()
            
            if choice == '1':
                self.handle_load_data()
            elif choice == '2':
                self.handle_save_data()
            elif choice == '3':
                self.handle_display_single_record()
            elif choice == '4':
                self.handle_display_multiple_records()
            elif choice == '5':
                self.handle_create_record()
            elif choice == '6':
                self.handle_edit_record()
            elif choice == '7':
                self.handle_delete_record()
            elif choice == '8':
                self.handle_search_records()
            elif choice == '9':
                self.handle_sort_records()
            elif choice == '10':
                self.handle_top_n_records()
            elif choice == '11':
                print(f"\nThank you for using the Farm Data Analyzer!")
                print(f"Application completed by {self._author_name}")
                sys.exit(0)
            
            input(f"\nPress Enter to continue... (Author: {self._author_name})")