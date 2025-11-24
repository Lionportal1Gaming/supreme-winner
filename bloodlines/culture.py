import json
from typing import Dict, List, Optional

class CultureManager:
    def __init__(self, config_path: str = "data/cultures.json"):
        self.data = self._load_data(config_path)

    def _load_data(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Culture config file '{path}' not found.")
            return {}

    def get_title(self, culture: str, title_type: str) -> str:
        """
        Get the localized title for a specific culture.
        title_type: 'ruler', 'heir', 'noble'
        """
        culture_data = self.data.get(culture, self.data.get("Generic"))
        if not culture_data:
            return title_type.capitalize()
        
        return culture_data.get("titles", {}).get(title_type, title_type.capitalize())

    def get_unit_name(self, culture: str, unit_tier: str) -> str:
        """
        Get the unit name for a specific culture.
        unit_tier: 'basic', 'elite'
        """
        culture_data = self.data.get(culture, self.data.get("Generic"))
        if not culture_data:
            return "Warriors"
            
        return culture_data.get("units", {}).get(unit_tier, "Warriors")

    def get_mechanics(self, culture: str) -> List[str]:
        culture_data = self.data.get(culture, self.data.get("Generic"))
        return culture_data.get("mechanics", [])
