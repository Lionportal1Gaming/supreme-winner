# Release Notes - v0.1.1 "Dynasty Foundation"

**Release Date:** November 23, 2025

## 🎉 What's New

### Major Features

#### 🎭 Relationship System
- Characters now track opinions of each other (-100 to +100)
- Five relationship tiers: Hostile, Unfriendly, Neutral, Friendly, Allied
- New [R] Relationships menu to view all character relationships
- Arranged marriages with positive opinion requirements
- +25 opinion boost when characters marry

#### 👨‍👩‍👧‍👦 Family Tree Viewer
- View detailed genealogy for any character
- See parents, spouse, children, and siblings at a glance
- Access via [R] → [F] in the relationships menu
- Perfect for tracking your dynasty's lineage

#### 🏗️ Basic Economy
- Construct buildings in your territories
- **Farm**: 50 gold cost, +1 gold/month income
- **Estate**: 200 gold cost, +5 gold/month income
- Automatic monthly income from all owned buildings
- Buildings persist through save/load

#### 🎯 Start Menu
- Professional launcher when starting the game
- Options: New Game, Load Game, Quit
- Displays game title and version

### New Events
- **Diplomatic Insult** - Lose opinion with another character
- **Generous Gift** - Gain opinion and 20 gold
- **Magnificent Feast** - Spend 30 gold to boost all relationships by +10

### Quality of Life
- Improved terminal rendering stability
- Better save/load reliability
- Updated UI to show all new commands
- Cleaner relationships display with status indicators

## 🔧 Technical Improvements

- Added `opinions` dictionary to Character model
- Implemented `get_opinion()`, `modify_opinion()`, and `arrange_marriage()` methods
- Added `get_family_tree()` for genealogy tracking
- Enhanced serialization to preserve relationship data
- Optimized UI rendering for better terminal compatibility

## 🐛 Bug Fixes

- Fixed terminal corruption issues with Rich console
- Resolved income generation bug (region ownership)
- Improved UI stability across different terminal emulators

## 📝 Notes

- **Best Experience**: Run in proper terminal (Terminal.app, iTerm2) rather than IDE-embedded terminals
- Save files from v0.1.0 may not be compatible
- All new features are fully functional and tested

## 🚀 Coming in v0.1.2

- More building types (Markets, Barracks, Temples)
- Expanded event pool with 10-15 new events
- Character creation system
- Enhanced dynasty mechanics

---

**Thank you for playing Project Aeterna!**
