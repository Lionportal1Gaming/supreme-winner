from .models import Region, Terrain, Polity, GovernmentType
from typing import Dict, List, Optional
import random

class WorldManager:
    def __init__(self, engine):
        self.engine = engine

    def create_initial_map(self):
        """Creates the 753 BC map nodes."""
        # 1. Italy
        latium = self._create_region("Latium", Terrain.PLAINS, neighbors=[])
        etruria = self._create_region("Etruria", Terrain.HILLS, neighbors=[latium.id])
        campania = self._create_region("Campania", Terrain.COASTAL, neighbors=[latium.id])
        
        # Link back
        latium.neighbors.extend([etruria.id, campania.id])
        
        # 2. Greece
        attica = self._create_region("Attica", Terrain.HILLS, neighbors=[])
        peloponnese = self._create_region("Peloponnese", Terrain.MOUNTAINS, neighbors=[attica.id])
        attica.neighbors.append(peloponnese.id)
        
        # 3. Near East
        egypt = self._create_region("Lower Egypt", Terrain.PLAINS, neighbors=[])
        judaea = self._create_region("Judaea", Terrain.HILLS, neighbors=[egypt.id])
        egypt.neighbors.append(judaea.id)
        
        self.engine.log("World Map generated (Italy, Greece, Near East).")

    def _create_region(self, name: str, terrain: Terrain, neighbors: List[str]) -> Region:
        region = Region(name=name, terrain=terrain, neighbors=neighbors)
        self.engine.regions[region.id] = region
        return region

    def move_character(self, char_id: str, target_region_id: str) -> bool:
        char = self.engine.characters.get(char_id)
        if not char:
            return False
            
        current_region_id = char.location_id
        if not current_region_id:
            # If nowhere, just place them
            char.location_id = target_region_id
            self.engine.log(f"{char.name} has arrived in {self.engine.regions[target_region_id].name}.")
            return True
            
        current_region = self.engine.regions.get(current_region_id)
        if target_region_id in current_region.neighbors:
            char.location_id = target_region_id
            self.engine.log(f"{char.name} moved from {current_region.name} to {self.engine.regions[target_region_id].name}.")
            return True
        else:
            self.engine.log(f"Cannot move to {self.engine.regions[target_region_id].name} - not adjacent!")
            return False

    def resolve_combat(self, attacker_id: str, defender_id: str):
        attacker = self.engine.characters[attacker_id]
        defender = self.engine.characters[defender_id]
        
        self.engine.log(f"COMBAT: {attacker.name} attacks {defender.name}!")
        
        # Simple roll: Martial + d20
        att_roll = attacker.martial + random.randint(1, 20)
        def_roll = defender.martial + random.randint(1, 20)
        
        if att_roll > def_roll:
            self.engine.log(f"{attacker.name} wins! ({att_roll} vs {def_roll})")
            # Defender wounded
            self.engine.modify_health(defender.id, -2.0)
        else:
            self.engine.log(f"{defender.name} repels the attack! ({def_roll} vs {att_roll})")
            # Attacker wounded
            self.engine.modify_health(attacker.id, -1.0)
