from typing import List, Dict, Optional
from .models import Character, Dynasty, Polity, Region, GovernmentType, Terrain
from .culture import CultureManager
from .events import EventManager, Event
from .government import GovernmentManager
from .world import WorldManager
import random
import json
import gzip
import os

class GameEngine:
    def __init__(self):
        self.culture_manager = CultureManager()
        self.event_manager = EventManager()
        self.government_manager = GovernmentManager(self)
        self.world_manager = WorldManager(self)
        self.current_event: Optional[Event] = None
        self.year = 753
        self.month = 1  # 1-12
        self.is_bc = True
        
        # Global State
        self.characters: Dict[str, Character] = {}
        self.dynasties: Dict[str, Dynasty] = {}
        self.polities: Dict[str, Polity] = {}
        self.regions: Dict[str, Region] = {}
        
        self.player_character_id: Optional[str] = None
        self.game_over = False
        self.logs: List[str] = []

    def save_game(self, filename: str):
        """Save the current game state to a compressed JSON file."""
        if not filename.endswith(".sav"):
            filename += ".sav"
            
        data = {
            "version": "0.1.0",
            "year": self.year,
            "month": self.month,
            "is_bc": self.is_bc,
            "player_character_id": self.player_character_id,
            "logs": self.logs,
            "characters": {k: v.to_dict() for k, v in self.characters.items()},
            "dynasties": {k: v.to_dict() for k, v in self.dynasties.items()},
            "polities": {k: v.to_dict() for k, v in self.polities.items()},
            "regions": {k: v.to_dict() for k, v in self.regions.items()}
        }
        
        try:
            with gzip.open(filename, 'wt', encoding='utf-8') as f:
                json.dump(data, f)
            self.log(f"Game saved to {filename}")
        except Exception as e:
            self.log(f"Error saving game: {e}")

    def load_game(self, filename: str) -> bool:
        """Load game state from a compressed JSON file."""
        if not filename.endswith(".sav"):
            filename += ".sav"
            
        if not os.path.exists(filename):
            self.log(f"Save file {filename} not found.")
            return False
            
        try:
            with gzip.open(filename, 'rt', encoding='utf-8') as f:
                data = json.load(f)
                
            self.year = data["year"]
            self.month = data["month"]
            self.is_bc = data["is_bc"]
            self.player_character_id = data["player_character_id"]
            self.logs = data["logs"]
            
            # Reconstruct objects
            self.characters = {k: Character.from_dict(v) for k, v in data["characters"].items()}
            self.dynasties = {k: Dynasty.from_dict(v) for k, v in data["dynasties"].items()}
            self.polities = {k: Polity.from_dict(v) for k, v in data["polities"].items()}
            self.regions = {k: Region.from_dict(v) for k, v in data["regions"].items()}
            
            # Re-link managers
            self.government_manager = GovernmentManager(self)
            self.world_manager = WorldManager(self)
            # Note: We don't need to reload static data like cultures/events as they are initialized in __init__
            
            self.log(f"Game loaded from {filename}")
            return True
        except Exception as e:
            self.log(f"Error loading game: {e}")
            return False

    def log(self, message: str):
        """Add a message to the game log."""
        date_str = self.get_date_string()
        self.logs.append(f"[{date_str}] {message}")
        # Keep log size manageable
        if len(self.logs) > 100:
            self.logs.pop(0)

    def get_date_string(self) -> str:
        era = "BC" if self.is_bc else "AD"
        return f"{self.month}/{self.year} {era}"

    def advance_month(self):
        """The core game loop tick."""
        self.month += 1
        if self.month > 12:
            self.month = 1
            if self.is_bc:
                self.year -= 1
                if self.year == 0:
                    self.is_bc = False
                    self.year = 1
            else:
                self.year += 1
        
        self.process_characters()
        self.process_births()
        self.process_polities()
        self.process_economy()
        self.process_events()

    def construct_building(self, region_id: str, building_type: str) -> bool:
        """Construct a building in a region."""
        if region_id not in self.regions:
            return False
            
        region = self.regions[region_id]
        player = self.characters[self.player_character_id]
        
        # Costs and Effects
        costs = {
            "farm": 50,
            "estate": 200
        }
        
        if building_type not in costs:
            return False
            
        cost = costs[building_type]
        
        if player.wealth >= cost:
            self.modify_wealth(player.id, -cost)
            if building_type in region.buildings:
                region.buildings[building_type] += 1
            else:
                region.buildings[building_type] = 1
            self.log(f"Constructed {building_type} in {region.name}.")
            return True
        else:
            self.log(f"Not enough wealth to build {building_type} (Cost: {cost}).")
            return False

    def process_economy(self):
        """Process monthly income from buildings."""
        # Building Income
        income_map = {
            "farm": 1,
            "estate": 5
        }
        
        for region in self.regions.values():
            # Find owner of region (Polity -> Ruler)
            if region.owner_polity_id:
                polity = self.polities[region.owner_polity_id]
                if polity.ruler_id:
                    ruler_id = polity.ruler_id
                    
                    total_income = 0
                    for b_type, count in region.buildings.items():
                        if b_type in income_map:
                            total_income += income_map[b_type] * count
                    
                    if total_income > 0:
                        self.modify_wealth(ruler_id, total_income)

    def get_opinion(self, char1_id: str, char2_id: str) -> int:
        """Get char1's opinion of char2."""
        if char1_id not in self.characters or char2_id not in self.characters:
            return 0
        return self.characters[char1_id].opinions.get(char2_id, 0)

    def modify_opinion(self, char1_id: str, char2_id: str, change: int):
        """Modify char1's opinion of char2 by change amount."""
        if char1_id not in self.characters or char2_id not in self.characters:
            return
        
        char1 = self.characters[char1_id]
        current = char1.opinions.get(char2_id, 0)
        new_opinion = max(-100, min(100, current + change))
        char1.opinions[char2_id] = new_opinion
        
        if change != 0:
            char2_name = self.characters[char2_id].name
            self.log(f"{char1.name} opinion of {char2_name}: {change:+d} (now {new_opinion})")

    def arrange_marriage(self, char1_id: str, char2_id: str) -> bool:
        """Arrange marriage between two characters."""
        if char1_id not in self.characters or char2_id not in self.characters:
            return False
        
        char1 = self.characters[char1_id]
        char2 = self.characters[char2_id]
        
        # Check requirements
        if not char1.is_alive or not char2.is_alive:
            self.log("Both characters must be alive to marry.")
            return False
        
        if char1.gender == char2.gender:
            self.log("Marriage requires opposite genders.")
            return False
        
        if char1.spouse_id or char2.spouse_id:
            self.log("One or both characters are already married.")
            return False
        
        if self.get_opinion(char1_id, char2_id) < 0 or self.get_opinion(char2_id, char1_id) < 0:
            self.log("Marriage requires positive opinion between both parties.")
            return False
        
        # Perform marriage
        char1.spouse_id = char2_id
        char2.spouse_id = char1_id
        
        # Opinion boost
        self.modify_opinion(char1_id, char2_id, 25)
        self.modify_opinion(char2_id, char1_id, 25)
        
        self.log(f"{char1.name} and {char2.name} have married!")
        return True

    def get_family_tree(self, char_id: str) -> Dict:
        """Get structured family tree data for a character."""
        if char_id not in self.characters:
            return {}
        
        char = self.characters[char_id]
        tree = {
            "character": char,
            "father": self.characters.get(char.father_id) if char.father_id else None,
            "mother": self.characters.get(char.mother_id) if char.mother_id else None,
            "spouse": self.characters.get(char.spouse_id) if char.spouse_id else None,
            "children": [],
            "siblings": []
        }
        
        # Get children
        for cid, c in self.characters.items():
            if c.father_id == char_id or c.mother_id == char_id:
                tree["children"].append(c)
        
        # Get siblings (same parents)
        if char.father_id or char.mother_id:
            for cid, c in self.characters.items():
                if cid != char_id and (
                    (char.father_id and c.father_id == char.father_id) or
                    (char.mother_id and c.mother_id == char.mother_id)
                ):
                    tree["siblings"].append(c)
        
        return tree



    def process_polities(self):
        for polity in self.polities.values():
            self.government_manager.process_government(polity)

    def process_births(self):
        """Handle childbirth."""
        # Simple check: Married couples, age 16-45
        # We need to track spouses. For now, let's just iterate all characters.
        # To avoid double counting, we only check for the mother.
        
        for char_id, char in list(self.characters.items()):
            if not char.is_alive or char.gender != "Female":
                continue
            
            if 16 <= char.age <= 45 and char.spouse_id:
                spouse = self.characters.get(char.spouse_id)
                if spouse and spouse.is_alive:
                    # Chance of birth: 2% per month (~24% per year)
                    if random.random() < 0.02:
                        self.create_child(char.id, spouse.id)

    def create_child(self, mother_id: str, father_id: str):
        mother = self.characters[mother_id]
        father = self.characters[father_id]
        
        gender = "Male" if random.random() < 0.5 else "Female"
        name = f"Child of {father.name}" # Placeholder name generator
        
        child = Character(
            name=name,
            age=0,
            gender=gender,
            dynasty_id=father.dynasty_id, # Patrilineal for now
            father_id=father.id,
            mother_id=mother.id,
            culture=father.culture
        )
        
        self.characters[child.id] = child
        mother.children_ids.append(child.id)
        father.children_ids.append(child.id)
        
        if child.dynasty_id in self.dynasties:
            self.dynasties[child.dynasty_id].members.append(child.id)
            
        self.log(f"A {gender} child, {name}, was born to {father.name} and {mother.name}!")

        self.log(f"A {gender} child, {name}, was born to {father.name} and {mother.name}!")

    def modify_wealth(self, char_id: str, amount: int):
        if char_id in self.characters:
            self.characters[char_id].wealth += amount
            self.log(f"{self.characters[char_id].name} wealth change: {amount}")

    def modify_health(self, char_id: str, amount: float):
        if char_id in self.characters:
            self.characters[char_id].health += amount
            self.log(f"{self.characters[char_id].name} health change: {amount}")

    def get_wealth(self, char_id: str) -> int:
        return self.characters[char_id].wealth if char_id in self.characters else 0

    def process_events(self):
        """Trigger random events."""
        if self.current_event:
            return # Don't trigger new event if one is pending
            
        # 30% chance of event per month
        if random.random() < 0.3:
            event = self.event_manager.get_random_event(self, self.player_character_id)
            if event:
                self.current_event = event
                self.log(f"EVENT: {event.title}")

    def resolve_event(self, option_index: int):
        if not self.current_event:
            return
            
        if 0 <= option_index < len(self.current_event.options):
            option = self.current_event.options[option_index]
            self.log(f"Selected: {option.text}")
            option.effect(self, self.player_character_id)
            self.current_event = None

    def get_character_title(self, char_id: str) -> str:
        char = self.characters[char_id]
        # Simple logic: if head of dynasty, use 'Noble' equivalent.
        # If ruler of polity, use 'Ruler' equivalent.
        
        # Check if ruler
        for polity in self.polities.values():
            if polity.ruler_id == char.id:
                return self.culture_manager.get_title(char.culture, "ruler")
        
        # Check if heir (simple check: eldest son of ruler)
        if char.father_id:
            father = self.characters[char.father_id]
            # If father is ruler
            is_prince = False
            for polity in self.polities.values():
                if polity.ruler_id == father.id:
                    is_prince = True
                    break
            
            if is_prince and father.children_ids[0] == char.id:
                 return self.culture_manager.get_title(char.culture, "heir")

        return self.culture_manager.get_title(char.culture, "noble")

    def process_characters(self):
        """Handle aging, health, and death."""
        for char_id, char in list(self.characters.items()):
            if not char.is_alive:
                continue
            
            # Simple aging (just for display, real age calculation can be more complex)
            # In a real simulation, we'd track birthdate. 
            # For now, let's just say they age every January.
            if self.month == 1:
                char.age += 1
            
            # Death check (very basic)
            if char.age > 50:
                death_chance = (char.age - 50) * 0.005
                if random.random() < death_chance:
                    self.kill_character(char_id, "Natural Causes")

    def kill_character(self, char_id: str, reason: str):
        char = self.characters[char_id]
        char.is_alive = False
        self.log(f"{char.name} has died of {reason} at age {char.age}.")
        
        if char_id == self.player_character_id:
            self.handle_player_succession()

    def handle_player_succession(self):
        """Find an heir or end the game."""
        player = self.characters[self.player_character_id]
        # Very simple primogeniture for now
        if player.children_ids:
            # Find first living child
            for child_id in player.children_ids:
                if self.characters[child_id].is_alive:
                    self.player_character_id = child_id
                    new_player = self.characters[child_id]
                    self.log(f"Long live {new_player.name}! The bloodline endures.")
                    return
        
        self.game_over = True
        self.log("Your bloodline has ended. Game Over.")



    def create_test_scenario(self):
        """Setup a basic scenario for testing."""
        # Initialize Map
        self.world_manager.create_initial_map()
        
        # Find Latium
        latium_id = next(r.id for r in self.regions.values() if r.name == "Latium")

        # Create Dynasty
        dynasty = Dynasty(name="Julii")
        self.dynasties[dynasty.id] = dynasty
        
        # Create Player
        player = Character(
            name="Lucius Julius",
            age=30,
            gender="Male",
            culture="Roman",
            dynasty_id=dynasty.id,
            martial=12,
            diplomacy=14,
            location_id=latium_id
        )
        self.characters[player.id] = player
        self.player_character_id = player.id
        dynasty.members.append(player.id)
        
        # Create Wife
        wife = Character(
            name="Aurelia",
            age=28,
            gender="Female",
            culture="Roman",
            spouse_id=player.id
        )
        self.characters[wife.id] = wife
        player.spouse_id = wife.id
        
        # Create Son
        son = Character(
            name="Gaius Julius",
            age=10,
            gender="Male",
            dynasty_id=dynasty.id,
            father_id=player.id,
            mother_id=wife.id
        )
        self.characters[son.id] = son
        player.children_ids.append(son.id)
        wife.children_ids.append(son.id)
        dynasty.members.append(son.id)
        
        # Create Polity
        rome = Polity(name="Roman Kingdom", government_type=GovernmentType.MONARCHY, ruler_id=player.id)
        self.polities[rome.id] = rome
        self.regions[latium_id].owner_polity_id = rome.id
        
        self.log("Welcome to Project Aeterna. The year is 753 BC.")
