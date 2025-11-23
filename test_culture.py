from engine import GameEngine
from models import Character

def test_culture():
    print("Initializing Engine...")
    engine = GameEngine()
    
    # Test Roman
    print("\nTesting Roman Culture...")
    roman_char = Character(name="Romulus", culture="Roman", gender="Male")
    engine.characters[roman_char.id] = roman_char
    
    # Mock him as ruler
    from models import Polity, GovernmentType
    rome = Polity(name="Rome", government_type=GovernmentType.MONARCHY, ruler_id=roman_char.id)
    engine.polities[rome.id] = rome
    
    title = engine.get_character_title(roman_char.id)
    if title == "Rex":
        print(f"PASS: Roman Ruler is '{title}'")
    else:
        print(f"FAIL: Roman Ruler is '{title}' (Expected 'Rex')")

    # Test Greek
    print("\nTesting Greek Culture...")
    greek_char = Character(name="Pericles", culture="Greek", gender="Male")
    engine.characters[greek_char.id] = greek_char
    
    athens = Polity(name="Athens", government_type=GovernmentType.REPUBLIC, ruler_id=greek_char.id)
    engine.polities[athens.id] = athens
    
    title = engine.get_character_title(greek_char.id)
    if title == "Archon":
        print(f"PASS: Greek Ruler is '{title}'")
    else:
        print(f"FAIL: Greek Ruler is '{title}' (Expected 'Archon')")

    # Test Tribal
    print("\nTesting Tribal Culture...")
    celt_char = Character(name="Vercingetorix", culture="Tribal", gender="Male")
    engine.characters[celt_char.id] = celt_char
    
    tribe = Polity(name="Arverni", government_type=GovernmentType.TRIBE, ruler_id=celt_char.id)
    engine.polities[tribe.id] = tribe
    
    title = engine.get_character_title(celt_char.id)
    if title == "Chieftain":
        print(f"PASS: Tribal Ruler is '{title}'")
    else:
        print(f"FAIL: Tribal Ruler is '{title}' (Expected 'Chieftain')")

if __name__ == "__main__":
    test_culture()
