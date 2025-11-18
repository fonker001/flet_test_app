import requests
import os
import sys
import tempfile
import subprocess
import time

def main():
    print("Starting update process...")
    
    repo_owner = "fonker001"
    repo_name = "flet_test_app"
    
    try:
        # Get latest release info
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            release_data = response.json()
            
            # Find the EXE download URL
            download_url = None
            for asset in release_data.get('assets', []):
                if asset['name'].endswith('.exe'):
                    download_url = asset['browser_download_url']
                    break
            
            if download_url:
                print("Downloading new version...")
                
                # Download the new EXE
                exe_response = requests.get(download_url)
                if exe_response.status_code == 200:
                    # Save to temporary file
                    temp_dir = tempfile.gettempdir()
                    new_exe_path = os.path.join(temp_dir, "MyApp_updated.exe")
                    
                    with open(new_exe_path, 'wb') as f:
                        f.write(exe_response.content)
                    
                    print("Update downloaded! Preparing to restart...")
                    
                    # Get current executable path
                    current_exe = sys.executable
                    
                    # Create a batch file to replace the EXE
                    batch_content = f"""
@echo off
echo Updating application...
timeout /t 3 /nobreak >nul
taskkill /f /im "{os.path.basename(current_exe)}" 2>nul
del "{current_exe}" 2>nul
move "{new_exe_path}" "{current_exe}" 2>nul
echo Launching updated application...
start "" "{current_exe}"
del "%~f0"
"""
                    batch_path = os.path.join(temp_dir, "update_script.bat")
                    with open(batch_path, 'w') as f:
                        f.write(batch_content)
                    
                    # Run the batch file
                    subprocess.Popen([batch_path], shell=True)
                    sys.exit(0)
                else:
                    print("Failed to download update")
            else:
                print("No EXE found in release assets")
        else:
            print("Failed to get release info")
            
    except Exception as e:
        print(f"Update error: {e}")
    
    input("Press Enter to close...")

if __name__ == "__main__":
    main()