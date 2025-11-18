import subprocess
import sys

def build_exe():
    # Build the executable
    subprocess.run([
        sys.executable, 
        "-m", "flet", "build", "windows",
        "--name", "MySelfUpdatingApp",
        "--product-name", "Self Updating Flet App",
        "--product-version", "1.0.0.0"
    ])

if __name__ == "__main__":
    build_exe()