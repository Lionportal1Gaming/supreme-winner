from bloodlines.engine import GameEngine
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from rich.table import Table
from time import sleep
import sys
import random

def main():
    console = Console()
    engine = GameEngine()
    engine.create_test_scenario()
    
    def generate_dashboard() -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # Header
        player = engine.characters[engine.player_character_id]
        dynasty = engine.dynasties[player.dynasty_id]
        title = engine.get_character_title(player.id)
        location = engine.regions[player.location_id].name if player.location_id else "Unknown"
        header_text = f"DATE: {engine.get_date_string()} | DYNASTY: {dynasty.name} | HEAD: {player.name} ({title}) | LOC: {location}"
        layout["header"].update(Panel(header_text, style="bold white on blue"))
        
        # Left Column: Stats & Info
        stats_table = Table(title=f"Character Stats ({player.culture})")
        stats_table.add_column("Stat", style="cyan")
        stats_table.add_column("Value", style="magenta")
        stats_table.add_row("Title", title)
        stats_table.add_row("Age", str(player.age))
        stats_table.add_row("Wealth", str(player.wealth))
        stats_table.add_row("Health", f"{player.health:.1f}")
        stats_table.add_row("Martial", str(player.martial))
        stats_table.add_row("Diplomacy", str(player.diplomacy))
        
        # Neighbors
        if player.location_id:
            current_region = engine.regions[player.location_id]
            neighbors = [engine.regions[nid].name for nid in current_region.neighbors]
            stats_table.add_row("Neighbors", ", ".join(neighbors))
        
        layout["left"].update(Panel(stats_table, title="Current Character"))
        
        # Right Column: Logs / Events
        if engine.current_event:
            event = engine.current_event
            event_text = f"[bold yellow]{event.title}[/bold yellow]\n\n{event.description}\n"
            for i, option in enumerate(event.options):
                event_text += f"\n[{i+1}] {option.text} ({option.tooltip})"
            
            layout["right"].update(Panel(event_text, title="Active Event", style="bold red"))
        else:
            log_text = "\n".join(engine.logs[-10:])
            layout["right"].update(Panel(log_text, title="Events Log", style="green"))
        
        # Footer: Commands
        layout["footer"].update(Panel("[ENTER] Next Month | [M] Move | [Q] Quit", title="Commands"))
        
        return layout

        return layout

    # Main Game Loop
    while not engine.game_over:
        console.clear()
        console.print(generate_dashboard())
        
        try:
            if engine.current_event:
                print("\nCommands: [Number] Select Option | [Q] Quit")
                print(f"EVENT: {engine.current_event.title}")
                for i, option in enumerate(engine.current_event.options):
                    print(f"[{i+1}] {option.text}")
            else:
                print("\nCommands: [ENTER] Next Month | [M] Move | [Q] Quit")
            
            cmd = input("> ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'm' and not engine.current_event:
                # Simple movement menu
                player = engine.characters[engine.player_character_id]
                if player.location_id:
                    current = engine.regions[player.location_id]
                    
                    # Redraw for submenu context (optional, but keeps it clean)
                    console.clear()
                    console.print(generate_dashboard())
                    print("\n--- Movement ---")
                    print(f"Location: {current.name}")
                    print("Neighbors:")
                    for i, nid in enumerate(current.neighbors):
                        n_name = engine.regions[nid].name
                        print(f"[{i+1}] {n_name}")
                    
                    try:
                        choice = input("Move to (Number): ")
                        idx = int(choice) - 1
                        if 0 <= idx < len(current.neighbors):
                            target = current.neighbors[idx]
                            engine.world_manager.move_character(player.id, target)
                        else:
                            print("Invalid choice.")
                            sleep(1)
                    except ValueError:
                        print("Invalid input.")
                        sleep(1)

            elif engine.current_event:
                # Event handling
                try:
                    if cmd.isdigit():
                        idx = int(cmd) - 1
                        if 0 <= idx < len(engine.current_event.options):
                            engine.resolve_event(idx)
                        else:
                            print("Invalid option.")
                            sleep(1)
                    else:
                        print("Please select an option to continue.")
                        sleep(1)
                except ValueError:
                    pass
            else:
                # Default: Advance month
                engine.advance_month()
                
        except KeyboardInterrupt:
            break
    
    console.print("[bold red]Game Over[/bold red]")

if __name__ == "__main__":
    main()
