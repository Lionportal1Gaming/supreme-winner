from bloodlines.engine import GameEngine
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from rich.table import Table
from rich.align import Align
from time import sleep
import sys
import random

def show_title_screen(console):
    """Display the game title screen."""
    title = """
╔═══════════════════════════════════════╗
║                                       ║
║        PROJECT AETERNA                ║
║                                       ║
║   A Dynastic Strategy Simulation      ║
║                                       ║
║           Version 0.1.1               ║
║                                       ║
╚═══════════════════════════════════════╝
    """
    console.print(Align.center(title), style="bold cyan")

def show_start_menu(console):
    """Show the start menu and return user choice."""
    while True:
        print("\n" + "="*40)
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style="cyan")
        menu_table.add_column("Description", style="white")
        menu_table.add_row("[N]", "New Game")
        menu_table.add_row("[L]", "Load Game")
        menu_table.add_row("[Q]", "Quit")
        
        console.print(Panel(menu_table, title="Main Menu", border_style="cyan"))
        print("="*40)
        
        choice = input("\n> ").strip().lower()
        
        if choice == 'n':
            return 'new'
        elif choice == 'l':
            return 'load'
        elif choice == 'q':
            return 'quit'
        else:
            print("Invalid option. Please try again.")
            sleep(1)

def main():
    console = Console()
    
    # Show title screen
    show_title_screen(console)
    sleep(1)
    
    # Show start menu
    menu_choice = show_start_menu(console)
    
    if menu_choice == 'quit':
        console.print("\n[bold cyan]Thanks for playing![/bold cyan]\n")
        return
    
    # Initialize engine
    engine = GameEngine()
    
    if menu_choice == 'new':
        engine.create_test_scenario()
    elif menu_choice == 'load':
        filename = input("Load from file (default: savegame): ").strip()
        if not filename:
            filename = "savegame"
        if not engine.load_game(filename):
            print("Failed to load game. Starting new game instead...")
            sleep(2)
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
            
            # Buildings
            if hasattr(current_region, 'buildings') and current_region.buildings:
                try:
                    b_list = [f"{k.title()}: {v}" for k, v in current_region.buildings.items()]
                    stats_table.add_row("Buildings", ", ".join(b_list))
                except Exception as e:
                    stats_table.add_row("Buildings", "Error displaying")
        
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
        layout["footer"].update(Panel("[ENTER] Next Month | [M] Move | [B] Build | [R] Relationships | [S] Save | [L] Load | [Q] Quit", title="Commands"))
        
        return layout

    # Main Game Loop
    while not engine.game_over:
        try:
            # Render dashboard with separator (no clear)
            print("\n" + "="*60 + "\n")
            console.print(generate_dashboard())
            print("="*60)
            
            # Show command prompt
            if engine.current_event:
                print("\nCommands: [Number] Select Option | [Q] Quit")
                print(f"EVENT: {engine.current_event.title}")
                for i, option in enumerate(engine.current_event.options):
                    print(f"[{i+1}] {option.text}")
            else:
                print("\nCommands: [ENTER] Next Month | [M] Move | [B] Build | [R] Relationships | [S] Save | [L] Load | [Q] Quit")
            
            cmd = input("> ").strip().lower()
            
            # Process commands
            if cmd == 'q':
                break
            elif cmd == 'm' and not engine.current_event:
                # Movement menu
                player = engine.characters[engine.player_character_id]
                if player.location_id:
                    current = engine.regions[player.location_id]
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
            elif cmd == 's' and not engine.current_event:
                filename = input("Save to file (default: savegame): ").strip()
                if not filename:
                    filename = "savegame"
                engine.save_game(filename)
                sleep(1)
            elif cmd == 'l' and not engine.current_event:
                filename = input("Load from file (default: savegame): ").strip()
                if not filename:
                    filename = "savegame"
                if engine.load_game(filename):
                    print("Game loaded successfully!")
                else:
                    print("Failed to load game.")
                sleep(1)
            elif cmd == 'r' and not engine.current_event:
                # Relationships Menu
                player = engine.characters[engine.player_character_id]
                print("\n--- Relationships ---")
                
                # Get all other characters
                other_chars = [(cid, engine.characters[cid]) for cid in engine.characters.keys() 
                              if cid != engine.player_character_id and engine.characters[cid].is_alive]
                
                if not other_chars:
                    print("No other characters known.")
                    sleep(1)
                else:
                    for i, (cid, char) in enumerate(other_chars):
                        opinion = engine.get_opinion(engine.player_character_id, cid)
                        
                        # Color code by opinion
                        if opinion >= 50:
                            status = "(Allied)"
                        elif opinion >= 10:
                            status = "(Friendly)"
                        elif opinion >= -9:
                            status = "(Neutral)"
                        elif opinion >= -49:
                            status = "(Unfriendly)"
                        else:
                            status = "(Hostile)"
                        
                        spouse_marker = " [SPOUSE]" if char.id == player.spouse_id else ""
                        print(f"[{i+1}] {char.name}{spouse_marker} - Opinion: {opinion:+d} {status}")
                    
                    print("\n[M] Arrange Marriage | [F] Family Tree | [Enter] Back")
                    choice = input("> ").strip().lower()
                    
                    if choice == 'f':
                        print("\nFamily Tree - Select character (Number) or press Enter for yourself:")
                        sel = input("> ").strip()
                        
                        # Determine which character to view
                        target_id = engine.player_character_id
                        if sel:
                            try:
                                idx = int(sel) - 1
                                if 0 <= idx < len(other_chars):
                                    target_id = other_chars[idx][0]
                            except ValueError:
                                pass
                        
                        # Display family tree
                        tree = engine.get_family_tree(target_id)
                        if tree:
                            char = tree["character"]
                            print(f"\n=== Family Tree: {char.name} ===\n")
                            
                            # Parents
                            print("Parents:")
                            if tree["father"]:
                                status = "Alive" if tree["father"].is_alive else "Deceased"
                                print(f"  Father: {tree['father'].name} (Age {tree['father'].age}, {status})")
                            else:
                                print("  Father: Unknown")
                            
                            if tree["mother"]:
                                status = "Alive" if tree["mother"].is_alive else "Deceased"
                                print(f"  Mother: {tree['mother'].name} (Age {tree['mother'].age}, {status})")
                            else:
                                print("  Mother: Unknown")
                            
                            # Spouse
                            print("\nSpouse:")
                            if tree["spouse"]:
                                print(f"  {tree['spouse'].name} (Age {tree['spouse'].age})")
                            else:
                                print("  None")
                            
                            # Children
                            print("\nChildren:")
                            if tree["children"]:
                                for child in tree["children"]:
                                    status = "" if child.is_alive else " (Deceased)"
                                    print(f"  - {child.name} (Age {child.age}){status}")
                            else:
                                print("  None")
                            
                            # Siblings
                            print("\nSiblings:")
                            if tree["siblings"]:
                                for sibling in tree["siblings"]:
                                    status = "" if sibling.is_alive else " (Deceased)"
                                    print(f"  - {sibling.name} (Age {sibling.age}){status}")
                            else:
                                print("  None")
                        
                        input("\nPress Enter to continue...")
                    elif choice == 'm':
                        print("\nArrange Marriage - Select character (Number):")
                        try:
                            sel = input("> ").strip()
                            idx = int(sel) - 1
                            if 0 <= idx < len(other_chars):
                                target_id, target_char = other_chars[idx]
                                engine.arrange_marriage(engine.player_character_id, target_id)
                            sleep(2)
                        except ValueError:
                            print("Invalid input.")
                            sleep(1)
            elif cmd == 'b' and not engine.current_event:
                # Build Menu
                player = engine.characters[engine.player_character_id]
                if player.location_id:
                    current = engine.regions[player.location_id]
                    print("\n--- Construction ---")
                    print(f"Location: {current.name}")
                    print(f"Existing Buildings: {current.buildings}")
                    print("\nAvailable Buildings:")
                    print("[1] Farm (Cost: 50, +1 Wealth/Month)")
                    print("[2] Estate (Cost: 200, +5 Wealth/Month)")
                    
                    try:
                        choice = input("Build (Number): ")
                        if choice == '1':
                            engine.construct_building(current.id, "farm")
                        elif choice == '2':
                            engine.construct_building(current.id, "estate")
                        else:
                            print("Invalid choice.")
                        sleep(1)
                    except ValueError:
                        pass
            else:
                # Default: Advance month
                engine.advance_month()
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n\nCRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()
            print("\nPress Enter to exit...")
            input()
            break
    
    print("\n\nGame Over")

if __name__ == "__main__":
    main()
