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

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "prestige": self.prestige,
            "members": self.members
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Dynasty':
        return cls(**data)

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
    
    # Relationships
    opinions: Dict[str, int] = field(default_factory=dict)  # char_id -> opinion (-100 to +100)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "is_alive": self.is_alive,
            "dynasty_id": self.dynasty_id,
            "culture": self.culture,
            "gender": self.gender,
            "father_id": self.father_id,
            "mother_id": self.mother_id,
            "spouse_id": self.spouse_id,
            "children_ids": self.children_ids,
            "martial": self.martial,
            "diplomacy": self.diplomacy,
            "stewardship": self.stewardship,
            "intrigue": self.intrigue,
            "learning": self.learning,
            "traits": self.traits,
            "health": self.health,
            "stress": self.stress,
            "wealth": self.wealth,
            "location_id": self.location_id,
            "opinions": self.opinions
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        return cls(**data)

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

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "government_type": self.government_type.value,
            "ruler_id": self.ruler_id,
            "capital_id": self.capital_id,
            "laws": self.laws,
            "term_end_date": self.term_end_date,
            "legitimacy": self.legitimacy,
            "prestige": self.prestige
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Polity':
        # Convert string back to Enum
        if "government_type" in data:
            data["government_type"] = GovernmentType(data["government_type"])
        return cls(**data)

@dataclass
class Region:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Region"
    terrain: Terrain = Terrain.PLAINS
    owner_polity_id: Optional[str] = None
    population: int = 1000
    wealth: int = 100
    neighbors: List[str] = field(default_factory=list) # List of Region IDs
    buildings: Dict[str, int] = field(default_factory=dict) # Building Type -> Count

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain.value,
            "owner_polity_id": self.owner_polity_id,
            "population": self.population,
            "wealth": self.wealth,
            "neighbors": self.neighbors,
            "buildings": self.buildings
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Region':
        # Convert string back to Enum
        if "terrain" in data:
            data["terrain"] = Terrain(data["terrain"])
        return cls(**data)
