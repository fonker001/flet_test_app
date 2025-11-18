import flet as ft
import os
import sys
import requests
import json
import subprocess
from pathlib import Path

def main(page: ft.Page):
    page.title = "Self-Updating Flet Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Version info (should match your GitHub release tag)
    current_version = "1.0.6"
    
    def check_for_updates(e):
        try:
            # Replace with your GitHub repo info
            repo_owner = "fonker001"
            repo_name = "flet_test_app"
            
            # Get latest release info from GitHub API
            api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name']
                
                if latest_version != current_version:
                    update_button.text = f"Update Available: {latest_version}"
                    update_button.bgcolor = ft.Colors.GREEN
                    update_button.disabled = False
                    page.snack_bar = ft.SnackBar(ft.Text(f"Update {latest_version} available!"))
                    page.snack_bar.open = True
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("You have the latest version!"))
                    page.snack_bar.open = True
                    
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Failed to check for updates"))
                page.snack_bar.open = True
                
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error checking updates: {ex}"))
            page.snack_bar.open = True
        
        page.update()

    def perform_update(e):
        try:
            update_button.text = "Updating..."
            update_button.disabled = True
            page.update()
            
            # Download and run updater script
            updater_url = "https://raw.githubusercontent.com/fonker001/flet_test_app/main/updater.py"
            updater_response = requests.get(updater_url)
            
            if updater_response.status_code == 200:
                # Save updater script
                with open("updater.py", "w") as f:
                    f.write(updater_response.text)
                
                # Run updater in a separate process
                subprocess.Popen([sys.executable, "updater.py"])
                page.window.close()  # Close current app
            else:
                raise Exception("Could not download updater")
                
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Update failed: {ex}"))
            page.snack_bar.open = True
            page.update()

    # UI Components
    version_text = ft.Text(f"Current Version: {current_version}", size=20)
    
    update_button = ft.ElevatedButton(
        text="Check for Updates",
        on_click=check_for_updates,
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE
    )
    
    page.add(
        ft.Column([
            ft.Icon(ft.Icons.UPDATE, size=50),
            version_text,
            ft.Text("This app can update itself from GitHub and anywhere in the world", size=16),
            update_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    # Auto-check for updates on app start
    check_for_updates(None)

if __name__ == "__main__":
    ft.app(target=main)