# Installation Guide - GUI Version

This guide will help you install and run the Asana Project Progress Tracker on Windows and macOS/Linux.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Asana account with API access

## Step 1: Install Python

### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: Open Command Prompt and type `python --version`

### macOS
1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```bash
   brew install python
   ```
3. Verify installation: Open Terminal and type `python3 --version`

## Step 2: Install Dependencies

1. Open terminal/command prompt in the project directory
2. Install the required packages:

```bash
# Windows
pip install -r requirements_gui.txt

# macOS/Linux
pip3 install -r requirements_gui.txt
```

## Step 3: Get Your Asana API Key

1. Go to [Asana Developer Console](https://app.asana.com/0/developer-console)
2. Click "Create a new app" or use an existing app
3. Go to the "Personal Access Tokens" section
4. Click "Create a new personal access token"
5. Copy the token (you'll only see it once!)

## Step 4: Run the Application

### Option 1: Using the launcher scripts

**Windows:**
- Double-click `run_gui.bat`
- Or run `python run_gui.py` in Command Prompt

**macOS/Linux:**
- Run `./run_gui.sh` in Terminal
- Or run `python3 run_gui.py` in Terminal

### Option 2: Direct execution

```bash
# Windows
python asana_progress_gui.py

# macOS/Linux
python3 asana_progress_gui.py
```

## Step 5: First Launch Setup

1. The application will open with a "Not connected" status
2. Click the "Settings" button
3. Enter your Asana API key in the text field
4. Click "Save"
5. The status should change to "Connected to Asana"
6. Click "Refresh" to load your projects

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install --upgrade pip
pip install -r requirements_gui.txt
```

**CustomTkinter not found:**
```bash
pip install customtkinter
```

**Pillow not found:**
```bash
pip install Pillow
```

**API key not working:**
- Verify the API key is correct
- Check that the key has the necessary permissions
- Try creating a new personal access token

**No projects showing:**
- Ensure you have access to projects in your Asana workspaces
- Check your internet connection
- Verify Asana API status

### Windows Specific

**Python not in PATH:**
- Reinstall Python and check "Add Python to PATH"
- Or add Python manually to your system PATH

**Permission errors:**
- Run Command Prompt as Administrator
- Or install packages with: `pip install --user -r requirements_gui.txt`

### macOS Specific

**Python3 not found:**
```bash
brew install python
```

**Permission errors:**
```bash
sudo pip3 install -r requirements_gui.txt
```

## Features Overview

Once running, you'll have access to:

- **Project Cards**: Visual representation of each project with progress bars
- **Workspace Filtering**: Filter projects by specific workspaces
- **Summary Dashboard**: Overview statistics and overall progress
- **Settings Panel**: Manage your API key securely
- **Real-time Refresh**: Update project data with one click

## Security Notes

- Your API key is stored securely in your system's keychain
- The key is never stored in plain text
- You can clear the key at any time using the Settings panel

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Python and package versions
3. Ensure your Asana API key is valid
4. Check your internet connection

## Uninstalling

To remove the application:
1. Delete the project folder
2. The API key will remain in your system keychain (you can remove it manually if desired)

To remove the API key from keychain:
- **Windows**: Use Credential Manager
- **macOS**: Use Keychain Access
- Or use the "Clear" button in the Settings panel 