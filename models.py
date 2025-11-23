from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import uuid

class GovernmentType(Enum):
    REPUBLIC = "Republic"
    MONARCHY = "Monarchy"
    TRIBE = "Tribe"

class Terrain(Enum):
    PLAINS = "Plains"
    HILLS = "Hills"
    DESERT = "Desert"
    MOUNTAINS = "Mountains"
    COASTAL = "Coastal"

@dataclass
class Dynasty:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unknown"
    prestige: int = 0
    members: List[str] = field(default_factory=list)  # List of Character IDs

@dataclass
class Character:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed"
    age: int = 16
    is_alive: bool = True
    dynasty_id: Optional[str] = None
    culture: str = "Generic"
    gender: str = "Male"  # "Male" or "Female"
    
    # Family
    father_id: Optional[str] = None
    mother_id: Optional[str] = None
    spouse_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # Stats (0-20 scale)
    martial: int = 5
    diplomacy: int = 5
    stewardship: int = 5
    intrigue: int = 5
    learning: int = 5
    
    # Traits
    traits: List[str] = field(default_factory=list)
    
    # State
    health: float = 10.0
    stress: float = 0.0
    wealth: int = 100
    location_id: Optional[str] = None

@dataclass
class Polity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Polity"
    government_type: GovernmentType = GovernmentType.TRIBE
    ruler_id: Optional[str] = None
    capital_id: Optional[str] = None
    laws: Dict[str, str] = field(default_factory=dict)
    
    # Government Specifics
    term_end_date: int = 0  # For Republics (Year)
    legitimacy: int = 100   # For Monarchies
    prestige: int = 0       # For Tribes

@dataclass
class Region:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Region"
    terrain: Terrain = Terrain.PLAINS
    owner_polity_id: Optional[str] = None
    population: int = 1000
    wealth: int = 100
    neighbors: List[str] = field(default_factory=list) # List of Region IDs
