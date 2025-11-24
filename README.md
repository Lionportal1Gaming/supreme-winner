# Project Aeterna v0.1.1 - Dynasty Foundation

**A text-based dynastic strategy game where you build and maintain a legacy across generations.**

## 🎮 About

Project Aeterna is a turn-based strategy game focused on dynasty management, political maneuvering, and building a lasting legacy. Starting in 753 BC as the ruler of Rome, you must navigate relationships, manage your economy, and secure your bloodline's future.

## ✨ Features (v0.1.1)

### Core Gameplay
- **Monthly Turn System** - Advance time and watch your dynasty evolve
- **Dynamic Events** - Random events that test your decision-making
- **World Map** - Navigate through regions of ancient Italy and beyond

### Economy & Development
- **Building System** - Construct Farms and Estates for passive income
- **Wealth Management** - Earn and spend gold strategically
- **Monthly Income** - Generate wealth from your territories

### Relationships & Dynasty
- **Opinion System** - Track relationships with other characters (-100 to +100)
- **Marriage System** - Arrange strategic marriages to strengthen alliances
- **Family Tree** - View detailed genealogy for any character
- **Relationship Events** - Diplomatic gifts, insults, and feasts

### Quality of Life
- **Save/Load System** - Resume your campaigns anytime
- **Start Menu** - Professional game launcher
- **Clean UI** - Rich-formatted terminal interface

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- `rich` library for terminal UI

### Setup
```bash
# Clone or download the game
cd BloodLines

# Install dependencies
pip3 install rich

# Run the game
python3 main.py
```

## 🎯 How to Play

### Starting Out
1. Launch the game with `python3 main.py`
2. Choose **[N] New Game** from the start menu
3. You begin as Lucius Julius, Rex of Rome in 753 BC

### Commands
- **[ENTER]** - Advance to next month
- **[M]** - Move to neighboring regions
- **[B]** - Build structures in your territory
- **[R]** - View relationships and arrange marriages
- **[S]** - Save your game
- **[L]** - Load a saved game
- **[Q]** - Quit

### Gameplay Tips
- Build Farms early for steady income (50 gold, +1/month)
- Maintain positive relationships for marriage opportunities
- Monitor your health and wealth carefully
- Use the Family Tree ([R] → [F]) to track your dynasty

## 📋 Game Mechanics

### Buildings
| Building | Cost | Income/Month |
|----------|------|--------------|
| Farm     | 50   | +1          |
| Estate   | 200  | +5          |

### Relationship Levels
- **Allied** (+50 to +100) - Strong bond
- **Friendly** (+10 to +49) - Positive connection
- **Neutral** (-9 to +9) - No strong feelings
- **Unfriendly** (-49 to -10) - Tension
- **Hostile** (-100 to -50) - Active enmity

### Marriage Requirements
- Both characters alive
- Opposite genders
- Neither already married
- Positive opinion between parties

## 🗺️ Roadmap

### v0.1.2 (Planned)
- More building types (Markets, Barracks, Temples)
- Expanded event pool (10-15 new events)
- Character creation system

### v0.2.0 (Future)
- Combat and warfare
- AI rulers with independent actions
- Advanced diplomacy options

## 🐛 Known Issues

- Game is best played in a proper terminal (Terminal.app, iTerm2)
- IDE-embedded terminals may have limited Rich rendering support

## 📝 Version History

### v0.1.1 - Dynasty Foundation (Current)
- Added start menu
- Implemented relationship system with opinions
- Added marriage mechanics
- Created family tree viewer
- Built basic economy with farms and estates
- Added save/load functionality

### v0.1.0 - Initial Release
- Core game loop
- Basic character system
- Event framework
- World generation

## 🤝 Contributing

This is a solo development project, but feedback is welcome!

## 📄 License

*License information to be added*

## 🙏 Credits

Developed by Alex Taylor
Built with Python and the Rich library

---

**Enjoy building your dynasty!** 🏛️
