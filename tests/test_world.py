from bloodlines.engine import GameEngine
from bloodlines.models import Character

def test_world():
    print("Initializing Engine...")
    engine = GameEngine()
    engine.create_test_scenario()
    
    player = engine.characters[engine.player_character_id]
    start_loc_id = player.location_id
    start_loc_name = engine.regions[start_loc_id].name
    print(f"Player Start: {start_loc_name}")
    
    if start_loc_name != "Latium":
        print(f"FAIL: Started in {start_loc_name} (Expected Latium)")
        return

    # Test Movement (Valid)
    print("\nTesting Movement...")
    # Latium neighbors: Etruria, Campania
    latium = engine.regions[start_loc_id]
    target_id = latium.neighbors[0]
    target_name = engine.regions[target_id].name
    
    print(f"Attempting move to {target_name}...")
    success = engine.world_manager.move_character(player.id, target_id)
    
    if success and player.location_id == target_id:
        print(f"PASS: Moved to {target_name}")
    else:
        print("FAIL: Movement failed.")

    # Test Movement (Invalid - Not Adjacent)
    # Find a non-neighbor (e.g., Egypt)
    egypt_id = next(r.id for r in engine.regions.values() if r.name == "Lower Egypt")
    print(f"\nAttempting invalid move to Lower Egypt...")
    success = engine.world_manager.move_character(player.id, egypt_id)
    
    if not success and player.location_id == target_id:
        print("PASS: Invalid movement blocked.")
    else:
        print("FAIL: Invalid movement allowed.")

    # Test Combat
    print("\nTesting Combat...")
    enemy = Character(name="Enemy", martial=10, location_id=target_id)
    engine.characters[enemy.id] = enemy
    
    initial_health = enemy.health
    engine.world_manager.resolve_combat(player.id, enemy.id)
    
    if enemy.health < initial_health or player.health < 10.0:
        print("PASS: Combat resolved (health changed).")
    else:
        print("FAIL: No health change after combat.")

if __name__ == "__main__":
    test_world()
