from dataclasses import dataclass, field
from typing import List, Callable, Optional, Dict
import random

@dataclass
class EventOption:
    text: str
    effect: Callable[['GameEngine', str], None]  # Takes engine and char_id
    tooltip: str = ""

@dataclass
class Event:
    id: str
    title: str
    description: str
    options: List[EventOption]
    trigger_condition: Callable[['GameEngine', str], bool]
    weight: int = 10  # Higher weight = more likely

class EventManager:
    def __init__(self):
        self.events: List[Event] = []
        self._register_generic_events()

    def _register_generic_events(self):
        # Example Event: Good Harvest
        self.events.append(Event(
            id="good_harvest",
            title="Good Harvest",
            description="The season has been kind. Our granaries are full.",
            options=[
                EventOption(
                    text="Excellent!",
                    effect=lambda engine, char_id: engine.modify_wealth(char_id, 50),
                    tooltip="Gain 50 Wealth"
                )
            ],
            trigger_condition=lambda engine, char_id: True, # Always possible
            weight=20
        ))
        
        # Example Event: Minor Sickness
        self.events.append(Event(
            id="minor_sickness",
            title="Feeling Unwell",
            description="You have developed a nasty cough.",
            options=[
                EventOption(
                    text="Rest and recover.",
                    effect=lambda engine, char_id: engine.modify_health(char_id, -1.0),
                    tooltip="Lose 1.0 Health"
                ),
                EventOption(
                    text="Consult a physician (Cost: 10)",
                    effect=lambda engine, char_id: self._physician_effect(engine, char_id),
                    tooltip="Cost 10 Wealth, maybe save health"
                )
            ],
            trigger_condition=lambda engine, char_id: True,
            weight=10
        ))
        
        # Relationship Event: Diplomatic Insult
        self.events.append(Event(
            id="diplomatic_insult",
            title="Diplomatic Insult",
            description="A foreign dignitary has insulted your honor at a gathering.",
            options=[
                EventOption(
                    text="Demand an apology!",
                    effect=lambda engine, char_id: self._insult_effect(engine, char_id),
                    tooltip="Lose opinion with a character"
                )
            ],
            trigger_condition=lambda engine, char_id: len(engine.characters) > 1,
            weight=5
        ))
        
        # Relationship Event: Gift Received
        self.events.append(Event(
            id="gift_received",
            title="Generous Gift",
            description="A neighboring ruler has sent you a valuable gift as a token of friendship.",
            options=[
                EventOption(
                    text="Accept graciously.",
                    effect=lambda engine, char_id: self._gift_effect(engine, char_id),
                    tooltip="Gain opinion with a character and wealth"
                )
            ],
            trigger_condition=lambda engine, char_id: len(engine.characters) > 1,
            weight=8
        ))
        
        # Relationship Event: Successful Feast
        self.events.append(Event(
            id="successful_feast",
            title="Magnificent Feast",
            description="Your grand feast was a tremendous success! Guests leave impressed.",
            options=[
                EventOption(
                    text="Excellent!",
                    effect=lambda engine, char_id: self._feast_effect(engine, char_id),
                    tooltip="Cost 30 Wealth, gain opinion with multiple characters"
                )
            ],
            trigger_condition=lambda engine, char_id: engine.get_wealth(char_id) >= 30 and len(engine.characters) > 1,
            weight=6
        ))

    def _insult_effect(self, engine, char_id):
        # Pick a random other character
        other_chars = [cid for cid in engine.characters.keys() if cid != char_id and engine.characters[cid].is_alive]
        if other_chars:
            target_id = random.choice(other_chars)
            engine.modify_opinion(char_id, target_id, -15)
            engine.modify_opinion(target_id, char_id, -10)

    def _gift_effect(self, engine, char_id):
        # Pick a random other character
        other_chars = [cid for cid in engine.characters.keys() if cid != char_id and engine.characters[cid].is_alive]
        if other_chars:
            target_id = random.choice(other_chars)
            engine.modify_opinion(char_id, target_id, 15)
            engine.modify_wealth(char_id, 20)

    def _feast_effect(self, engine, char_id):
        engine.modify_wealth(char_id, -30)
        # Boost opinion with all other characters
        for cid in engine.characters.keys():
            if cid != char_id and engine.characters[cid].is_alive:
                engine.modify_opinion(cid, char_id, 10)


    def _physician_effect(self, engine, char_id):
        if engine.get_wealth(char_id) >= 10:
            engine.modify_wealth(char_id, -10)
            # 50% chance to save health
            if random.random() > 0.5:
                engine.log("The physician's treatment worked!")
            else:
                engine.log("The treatment failed.")
                engine.modify_health(char_id, -1.0)
        else:
            engine.log("You cannot afford a physician!")
            engine.modify_health(char_id, -1.0)

    def get_random_event(self, engine, char_id: str) -> Optional[Event]:
        # Filter valid events
        valid_events = [e for e in self.events if e.trigger_condition(engine, char_id)]
        if not valid_events:
            return None
            
        # Weighted random choice
        total_weight = sum(e.weight for e in valid_events)
        pick = random.uniform(0, total_weight)
        current = 0
        for event in valid_events:
            current += event.weight
            if pick <= current:
                return event
        return None
