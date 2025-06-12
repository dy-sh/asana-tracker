#!/usr/bin/env python3
"""
Launcher script for Asana Project Progress Tracker GUI
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from asana_progress_gui import main
    main()
except ImportError as e:
    print(f"Error: {e}")
    print("Please install the required dependencies:")
    print("pip install -r requirements_gui.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error running the application: {e}")
    sys.exit(1) 