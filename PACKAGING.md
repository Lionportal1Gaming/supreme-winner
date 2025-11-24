# Project Aeterna - Distribution Package

## 📦 Packaging v0.1.1 for Distribution

### Files to Include

**Core Game Files:**
```
BloodLines/
├── main.py                    # Game launcher
├── bloodlines/
│   ├── __init__.py
│   ├── engine.py             # Core game logic
│   ├── models.py             # Data models
│   ├── events.py             # Event system
│   ├── culture.py            # Culture manager
│   ├── government.py         # Government types
│   └── world.py              # World generation
├── cultures.json              # Culture data
├── README.md                  # User documentation
├── RELEASE_NOTES.md          # Version history
└── requirements.txt          # Python dependencies
```

### Create Distribution Package

#### Option 1: ZIP Archive (Recommended)
```bash
cd /Users/alextaylor/Documents/Coding
zip -r ProjectAeterna-v0.1.1.zip BloodLines/ \
  -x "*.pyc" -x "*__pycache__/*" -x "*.save" \
  -x ".git/*" -x ".DS_Store" -x "savegame*"
```

#### Option 2: Git Tag & Release
```bash
cd /Users/alextaylor/Documents/Coding/BloodLines
git add .
git commit -m "Release v0.1.1 - Dynasty Foundation"
git tag -a v0.1.1 -m "Version 0.1.1 - Dynasty Foundation"
git push origin main --tags
```

### Create requirements.txt
```bash
cd /Users/alextaylor/Documents/Coding/BloodLines
echo "rich>=13.0.0" > requirements.txt
```

### Distribution Checklist

- [x] README.md created with installation instructions
- [x] RELEASE_NOTES.md with version history
- [x] Version number updated in game (v0.1.1)
- [ ] requirements.txt created
- [ ] Test fresh install on clean system
- [ ] Create distribution ZIP
- [ ] Upload to itch.io or GitHub

### Installation Instructions for Users

**Windows:**
```bash
# Extract ZIP
# Open Command Prompt
pip install rich
python main.py
```

**Mac/Linux:**
```bash
# Extract ZIP
# Open Terminal
pip3 install rich
python3 main.py
```

### Itch.io Upload Instructions

1. Create new project: "Project Aeterna"
2. Upload: `ProjectAeterna-v0.1.1.zip`
3. Classification: "Downloadable"
4. Kind: "Other"
5. Price: Free (or set price)
6. Description: Copy from README.md
7. Tags: strategy, text-based, dynasty, simulation
8. Platform: Windows, macOS, Linux (Python cross-platform)

### GitHub Release Instructions

1. Go to Releases → Draft New Release
2. Tag: v0.1.1
3. Title: "v0.1.1 - Dynasty Foundation"
4. Description: Copy from RELEASE_NOTES.md
5. Attach: `ProjectAeterna-v0.1.1.zip`
6. Publish Release

---

**Ready to distribute!** 🚀
