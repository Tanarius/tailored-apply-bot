#!/usr/bin/env python3
"""
Job Bot Launcher - Windows-Friendly Version
===========================================

Double-click this file to start the Job Bot!
Handles errors gracefully and keeps window open.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import requests
        import bs4
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required packages"""
    print("Installing required packages...")
    print("This may take a moment...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4", "requests"], 
                      capture_output=True, check=True)
        print("✓ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        return False

def main():
    print("=" * 60)
    print("    JOB BOT LAUNCHER")
    print("=" * 60)
    print("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("✗ Python 3.6 or higher required")
        input("Press Enter to close...")
        return
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check dependencies
    if not check_dependencies():
        print("✗ Required packages not found")
        print("\nWould you like to install them now?")
        choice = input("Install packages? (y/n): ").strip().lower()
        
        if choice in ['y', 'yes']:
            if not install_dependencies():
                print("\nInstallation failed. Please run manually:")
                print("pip install beautifulsoup4 requests")
                input("Press Enter to close...")
                return
        else:
            print("Cannot proceed without required packages.")
            input("Press Enter to close...")
            return
    
    print("✓ All requirements satisfied")
    print("\nStarting Job Bot...")
    print("=" * 60)
    
    # Start the main bot
    try:
        # Run the bot script directly
        result = subprocess.run([sys.executable, "job-bot.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode != 0:
            print("✗ Job Bot encountered an error")
    except FileNotFoundError:
        print("✗ job-bot.py not found in current directory")
        input("Press Enter to close...")
    except Exception as e:
        print(f"✗ Error starting Job Bot: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nJob Bot launcher stopped by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        input("Press Enter to close...")