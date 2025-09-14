from rich.console import Console
from rich.table import Table
from risk_scoring import calculate_risk
from chat_analyzer import analyze_chat
from report_generator import generate_doc_report
import os
import openpyxl
import csv

console = Console()

def display_result(result: dict):
    """Display one message analysis in a table"""
    table = Table(title="EmoShield Risk Report")

    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Message", result["text"])
    table.add_row("Total Score", str(result["total_score"]))
    table.add_row("Risk Level", result["risk_level"])
    table.add_row("Hidden Score", str(result["hidden_score"]))
    table.add_row("Emoji Score", str(result["emoji_score"]))
    table.add_row("Keywords", ", ".join(result["keywords"]) or "None")
    table.add_row("Sentiment", result["sentiment"]["label"])
    table.add_row("Patterns", ", ".join(result["emoji_report"]["patterns"]) or "None")
    table.add_row("Anomalies", ", ".join(result["emoji_report"]["anomaly"]["anomalies"]) or "None")

    console.print(table)

def export_to_csv(results, filename="EmoShield_Report.csv"):
    """Export results to CSV"""
    keys = results[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    console.print(f"[bold green]Report exported to {filename}[/bold green]")


def export_to_excel(results, filename="EmoShield_Report.xlsx"):
    """Export results to Excel"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "EmoShield Report"

    # Write header
    headers = list(results[0].keys())
    ws.append(headers)

    # Write rows
    for row in results:
        ws.append(list(row.values()))

    wb.save(filename)
    console.print(f"[bold green]Report exported to {filename}[/bold green]")

if __name__ == "__main__":
    console.print("[bold yellow]Welcome to EmoShield Terminal Dashboard 🛡️[/bold yellow]")

    while True:
        console.print("\n[bold cyan]Choose an option:[/bold cyan]")
        console.print("1. Analyze single message")
        console.print("2. Scan exported chat file")
        console.print("3. Exit")

        choice = console.input("[bold green]Enter choice (1/2/3): [/bold green] ")

        if choice == "1":
            msg = console.input("\n[bold green]Enter a chat message: [/bold green] ")
            result = calculate_risk(msg)
            display_result(result)

        elif choice == "2":
            filepath = console.input("\n[bold green]Enter path to chat file: [/bold green] ").strip()
            if not os.path.exists(filepath):
                console.print(f"[bold red]File not found: {filepath}[/bold red]")
                continue

            # Analyze chat file
            results = analyze_chat(filepath)

            console.print("\n[bold cyan]Choose export format:[/bold cyan]")
            console.print("1. CSV")
            console.print("2. Excel")
            console.print("3. DOCX Report")
            console.print("4. None")

            export_choice = console.input("[bold green]Enter choice (1/2/3/4): [/bold green] ")

            if export_choice == "1":
                export_to_csv(results)
            elif export_choice == "2":
                export_to_excel(results)
            elif export_choice == "3":
                generate_doc_report(results, "EmoShield_Report.docx")
            else:
                console.print("[bold yellow]No export selected.[/bold yellow]")
                
        elif choice == "3":
            console.print("[bold red]Exiting EmoShield...[/bold red]")
            break
        else:
            console.print("[bold red]Invalid choice![/bold red]")