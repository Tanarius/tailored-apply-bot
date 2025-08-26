#!/usr/bin/env python3
"""
TailoredApply Bot - Interactive Version
======================================

User-friendly interactive job application content generator.
Just run and follow the prompts!

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import sys
from pathlib import Path

# Import our main bot functionality
import subprocess
import importlib.util

# Check if main bot file exists and import it
main_bot_file = Path(__file__).parent / "tailored-apply-bot.py"
if main_bot_file.exists():
    # Import the TailoredApplyBot class from the main file
    spec = importlib.util.spec_from_file_location("tailored_apply_bot", main_bot_file)
    tailored_apply_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tailored_apply_module)
    TailoredApplyBot = tailored_apply_module.TailoredApplyBot
else:
    print("Error: tailored-apply-bot.py not found in the same directory!")
    sys.exit(1)

def clear_screen():
    """Clear terminal screen for better UX"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print attractive header"""
    print("=" * 70)
    print("    TailoredApply Bot - Interactive Job Application Generator")
    print("=" * 70)
    print("Transform job postings into personalized application content!")
    print("Built by Trey - Infrastructure Engineer → AI/Automation Specialist")
    print("=" * 70)
    print()

def print_instructions():
    """Print usage instructions"""
    print("HOW IT WORKS:")
    print("1. Find any job posting online (Indeed, LinkedIn, company site)")
    print("2. Copy the URL from your browser")
    print("3. Paste it below and hit Enter")
    print("4. Get personalized cover letter + talking points!")
    print()
    print("EXAMPLES:")
    print("• https://jobs.careers.microsoft.com/job/12345")
    print("• https://www.indeed.com/viewjob?jk=abcdef")
    print("• https://company.com/careers/infrastructure-engineer")
    print()

def get_user_input():
    """Get job URL from user with validation"""
    while True:
        print("-" * 50)
        url = input("Paste job posting URL here: ").strip()
        
        if not url:
            print("Please enter a URL!")
            continue
            
        if not url.startswith(('http://', 'https://')):
            print("Please enter a valid URL (starting with http:// or https://)")
            continue
            
        return url

def display_results(result):
    """Display results in user-friendly format"""
    if not result:
        print("\nSorry, couldn't process that job posting.")
        print("Try a different URL or check your internet connection.")
        return
    
    job_data = result['job_data']
    analysis = result['analysis']
    
    print("\n" + "=" * 60)
    print("SUCCESS! Generated your application content:")
    print("=" * 60)
    
    print(f"JOB: {job_data['title']}")
    print(f"COMPANY: {job_data['company']}")
    print(f"FIT SCORE: {analysis['fit_score']}/10 match")
    print(f"TEMPLATE USED: {analysis['template_type'].replace('_', ' ').title()}")
    
    print("\n" + "-" * 40)
    print("COVER LETTER PREVIEW:")
    print("-" * 40)
    cover_letter = result['cover_letter']
    preview = cover_letter[:400] + "..." if len(cover_letter) > 400 else cover_letter
    print(preview)
    
    print("\n" + "-" * 40)
    print("KEY TALKING POINTS FOR INTERVIEWS:")
    print("-" * 40)
    for i, point in enumerate(analysis['talking_points'], 1):
        print(f"{i}. {point}")
    
    print("\n" + "-" * 40)
    print("MEMORY PLATFORM CONNECTION:")
    print("-" * 40)
    print(analysis['memory_platform_connection'])
    
    print("\n" + "-" * 40)
    print("FILES CREATED:")
    print("-" * 40)
    print(f"Cover Letter: {result['files']['cover_letter']}")
    print(f"Full Analysis: {result['files']['analysis']}")

def ask_continue():
    """Ask user if they want to process another job"""
    print("\n" + "=" * 60)
    while True:
        choice = input("Process another job posting? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no")

def print_tips():
    """Print helpful tips"""
    print("\nPRO TIPS:")
    print("• The bot works best with detailed job postings")
    print("• Generated content is customized but review before sending")
    print("• Each run creates new files so you won't lose previous work")
    print("• The Memory Platform mentions help explain your AI transition")
    print()

def main():
    """Interactive main loop"""
    try:
        # Initial setup
        clear_screen()
        print_header()
        print_instructions()
        print_tips()
        
        # Initialize bot
        print("Initializing TailoredApply Bot...")
        bot = TailoredApplyBot()
        print("Ready to generate application content!")
        
        # Main interaction loop
        while True:
            try:
                # Get URL from user
                url = get_user_input()
                
                print(f"\nProcessing: {url}")
                print("This may take 10-30 seconds depending on the website...")
                print()
                
                # Process the job
                result = bot.process_job_application(url)
                
                # Show results
                display_results(result)
                
                # Ask if they want to continue
                if not ask_continue():
                    break
                    
                # Clear screen for next iteration
                clear_screen()
                print_header()
                
            except KeyboardInterrupt:
                print("\n\nStopping TailoredApply Bot...")
                break
            except Exception as e:
                print(f"\nError processing job posting: {e}")
                print("Let's try another one!")
                continue
        
        # Goodbye message
        print("\n" + "=" * 60)
        print("Thanks for using TailoredApply Bot!")
        print("Good luck with your job applications!")
        print("Visit https://tanarius.github.io for more automation tools")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Make sure you have the required packages installed:")
        print("pip install beautifulsoup4 requests")

if __name__ == "__main__":
    main()