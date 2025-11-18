import requests
import os
import sys
import tempfile
import subprocess
import time

def main():
    print("=== UPDATER STARTED ===")
    
    repo_owner = "fonker001"
    repo_name = "flet_test_app"
    
    try:
        print("1. Getting latest release info from GitHub...")
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data['tag_name']
            print(f"2. Found release: {latest_version}")
            
            # Find the EXE download URL
            download_url = None
            for asset in release_data.get('assets', []):
                print(f"3. Checking asset: {asset['name']}")
                if asset['name'].endswith('.exe'):
                    download_url = asset['browser_download_url']
                    print(f"4. Found EXE download URL: {download_url}")
                    break
            
            if download_url:
                print("5. Downloading new version...")
                
                # Download the new EXE directly
                exe_response = requests.get(download_url)
                if exe_response.status_code == 200:
                    # Save to temporary file
                    temp_dir = tempfile.gettempdir()
                    new_exe_path = os.path.join(temp_dir, "MyApp_updated.exe")
                    
                    with open(new_exe_path, 'wb') as f:
                        f.write(exe_response.content)
                    
                    print(f"6. Update downloaded to: {new_exe_path}")
                    print("7. Preparing to replace current app...")
                    
                    # Get current executable path
                    current_exe = sys.executable
                    print(f"8. Current app: {current_exe}")
                    
                    # Create a simple batch script to handle the replacement
                    batch_content = f"""@echo off
echo ========================================
echo          UPDATING APPLICATION
echo ========================================
echo Waiting for current app to close...
timeout /t 2 /nobreak >nul

echo Replacing old version with new version...
del "{current_exe}" 2>nul
move "{new_exe_path}" "{current_exe}" 2>nul

if exist "{current_exe}" (
    echo Update successful!
    echo Starting new version...
    start "" "{current_exe}"
) else (
    echo Update failed - file not replaced
    pause
)

echo Cleaning up...
del "%~f0"
"""
                    batch_path = os.path.join(temp_dir, "update_myapp.bat")
                    with open(batch_path, 'w') as f:
                        f.write(batch_content)
                    
                    print("9. Launching update script...")
                    # Run the batch file and exit
                    subprocess.Popen([batch_path], shell=True)
                    print("10. Update process started. Closing current app.")
                    
                else:
                    print(f"Download failed with status: {exe_response.status_code}")
                    input("Press Enter to close...")
            else:
                print("No EXE file found in the release assets!")
                print("Make sure you uploaded MyApp.exe to the GitHub release")
                input("Press Enter to close...")
        else:
            print(f"Failed to get release info: {response.status_code}")
            input("Press Enter to close...")
            
    except Exception as e:
        print(f"Update error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")

if __name__ == "__main__":
    main()