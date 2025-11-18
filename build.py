import os
import subprocess
import sys

def build_exe():
    # Method 1: Using flet command directly (if installed as CLI)
    try:
        subprocess.run([
            "flet", "build", "windows",
            "--name", "MySelfUpdatingApp",
            "--product-name", "Self Updating Flet App",
            "--product-version", "1.0.0.0",
            "--add-to-path", "false"
        ], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Method 2: Using python -m flet
        try:
            subprocess.run([
                sys.executable, "-m", "flet", "build", "windows",
                "--name", "MySelfUpdatingApp", 
                "--product-name", "Self Updating Flet App",
                "--product-version", "1.0.0.0",
                "--add-to-path", "false"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            # Method 3: Manual build using flet package
            manual_build()

def manual_build():
    """Alternative manual build method"""
    print("Attempting manual build...")
    try:
        import flet
        from flet.cli import main
        sys.argv = [
            "flet", "build", "windows",
            "--name", "MySelfUpdatingApp",
            "--product-name", "Self Updating Flet App", 
            "--product-version", "1.0.0.0"
        ]
        main()
    except Exception as e:
        print(f"Manual build also failed: {e}")
        print("\nTrying direct command...")

if __name__ == "__main__":
    build_exe()