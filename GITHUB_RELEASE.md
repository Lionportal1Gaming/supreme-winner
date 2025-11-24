# GitHub Release Guide - v0.1.1

## Step 1: Initialize Git Repository (if not done)

```bash
cd /Users/alextaylor/Documents/Coding/BloodLines

# Initialize git
git init

# Add .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Save files
*.save
savegame*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Distribution
*.zip
EOF

# Add all files
git add .
git commit -m "Initial commit - Project Aeterna v0.1.1"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `project-aeterna` or `BloodLines`
3. Description: "A text-based dynastic strategy game"
4. Public or Private (your choice)
5. **DO NOT** initialize with README (we have one)
6. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add your GitHub repo as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/project-aeterna.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Create Release on GitHub

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. **Tag version:** `v0.1.1`
4. **Release title:** `v0.1.1 - Dynasty Foundation`
5. **Description:** Copy from RELEASE_NOTES.md
6. **Attach files:** Upload `ProjectAeterna-v0.1.1.zip`
7. Click "Publish release"

## Alternative: Using Git Tags

```bash
# Create tag
git tag -a v0.1.1 -m "Version 0.1.1 - Dynasty Foundation"

# Push tag
git push origin v0.1.1

# Then create release on GitHub web interface
```

---

**Done! Your game is now on GitHub!**
