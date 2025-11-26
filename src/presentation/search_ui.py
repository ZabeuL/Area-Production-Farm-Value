"""
search_ui.py

Presentation layer for interactive search interface using rich library.
Provides beautiful console-based interactive search with multiple operators,
boolean logic, and result visualization.

Classes:
    SearchUI: Interactive user interface for advanced search functionality.

Author: Lucas Zabeu
"""

import sys
import os
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.syntax import Syntax
from rich import box
from rich.text import Text

from ..business.search_engine import (
    SearchEngine, SearchCondition, ComparisonOperator, BooleanOperator
)
from ..business.farm_data_service import FarmDataService


class SearchUI:
    """
    Interactive user interface for advanced search functionality.
    
    This class provides a rich console-based interface for:
    - Multi-column filtering with various operators
    - Boolean logic (AND/OR) for combining conditions
    - Interactive result display with customization
    - CSV export and summary statistics
    - Search refinement on previous results
    """
    
    def __init__(self, service: FarmDataService):
        """
        Initialize search UI with a data service.
        
        Args:
            service: FarmDataService instance containing farm records
        """
        self._service = service
        self._console = Console()
        self._author_name = "Lucas Zabeu"
        self._search_engine: Optional[SearchEngine] = None
        
    def initialize_search_engine(self) -> bool:
        """
        Initialize the search engine with current records from service.
        
        Returns:
            True if initialization successful, False otherwise
        """
        if self._service.record_count == 0:
            self._console.print("[red]No data loaded. Please load data first.[/red]")
            return False
        
        records = self._service.get_all_records()
        self._search_engine = SearchEngine.from_records(records)
        return True
    
    def display_search_header(self) -> None:
        """Display the search interface header."""
        header = Panel(
            f"[bold cyan]ADVANCED SEARCH SYSTEM[/bold cyan]\n"
            f"Interactive Multi-Column Filtering\n"
            f"Author: {self._author_name}",
            border_style="cyan",
            box=box.DOUBLE
        )
        self._console.print(header)
    
    def display_available_columns(self) -> None:
        """Display available columns in a formatted table."""
        if not self._search_engine:
            return
        
        columns = self._search_engine.get_available_columns()
        
        table = Table(title="Available Columns", box=box.ROUNDED)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Column Name", style="green")
        table.add_column("Type", style="yellow")
        
        for idx, col in enumerate(columns, 1):
            col_type = self._search_engine.get_column_type(col)
            table.add_row(str(idx), col, col_type)
        
        self._console.print(table)
    
    def display_operator_help(self) -> None:
        """Display available operators and their usage."""
        table = Table(title="Available Operators", box=box.ROUNDED)
        table.add_column("Operator", style="cyan")
        table.add_column("Symbol/Keyword", style="green")
        table.add_column("Description", style="white")
        table.add_column("Example", style="yellow")
        
        operators = [
            ("Equal", "==", "Exact match", "GEO == Ontario"),
            ("Not Equal", "!=", "Not matching", "VALUE != 0"),
            ("Greater Than", ">", "Numeric comparison", "VALUE > 1000"),
            ("Less Than", "<", "Numeric comparison", "VALUE < 500"),
            ("Greater Equal", ">=", "Numeric comparison", "VALUE >= 100"),
            ("Less Equal", "<=", "Numeric comparison", "VALUE <= 2000"),
            ("Contains", "contains", "Text contains substring", "GEO contains Canada"),
            ("Starts With", "startswith", "Text starts with", "GEO startswith A"),
            ("Ends With", "endswith", "Text ends with", "GEO endswith ia"),
            ("Regex", "regex", "Regular expression", "GEO regex ^[A-C].*"),
        ]
        
        for op_name, symbol, desc, example in operators:
            table.add_row(op_name, symbol, desc, example)
        
        self._console.print(table)
    
    def get_search_condition(self) -> Optional[SearchCondition]:
        """
        Interactively get a search condition from the user.
        
        Returns:
            SearchCondition object or None if user cancels
        """
        self._console.print("\n[bold]Create Search Condition[/bold]")
        
        # Display available columns
        self.display_available_columns()
        
        # Get column name
        column = Prompt.ask(
            "\n[cyan]Enter column name[/cyan]",
            console=self._console
        ).strip()
        
        if column not in self._search_engine.get_available_columns():
            self._console.print(f"[red]Invalid column: {column}[/red]")
            return None
        
        # Display operators
        self._console.print("\n[bold]Available Operators:[/bold]")
        self._console.print("Comparison: ==, !=, >, <, >=, <=")
        self._console.print("Text: contains, startswith, endswith, regex")
        
        # Get operator
        operator_input = Prompt.ask(
            "\n[cyan]Enter operator[/cyan]",
            default="==",
            console=self._console
        ).strip().lower()
        
        # Map operator string to enum
        operator_map = {
            "==": ComparisonOperator.EQUALS,
            "!=": ComparisonOperator.NOT_EQUALS,
            ">": ComparisonOperator.GREATER_THAN,
            "<": ComparisonOperator.LESS_THAN,
            ">=": ComparisonOperator.GREATER_EQUAL,
            "<=": ComparisonOperator.LESS_EQUAL,
            "contains": ComparisonOperator.CONTAINS,
            "startswith": ComparisonOperator.STARTSWITH,
            "endswith": ComparisonOperator.ENDSWITH,
            "regex": ComparisonOperator.REGEX,
        }
        
        if operator_input not in operator_map:
            self._console.print(f"[red]Invalid operator: {operator_input}[/red]")
            return None
        
        operator = operator_map[operator_input]
        
        # Get search value
        value = Prompt.ask(
            f"\n[cyan]Enter value to search for[/cyan]",
            console=self._console
        ).strip()
        
        # Convert value to appropriate type
        converted_value = self._search_engine._convert_value(column, value)
        
        # Ask about case sensitivity for text operations
        case_sensitive = False
        if operator in [ComparisonOperator.CONTAINS, ComparisonOperator.STARTSWITH,
                       ComparisonOperator.ENDSWITH, ComparisonOperator.REGEX]:
            case_sensitive = Confirm.ask(
                "[cyan]Case-sensitive search?[/cyan]",
                default=False,
                console=self._console
            )
        
        return SearchCondition(
            column=column,
            operator=operator,
            value=converted_value,
            case_sensitive=case_sensitive
        )
    
    def display_results(self, results, limit: Optional[int] = None) -> None:
        """
        Display search results in a formatted table.
        
        Args:
            results: pandas DataFrame with search results
            limit: Maximum number of rows to display
        """
        if results is None or len(results) == 0:
            self._console.print("[yellow]No results found.[/yellow]")
            return
        
        # Ask user which columns to display
        self._console.print(f"\n[green]Found {len(results)} matching records[/green]")
        
        display_all_cols = Confirm.ask(
            "[cyan]Display all columns?[/cyan]",
            default=True,
            console=self._console
        )
        
        if display_all_cols:
            columns_to_show = list(results.columns)
        else:
            self._console.print("\nAvailable columns:")
            for idx, col in enumerate(results.columns, 1):
                self._console.print(f"  {idx}. {col}")
            
            col_input = Prompt.ask(
                "\n[cyan]Enter column numbers to display (comma-separated)[/cyan]",
                default="1,2,3",
                console=self._console
            )
            
            try:
                col_indices = [int(x.strip()) - 1 for x in col_input.split(',')]
                columns_to_show = [list(results.columns)[i] for i in col_indices 
                                 if 0 <= i < len(results.columns)]
            except (ValueError, IndexError):
                columns_to_show = list(results.columns)[:5]
        
        # Ask about row limit
        if limit is None:
            if len(results) > 20:
                limit = IntPrompt.ask(
                    f"[cyan]Display how many rows? (max {len(results)})[/cyan]",
                    default=20,
                    console=self._console
                )
            else:
                limit = len(results)
        
        # Create table
        table = Table(
            title=f"Search Results ({min(limit, len(results))} of {len(results)} records)",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        # Add columns
        table.add_column("Row", style="dim", width=4)
        for col in columns_to_show:
            table.add_column(col, style="green", max_width=30)
        
        # Add rows
        display_df = results[columns_to_show].head(limit)
        for idx, row in display_df.iterrows():
            row_data = [str(idx)]
            for col in columns_to_show:
                value = str(row[col])
                # Truncate long values
                if len(value) > 30:
                    value = value[:27] + "..."
                row_data.append(value)
            table.add_row(*row_data)
        
        self._console.print(table)
    
    def display_summary_statistics(self, stats: Dict[str, Any]) -> None:
        """
        Display summary statistics in a formatted panel.
        
        Args:
            stats: Dictionary containing summary statistics
        """
        summary_text = f"[bold cyan]Summary Statistics[/bold cyan]\n\n"
        summary_text += f"Total Records: [green]{stats.get('total_records', 0)}[/green]\n\n"
        
        # Display numeric summaries
        if 'numeric_summary' in stats:
            summary_text += "[bold]Numeric Columns:[/bold]\n"
            for col, col_stats in stats['numeric_summary'].items():
                if isinstance(col_stats, dict) and 'mean' in col_stats:
                    summary_text += f"  {col}:\n"
                    summary_text += f"    Mean: {col_stats['mean']:.2f}\n"
                    summary_text += f"    Min: {col_stats['min']:.2f}\n"
                    summary_text += f"    Max: {col_stats['max']:.2f}\n"
        
        panel = Panel(summary_text, border_style="green", box=box.ROUNDED)
        self._console.print(panel)
    
    def handle_search_interactive(self) -> None:
        """Main interactive search handler."""
        if not self.initialize_search_engine():
            return
        
        self.display_search_header()
        
        self._console.print("\n[bold yellow]Interactive Search System[/bold yellow]")
        self._console.print("Filter records using multiple conditions with AND/OR logic\n")
        
        # Show operator help
        show_help = Confirm.ask(
            "[cyan]Show operator help?[/cyan]",
            default=True,
            console=self._console
        )
        if show_help:
            self.display_operator_help()
        
        conditions: List[SearchCondition] = []
        
        # Get first condition
        self._console.print("\n[bold]First Search Condition[/bold]")
        condition = self.get_search_condition()
        if not condition:
            return
        
        conditions.append(condition)
        
        # Ask for additional conditions
        boolean_op = BooleanOperator.AND
        
        while True:
            add_more = Confirm.ask(
                "\n[cyan]Add another condition?[/cyan]",
                default=False,
                console=self._console
            )
            
            if not add_more:
                break
            
            # Get boolean operator for combining
            if len(conditions) == 1:
                op_choice = Prompt.ask(
                    "[cyan]Combine conditions with[/cyan]",
                    choices=["AND", "OR"],
                    default="AND",
                    console=self._console
                )
                boolean_op = BooleanOperator.AND if op_choice == "AND" else BooleanOperator.OR
            
            # Get next condition
            condition = self.get_search_condition()
            if condition:
                conditions.append(condition)
        
        # Ask about search refinement
        refine = False
        if self._search_engine.get_last_results() is not None:
            refine = Confirm.ask(
                "\n[cyan]Refine previous search results?[/cyan]",
                default=False,
                console=self._console
            )
        
        # Execute search
        self._console.print("\n[yellow]Executing search...[/yellow]")
        
        try:
            results = self._search_engine.search(
                conditions=conditions,
                boolean_op=boolean_op,
                refine_previous=refine
            )
            
            # Display results
            self.display_results(results)
            
            # Post-search options
            self.display_post_search_options(results)
            
        except Exception as e:
            self._console.print(f"[red]Search error: {e}[/red]")
    
    def display_post_search_options(self, results) -> None:
        """
        Display options for working with search results.
        
        Args:
            results: pandas DataFrame with search results
        """
        if results is None or len(results) == 0:
            return
        
        self._console.print("\n[bold]Post-Search Options:[/bold]")
        self._console.print("1. Export to CSV")
        self._console.print("2. Show summary statistics")
        self._console.print("3. Show unique values for a column")
        self._console.print("4. Refine search (search within results)")
        self._console.print("5. Clear results and start new search")
        self._console.print("6. Return to main menu")
        
        choice = Prompt.ask(
            "\n[cyan]Select option[/cyan]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="6",
            console=self._console
        )
        
        if choice == "1":
            self.handle_export_csv(results)
        elif choice == "2":
            stats = self._search_engine.get_summary_statistics(results)
            self.display_summary_statistics(stats)
        elif choice == "3":
            self.handle_unique_values(results)
        elif choice == "4":
            self.handle_search_interactive()
        elif choice == "5":
            self._search_engine.clear_results()
            self._console.print("[green]Results cleared.[/green]")
        
    def handle_export_csv(self, results) -> None:
        """
        Handle CSV export of search results.
        
        Args:
            results: pandas DataFrame to export
        """
        filename = Prompt.ask(
            "\n[cyan]Enter output filename[/cyan]",
            default="search_results.csv",
            console=self._console
        )
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        if self._search_engine.export_to_csv(filename, results):
            self._console.print(f"[green]✓ Results exported to {filename}[/green]")
        else:
            self._console.print("[red]✗ Export failed[/red]")
    
    def handle_unique_values(self, results) -> None:
        """
        Display unique values for a selected column.
        
        Args:
            results: pandas DataFrame to analyze
        """
        column = Prompt.ask(
            "\n[cyan]Enter column name[/cyan]",
            console=self._console
        )
        
        unique_vals = self._search_engine.get_unique_values(column, results)
        
        if unique_vals:
            self._console.print(f"\n[bold]Unique values in {column}:[/bold]")
            self._console.print(f"Count: [green]{len(unique_vals)}[/green]\n")
            
            # Display in columns
            for i, val in enumerate(unique_vals[:50], 1):
                self._console.print(f"  {i}. {val}")
            
            if len(unique_vals) > 50:
                self._console.print(f"\n... and {len(unique_vals) - 50} more values")
        else:
            self._console.print(f"[yellow]No unique values found for {column}[/yellow]")
