# Asana Project Progress Tracker

A modern, cross-platform GUI application that displays progress bars for all your Asana projects with a beautiful interface. Built with CustomTkinter for Windows and macOS compatibility.

## Features

- 🖥️ **Modern GUI Interface** - Beautiful, responsive design with dark/light theme support
- 🔍 **Cross-Platform** - Works seamlessly on Windows and macOS
- 📊 **Visual Progress Bars** - Real-time progress visualization for all projects
- 📋 **Workspace Organization** - Projects grouped by workspace with filtering
- 🏷️ **Status Indicators** - Color-coded project status ("on track", "at risk", "on hold", etc.)
- 📈 **Summary Dashboard** - Overview statistics and overall progress
- 🔐 **Secure API Storage** - API key stored securely in system keychain
- 🔄 **Real-time Refresh** - Update project data with one click
- ⚙️ **Settings Panel** - Easy API key management

## Screenshots

The GUI features:
- Clean, modern interface with dark theme
- Project cards with progress bars and status indicators
- Workspace filtering and organization
- Summary statistics dashboard
- Settings panel for API key management

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements_gui.txt
```

### 2. Get Your Asana API Key

1. Go to [Asana Developer Console](https://app.asana.com/0/developer-console)
2. Create a new app or use an existing one
3. Copy your Personal Access Token

### 3. Run the Application

```bash
python asana_progress_gui.py
```

## Usage

1. **First Launch**: The app will prompt you to enter your Asana API key in the Settings panel
2. **Connect**: Enter your API key and click "Save" to connect to Asana
3. **Refresh**: Click the "Refresh" button to load your latest project data
4. **Filter**: Use the workspace dropdown to filter projects by specific workspaces
5. **Settings**: Access the Settings panel to manage your API key

## Features Overview

### Project Cards
Each project is displayed in a card showing:
- Project name
- Visual progress bar with percentage
- Task count (completed/total)
- Color-coded status indicator
- Workspace information

### Summary Dashboard
- Total projects count
- Active, completed, and archived projects
- Overall progress across all projects
- Total task completion statistics

### Workspace Filtering
- Filter projects by specific workspaces
- "All Workspaces" option to view everything
- Automatic workspace detection

### Settings Panel
- API key management
- Secure storage in system keychain
- Easy key updates and clearing

## Requirements

- Python 3.7+
- Asana API access
- Required packages: `asana`, `keyring`, `customtkinter`, `Pillow`

## Cross-Platform Support

This application is built with **CustomTkinter**, a modern Python UI framework that provides:
- **Windows**: Native Windows appearance and behavior
- **macOS**: Native macOS appearance and behavior
- **Consistent Experience**: Same interface and functionality across platforms
- **Modern Themes**: Built-in dark/light theme support

## Troubleshooting

- **API Key Error**: Use the Settings panel to update your Asana API key
- **No Projects Found**: Check that you have access to projects in your Asana workspaces
- **Connection Issues**: Verify your internet connection and Asana API status
- **Keychain Issues**: If keychain storage fails, you can still use the app but will need to enter the API key each time

## Comparison with Console Version

| Feature | Console Version | GUI Version |
|---------|----------------|-------------|
| Interface | Terminal/Console | Modern GUI |
| Cross-platform | Yes | Yes |
| Progress visualization | Text-based bars | Visual progress bars |
| Project organization | Tables by workspace | Cards with filtering |
| Settings management | Command line | GUI panel |
| Real-time updates | Manual re-run | One-click refresh |
| Theme support | Rich colors | Dark/light themes |

## Development

The GUI version maintains all the core functionality of the original console application while providing:
- Better user experience
- Visual progress representation
- Easier project management
- Modern interface design
- Cross-platform compatibility

## License

This project is open source and available under the MIT License. 