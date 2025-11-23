from engine import GameEngine
from models import Polity, GovernmentType, Character

def test_government():
    print("Initializing Engine...")
    engine = GameEngine()
    
    # Test Republic Election
    print("\nTesting Republic Election...")
    republic = Polity(name="Roman Republic", government_type=GovernmentType.REPUBLIC)
    republic.term_end_date = 753 # Ends this year
    engine.polities[republic.id] = republic
    
    # Create candidates
    c1 = Character(name="Candidate 1", age=35, gender="Male")
    c2 = Character(name="Candidate 2", age=40, gender="Male")
    engine.characters[c1.id] = c1
    engine.characters[c2.id] = c2
    
    # Process
    engine.government_manager.process_government(republic)
    
    if republic.ruler_id:
        ruler = engine.characters[republic.ruler_id]
        print(f"PASS: Election held. Winner: {ruler.name}")
        print(f"New Term End: {republic.term_end_date}")
    else:
        print("FAIL: No election held or no winner.")

    # Test Monarchy Legitimacy
    print("\nTesting Monarchy Legitimacy...")
    king = Character(name="King", diplomacy=15) # High diplomacy
    engine.characters[king.id] = king
    monarchy = Polity(name="Kingdom", government_type=GovernmentType.MONARCHY, ruler_id=king.id, legitimacy=50)
    engine.polities[monarchy.id] = monarchy
    
    initial_legitimacy = monarchy.legitimacy
    engine.government_manager.process_government(monarchy)
    
    if monarchy.legitimacy > initial_legitimacy:
        print(f"PASS: Legitimacy increased to {monarchy.legitimacy}")
    else:
        print(f"FAIL: Legitimacy {monarchy.legitimacy} (Expected > {initial_legitimacy})")

    # Test Tribal Prestige
    print("\nTesting Tribal Prestige...")
    tribe = Polity(name="Tribe", government_type=GovernmentType.TRIBE, prestige=10)
    engine.polities[tribe.id] = tribe
    
    engine.government_manager.process_government(tribe)
    
    if tribe.prestige < 10:
        print(f"PASS: Prestige decayed to {tribe.prestige}")
    else:
        print(f"FAIL: Prestige {tribe.prestige} (Expected < 10)")

if __name__ == "__main__":
    test_government()
