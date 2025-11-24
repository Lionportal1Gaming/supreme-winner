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
