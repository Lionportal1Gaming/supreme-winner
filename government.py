from models import Polity, GovernmentType, Character
import random

class GovernmentManager:
    def __init__(self, engine):
        self.engine = engine

    def process_government(self, polity: Polity):
        if polity.government_type == GovernmentType.REPUBLIC:
            self._process_republic(polity)
        elif polity.government_type == GovernmentType.MONARCHY:
            self._process_monarchy(polity)
        elif polity.government_type == GovernmentType.TRIBE:
            self._process_tribe(polity)

    def _process_republic(self, polity: Polity):
        # Election Check
        if self.engine.year >= polity.term_end_date:
            self._hold_election(polity)

    def _hold_election(self, polity: Polity):
        self.engine.log(f"Elections are held in {polity.name}!")
        
        # Simple election logic: Random candidate wins for now
        # In a real game, this would weigh influence/bribery
        candidates = [c for c in self.engine.characters.values() 
                     if c.is_alive and c.age >= 30 and c.gender == "Male"] # Basic eligibility
        
        if candidates:
            winner = random.choice(candidates)
            polity.ruler_id = winner.id
            polity.term_end_date = self.engine.year + 1 # 1 Year term
            self.engine.log(f"{winner.name} has been elected as Ruler of {polity.name}!")
        else:
            self.engine.log(f"No eligible candidates found for {polity.name}.")

    def _process_monarchy(self, polity: Polity):
        # Legitimacy decay/gain
        # If ruler has high stats, legitimacy increases
        ruler = self.engine.characters.get(polity.ruler_id)
        if ruler:
            if ruler.diplomacy > 10:
                polity.legitimacy = min(100, polity.legitimacy + 1)
            elif ruler.diplomacy < 5:
                polity.legitimacy = max(0, polity.legitimacy - 1)

    def _process_tribe(self, polity: Polity):
        # Prestige decay
        polity.prestige = max(0, polity.prestige - 1)
        
        # Challenge for leadership
        # If a strong warrior exists, they might challenge a weak chief
        ruler = self.engine.characters.get(polity.ruler_id)
        if ruler and ruler.martial < 5:
            self.engine.log(f"Rumors of a challenge to {ruler.name}'s leadership spread...")
