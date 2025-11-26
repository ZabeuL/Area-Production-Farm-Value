import pandas as pd
import rich
from rich.console import Console
from rich.table import Table

print(f"pandas version: {pd.__version__}")
print(f"rich installed: {rich.__file__}")

# Quick functionality test
console = Console()
console.print("[bold green]✓ Both libraries installed successfully![/bold green]")

# Test table creation
table = Table(title="Test Table")
table.add_column("Library", style="cyan")
table.add_column("Status", style="green")
table.add_row("pandas", "✓ Ready")
table.add_row("rich", "✓ Ready")
console.print(table)