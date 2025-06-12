#!/usr/bin/env python3
"""
Asana Project Progress Tracker - GUI Version

A modern GUI application that connects to the Asana API and displays progress bars
for all projects with a beautiful cross-platform interface.
"""

import os
import sys
import threading
import tkinter as tk
from typing import List, Dict, Any
import asana
import keyring
import getpass
import customtkinter as ctk
from PIL import Image, ImageTk
import json
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AsanaProgressTrackerGUI:
    def __init__(self):
        """
        Initialize the Asana progress tracker GUI.
        """
        self.root = ctk.CTk()
        self.root.title("Asana Project Progress Tracker")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize variables
        self.client = None
        self.projects_data = []
        self.current_workspace_filter = "All Workspaces"
        
        # Setup UI
        self.setup_ui()
        
        # Try to load API key and connect
        self.load_api_key()
        # Automatically refresh if API key is found and connected
        if self.client:
            self.refresh_data()
        else:
            self.show_settings()
    
    def setup_ui(self):
        """
        Setup the main UI components.
        """
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(self.root)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Asana Project Progress Tracker", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        
        # Connection status
        self.status_label = ctk.CTkLabel(
            header_frame, 
            text="Not connected", 
            font=ctk.CTkFont(size=14),
            text_color="red"
        )
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Controls frame
        controls_frame = ctk.CTkFrame(header_frame)
        controls_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="e")
        
        # Workspace filter
        ctk.CTkLabel(controls_frame, text="Workspace:").pack(side="left", padx=(0, 10))
        self.workspace_var = ctk.StringVar(value="All Workspaces")
        self.workspace_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["All Workspaces"],
            variable=self.workspace_var,
            command=self.filter_by_workspace
        )
        self.workspace_menu.pack(side="left", padx=(0, 20))
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            controls_frame,
            text="Refresh",
            command=self.refresh_data,
            width=100
        )
        self.refresh_button.pack(side="left", padx=(0, 10))
        
        # Settings button
        settings_button = ctk.CTkButton(
            controls_frame,
            text="Settings",
            command=self.show_settings,
            width=100
        )
        settings_button.pack(side="left")
        
        # Main content frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Summary frame
        self.summary_frame = ctk.CTkFrame(main_frame)
        self.summary_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)
        
        # Projects scrollable frame
        self.projects_frame = ctk.CTkScrollableFrame(main_frame)
        self.projects_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.projects_frame.grid_columnconfigure(0, weight=1)
        
        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.projects_frame,
            text="Click 'Refresh' to load your Asana projects",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.grid(row=0, column=0, padx=20, pady=50)
    
    def load_api_key(self):
        """
        Try to load API key from keychain and connect to Asana.
        """
        try:
            stored_key = keyring.get_password("asana_cli", "api_key")
            if stored_key:
                self.connect_to_asana(stored_key)
            else:
                self.status_label.configure(text="API key not found", text_color="orange")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
    
    def connect_to_asana(self, api_key: str):
        """
        Connect to Asana API.
        
        Args:
            api_key: Asana API key
        """
        try:
            self.client = asana.Client.access_token(api_key)
            # Test the connection
            self.client.users.me()
            self.status_label.configure(text="Connected to Asana", text_color="green")
            return True
        except Exception as e:
            self.status_label.configure(text=f"Connection failed: {str(e)}", text_color="red")
            return False
    
    def show_settings(self):
        """
        Show settings dialog for API key management.
        """
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (300 // 2)
        settings_window.geometry(f"500x300+{x}+{y}")
        
        # Settings content
        content_frame = ctk.CTkFrame(settings_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content_frame,
            text="API Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 30))
        
        # API Key section
        api_frame = ctk.CTkFrame(content_frame)
        api_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            api_frame,
            text="Asana API Key:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10))
        
        api_key_entry = ctk.CTkEntry(api_frame, width=400, show="*")
        api_key_entry.pack(pady=(0, 10))
        
        # Try to load current API key
        try:
            stored_key = keyring.get_password("asana_cli", "api_key")
            if stored_key:
                api_key_entry.insert(0, stored_key)
        except:
            pass
        
        # Buttons
        button_frame = ctk.CTkFrame(api_frame)
        button_frame.pack(pady=20)
        
        def save_api_key():
            api_key = api_key_entry.get().strip()
            if api_key:
                try:
                    keyring.set_password("asana_cli", "api_key", api_key)
                    if self.connect_to_asana(api_key):
                        self.status_label.configure(text="Connected to Asana", text_color="green")
                        settings_window.destroy()
                    else:
                        # Show error
                        pass
                except Exception as e:
                    # Show error
                    pass
        
        def clear_api_key():
            try:
                keyring.delete_password("asana_cli", "api_key")
                api_key_entry.delete(0, "end")
                self.client = None
                self.status_label.configure(text="API key cleared", text_color="orange")
            except Exception as e:
                pass
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_api_key,
            width=100
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=clear_api_key,
            width=100
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=settings_window.destroy,
            width=100
        ).pack(side="left", padx=10)
        
        # Help text
        help_text = """
To get your Asana API key:
1. Go to https://app.asana.com/0/developer-console
2. Create a new app or use an existing one
3. Copy your Personal Access Token
        """
        
        help_label = ctk.CTkLabel(
            content_frame,
            text=help_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        help_label.pack(pady=20)
    
    def refresh_data(self):
        """
        Refresh project data from Asana, showing a determinate loading progress bar with percentage.
        """
        if not self.client:
            self.show_settings()
            return

        # Clear current data
        self.clear_projects_display()

        # Show loading progress bar (determinate)
        self.loading_label.configure(text="Loading projects...")
        self.loading_label.grid(row=0, column=0, padx=20, pady=(50, 10))
        if hasattr(self, 'loading_progress'):
            self.loading_progress.destroy()
        self.loading_progress = ctk.CTkProgressBar(self.projects_frame, height=12, mode="determinate")
        self.loading_progress.grid(row=1, column=0, padx=0, pady=(0, 10))
        self.loading_progress.set(0)
        if hasattr(self, 'loading_percent_label'):
            self.loading_percent_label.destroy()
        self.loading_percent_label = ctk.CTkLabel(self.projects_frame, text="0%", font=ctk.CTkFont(size=14))
        self.loading_percent_label.grid(row=2, column=0, padx=20, pady=(0, 50))
        self.refresh_button.configure(state="disabled")

        # Run in background thread
        thread = threading.Thread(target=self._load_projects_thread_with_progress)
        thread.daemon = True
        thread.start()
    
    def _load_projects_thread_with_progress(self):
        """
        Load projects in background thread, updating progress bar with percentage.
        """
        try:
            # Get all projects
            projects = self.get_all_projects()
            total = len(projects)
            project_progress = []
            for idx, project in enumerate(projects):
                progress_info = self.get_project_progress(project)
                project_progress.append(progress_info)
                percent = (idx + 1) / total if total > 0 else 1
                self.root.after(0, lambda p=percent: self.loading_progress.set(p))
                self.root.after(0, lambda p=percent: self.loading_percent_label.configure(text=f"{int(p*100)}%"))
            # Update UI in main thread
            self.root.after(0, lambda: self.update_projects_display(project_progress))
            self.root.after(0, self._hide_loading_progress)
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error loading projects: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.refresh_button.configure(state="normal"))
    
    def _hide_loading_progress(self):
        if hasattr(self, 'loading_progress'):
            self.loading_progress.destroy()
        if hasattr(self, 'loading_percent_label'):
            self.loading_percent_label.destroy()
    
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Fetch all projects accessible to the user.
        
        Returns:
            List of project dictionaries
        """
        # Get all workspaces
        workspaces = self.client.workspaces.find_all()
        
        all_projects = []
        for workspace in workspaces:
            workspace_name = workspace.get('name', 'Unknown Workspace')
            
            # Get projects in this workspace
            projects = self.client.projects.find_all({
                'workspace': workspace['gid'],
                'opt_fields': 'name,completed,completed_at,owner,team,notes,color,created_at,due_date,start_on,archived'
            })
            
            for project in projects:
                project['workspace_name'] = workspace_name
                all_projects.append(project)
        
        return all_projects
    
    def get_project_progress(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate progress for a specific project based on completed tasks.
        
        Args:
            project: Project dictionary from Asana API
            
        Returns:
            Dictionary with progress information
        """
        try:
            project_gid = project['gid']
            project_name = project.get('name', 'Unnamed Project')
            
            # Get all tasks in the project
            tasks_generator = self.client.tasks.find_by_project(project_gid, {
                'opt_fields': 'completed,completed_at,name'
            })
            
            # Convert generator to list
            tasks = list(tasks_generator)
            
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task.get('completed', False))
            
            # Calculate percentage
            percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # Get project status
            try:
                statuses = self.client.project_statuses.find_by_project(project_gid, {
                    'opt_fields': 'text,color,created_at'
                })
                if statuses:
                    latest_status = max(statuses, key=lambda x: x.get('created_at', ''))
                    color = latest_status.get('color', None)
                    
                    if color == 'green':
                        status_text = 'On track'
                    elif color == 'blue':
                        status_text = 'On hold'
                    elif color == 'yellow':
                        status_text = 'At risk'
                    elif color == 'red':
                        status_text = 'Off track'
                    elif color == 'complete':
                        status_text = 'Completed'
                    else:
                        status_text = 'No status'
                else:
                    status_text = 'No status'
            except Exception:
                if project.get('completed', False):
                    status_text = 'Completed'
                elif project.get('archived', False):
                    status_text = 'Archived'
                else:
                    status_text = 'Active'
            
            return {
                'name': project_name,
                'workspace': project.get('workspace_name', 'Unknown'),
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'percentage': percentage,
                'completed': project.get('completed', False),
                'archived': project.get('archived', False),
                'status': status_text,
                'color': project.get('color', 'light-blue')
            }
            
        except Exception as e:
            return {
                'name': project.get('name', 'Unknown'),
                'workspace': project.get('workspace_name', 'Unknown'),
                'total_tasks': 0,
                'completed_tasks': 0,
                'percentage': 0,
                'completed': project.get('completed', False),
                'archived': project.get('archived', False),
                'status': 'Error',
                'color': 'red'
            }
    
    def update_projects_display(self, projects: List[Dict[str, Any]]):
        """
        Update the projects display with new data in a compact table layout.
        Args:
            projects: List of project progress dictionaries
        """
        self.projects_data = projects
        self.clear_projects_display()

        if not projects:
            self.loading_label.configure(text="No projects found")
            return

        # Update workspace filter options
        workspaces = list(set(p['workspace'] for p in projects))
        workspaces.insert(0, "All Workspaces")
        self.workspace_menu.configure(values=workspaces)

        # Update summary
        self.update_summary(projects)

        # Group projects by workspace
        workspace_groups = {}
        for project in projects:
            workspace_name = project['workspace']
            if workspace_name not in workspace_groups:
                workspace_groups[workspace_name] = []
            workspace_groups[workspace_name].append(project)

        row = 0
        for workspace_name, workspace_projects in workspace_groups.items():
            # Workspace header (aligned with table)
            workspace_frame = ctk.CTkFrame(self.projects_frame, fg_color="transparent")
            workspace_frame.grid(row=row, column=0, padx=20, pady=(20, 0), sticky="w")
            workspace_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                workspace_frame,
                text=f"Workspace: {workspace_name}",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w",
                width=630  # sum of all column widths + paddings
            ).grid(row=0, column=0, padx=0, pady=5, sticky="w")
            row += 1

            # Table header (no Workspace column, new order)
            table_header = ctk.CTkFrame(self.projects_frame, fg_color="transparent")
            table_header.grid(row=row, column=0, padx=20, pady=(0, 0), sticky="ew")
            table_header.grid_columnconfigure(1, weight=1)  # Make progress column expandable
            
            # Column definitions (widths must match data rows)
            col_defs = [240, 200, 90, 100]
            
            # Project Name
            ctk.CTkLabel(
                table_header,
                text="Project Name",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#bbbbbb",
                width=col_defs[0],
                anchor="w"
            ).grid(row=0, column=0, padx=2, pady=4, sticky="w")
            
            # Progress
            ctk.CTkLabel(
                table_header,
                text="Progress",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#bbbbbb",
                width=col_defs[1],
                anchor="w"
            ).grid(row=0, column=1, padx=2, pady=4, sticky="w")
            
            # Tasks
            ctk.CTkLabel(
                table_header,
                text="Tasks",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#bbbbbb",
                width=col_defs[2],
                anchor="e"
            ).grid(row=0, column=2, padx=(2, 18), pady=4, sticky="e")
            
            # Status
            ctk.CTkLabel(
                table_header,
                text="Status",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#bbbbbb",
                width=col_defs[3],
                anchor="w"
            ).grid(row=0, column=3, padx=2, pady=4, sticky="w")
            row += 1

            # Sort projects by percentage
            sorted_projects = sorted(workspace_projects, key=lambda x: x['percentage'], reverse=True)
            for idx, project in enumerate(sorted_projects):
                table_row = self.create_project_table_row(project, idx)
                table_row.grid(row=row, column=0, padx=20, pady=1, sticky="ew")
                row += 1

        self.loading_label.grid_remove()

    def create_project_table_row(self, project: Dict[str, Any], idx: int = 0) -> ctk.CTkFrame:
        """
        Create a compact table row for a project, with fixed column widths and optional alternating background.
        Args:
            project: Project data dictionary
            idx: Row index for alternating background
        Returns:
            CTkFrame containing the table row
        """
        # Use default gray background for rows
        bg_color = None  # Use default CTkFrame color
        row_frame = ctk.CTkFrame(self.projects_frame, fg_color=bg_color)
        row_frame.grid_columnconfigure(1, weight=1)

        # Column definitions (widths must match header)
        col_defs = [240, 200, 90, 100]
        # Project Name
        ctk.CTkLabel(
            row_frame,
            text=project['name'],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            width=col_defs[0]
        ).grid(row=0, column=0, padx=2, pady=4, sticky="w")

        # Progress (small bar + percent)
        progress_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=col_defs[1])
        progress_frame.grid_columnconfigure(0, weight=1)
        progress_bar = ctk.CTkProgressBar(progress_frame, height=10, width=100)
        progress_bar.set(project['percentage'] / 100)
        progress_bar.grid(row=0, column=0, padx=(0, 4), pady=0, sticky="ew")
        ctk.CTkLabel(
            progress_frame,
            text=f"{project['percentage']:.1f}%",
            font=ctk.CTkFont(family="Consolas", size=12),
            width=50,
            anchor="e"
        ).grid(row=0, column=1, padx=0, pady=0, sticky="e")
        progress_frame.grid(row=0, column=1, padx=2, pady=4, sticky="ew")

        # Tasks
        ctk.CTkLabel(
            row_frame,
            text=f"{project['completed_tasks']}/{project['total_tasks']}",
            font=ctk.CTkFont(family="Consolas", size=12),
            width=col_defs[2],
            anchor="e"
        ).grid(row=0, column=2, padx=(2, 18), pady=4, sticky="e")  # Extra right padding before status

        # Status
        status_color = self.get_status_color(project['status'])
        ctk.CTkLabel(
            row_frame,
            text=project['status'],
            font=ctk.CTkFont(size=12),
            text_color=status_color,
            anchor="w",
            width=col_defs[3]
        ).grid(row=0, column=3, padx=2, pady=4, sticky="w")

        return row_frame
    
    def get_status_color(self, status: str) -> str:
        """
        Get color for project status.
        
        Args:
            status: Project status text
            
        Returns:
            Color string
        """
        status_lower = status.lower()
        if status_lower == 'on track':
            return "#00ff00"  # Green
        elif status_lower == 'on hold':
            return "#0080ff"  # Blue
        elif status_lower == 'at risk':
            return "#ffff00"  # Yellow
        elif status_lower == 'off track':
            return "#ff0000"  # Red
        elif status_lower == 'completed':
            return "#00ff00"  # Green
        elif 'archived' in status_lower:
            return "#808080"  # Gray
        else:
            return "#ffffff"  # White
    
    def update_summary(self, projects: List[Dict[str, Any]]):
        """
        Update the summary display.
        
        Args:
            projects: List of project progress dictionaries
        """
        # Clear existing summary
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        total_projects = len(projects)
        completed_projects = sum(1 for p in projects if p['completed'])
        active_projects = sum(1 for p in projects if not p['completed'] and not p['archived'])
        archived_projects = sum(1 for p in projects if p['archived'])
        
        total_tasks = sum(p['total_tasks'] for p in projects)
        completed_tasks = sum(p['completed_tasks'] for p in projects)
        overall_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Summary grid
        summary_grid = ctk.CTkFrame(self.summary_frame)
        summary_grid.pack(fill="x", padx=20, pady=10)
        
        # Configure grid columns
        for i in range(4):
            summary_grid.grid_columnconfigure(i, weight=1)
        
        # Summary items
        summary_items = [
            ("Total Projects", str(total_projects), "#ffffff"),
            ("Active Projects", str(active_projects), "#00ff00"),
            ("Completed Projects", str(completed_projects), "#0080ff"),
            ("Archived Projects", str(archived_projects), "#808080"),
        ]
        
        for i, (label, value, color) in enumerate(summary_items):
            item_frame = ctk.CTkFrame(summary_grid)
            item_frame.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(pady=(8, 3))
            
            ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=color
            ).pack(pady=(0, 8))
        
        # Overall progress
        progress_frame = ctk.CTkFrame(self.summary_frame)
        progress_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            progress_frame,
            text="Overall Progress",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(12, 3))
        
        progress_bar = ctk.CTkProgressBar(progress_frame)
        progress_bar.pack(pady=(0, 8), padx=20, fill="x")
        progress_bar.set(overall_percentage / 100)
        
        ctk.CTkLabel(
            progress_frame,
            text=f"{completed_tasks}/{total_tasks} tasks completed ({overall_percentage:.1f}%)",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 12))
    
    def filter_by_workspace(self, workspace: str):
        """
        Filter projects by workspace.
        
        Args:
            workspace: Workspace name to filter by
        """
        self.current_workspace_filter = workspace
        self.update_projects_display(self.projects_data)
    
    def clear_projects_display(self):
        """
        Clear the projects display.
        """
        for widget in self.projects_frame.winfo_children():
            if widget != self.loading_label:
                widget.destroy()
    
    def show_error(self, message: str):
        """
        Show error message.
        
        Args:
            message: Error message to display
        """
        self.loading_label.configure(text=message)
        self.refresh_button.configure(state="normal")
    
    def run(self):
        """
        Start the GUI application.
        """
        self.root.mainloop()


def main():
    """
    Main function to run the Asana progress tracker GUI.
    """
    app = AsanaProgressTrackerGUI()
    app.run()


if __name__ == "__main__":
    main() 