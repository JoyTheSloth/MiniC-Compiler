#!/usr/bin/env python
import os
import urllib.request
import platform
import subprocess

def download_file(url, destination):
    """Download a file from URL to destination"""
    print(f"Downloading {destination} from {url}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"Successfully downloaded {destination}")
        return True
    except Exception as e:
        print(f"Error downloading {destination}: {e}")
        return False

def main():
    # Create directories if they don't exist
    os.makedirs("src/icg", exist_ok=True)
    
    # URLs for pre-generated files (these would be your GitHub URLs to the raw files)
    # For example: https://raw.githubusercontent.com/yourusername/MiniC-Compiler/main/src/icg/lex.yy.c
    # Replace these with actual URLs to your pre-generated files
    files = {
        "src/icg/lex.yy.c": "https://raw.githubusercontent.com/yourrepo/MiniC-Compiler/main/src/icg/lex.yy.c",
        "src/icg/minic.tab.c": "https://raw.githubusercontent.com/yourrepo/MiniC-Compiler/main/src/icg/minic.tab.c",
        "src/icg/minic.tab.h": "https://raw.githubusercontent.com/yourrepo/MiniC-Compiler/main/src/icg/minic.tab.h"
    }
    
    # If URLs are not available, create dummy files for testing
    if not os.path.exists("src/icg/lex.yy.c"):
        print("Warning: Creating dummy lex.yy.c file for testing purposes.")
        with open("src/icg/lex.yy.c", "w") as f:
            f.write("/* Dummy lex.yy.c file for testing */\n")
            f.write("#include <stdio.h>\n")
            f.write("/* This is just a placeholder. You need the actual generated file to compile properly. */\n")
    
    if not os.path.exists("src/icg/minic.tab.c"):
        print("Warning: Creating dummy minic.tab.c file for testing purposes.")
        with open("src/icg/minic.tab.c", "w") as f:
            f.write("/* Dummy minic.tab.c file for testing */\n")
            f.write("#include <stdio.h>\n")
            f.write("/* This is just a placeholder. You need the actual generated file to compile properly. */\n")
    
    if not os.path.exists("src/icg/minic.tab.h"):
        print("Warning: Creating dummy minic.tab.h file for testing purposes.")
        with open("src/icg/minic.tab.h", "w") as f:
            f.write("/* Dummy minic.tab.h file for testing */\n")
            f.write("#ifndef MINIC_TAB_H\n")
            f.write("#define MINIC_TAB_H\n")
            f.write("/* This is just a placeholder. You need the actual generated file to compile properly. */\n")
            f.write("#endif /* MINIC_TAB_H */\n")
    
    print("\nAttempting to run build_no_flex.bat...")
    if platform.system() == "Windows":
        subprocess.call(["build_no_flex.bat"])
    else:
        print("This script is designed for Windows. Please run build_no_flex.bat manually.")

if __name__ == "__main__":
    main() 