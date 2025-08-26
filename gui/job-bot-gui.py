#!/usr/bin/env python3
"""
Job Bot GUI - Professional Desktop Application
==============================================

Simple, clean GUI for job application content generation.
No command line needed - just click and paste!

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from pathlib import Path
import webbrowser

# Import our bot functionality
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    messagebox.showerror("Missing Dependencies", 
                        "Please install required packages:\npip install beautifulsoup4 requests")
    sys.exit(1)

# Import our existing bot logic
import json
import re
from datetime import datetime
from urllib.parse import urlparse

class JobBotGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.processing = False
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("Job Bot - Application Content Generator")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        # Set icon if available
        try:
            self.root.iconbitmap('job-bot.ico')  # Optional
        except:
            pass
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Job Bot", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Instant Job Application Content Generator",
                                  font=('Arial', 10))
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        author_label = ttk.Label(header_frame,
                                text="Built by Trey (Infrastructure → AI Engineer)",
                                font=('Arial', 9), foreground='gray')
        author_label.grid(row=2, column=0, sticky=tk.W)
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Step 1: Job Posting URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="Paste job URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 10))
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.generate_btn = ttk.Button(url_frame, text="Generate Application", 
                                      command=self.start_processing)
        self.generate_btn.grid(row=0, column=2)
        
        # Examples
        examples_frame = ttk.Frame(url_frame)
        examples_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(examples_frame, text="Examples:", font=('Arial', 8)).grid(row=0, column=0, sticky=tk.W)
        
        example_links = [
            ("Indeed", "https://www.indeed.com/viewjob?jk=example"),
            ("LinkedIn", "https://linkedin.com/jobs/view/example"),
            ("Company Site", "https://company.com/careers/job-id")
        ]
        
        for i, (name, url) in enumerate(example_links):
            btn = ttk.Button(examples_frame, text=name, 
                           command=lambda u=url: self.url_var.set(u),
                           style='Link.TButton')
            btn.grid(row=0, column=i+1, padx=(5, 0))
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar(value="Ready to generate application content...")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, pady=(5, 0))
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Generated Content", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Notebook for tabbed results
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cover Letter tab
        self.cover_letter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cover_letter_frame, text="Cover Letter")
        
        self.cover_letter_text = scrolledtext.ScrolledText(
            self.cover_letter_frame, 
            wrap=tk.WORD, 
            font=('Arial', 10),
            height=15
        )
        self.cover_letter_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Talking Points tab
        self.talking_points_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.talking_points_frame, text="Talking Points")
        
        self.talking_points_text = scrolledtext.ScrolledText(
            self.talking_points_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            height=15
        )
        self.talking_points_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Job Details tab
        self.job_details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.job_details_frame, text="Job Analysis")
        
        self.job_details_text = scrolledtext.ScrolledText(
            self.job_details_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            height=15
        )
        self.job_details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.save_btn = ttk.Button(button_frame, text="Save Files", 
                                  command=self.save_files, state='disabled')
        self.save_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.folder_btn = ttk.Button(button_frame, text="Open Folder", 
                                    command=self.open_folder, state='disabled')
        self.folder_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.copy_btn = ttk.Button(button_frame, text="Copy Cover Letter", 
                                  command=self.copy_cover_letter, state='disabled')
        self.copy_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Spacer
        button_frame.columnconfigure(3, weight=1)
        
        # Help and About buttons
        ttk.Button(button_frame, text="About", 
                  command=self.show_about).grid(row=0, column=4, padx=(10, 0))
        
        # Configure main grid weights
        main_frame.rowconfigure(3, weight=1)
        
        # Store results for saving
        self.current_results = None
        
    def start_processing(self):
        """Start processing in background thread"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a job posting URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            messagebox.showwarning("Invalid URL", "Please enter a valid URL starting with http:// or https://")
            return
        
        if self.processing:
            return
            
        # Start processing
        self.processing = True
        self.generate_btn.config(state='disabled')
        self.progress.start()
        
        # Run in background thread
        thread = threading.Thread(target=self.process_job, args=(url,))
        thread.daemon = True
        thread.start()
    
    def process_job(self, url):
        """Process job in background thread"""
        try:
            # Update status
            self.root.after(0, lambda: self.status_var.set("Reading job posting..."))
            
            # Scrape job
            job_data = self.scrape_job(url)
            
            self.root.after(0, lambda: self.status_var.set("Generating personalized content..."))
            
            # Generate content
            cover_letter = self.generate_cover_letter(job_data)
            talking_points = self.generate_talking_points(job_data)
            
            # Store results
            results = {
                'job_data': job_data,
                'cover_letter': cover_letter,
                'talking_points': talking_points
            }
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.display_results(results))
            
        except Exception as e:
            self.root.after(0, lambda: self.handle_error(str(e)))
    
    def scrape_job(self, url):
        """Scrape job posting - simplified version"""
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
        
        # Get description
        description = soup.get_text().lower()
        
        return {
            'title': title,
            'company': company,
            'description': description,
            'url': url
        }
    
    def generate_cover_letter(self, job_data):
        """Generate cover letter - same logic as CLI version"""
        description = job_data['description']
        
        # Memory Platform connections based on job type
        if 'automation' in description:
            memory_connection = "Like building the Memory Platform to automate family connection discovery, I focus on creating systems that solve real problems through intelligent automation."
        elif 'infrastructure' in description:
            memory_connection = "The Memory Platform requires solid infrastructure to handle family data securely - same foundation thinking I'd bring to your infrastructure challenges."
        elif 'data' in description:
            memory_connection = "Memory Platform processes family stories into meaningful insights - similar data transformation skills I'd apply to your business challenges."
        else:
            memory_connection = "My Memory Platform project demonstrates end-to-end thinking: from infrastructure through AI implementation - the comprehensive approach valuable for any technical role."
        
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
    
    def generate_talking_points(self, job_data):
        """Generate talking points for interviews"""
        points = f"""KEY TALKING POINTS FOR INTERVIEW:

Company: {job_data['company']}
Position: {job_data['title']}

1. INFRASTRUCTURE STABILITY
   - 99.8% uptime track record demonstrates reliability
   - Experience with Linux/Windows server management
   - Strong foundation in system monitoring and maintenance

2. AUTOMATION DEVELOPMENT
   - Built production GitHub integration bot (Python, APIs)
   - Content generation and automation systems
   - Practical experience with API development

3. AI TRANSITION JOURNEY
   - Actively building Memory Platform using machine learning
   - Data processing and analysis components
   - Shows commitment to staying current with technology

4. GROWTH MINDSET
   - Choosing to transition into AI shows adaptability
   - Learning new technologies while maintaining core strengths
   - Perfect fit for companies needing both stability and innovation

5. MEMORY PLATFORM CONNECTION
   - Demonstrates end-to-end thinking from infrastructure to AI
   - Real-world application of technical skills
   - Shows ability to build complete solutions

PORTFOLIO LINKS TO MENTION:
• Portfolio: https://tanarius.github.io
• GitHub: https://github.com/Tanarius  
• Recent Project: GitHub Development Logger Bot
• Current Project: Memory Platform (AI family connections)

QUESTIONS TO ASK THEM:
• What automation challenges is your infrastructure team facing?
• How is your company approaching AI integration?
• What opportunities exist for process improvement?
• How does this role contribute to the company's technical evolution?"""

        return points
    
    def display_results(self, results):
        """Display results in GUI"""
        self.current_results = results
        
        # Stop progress and update status
        self.progress.stop()
        self.status_var.set(f"Successfully generated content for {results['job_data']['company']}")
        
        # Enable buttons
        self.generate_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.folder_btn.config(state='normal')
        self.copy_btn.config(state='normal')
        
        # Clear and populate text areas
        self.cover_letter_text.delete(1.0, tk.END)
        self.cover_letter_text.insert(1.0, results['cover_letter'])
        
        self.talking_points_text.delete(1.0, tk.END)
        self.talking_points_text.insert(1.0, results['talking_points'])
        
        job_analysis = f"""JOB ANALYSIS SUMMARY

Company: {results['job_data']['company']}
Position: {results['job_data']['title']}
URL: {results['job_data']['url']}

CONTENT GENERATION APPROACH:
• Template selected based on job description keywords
• Memory Platform integration customized for role context
• Infrastructure + AI transition narrative maintained
• Professional portfolio links included

SKILL MATCHING HIGHLIGHTS:
• Infrastructure experience (99.8% uptime)
• Automation development (GitHub bot)
• AI learning trajectory (Memory Platform)
• Growth mindset demonstration

FILES THAT WILL BE CREATED:
• Professional cover letter (ready to customize)
• Complete talking points for interviews
• Full job data and analysis (JSON format)

MEMORY PLATFORM MENTIONS:
This application naturally mentions your Memory Platform project to:
1. Demonstrate AI/automation skills
2. Show real project experience
3. Explain your career transition story
4. Position you as innovative but grounded

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        self.job_details_text.delete(1.0, tk.END)
        self.job_details_text.insert(1.0, job_analysis)
        
        # Switch to cover letter tab
        self.notebook.select(0)
        
        self.processing = False
    
    def handle_error(self, error_msg):
        """Handle processing errors"""
        self.progress.stop()
        self.status_var.set("Error processing job posting")
        self.generate_btn.config(state='normal')
        self.processing = False
        
        messagebox.showerror("Processing Error", 
                           f"Could not process job posting:\n\n{error_msg}\n\nTry a different URL or check your internet connection.")
    
    def save_files(self):
        """Save files to Generated_Applications folder"""
        if not self.current_results:
            return
        
        try:
            # Create folder
            apps_folder = Path("Generated_Applications")
            apps_folder.mkdir(exist_ok=True)
            
            # Generate filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_clean = re.sub(r'[^\w\s-]', '', self.current_results['job_data']['company']).strip()
            company_clean = re.sub(r'[-\s]+', '_', company_clean)
            
            # Save cover letter
            cover_letter_file = apps_folder / f"application_{company_clean}_{timestamp}_cover_letter.txt"
            with open(cover_letter_file, 'w', encoding='utf-8') as f:
                f.write(self.current_results['cover_letter'])
            
            # Save talking points
            talking_points_file = apps_folder / f"application_{company_clean}_{timestamp}_talking_points.txt"
            with open(talking_points_file, 'w', encoding='utf-8') as f:
                f.write(self.current_results['talking_points'])
            
            # Save full data
            data_file = apps_folder / f"application_{company_clean}_{timestamp}_full_data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'job_data': self.current_results['job_data'],
                    'cover_letter': self.current_results['cover_letter'],
                    'talking_points': self.current_results['talking_points'],
                    'generated_at': datetime.now().isoformat()
                }, f, indent=2)
            
            messagebox.showinfo("Files Saved", 
                              f"Application content saved to Generated_Applications folder:\n\n"
                              f"• {cover_letter_file.name}\n"
                              f"• {talking_points_file.name}\n"
                              f"• {data_file.name}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save files: {e}")
    
    def open_folder(self):
        """Open the Generated_Applications folder"""
        try:
            folder_path = Path("Generated_Applications")
            folder_path.mkdir(exist_ok=True)
            
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{folder_path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def copy_cover_letter(self):
        """Copy cover letter to clipboard"""
        if not self.current_results:
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_results['cover_letter'])
        messagebox.showinfo("Copied", "Cover letter copied to clipboard!")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Job Bot - Application Content Generator

Version: 1.0
Author: Trey (Infrastructure Engineer → AI/Automation Specialist)

This tool generates personalized job application content by:
• Analyzing job postings from any website
• Creating tailored cover letters
• Generating interview talking points  
• Including Memory Platform project mentions

Triple-Duty Strategy:
✓ Speeds up your job applications
✓ Showcases automation/AI skills to employers
✓ Markets your Memory Platform project naturally

Portfolio: https://tanarius.github.io
GitHub: https://github.com/Tanarius

Built with Python, tkinter, BeautifulSoup, and requests."""

        messagebox.showinfo("About Job Bot", about_text)

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Configure ttk styles
    style = ttk.Style()
    style.configure('Link.TButton', font=('Arial', 8, 'underline'))
    
    app = JobBotGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.processing:
            if messagebox.askokcancel("Processing", "Job Bot is still processing. Close anyway?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()