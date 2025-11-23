from engine import GameEngine
from models import Character

def test_engine():
    print("Initializing Engine...")
    engine = GameEngine()
    engine.create_test_scenario()
    
    player = engine.characters[engine.player_character_id]
    print(f"Player: {player.name}, Age: {player.age}, Gender: {player.gender}")
    
    # Test Aging
    print("\nTesting Aging...")
    initial_age = player.age
    # Advance 12 months
    for _ in range(12):
        engine.advance_month()
    
    if player.age == initial_age + 1:
        print("PASS: Player aged correctly.")
    else:
        print(f"FAIL: Player age {player.age} (expected {initial_age + 1})")
        
    # Test Birth (Force it)
    print("\nTesting Birth...")
    # Find wife
    wife_id = player.spouse_id
    wife = engine.characters[wife_id]
    
    # Force create child
    initial_children_count = len(player.children_ids)
    engine.create_child(wife.id, player.id)
    
    if len(player.children_ids) == initial_children_count + 1:
        print("PASS: Child created and linked.")
        child_id = player.children_ids[-1]
        child = engine.characters[child_id]
        print(f"Child Name: {child.name}, Gender: {child.gender}")
    else:
        print("FAIL: Child not linked.")

    # Test Death
    print("\nTesting Death...")
    engine.kill_character(player.id, "Testing")
    if not player.is_alive:
        print("PASS: Player died.")
    else:
        print("FAIL: Player still alive.")
        
    if engine.player_character_id != player.id:
         print(f"PASS: Succession occurred. New Player: {engine.characters[engine.player_character_id].name}")
    else:
         print("FAIL: Succession failed.")

if __name__ == "__main__":
    test_engine()
