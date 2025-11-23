from engine import GameEngine
from events import EventManager

def test_events():
    print("Initializing Engine...")
    engine = GameEngine()
    engine.create_test_scenario()
    player_id = engine.player_character_id
    
    print(f"Initial Wealth: {engine.get_wealth(player_id)}")
    
    # Force trigger 'Good Harvest'
    print("\nTesting Event Triggering...")
    # We can manually fetch it from the manager to test
    harvest_event = next(e for e in engine.event_manager.events if e.id == "good_harvest")
    
    engine.current_event = harvest_event
    print(f"Event Set: {engine.current_event.title}")
    
    # Resolve Event (Option 0: Gain 50 Wealth)
    print("\nResolving Event...")
    engine.resolve_event(0)
    
    current_wealth = engine.get_wealth(player_id)
    print(f"New Wealth: {current_wealth}")
    
    if current_wealth == 150: # 100 start + 50
        print("PASS: Wealth updated correctly.")
    else:
        print(f"FAIL: Wealth is {current_wealth} (Expected 150)")
        
    if engine.current_event is None:
        print("PASS: Event cleared.")
    else:
        print("FAIL: Event still active.")

if __name__ == "__main__":
    test_events()
