import os
import requests
import zipfile
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    print("Starting update process...")
    
    repo_owner = "fonker001"
    repo_name = "flet_test_app"
    
    try:
        # Get latest release download URL
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            release_data = response.json()
            
            # Look for source code zipball
            zip_url = release_data['zipball_url']
            
            # Download the source code
            print("Downloading update...")
            zip_response = requests.get(zip_url)
            
            if zip_response.status_code == 200:
                # Save zip file
                zip_path = "update.zip"
                with open(zip_path, "wb") as f:
                    f.write(zip_response.content)
                
                # Extract and update files
                print("Extracting update...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall("temp_update")
                
                # Find the extracted folder
                extract_dir = Path("temp_update")
                subdirs = list(extract_dir.iterdir())
                if subdirs:
                    source_dir = subdirs[0]
                    
                    # Copy files to current directory (except updater itself)
                    for item in source_dir.iterdir():
                        if item.name != "updater.py":
                            if item.is_dir():
                                if Path(item.name).exists():
                                    shutil.rmtree(item.name)
                                shutil.copytree(item, item.name)
                            else:
                                shutil.copy2(item, item.name)
                
                # Cleanup
                shutil.rmtree("temp_update")
                os.remove("zip_path")
                
                # Restart the application
                print("Update complete! Restarting...")
                subprocess.Popen([sys.executable, "main.py"])
                
            else:
                print("Failed to download update")
        else:
            print("Failed to get release info")
            
    except Exception as e:
        print(f"Update error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()