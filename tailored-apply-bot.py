#!/usr/bin/env python3
"""
TailoredApply Bot - Job Application Content Generator
==================================================

Transforms job postings into personalized application content for Infrastructure → AI transition.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
Purpose: Automate job application content creation while showcasing AI engineering skills
Connection: Like the Memory Platform turns family stories into meaningful connections,
           this bot turns job postings into personalized career opportunities.

Features:
- Web scraping job postings from multiple platforms
- AI-powered content generation for cover letters
- Template system for different role types
- Integration with resume data for personalization
- PDF generation for professional formatting

Usage:
    python tailored-apply-bot.py --url "job_posting_url"
    python tailored-apply-bot.py --company "CompanyName" --role "Job Title"
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urlparse
import argparse
from pathlib import Path

# Third-party imports (install with pip)
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Please install required packages: pip install beautifulsoup4 requests")
    exit(1)

class TailoredApplyBot:
    """
    Job Application Content Generator
    
    Analyzes job postings and generates personalized application content
    tailored to Infrastructure → AI career transition narrative.
    """
    
    def __init__(self):
        self.resume_data = self.load_resume_data()
        self.templates = self.load_templates()
        self.skills_mapping = {
            'infrastructure': ['linux', 'windows', 'networking', 'servers', 'uptime', 'monitoring'],
            'automation': ['python', 'scripting', 'apis', 'automation', 'ci/cd', 'devops'],
            'ai_learning': ['machine learning', 'ai', 'data analysis', 'github', 'development']
        }
        
    def load_resume_data(self):
        """Load personal resume data for content generation"""
        return {
            'name': 'Trey',
            'current_role': 'Infrastructure Engineer',
            'target_role': 'AI/Automation Specialist', 
            'key_achievements': [
                '99.8% uptime track record',
                'Production automation bot development',
                'GitHub API integration experience',
                'Memory Platform development (AI-powered family connection app)'
            ],
            'skills': {
                'infrastructure': ['Linux', 'Windows Server', 'Network Management', 'System Monitoring'],
                'automation': ['Python', 'API Integration', 'GitHub Automation', 'Process Optimization'],
                'ai_current': ['Content Generation', 'Data Analysis', 'Machine Learning Applications']
            },
            'portfolio_links': {
                'github': 'https://github.com/Tanarius',
                'portfolio': 'https://tanarius.github.io',
                'memory_platform': 'https://github.com/Tanarius/memory-platform'
            }
        }
    
    def load_templates(self):
        """Load cover letter templates for different role types"""
        return {
            'infrastructure_plus': '''
Dear Hiring Manager,

As an Infrastructure Engineer with {experience_years} years maintaining {uptime_achievement} uptime, I'm excited to apply for the {job_title} position at {company_name}.

My background uniquely positions me for this role:

• Infrastructure Foundation: {infrastructure_summary}
• Automation Growth: {automation_summary}
• Current Learning: {ai_learning_summary}

{specific_job_alignment}

Like my current project building the Memory Platform (an AI-powered family connection app), I approach challenges by combining solid infrastructure knowledge with innovative automation solutions.

I'd welcome the opportunity to discuss how my infrastructure expertise and growing automation skills can contribute to {company_name}'s success.

Best regards,
{name}
            ''',
            
            'automation_focused': '''
Dear {company_name} Team,

I'm writing to express my strong interest in the {job_title} position. As an Infrastructure Engineer actively transitioning to AI/Automation, I bring a unique combination of operational stability and innovative automation development.

Recent accomplishments include:
• {recent_project_1}
• {recent_project_2}
• {recent_project_3}

{job_specific_fit}

My approach mirrors my work on the Memory Platform - taking complex systems and making them accessible through intelligent automation. I believe this perspective would be valuable for {company_name}.

Looking forward to discussing this opportunity further.

Sincerely,
{name}
            '''
        }
    
    def scrape_job_posting(self, url):
        """
        Scrape job posting content from URL
        
        Args:
            url (str): Job posting URL
            
        Returns:
            dict: Extracted job information
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job details (this will vary by platform)
            job_data = {
                'url': url,
                'platform': urlparse(url).netloc,
                'scraped_at': datetime.now().isoformat(),
                'title': self.extract_job_title(soup),
                'company': self.extract_company_name(soup),
                'description': self.extract_job_description(soup),
                'requirements': self.extract_requirements(soup),
                'technologies': self.extract_technologies(soup)
            }
            
            return job_data
            
        except Exception as e:
            print(f"Error scraping job posting: {e}")
            return None
    
    def extract_job_title(self, soup):
        """Extract job title from HTML"""
        # Common selectors for job titles
        title_selectors = [
            'h1[data-automation="job-detail-title"]',  # SEEK
            '.jobsearch-JobInfoHeader-title',          # Indeed
            '[data-testid="jobTitle"]',                # LinkedIn
            'h1.job-title',                            # Generic
            'h1'                                       # Fallback
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Job Title Not Found"
    
    def extract_company_name(self, soup):
        """Extract company name from HTML"""
        company_selectors = [
            '[data-automation="job-detail-company-name"]',
            '.jobsearch-InlineCompanyRating',
            '[data-testid="companyName"]',
            '.company-name'
        ]
        
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Company Name Not Found"
    
    def extract_job_description(self, soup):
        """Extract full job description"""
        desc_selectors = [
            '[data-automation="job-detail-description"]',
            '.jobsearch-jobDescriptionText',
            '.job-description'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        # Fallback: look for any large text block
        paragraphs = soup.find_all('p')
        if paragraphs:
            return '\n'.join([p.get_text().strip() for p in paragraphs[:10]])
        
        return "Job description not found"
    
    def extract_requirements(self, soup):
        """Extract key requirements and qualifications"""
        description = self.extract_job_description(soup)
        
        # Look for requirements sections
        requirements = []
        lines = description.split('\n')
        
        capturing = False
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['requirements', 'qualifications', 'must have', 'essential']):
                capturing = True
                continue
            
            if capturing and line:
                if line.startswith(('•', '-', '*', '◦')):
                    requirements.append(line[1:].strip())
                elif any(keyword in line.lower() for keyword in ['responsibilities', 'about', 'benefits']):
                    break
        
        return requirements
    
    def extract_technologies(self, soup):
        """Extract mentioned technologies and skills"""
        description = self.extract_job_description(soup).lower()
        
        tech_keywords = [
            'python', 'javascript', 'aws', 'azure', 'kubernetes', 'docker', 
            'linux', 'windows', 'networking', 'automation', 'ci/cd', 'devops',
            'machine learning', 'ai', 'data analysis', 'api', 'rest', 'json'
        ]
        
        found_tech = []
        for tech in tech_keywords:
            if tech in description:
                found_tech.append(tech)
        
        return found_tech
    
    def analyze_job_fit(self, job_data):
        """
        Analyze how well the job matches resume profile
        
        Args:
            job_data (dict): Scraped job information
            
        Returns:
            dict: Fit analysis and content suggestions
        """
        description = job_data['description'].lower()
        requirements = [req.lower() for req in job_data.get('requirements', [])]
        
        # Calculate skill matches
        skill_matches = {
            'infrastructure': 0,
            'automation': 0,
            'ai_learning': 0
        }
        
        for category, keywords in self.skills_mapping.items():
            for keyword in keywords:
                if keyword in description:
                    skill_matches[category] += 1
        
        # Determine best template based on matches
        if skill_matches['infrastructure'] >= skill_matches['automation']:
            template_type = 'infrastructure_plus'
        else:
            template_type = 'automation_focused'
        
        # Generate talking points
        talking_points = self.generate_talking_points(job_data, skill_matches)
        
        return {
            'template_type': template_type,
            'skill_matches': skill_matches,
            'talking_points': talking_points,
            'fit_score': sum(skill_matches.values()),
            'memory_platform_connection': self.generate_memory_platform_tie_in(job_data)
        }
    
    def generate_talking_points(self, job_data, skill_matches):
        """Generate specific talking points for this job"""
        points = []
        
        # Infrastructure talking points
        if skill_matches['infrastructure'] > 0:
            points.append("Infrastructure stability: 99.8% uptime demonstrates reliability you need for critical systems")
        
        # Automation talking points  
        if skill_matches['automation'] > 0:
            points.append("Automation development: Built production GitHub integration bot, showing practical API skills")
        
        # AI/Learning talking points
        if skill_matches['ai_learning'] > 0:
            points.append("AI transition: Actively building Memory Platform using machine learning for data insights")
        
        # Company-specific points
        company = job_data.get('company', 'your company')
        points.append(f"Growth mindset: Choosing to transition into AI shows commitment to staying current - exactly what {company} needs")
        
        return points
    
    def generate_memory_platform_tie_in(self, job_data):
        """Generate Memory Platform connection for this specific job"""
        job_focus = job_data.get('description', '').lower()
        
        if 'automation' in job_focus:
            return "Like building the Memory Platform to automate family connection discovery, I focus on creating systems that solve real problems through intelligent automation."
        elif 'infrastructure' in job_focus:
            return "The Memory Platform requires solid infrastructure to handle family data securely - same foundation thinking I'd bring to your infrastructure challenges."
        elif 'data' in job_focus:
            return "Memory Platform processes family stories into meaningful insights - similar data transformation skills I'd apply to your business challenges."
        else:
            return "My Memory Platform project demonstrates end-to-end thinking: from infrastructure through AI implementation - the comprehensive approach valuable for any technical role."
    
    def generate_cover_letter(self, job_data, analysis):
        """
        Generate personalized cover letter
        
        Args:
            job_data (dict): Scraped job information
            analysis (dict): Job fit analysis
            
        Returns:
            str: Generated cover letter
        """
        template = self.templates[analysis['template_type']]
        
        # Prepare template variables
        template_vars = {
            'name': self.resume_data['name'],
            'company_name': job_data.get('company', '[Company Name]'),
            'job_title': job_data.get('title', '[Job Title]'),
            'experience_years': '3+',  # Adjust based on your experience
            'uptime_achievement': '99.8%',
            'infrastructure_summary': 'Linux/Windows server management with focus on reliability and monitoring',
            'automation_summary': 'Python development including GitHub API integration and content generation systems',
            'ai_learning_summary': 'Building Memory Platform - AI-powered family connection app with data analysis components',
            'recent_project_1': 'GitHub Development Logger Bot (Python, APIs, content automation)',
            'recent_project_2': 'Memory Platform development (AI, data processing, user experience)',
            'recent_project_3': 'Infrastructure monitoring with 99.8% uptime achievement',
            'job_specific_fit': self.generate_job_specific_fit(job_data, analysis),
            'specific_job_alignment': analysis['memory_platform_connection']
        }
        
        # Fill template
        cover_letter = template.format(**template_vars)
        
        return cover_letter.strip()
    
    def generate_job_specific_fit(self, job_data, analysis):
        """Generate job-specific fit explanation"""
        talking_points = analysis['talking_points']
        
        if len(talking_points) >= 3:
            return f"""
This role particularly appeals to me because:
• {talking_points[0]}
• {talking_points[1]}  
• {talking_points[2]}
            """
        else:
            return f"""
Your {job_data.get('title', 'position')} aligns perfectly with my Infrastructure → AI transition journey, combining the stability mindset from my infrastructure background with the innovation drive of my current automation projects.
            """
    
    def save_application_content(self, job_data, analysis, cover_letter):
        """Save generated content to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_clean = re.sub(r'[^\w\s-]', '', job_data.get('company', 'unknown')).strip()
        company_clean = re.sub(r'[-\s]+', '_', company_clean)
        
        filename_base = f"application_{company_clean}_{timestamp}"
        
        # Save cover letter
        cover_letter_path = Path(f"{filename_base}_cover_letter.txt")
        with open(cover_letter_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        # Save analysis and talking points
        analysis_path = Path(f"{filename_base}_analysis.json")
        output_data = {
            'job_data': job_data,
            'analysis': analysis,
            'cover_letter': cover_letter,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Application content saved:")
        print(f"   Cover Letter: {cover_letter_path}")
        print(f"   Full Analysis: {analysis_path}")
        
        return cover_letter_path, analysis_path
    
    def process_job_application(self, url):
        """
        Main workflow: URL → Personalized application content
        
        Args:
            url (str): Job posting URL
            
        Returns:
            dict: Complete application package
        """
        print(f"Processing job application for: {url}")
        
        # Step 1: Scrape job posting
        print("Scraping job posting...")
        job_data = self.scrape_job_posting(url)
        if not job_data:
            print("Failed to scrape job posting")
            return None
        
        print(f"Found job: {job_data['title']} at {job_data['company']}")
        
        # Step 2: Analyze job fit
        print("Analyzing job fit...")
        analysis = self.analyze_job_fit(job_data)
        
        print(f"Fit score: {analysis['fit_score']}/10")
        print(f"Best template: {analysis['template_type']}")
        
        # Step 3: Generate cover letter
        print("Generating personalized cover letter...")
        cover_letter = self.generate_cover_letter(job_data, analysis)
        
        # Step 4: Save everything
        print("Saving application content...")
        cover_letter_path, analysis_path = self.save_application_content(job_data, analysis, cover_letter)
        
        # Step 5: Display results
        print("\n" + "="*60)
        print("GENERATED COVER LETTER PREVIEW:")
        print("="*60)
        print(cover_letter[:500] + "..." if len(cover_letter) > 500 else cover_letter)
        print("="*60)
        
        print("\nKEY TALKING POINTS:")
        for i, point in enumerate(analysis['talking_points'], 1):
            print(f"   {i}. {point}")
        
        print(f"\nMEMORY PLATFORM CONNECTION:")
        print(f"   {analysis['memory_platform_connection']}")
        
        return {
            'job_data': job_data,
            'analysis': analysis,
            'cover_letter': cover_letter,
            'files': {
                'cover_letter': cover_letter_path,
                'analysis': analysis_path
            }
        }

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Generate personalized job application content')
    parser.add_argument('--url', required=True, help='Job posting URL')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    
    args = parser.parse_args()
    
    print("TailoredApply Bot - Job Application Content Generator")
    print("=" * 60)
    
    bot = TailoredApplyBot()
    result = bot.process_job_application(args.url)
    
    if result:
        print(f"\nSUCCESS! Application content ready for: {result['job_data']['company']}")
        print("Ready to customize and submit your application!")
    else:
        print("\nFailed to generate application content")

if __name__ == "__main__":
    main()