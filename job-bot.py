#!/usr/bin/env python3
"""
Job Bot - Super Simple Job Application Generator
===============================================

Just run this file and follow the prompts!
Double-click or type: python job-bot.py

No command line arguments needed - totally interactive!
"""

import os
import sys
import json
import re
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# Required imports
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system("pip install beautifulsoup4 requests")
    import requests
    from bs4 import BeautifulSoup

def clear_screen():
    """Clear screen for better UX"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Welcome message"""
    print("=" * 65)
    print("  JOB BOT - Instant Job Application Content Generator")  
    print("=" * 65)
    print("Paste any job URL -> Get personalized cover letter!")
    print("Built by Trey (Infrastructure -> AI Engineer)")
    print("Every letter mentions your Memory Platform project")
    print("=" * 65)
    print()

def get_job_url():
    """Get job URL from user"""
    print("STEP 1: Find a job posting online")
    print("STEP 2: Copy the URL from your browser") 
    print("STEP 3: Paste it below")
    print()
    
    while True:
        url = input("Paste job URL here: ").strip()
        
        if not url:
            print("Please paste a URL!")
            continue
            
        if not url.startswith(('http://', 'https://')):
            print("Please enter a valid URL (starting with http/https)")
            continue
            
        return url

def scrape_job(url):
    """Simple job scraping"""
    try:
        print("Reading job posting...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic info
        title = "Job Position"
        company = "Company"
        
        # Try to find title
        title_selectors = ['h1', '[data-testid="jobTitle"]', '.job-title', '.jobsearch-JobInfoHeader-title']
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                title = element.get_text().strip()
                break
        
        # Try to find company
        company_selectors = ['.company-name', '[data-testid="companyName"]', '.jobsearch-InlineCompanyRating']
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                company = element.get_text().strip()
                break
        
        # Get description for keyword matching
        description = soup.get_text().lower()
        
        return {
            'title': title,
            'company': company,
            'description': description,
            'url': url
        }
        
    except Exception as e:
        print(f"Warning: Couldn't fully read job posting: {e}")
        return {
            'title': 'Job Position', 
            'company': 'Target Company',
            'description': '',
            'url': url
        }

def generate_cover_letter(job_data):
    """Generate personalized cover letter"""
    
    description = job_data['description']
    
    # Detect job type based on keywords
    if any(word in description for word in ['infrastructure', 'server', 'network', 'uptime']):
        template = "infrastructure"
    elif any(word in description for word in ['automation', 'python', 'script', 'devops']):
        template = "automation"
    else:
        template = "general"
    
    # Memory Platform connections based on job type
    if 'automation' in description:
        memory_connection = "Like building the Memory Platform to automate family connection discovery, I focus on creating systems that solve real problems through intelligent automation."
    elif 'infrastructure' in description:
        memory_connection = "The Memory Platform requires solid infrastructure to handle family data securely - same foundation thinking I'd bring to your infrastructure challenges."
    elif 'data' in description:
        memory_connection = "Memory Platform processes family stories into meaningful insights - similar data transformation skills I'd apply to your business challenges."
    else:
        memory_connection = "My Memory Platform project demonstrates end-to-end thinking: from infrastructure through AI implementation - the comprehensive approach valuable for any technical role."
    
    # Generate cover letter
    cover_letter = f"""Dear Hiring Manager,

As an Infrastructure Engineer with 3+ years maintaining 99.8% uptime, I'm excited to apply for the {job_data['title']} position at {job_data['company']}.

My background uniquely positions me for this role:

• Infrastructure Foundation: Linux/Windows server management with focus on reliability and monitoring
• Automation Growth: Python development including GitHub API integration and content generation systems  
• Current Learning: Building Memory Platform - AI-powered family connection app with data analysis components

{memory_connection}

Recent accomplishments that demonstrate my Infrastructure → AI transition:
• GitHub Development Logger Bot (Python, APIs, content automation)
• Memory Platform development (AI, data processing, user experience)
• Infrastructure monitoring with 99.8% uptime achievement

Like my current project building the Memory Platform (an AI-powered family connection app), I approach challenges by combining solid infrastructure knowledge with innovative automation solutions.

I'd welcome the opportunity to discuss how my infrastructure expertise and growing automation skills can contribute to {job_data['company']}'s success.

Best regards,
Trey

Portfolio: https://tanarius.github.io
GitHub: https://github.com/Tanarius
Memory Platform: AI-powered family connections through technology"""

    return cover_letter

def save_files(job_data, cover_letter):
    """Save generated content"""
    # Create applications folder if it doesn't exist
    apps_folder = Path("Generated_Applications")
    apps_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_clean = re.sub(r'[^\w\s-]', '', job_data['company']).strip()
    company_clean = re.sub(r'[-\s]+', '_', company_clean)
    
    # Save cover letter in the applications folder
    cover_letter_file = apps_folder / f"application_{company_clean}_{timestamp}_cover_letter.txt"
    with open(cover_letter_file, 'w', encoding='utf-8') as f:
        f.write(cover_letter)
    
    # Save job data
    analysis_file = apps_folder / f"application_{company_clean}_{timestamp}_job_data.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        output_data = {
            'job_data': job_data,
            'cover_letter': cover_letter,
            'generated_at': datetime.now().isoformat(),
            'talking_points': [
                "Infrastructure stability: 99.8% uptime demonstrates reliability you need for critical systems",
                "Automation development: Built production GitHub integration bot, showing practical API skills", 
                "AI transition: Actively building Memory Platform using machine learning for data insights",
                f"Growth mindset: Choosing to transition into AI shows commitment to staying current - exactly what {job_data['company']} needs"
            ]
        }
        json.dump(output_data, f, indent=2)
    
    return str(cover_letter_file), str(analysis_file)

def display_results(job_data, cover_letter, files):
    """Show results to user"""
    print("\n" + "=" * 60)
    print("SUCCESS! Your application content is ready!")
    print("=" * 60)
    
    print(f"JOB: {job_data['title']}")
    print(f"COMPANY: {job_data['company']}")
    print()
    
    print("COVER LETTER PREVIEW:")
    print("-" * 40)
    preview = cover_letter[:300] + "..." if len(cover_letter) > 300 else cover_letter
    print(preview)
    print("-" * 40)
    
    print("\nFILES CREATED:")
    print(f"Cover Letter: {files[0]}")
    print(f"Full Data: {files[1]}")
    
    print("\nKEY TALKING POINTS:")
    print("1. Infrastructure stability: 99.8% uptime track record")
    print("2. Automation skills: GitHub bot development")
    print("3. AI transition: Memory Platform project")
    print("4. Growth mindset: Learning new technologies")
    
    print("\nMEMORY PLATFORM MENTION:")
    print("Every cover letter naturally mentions your AI project!")
    
    # Ask if they want to open the folder
    print(f"\nFiles saved to: Generated_Applications folder")
    choice = input("Open folder to see your files? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        try:
            import subprocess
            subprocess.run(['explorer', 'Generated_Applications'], check=True)
        except:
            print("Could not open folder automatically")

def ask_another():
    """Ask if user wants to process another job"""
    print("\n" + "=" * 60)
    while True:
        choice = input("Process another job posting? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def main():
    """Main interactive loop"""
    try:
        while True:
            clear_screen()
            print_welcome()
            
            # Get job URL
            url = get_job_url()
            
            print()
            # Process job
            job_data = scrape_job(url)
            
            print("Generating personalized cover letter...")
            cover_letter = generate_cover_letter(job_data)
            
            print("Saving files...")
            files = save_files(job_data, cover_letter)
            
            # Show results
            display_results(job_data, cover_letter, files)
            
            # Ask for another
            if not ask_another():
                break
        
        print("\nThanks for using Job Bot!")
        print("Good luck with your applications!")
        print("Visit: https://tanarius.github.io")
        
    except KeyboardInterrupt:
        print("\n\nThanks for using Job Bot!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Try running: pip install beautifulsoup4 requests")
    
    # Keep window open on Windows
    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()