# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import threading
import subprocess
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from smart_job_hunter_ai import SmartJobHunterAI
except ImportError as e:
    SmartJobHunterAI = None

class SimpleJobHunterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Find & Apply to Jobs")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        self.job_hunter = SmartJobHunterAI() if SmartJobHunterAI else None
        self.setup_styles()
        self.create_interface()
    
    def setup_styles(self):
        """Setup clean dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        colors = {
            'bg': '#1e1e1e', 'fg': '#ffffff', 'entry_bg': '#2d2d2d',
            'button_bg': '#238636', 'frame_bg': '#2d2d2d'
        }
        
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        style.configure('TButton', background=colors['button_bg'], foreground=colors['fg'], font=('Segoe UI', 10, 'bold'))
        style.configure('TEntry', fieldbackground=colors['entry_bg'], foreground=colors['fg'])
    
    def create_interface(self):
        """Create simple 3-step interface"""
        # Header
        header = tk.Label(self.root, text="🎯 Find & Apply to Jobs", 
                         font=('Segoe UI', 20, 'bold'), bg='#1e1e1e', fg='#ffffff')
        header.pack(pady=20)
        
        # Step 1: Job URL Input
        step1_frame = ttk.Frame(self.root)
        step1_frame.pack(fill='x', padx=40, pady=20)
        
        tk.Label(step1_frame, text="Step 1: Paste Job URL", 
                font=('Segoe UI', 14, 'bold'), bg='#1e1e1e', fg='#ffffff').pack(anchor='w')
        
        url_frame = ttk.Frame(step1_frame)
        url_frame.pack(fill='x', pady=(10, 0))
        
        self.url_entry = ttk.Entry(url_frame, font=('Segoe UI', 12))
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        analyze_btn = ttk.Button(url_frame, text="Analyze Job", command=self.analyze_job)
        analyze_btn.pack(side='right')
        
        # Step 2: Results (side by side)
        step2_frame = ttk.Frame(self.root)
        step2_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        tk.Label(step2_frame, text="Step 2: Review Analysis", 
                font=('Segoe UI', 14, 'bold'), bg='#1e1e1e', fg='#ffffff').pack(anchor='w')
        
        results_frame = ttk.Frame(step2_frame)
        results_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Left side - Job Info
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="Job Details", font=('Segoe UI', 12, 'bold'), 
                bg='#1e1e1e', fg='#ffffff').pack(anchor='w')
        self.job_info = scrolledtext.ScrolledText(left_frame, height=12, wrap='word', 
                                                 font=('Segoe UI', 10))
        self.job_info.pack(fill='both', expand=True, pady=(5, 0))
        
        # Right side - AI Analysis
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="AI Analysis & Fit Score", font=('Segoe UI', 12, 'bold'),
                bg='#1e1e1e', fg='#ffffff').pack(anchor='w')
        self.analysis_info = scrolledtext.ScrolledText(right_frame, height=12, wrap='word',
                                                      font=('Segoe UI', 10))
        self.analysis_info.pack(fill='both', expand=True, pady=(5, 0))
        
        # Step 3: Actions
        step3_frame = ttk.Frame(self.root)
        step3_frame.pack(fill='x', padx=40, pady=20)
        
        tk.Label(step3_frame, text="Step 3: Take Action", 
                font=('Segoe UI', 14, 'bold'), bg='#1e1e1e', fg='#ffffff').pack(anchor='w')
        
        actions_frame = ttk.Frame(step3_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(actions_frame, text="Generate Application", 
                  command=self.generate_application).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Practice Interview", 
                  command=self.practice_interview).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Find Learning Resources", 
                  command=self.find_learning).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Save Analysis", 
                  command=self.save_analysis).pack(side='left')
    
    def analyze_job(self):
        """Analyze job posting"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a job URL")
            return
        
        # Clear previous results
        self.job_info.delete(1.0, tk.END)
        self.analysis_info.delete(1.0, tk.END)
        
        # Show loading
        self.job_info.insert(tk.END, "Analyzing job posting...\n\nThis may take a moment.")
        self.analysis_info.insert(tk.END, "Running AI analysis...\n\nPlease wait.")
        
        def analyze():
            try:
                if not self.job_hunter:
                    # Demo mode - create mock analysis
                    self.root.after(0, self.show_demo_analysis, url)
                else:
                    analysis = self.job_hunter.analyze_job_opportunity(url)
                    if analysis:
                        self.root.after(0, self.display_results, analysis)
                    else:
                        self.root.after(0, self.show_error, "Could not analyze job")
            except Exception as e:
                self.root.after(0, self.show_error, f"Analysis failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def show_error(self, message):
        """Show error message safely"""
        messagebox.showerror("Error", message)
    
    def show_demo_analysis(self, url):
        """Show demo analysis for testing"""
        import random
        
        # Parse basic info from URL
        company = "Demo Company"
        job_title = "Software Engineer"
        
        if "linkedin" in url.lower():
            company = "LinkedIn Company"
        elif "indeed" in url.lower():
            company = "Indeed Company"
        elif "google" in url.lower():
            company = "Google"
            job_title = "Senior Software Engineer"
        
        # Mock job details
        job_details = f"""Job Title: {job_title}
Company: {company}
Location: San Francisco, CA
Salary: $120,000 - $180,000

Job Description:
We are looking for a talented software engineer to join our dynamic team. You will work on cutting-edge projects, collaborate with cross-functional teams, and help build scalable solutions that impact millions of users.

Required Skills:
Python, JavaScript, React, Node.js, AWS, Docker, Git

Key Requirements:
• 3+ years of software development experience
• Strong problem-solving and analytical skills
• Experience with cloud platforms (AWS/GCP/Azure)
• Knowledge of modern web frameworks
• Bachelor's degree in Computer Science or related field"""
        
        self.job_info.delete(1.0, tk.END)
        self.job_info.insert(1.0, job_details)
        
        # Mock AI analysis
        match_score = random.randint(75, 95)
        ai_analysis = f"""MATCH SCORE: {match_score}/100

SKILL ANALYSIS:
Strong match for required technical skills. Your Python and JavaScript experience aligns well with the role requirements. Consider strengthening AWS and Docker knowledge.

EXPERIENCE ALIGNMENT:
Your background shows good alignment with the seniority level. The role requires 3+ years experience which matches your profile well.

CULTURE FIT:
Company values innovation and collaboration, which aligns with your professional approach. The fast-paced startup environment suits your adaptability.

TOP RECOMMENDATIONS:
• Highlight your Python projects in your application
• Emphasize any cloud platform experience
• Mention specific JavaScript frameworks you've used
• Include examples of collaborative team projects
• Quantify your impact in previous roles

AREAS TO IMPROVE:
• Research the company's recent product launches
• Prepare examples of scalable solutions you've built
• Review AWS fundamentals for technical interviews"""
        
        self.analysis_info.delete(1.0, tk.END)
        self.analysis_info.insert(1.0, ai_analysis)
        
        messagebox.showinfo("Analysis Complete", f"Job analysis complete!\nMatch Score: {match_score}/100\n\n(Demo Mode - Mock Analysis)")
    
    def display_results(self, analysis):
        """Display analysis results"""
        # Store analysis for data passing to other tools
        self.current_analysis = analysis
        
        # Job details
        self.job_info.delete(1.0, tk.END)
        job_details = f"""🎯 JOB OVERVIEW
Job Title: {analysis.title}
Company: {analysis.company}
Location: {analysis.location}
Job Type: {analysis.job_type.title()}
Salary: {analysis.salary_range or 'Not specified'}
Industry: {analysis.industry.title()}
Company Size: {analysis.company_size.replace('_', ' ').title()}

📋 JOB DESCRIPTION:
{analysis.description}

🔧 REQUIRED SKILLS:
{chr(10).join([f"• {req}" for req in analysis.requirements[:10]])}

⭐ PREFERRED QUALIFICATIONS:
{chr(10).join([f"• {qual}" for qual in analysis.preferred_qualifications[:8]])}"""
        
        self.job_info.insert(1.0, job_details)
        
        # Enhanced AI analysis
        self.analysis_info.delete(1.0, tk.END)
        overall_score = int(analysis.overall_rating)
        
        # Get company intelligence data
        company_intel_text = self.get_company_intelligence(analysis)
        
        ai_analysis = f"""🎯 OVERALL RATING: {overall_score}/100

📊 DETAILED SCORES:
• Skill Match: {int(analysis.skill_match_score)}/100
• Culture Fit: {int(analysis.culture_fit_score)}/100  
• Growth Potential: {int(analysis.growth_potential_score)}/100
• Success Probability: {int(analysis.success_probability)}/100

{company_intel_text}

🚀 COMPETITIVE ADVANTAGES:
{chr(10).join([f"• {adv}" for adv in analysis.competitive_advantages]) if analysis.competitive_advantages else "• No specific advantages identified"}

📚 SKILL GAPS TO ADDRESS:
{chr(10).join([f"• {skill}" for skill in analysis.required_skills_missing]) if analysis.required_skills_missing else "• No critical skill gaps identified based on current profile"}

💡 APPLICATION STRATEGY:
{analysis.application_strategy}

⏰ TIMING & FOLLOW-UP:
• Optimal Timing: {analysis.optimal_timing.replace('_', ' ').title()}
• Follow-up Strategy: {analysis.follow_up_strategy}"""
        
        self.analysis_info.insert(1.0, ai_analysis)
        
        messagebox.showinfo("Analysis Complete", f"Job analysis complete!\nOverall Rating: {overall_score}/100")
    
    def get_company_intelligence(self, analysis):
        """Get company intelligence information"""
        # Try to get more detailed company info from the AI system
        try:
            company_info = f"""🏢 COMPANY INTELLIGENCE:
• Industry: {analysis.industry.title()}
• Company Size: {analysis.company_size.replace('_', ' ').title()}
• Work Environment: {analysis.job_type.title()} position
• Growth Stage: Established (based on job posting analysis)"""
            
            # Add culture insights if available
            if hasattr(analysis, 'culture_insights'):
                company_info += f"\n• Culture Insights: {analysis.culture_insights}"
                
            return company_info
        except:
            return """🏢 COMPANY INTELLIGENCE:
• Basic company information extracted from job posting
• Full company analysis available in advanced mode"""
    
    def generate_application(self):
        """Generate application materials"""
        try:
            # Try to launch AI Commander
            import subprocess
            subprocess.Popen([
                'python', 
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gui', 'ai_commander_gui.py')
            ])
            messagebox.showinfo("Launching", "AI Commander launched for application generation!")
        except Exception as e:
            messagebox.showinfo("Generate Application", 
                               "Application generation ready!\n\n" +
                               "This will create:\n" +
                               "• Tailored cover letter\n" +
                               "• Optimized resume\n" +
                               "• Key talking points\n\n" +
                               "(Launch AI Commander manually if needed)")
    
    def practice_interview(self):
        """Launch interview practice with job data"""
        try:
            # Check if we have analysis data to pass
            if hasattr(self, 'current_analysis') and self.current_analysis:
                # Create a data file to pass job info to interview prep
                import tempfile
                import json
                
                job_data = {
                    'company': self.current_analysis.company,
                    'job_title': self.current_analysis.title,
                    'location': self.current_analysis.location,
                    'industry': self.current_analysis.industry,
                    'job_type': self.current_analysis.job_type,
                    'requirements': self.current_analysis.requirements,
                    'description': self.current_analysis.description,
                    'skill_gaps': self.current_analysis.required_skills_missing,
                    'competitive_advantages': self.current_analysis.competitive_advantages
                }
                
                # Save to temp file
                temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                data_file = os.path.join(temp_dir, 'current_job_analysis.json')
                
                with open(data_file, 'w') as f:
                    json.dump(job_data, f, indent=2)
                
                # Launch interview prep
                interview_gui_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    '07-INTERVIEW-PREP-AI', 'gui', 'simple-interview-gui.py'
                )
                subprocess.Popen(['python', interview_gui_path])
                messagebox.showinfo("Launching Interview Practice", 
                                   f"Interview Practice launched with job data!\n\n" +
                                   f"Company: {self.current_analysis.company}\n" +
                                   f"Role: {self.current_analysis.title}\n\n" +
                                   "Job-specific questions will be generated automatically.")
            else:
                # Launch without data
                interview_gui_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    '07-INTERVIEW-PREP-AI', 'gui', 'simple-interview-gui.py'
                )
                subprocess.Popen(['python', interview_gui_path])
                messagebox.showinfo("Launching", "Interview Practice launched!\n\n(Analyze a job first to get custom questions)")
                
        except Exception as e:
            messagebox.showinfo("Practice Interview", 
                               "Interview practice ready!\n\n" +
                               "This includes:\n" +
                               "• Job-specific questions\n" +
                               "• AI mock interview\n" +
                               "• Real-time feedback\n\n" +
                               f"(Launch Interview Practice manually if needed - Error: {e})")
    
    def find_learning(self):
        """Find learning resources"""
        try:
            # Try to launch Learning Coach
            learning_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                '06-LEARNING-COACH', 'gui', 'learning_coach_gui.py'
            )
            subprocess.Popen(['python', learning_path])
            messagebox.showinfo("Launching", "Learning Coach launched!")
        except Exception as e:
            messagebox.showinfo("Find Learning", 
                               "Learning resources ready!\n\n" +
                               "This provides:\n" +
                               "• Skill gap analysis\n" +
                               "• Learning roadmap\n" +
                               "• Resource recommendations\n\n" +
                               "(Launch Learning Coach manually if needed)")
    
    def save_analysis(self):
        """Save analysis results"""
        try:
            # Create saves directory
            saves_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saves')
            os.makedirs(saves_dir, exist_ok=True)
            
            # Get current analysis
            job_content = self.job_info.get(1.0, tk.END).strip()
            analysis_content = self.analysis_info.get(1.0, tk.END).strip()
            
            if job_content and analysis_content and "Job Title:" in job_content:
                # Generate filename from timestamp
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"job_analysis_{timestamp}.txt"
                filepath = os.path.join(saves_dir, filename)
                
                # Save analysis
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("=== JOB ANALYSIS REPORT ===\n\n")
                    f.write("JOB DETAILS:\n")
                    f.write(job_content)
                    f.write("\n\n" + "="*50 + "\n\n")
                    f.write("AI ANALYSIS:\n")
                    f.write(analysis_content)
                    f.write(f"\n\n--- Saved on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')} ---")
                
                messagebox.showinfo("Saved", f"Job analysis saved!\n\nLocation: {filepath}")
            else:
                messagebox.showwarning("Nothing to Save", "Please analyze a job first before saving.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save analysis: {str(e)}")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    app = SimpleJobHunterGUI()
    app.run()

if __name__ == "__main__":
    main()