#!/usr/bin/env python3
"""
Smart Job Hunter AI - Intelligent Application Strategy Engine
===========================================================

AI-powered job application system that analyzes job fit, company culture,
success probability, and creates strategic application campaigns. Integrates
with Learning Coach for skill-based targeting and Developer Brand AI for
content optimization.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import json
import openai
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re
import statistics
from dataclasses import dataclass, asdict
from urllib.parse import urlparse, urljoin

# Set up OpenAI API
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent.parent / "applying-assistant" / ".env")
    openai.api_key = os.getenv("OPENAI_API_KEY")
except ImportError:
    openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class JobAnalysis:
    """Complete analysis of a job opportunity"""
    job_id: str
    title: str
    company: str
    url: str
    description: str
    requirements: List[str]
    preferred_qualifications: List[str]
    salary_range: Optional[str]
    location: str
    job_type: str  # "remote", "hybrid", "onsite"
    company_size: Optional[str]
    industry: str
    
    # AI Analysis Results
    skill_match_score: float      # 0-100 how well skills match
    culture_fit_score: float      # 0-100 company culture compatibility
    growth_potential_score: float # 0-100 career growth opportunity
    success_probability: float    # 0-100 likelihood of getting hired
    overall_rating: float         # 0-100 overall job attractiveness
    
    # Strategic Insights
    required_skills_missing: List[str]
    competitive_advantages: List[str]
    application_strategy: str
    optimal_timing: str
    follow_up_strategy: str

@dataclass
class CompanyIntelligence:
    """Deep company analysis and culture insights"""
    name: str
    website: str
    size: str
    industry: str
    founding_year: Optional[int]
    headquarters: str
    
    # Culture Analysis
    values: List[str]
    culture_keywords: List[str]
    work_environment: str  # "collaborative", "competitive", "innovative", etc.
    management_style: str
    growth_stage: str      # "startup", "scale-up", "mature", "enterprise"
    
    # Market Intelligence
    recent_news: List[str]
    funding_status: Optional[str]
    competitors: List[str]
    tech_stack: List[str]
    hiring_trends: Dict[str, Any]
    glassdoor_rating: Optional[float]
    
    # Strategic Assessment
    stability_score: float        # 0-100 company stability
    innovation_score: float       # 0-100 innovation/growth potential
    culture_match_score: float    # 0-100 culture fit for candidate
    hiring_difficulty: str        # "easy", "moderate", "competitive", "very_competitive"

@dataclass
class ApplicationStrategy:
    """Strategic application plan"""
    job_id: str
    priority_level: int           # 1-5, 5 being highest priority
    application_timing: str       # "immediate", "1-2 days", "1 week", "after skill development"
    preparation_needed: List[str]
    skill_gaps_to_address: List[str]
    networking_opportunities: List[str]
    content_strategy: Dict[str, str]  # platform -> content approach
    success_factors: List[str]
    risk_mitigation: List[str]

class SmartJobHunterAI:
    """Intelligent job hunting system with AI-powered analysis and strategy"""
    
    def __init__(self):
        self.ai_enabled = bool(openai.api_key)
        
        # Integration paths
        self.learning_coach_path = Path(__file__).parent.parent.parent / "03-LEARNING-ASSISTANT" / "Learning_Data"
        self.brand_ai_path = Path(__file__).parent.parent.parent / "02-GITHUB-DEV-LOGGER" / "Brand_Data"
        self.job_data_path = Path(__file__).parent.parent / "Job_Intelligence"
        self.job_data_path.mkdir(exist_ok=True)
        
        # Load user profile and preferences
        self.user_profile = self.load_user_profile()
        self.job_history = self.load_job_history()
        self.success_metrics = self.load_success_metrics()
        
        # Initialize skill and preference databases
        self.skill_database = self.build_skill_database()
        self.company_database = self.load_company_database()
        
        print(f"Smart Job Hunter AI initialized - AI Mode: {'ENABLED' if self.ai_enabled else 'DISABLED'}")
    
    def load_user_profile(self) -> Dict[str, Any]:
        """Load user profile and career preferences"""
        profile_path = self.job_data_path / "user_profile.json"
        if profile_path.exists():
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "personal_info": {
                "name": "Trey",
                "current_role": "Infrastructure Engineer", 
                "target_role": "AI/Automation Specialist",
                "experience_years": 4,
                "location_preferences": ["Remote", "Hybrid"],
                "salary_target": {"min": 80000, "max": 120000}
            },
            "skills": {
                "expert": ["infrastructure", "system_administration", "uptime_management"],
                "proficient": ["python", "automation", "linux", "windows_server"],
                "developing": ["machine_learning", "ai_development", "data_analysis"],
                "interested": ["cloud_computing", "devops", "kubernetes"]
            },
            "preferences": {
                "company_size": ["startup", "scale-up", "mid-size"],
                "culture_values": ["innovation", "learning", "growth", "collaboration"],
                "work_style": "autonomous_with_mentorship",
                "travel_willingness": "minimal",
                "relocation_willingness": False
            },
            "career_goals": {
                "short_term": "Transition to AI/Automation role within 30 days",
                "mid_term": "Become AI systems specialist within 1 year", 
                "long_term": "Lead AI infrastructure teams within 3 years"
            }
        }
    
    def load_job_history(self) -> List[Dict[str, Any]]:
        """Load historical job applications and outcomes"""
        history_path = self.job_data_path / "application_history.json"
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def load_success_metrics(self) -> Dict[str, Any]:
        """Load success metrics and patterns"""
        return {
            "application_success_rate": 0.15,  # 15% typical success rate
            "interview_success_factors": [
                "infrastructure_experience_match",
                "automation_project_demonstration", 
                "learning_mindset_evidence",
                "cultural_fit_indicators"
            ],
            "optimal_application_timing": "tuesday_wednesday_morning",
            "best_performing_content_themes": [
                "infrastructure_reliability_story",
                "systematic_learning_approach",
                "practical_project_examples"
            ]
        }
    
    def build_skill_database(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive skill analysis database"""
        return {
            # Infrastructure Skills
            "infrastructure": {
                "category": "core_competency", 
                "market_demand": "high",
                "salary_impact": 1.2,
                "transition_relevance": "foundational"
            },
            "system_administration": {
                "category": "core_competency",
                "market_demand": "medium", 
                "salary_impact": 1.0,
                "transition_relevance": "foundational"
            },
            
            # AI/Automation Skills  
            "machine_learning": {
                "category": "target_skill",
                "market_demand": "very_high",
                "salary_impact": 1.5,
                "transition_relevance": "critical"
            },
            "python": {
                "category": "technical_skill",
                "market_demand": "very_high", 
                "salary_impact": 1.3,
                "transition_relevance": "essential"
            },
            "automation": {
                "category": "target_skill",
                "market_demand": "high",
                "salary_impact": 1.3,
                "transition_relevance": "critical"
            },
            
            # Cloud/DevOps Skills
            "aws": {
                "category": "cloud_platform",
                "market_demand": "very_high",
                "salary_impact": 1.4,
                "transition_relevance": "valuable"
            },
            "docker": {
                "category": "devops_tool",
                "market_demand": "high",
                "salary_impact": 1.2,
                "transition_relevance": "valuable"
            },
            "kubernetes": {
                "category": "devops_tool", 
                "market_demand": "high",
                "salary_impact": 1.3,
                "transition_relevance": "valuable"
            }
        }
    
    def load_company_database(self) -> Dict[str, Any]:
        """Load known company intelligence"""
        company_db_path = self.job_data_path / "company_database.json"
        if company_db_path.exists():
            try:
                with open(company_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def scrape_job_posting(self, url: str) -> Dict[str, Any]:
        """Enhanced job posting scraper with intelligent extraction"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job information using multiple strategies
            job_data = {
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'title': self.extract_job_title(soup, url),
                'company': self.extract_company_name(soup, url),
                'location': self.extract_location(soup),
                'description': self.extract_job_description(soup),
                'salary': self.extract_salary_info(soup),
                'job_type': self.extract_job_type(soup)
            }
            
            # Enhanced content analysis
            job_data['requirements'] = self.extract_requirements(job_data['description'])
            job_data['preferred_qualifications'] = self.extract_preferred_qualifications(job_data['description'])
            job_data['industry'] = self.identify_industry(job_data['description'], job_data['company'])
            job_data['company_size'] = self.estimate_company_size(job_data['company'], soup)
            
            return job_data
            
        except Exception as e:
            print(f"Error scraping job posting: {e}")
            return self.create_fallback_job_data(url)
    
    def extract_job_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract job title using multiple strategies"""
        selectors = [
            'h1[data-testid="jobTitle"]',
            'h1.jobsearch-JobInfoHeader-title', 
            'h1.job-title',
            'h1[class*="job-title"]',
            'h1[class*="title"]',
            '.job-header h1',
            'h1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                title = element.get_text().strip()
                # Clean up title
                title = re.sub(r'\s+', ' ', title)
                return title
        
        # Fallback: extract from URL or page title
        if 'indeed.com' in url:
            return "Job Position (Indeed)"
        elif 'linkedin.com' in url:
            return "Job Position (LinkedIn)"
        
        return "Job Position"
    
    def extract_company_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract company name using multiple strategies"""
        selectors = [
            '[data-testid="companyName"]',
            '.jobsearch-InlineCompanyRating a',
            '.company-name',
            '[class*="company"] a',
            '[class*="company-name"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                company = element.get_text().strip()
                # Clean company name
                company = re.sub(r'\s+', ' ', company)
                return company
        
        return "Company"
    
    def extract_location(self, soup: BeautifulSoup) -> str:
        """Extract job location"""
        selectors = [
            '[data-testid="jobLocation"]',
            '.jobsearch-InlineCompanyRating + div',
            '[class*="location"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                location = element.get_text().strip()
                return location
        
        return "Location not specified"
    
    def extract_job_description(self, soup: BeautifulSoup) -> str:
        """Extract complete job description"""
        # Try to find job description container
        desc_selectors = [
            '[data-testid="jobDescription"]',
            '.jobsearch-jobDescriptionText',
            '#jobDescriptionText',
            '.job-description',
            '[class*="description"]'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                # Get text while preserving some structure
                description = element.get_text(separator='\n', strip=True)
                return description
        
        # Fallback: get all text from page
        return soup.get_text()
    
    def extract_salary_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract salary information if available"""
        salary_patterns = [
            r'\$[\d,]+\s*-\s*\$[\d,]+',
            r'\$[\d,]+[kK]?\s*-\s*\$[\d,]+[kK]?',
            r'[\d,]+\s*-\s*[\d,]+\s*(USD|dollars)',
        ]
        
        text = soup.get_text()
        for pattern in salary_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return None
    
    def extract_job_type(self, soup: BeautifulSoup) -> str:
        """Determine if job is remote, hybrid, or onsite"""
        text = soup.get_text().lower()
        
        if any(term in text for term in ['remote', '100% remote', 'fully remote', 'work from home']):
            return 'remote'
        elif any(term in text for term in ['hybrid', 'flexible', 'some remote']):
            return 'hybrid' 
        else:
            return 'onsite'
    
    def extract_requirements(self, description: str) -> List[str]:
        """Extract job requirements from description"""
        requirements = []
        
        # Look for requirements sections
        req_patterns = [
            r'requirements?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'qualifications?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'must have:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'required skills?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        description_lower = description.lower()
        for pattern in req_patterns:
            matches = re.finditer(pattern, description_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                req_text = match.group(1)
                # Split by bullet points or newlines
                req_items = re.split(r'[•\n\-\*]', req_text)
                for item in req_items:
                    item = item.strip()
                    if len(item) > 10 and len(item) < 200:  # Filter reasonable requirements
                        requirements.append(item)
        
        # Also look for common skill mentions
        skill_patterns = [
            r'(\d+\+?\s*years?\s*(?:of\s*)?experience\s*(?:with\s*)?[\w\s,]+)',
            r'(bachelor\'?s?\s*(?:degree)?(?:\s*in\s*[\w\s]+)?)',
            r'(master\'?s?\s*(?:degree)?(?:\s*in\s*[\w\s]+)?)',
            r'(experience\s*(?:with|in)\s*[\w\s,]+)',
            r'(proficient\s*(?:with|in)\s*[\w\s,]+)',
            r'(knowledge\s*of\s*[\w\s,]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.finditer(pattern, description_lower, re.IGNORECASE)
            for match in matches:
                req = match.group(1).strip()
                if len(req) > 10:
                    requirements.append(req)
        
        return list(set(requirements[:10]))  # Limit and deduplicate
    
    def extract_preferred_qualifications(self, description: str) -> List[str]:
        """Extract preferred/nice-to-have qualifications"""
        preferred = []
        
        pref_patterns = [
            r'preferred:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'nice to have:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'bonus:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'plus:?\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        description_lower = description.lower()
        for pattern in pref_patterns:
            matches = re.finditer(pattern, description_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                pref_text = match.group(1)
                pref_items = re.split(r'[•\n\-\*]', pref_text)
                for item in pref_items:
                    item = item.strip()
                    if len(item) > 10 and len(item) < 200:
                        preferred.append(item)
        
        return list(set(preferred[:8]))
    
    def identify_industry(self, description: str, company: str) -> str:
        """Identify company industry from job description"""
        industry_keywords = {
            'technology': ['software', 'tech', 'saas', 'platform', 'api', 'cloud', 'ai', 'ml'],
            'finance': ['bank', 'financial', 'fintech', 'trading', 'investment'],
            'healthcare': ['health', 'medical', 'hospital', 'pharmaceutical'],
            'ecommerce': ['ecommerce', 'retail', 'marketplace', 'shopping'],
            'enterprise': ['enterprise', 'b2b', 'corporate', 'business solutions'],
            'startup': ['startup', 'early stage', 'seed', 'venture'],
            'consulting': ['consulting', 'advisory', 'professional services']
        }
        
        text = (description + ' ' + company).lower()
        
        for industry, keywords in industry_keywords.items():
            if sum(keyword in text for keyword in keywords) >= 2:
                return industry
        
        return 'technology'  # Default for most AI/automation roles
    
    def estimate_company_size(self, company: str, soup: BeautifulSoup) -> str:
        """Estimate company size from available information"""
        if soup is None:
            # Fallback to company name analysis only
            if any(term in company.lower() for term in ['inc', 'corp', 'ltd', 'llc']):
                return 'medium'
            return 'unknown'
            
        text = soup.get_text().lower()
        
        size_indicators = {
            'startup': ['startup', 'early stage', '1-10 employees', '11-50 employees'],
            'small': ['small', '51-200 employees', '201-500 employees'],
            'medium': ['medium', '501-1000 employees', '1001-5000 employees'],
            'large': ['large', '5001-10000 employees', 'enterprise', 'fortune'],
            'very_large': ['10000+ employees', 'multinational', 'global']
        }
        
        for size, indicators in size_indicators.items():
            if any(indicator in text for indicator in indicators):
                return size
        
        # Try to infer from company name
        if any(term in company.lower() for term in ['inc', 'corp', 'ltd', 'llc']):
            return 'medium'
        
        return 'unknown'
    
    def analyze_job_fit(self, job_data: Dict[str, Any]) -> JobAnalysis:
        """Comprehensive AI-powered job fit analysis"""
        
        # Calculate skill match score
        skill_match = self.calculate_skill_match_score(
            job_data['requirements'] + job_data['preferred_qualifications']
        )
        
        # Get company intelligence
        company_intel = self.analyze_company_culture(job_data['company'], job_data['description'])
        culture_fit = company_intel.culture_match_score
        
        # Calculate growth potential
        growth_potential = self.calculate_growth_potential(job_data, company_intel)
        
        # Predict success probability using AI/ML
        success_prob = self.predict_application_success(job_data, skill_match, culture_fit)
        
        # Calculate overall rating
        overall_rating = (skill_match * 0.3 + culture_fit * 0.25 + 
                         growth_potential * 0.25 + success_prob * 0.2)
        
        # Generate strategic insights
        missing_skills = self.identify_missing_skills(job_data['requirements'])
        advantages = self.identify_competitive_advantages(job_data, skill_match)
        strategy = self.generate_application_strategy(job_data, skill_match, culture_fit)
        
        return JobAnalysis(
            job_id=self.generate_job_id(job_data['url']),
            title=job_data['title'],
            company=job_data['company'],
            url=job_data['url'],
            description=job_data['description'][:500],  # Truncate for storage
            requirements=job_data['requirements'],
            preferred_qualifications=job_data['preferred_qualifications'],
            salary_range=job_data.get('salary'),
            location=job_data['location'],
            job_type=job_data['job_type'],
            company_size=job_data.get('company_size', 'unknown'),
            industry=job_data['industry'],
            skill_match_score=skill_match,
            culture_fit_score=culture_fit,
            growth_potential_score=growth_potential,
            success_probability=success_prob,
            overall_rating=overall_rating,
            required_skills_missing=missing_skills,
            competitive_advantages=advantages,
            application_strategy=strategy,
            optimal_timing=self.determine_optimal_timing(overall_rating),
            follow_up_strategy=self.generate_follow_up_strategy(company_intel)
        )
    
    def calculate_skill_match_score(self, requirements: List[str]) -> float:
        """Calculate how well user skills match job requirements"""
        user_skills = self.user_profile['skills']
        all_user_skills = (user_skills['expert'] + user_skills['proficient'] + 
                          user_skills['developing'])
        
        matched_requirements = 0
        total_weight = 0
        
        for req in requirements:
            req_lower = req.lower()
            weight = 1.0  # Base weight
            
            # Increase weight for critical skills
            if any(critical in req_lower for critical in ['python', 'automation', 'ai', 'ml', 'machine learning']):
                weight = 2.0
            
            total_weight += weight
            
            # Check for skill matches
            for skill in all_user_skills:
                if skill.lower() in req_lower or any(synonym in req_lower for synonym in self.get_skill_synonyms(skill)):
                    # Weight by proficiency level
                    if skill in user_skills['expert']:
                        matched_requirements += weight * 1.0
                    elif skill in user_skills['proficient']:
                        matched_requirements += weight * 0.8
                    elif skill in user_skills['developing']:
                        matched_requirements += weight * 0.5
                    break
        
        if total_weight == 0:
            return 50.0  # Default score if no requirements identified
        
        score = (matched_requirements / total_weight) * 100
        return min(100.0, score)
    
    def get_skill_synonyms(self, skill: str) -> List[str]:
        """Get synonyms for skill matching"""
        synonyms = {
            'python': ['python', 'py', 'python3'],
            'automation': ['automation', 'automate', 'scripting', 'scripts'],
            'infrastructure': ['infrastructure', 'infra', 'systems', 'sysadmin'],
            'machine_learning': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
            'linux': ['linux', 'unix', 'ubuntu', 'centos', 'redhat'],
            'aws': ['aws', 'amazon web services', 'ec2', 's3', 'cloud'],
            'docker': ['docker', 'containerization', 'containers'],
            'kubernetes': ['kubernetes', 'k8s', 'container orchestration']
        }
        return synonyms.get(skill, [skill])
    
    def analyze_company_culture(self, company_name: str, job_description: str) -> CompanyIntelligence:
        """Analyze company culture and fit using AI"""
        
        # Check if we have cached company data
        if company_name in self.company_database:
            cached_data = self.company_database[company_name]
            cached_intel = CompanyIntelligence(**cached_data)
            # Update culture match score based on current user profile
            cached_intel.culture_match_score = self.calculate_culture_fit(cached_intel)
            return cached_intel
        
        # Extract culture indicators from job description
        culture_keywords = self.extract_culture_keywords(job_description)
        values = self.extract_company_values(job_description)
        work_environment = self.analyze_work_environment(job_description)
        
        # Create company intelligence object
        company_intel = CompanyIntelligence(
            name=company_name,
            website=f"https://{company_name.lower().replace(' ', '')}.com",
            size=self.estimate_company_size(company_name, None),
            industry=self.identify_industry(job_description, company_name),
            founding_year=None,
            headquarters="Location not specified",
            values=values,
            culture_keywords=culture_keywords,
            work_environment=work_environment,
            management_style="collaborative",  # Default assumption
            growth_stage=self.estimate_growth_stage(job_description),
            recent_news=[],
            funding_status=None,
            competitors=[],
            tech_stack=self.extract_tech_stack(job_description),
            hiring_trends={},
            glassdoor_rating=None,
            stability_score=75.0,  # Default
            innovation_score=self.calculate_innovation_score(job_description),
            culture_match_score=0,  # Will be calculated
            hiring_difficulty="moderate"
        )
        
        # Calculate culture fit
        company_intel.culture_match_score = self.calculate_culture_fit(company_intel)
        
        # Cache the results
        self.company_database[company_name] = asdict(company_intel)
        self.save_company_database()
        
        return company_intel
    
    def extract_culture_keywords(self, description: str) -> List[str]:
        """Extract culture-related keywords from job description"""
        culture_patterns = [
            'collaborative', 'innovative', 'fast-paced', 'dynamic', 'flexible',
            'learning', 'growth', 'mentorship', 'autonomous', 'independent',
            'team-oriented', 'results-driven', 'data-driven', 'customer-focused'
        ]
        
        found_keywords = []
        description_lower = description.lower()
        
        for keyword in culture_patterns:
            if keyword in description_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def extract_company_values(self, description: str) -> List[str]:
        """Extract stated company values"""
        values_patterns = [
            r'values?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'culture:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'we believe:?\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        values = []
        for pattern in values_patterns:
            matches = re.finditer(pattern, description, re.IGNORECASE | re.DOTALL)
            for match in matches:
                values_text = match.group(1)
                # Extract individual values
                value_items = re.split(r'[,•\n\-]', values_text)
                for item in value_items:
                    item = item.strip()
                    if len(item) > 3 and len(item) < 50:
                        values.append(item)
        
        return values[:5]  # Limit to top 5
    
    def analyze_work_environment(self, description: str) -> str:
        """Analyze work environment from description"""
        environment_indicators = {
            'collaborative': ['collaborative', 'team', 'together', 'partnership'],
            'competitive': ['competitive', 'fast-paced', 'aggressive', 'results-driven'],
            'innovative': ['innovative', 'creative', 'cutting-edge', 'experimental'],
            'supportive': ['supportive', 'mentorship', 'learning', 'growth'],
            'autonomous': ['autonomous', 'independent', 'self-directed', 'ownership']
        }
        
        description_lower = description.lower()
        environment_scores = {}
        
        for env, indicators in environment_indicators.items():
            score = sum(1 for indicator in indicators if indicator in description_lower)
            environment_scores[env] = score
        
        # Return the environment with highest score
        if environment_scores:
            return max(environment_scores, key=environment_scores.get)
        
        return 'collaborative'  # Default
    
    def estimate_growth_stage(self, description: str) -> str:
        """Estimate company growth stage"""
        description_lower = description.lower()
        
        if any(term in description_lower for term in ['startup', 'early stage', 'seed']):
            return 'startup'
        elif any(term in description_lower for term in ['scale', 'scaling', 'rapid growth']):
            return 'scale-up'
        elif any(term in description_lower for term in ['established', 'mature', 'leader']):
            return 'mature'
        elif any(term in description_lower for term in ['enterprise', 'fortune', 'global']):
            return 'enterprise'
        
        return 'mature'  # Default
    
    def extract_tech_stack(self, description: str) -> List[str]:
        """Extract technology stack from job description"""
        tech_keywords = [
            'python', 'javascript', 'java', 'c++', 'go', 'rust',
            'react', 'vue', 'angular', 'node', 'express',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'mysql', 'postgresql', 'mongodb', 'redis',
            'tensorflow', 'pytorch', 'scikit-learn'
        ]
        
        found_tech = []
        description_lower = description.lower()
        
        for tech in tech_keywords:
            if tech in description_lower:
                found_tech.append(tech)
        
        return found_tech
    
    def calculate_innovation_score(self, description: str) -> float:
        """Calculate company innovation score from description"""
        innovation_indicators = [
            'ai', 'machine learning', 'cutting-edge', 'innovative',
            'research', 'r&d', 'breakthrough', 'disruptive',
            'next-generation', 'advanced', 'emerging'
        ]
        
        description_lower = description.lower()
        innovation_count = sum(1 for indicator in innovation_indicators 
                             if indicator in description_lower)
        
        # Normalize to 0-100 scale
        score = min(100.0, (innovation_count / len(innovation_indicators)) * 100)
        return score
    
    def calculate_culture_fit(self, company_intel: CompanyIntelligence) -> float:
        """Calculate culture fit score based on user preferences"""
        user_values = set(self.user_profile['preferences']['culture_values'])
        company_values = set([v.lower() for v in company_intel.values])
        company_keywords = set(company_intel.culture_keywords)
        
        # Calculate overlap
        values_overlap = len(user_values.intersection(company_values))
        keywords_overlap = len(user_values.intersection(company_keywords))
        
        # Weight different factors
        values_score = (values_overlap / max(len(user_values), 1)) * 50
        keywords_score = (keywords_overlap / max(len(user_values), 1)) * 30
        
        # Add bonus for work environment match
        environment_bonus = 20 if company_intel.work_environment in ['collaborative', 'innovative'] else 10
        
        total_score = values_score + keywords_score + environment_bonus
        return min(100.0, total_score)
    
    def calculate_growth_potential(self, job_data: Dict[str, Any], company_intel: CompanyIntelligence) -> float:
        """Calculate career growth potential score"""
        growth_factors = {
            'company_growth_stage': {
                'startup': 85, 'scale-up': 90, 'mature': 70, 'enterprise': 60
            },
            'industry_growth': {
                'technology': 85, 'ai': 95, 'fintech': 80, 'healthcare': 75
            },
            'role_level': 70,  # Default for mid-level roles
            'learning_opportunities': 80  # Default
        }
        
        # Base score from company stage
        stage_score = growth_factors['company_growth_stage'].get(company_intel.growth_stage, 70)
        
        # Industry growth score
        industry_score = growth_factors['industry_growth'].get(company_intel.industry, 70)
        
        # Role progression indicators
        description_lower = job_data['description'].lower()
        role_score = growth_factors['role_level']
        
        if any(term in description_lower for term in ['senior', 'lead', 'principal']):
            role_score = 85
        elif any(term in description_lower for term in ['junior', 'entry']):
            role_score = 90  # High growth potential from junior roles
        
        # Learning and development opportunities
        learning_score = growth_factors['learning_opportunities']
        if any(term in description_lower for term in ['mentorship', 'learning', 'training', 'development']):
            learning_score = 90
        
        # Calculate weighted average
        total_score = (stage_score * 0.3 + industry_score * 0.3 + 
                      role_score * 0.2 + learning_score * 0.2)
        
        return total_score
    
    def predict_application_success(self, job_data: Dict[str, Any], skill_match: float, culture_fit: float) -> float:
        """AI-powered application success prediction"""
        
        if not self.ai_enabled:
            return self.calculate_template_success_prediction(skill_match, culture_fit)
        
        try:
            # Create context for AI prediction
            context = {
                'job_title': job_data['title'],
                'company': job_data['company'],
                'industry': job_data['industry'],
                'job_type': job_data['job_type'],
                'skill_match_score': skill_match,
                'culture_fit_score': culture_fit,
                'user_background': 'Infrastructure Engineer transitioning to AI/Automation',
                'experience_years': self.user_profile['personal_info']['experience_years'],
                'current_skills': self.user_profile['skills'],
                'application_history_success_rate': self.success_metrics['application_success_rate']
            }
            
            prompt = f"""Analyze application success probability for this job opportunity:

JOB CONTEXT:
- Title: {context['job_title']}
- Company: {context['company']}  
- Industry: {context['industry']}
- Job Type: {context['job_type']}

CANDIDATE ANALYSIS:
- Background: {context['user_background']}
- Experience: {context['experience_years']} years
- Skill Match Score: {skill_match:.1f}%
- Culture Fit Score: {culture_fit:.1f}% 
- Historical Success Rate: {self.success_metrics['application_success_rate']*100:.1f}%

Based on the skill match, culture fit, candidate background, and market conditions, 
predict the probability (0-100) that this application will result in at least an initial interview.

Consider:
1. How well the Infrastructure → AI transition story fits this role
2. Market demand for these skills
3. Competition level for similar roles
4. Company hiring patterns and preferences
5. Candidate's unique value proposition

Provide only a numerical percentage (0-100) as your response."""

            # Try new OpenAI client format first
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai.api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=50
                )
                ai_response = response.choices[0].message.content.strip()
            except:
                # Fallback to old format
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=50
                )
                ai_response = response.choices[0].message.content.strip()
            
            # Extract numerical value
            probability = re.search(r'\d+', ai_response)
            if probability:
                return min(100.0, float(probability.group()))
            
        except Exception as e:
            print(f"AI success prediction failed: {e}")
        
        return self.calculate_template_success_prediction(skill_match, culture_fit)
    
    def calculate_template_success_prediction(self, skill_match: float, culture_fit: float) -> float:
        """Template-based success prediction when AI is not available"""
        
        # Base success rate adjusted by skill and culture fit
        base_rate = self.success_metrics['application_success_rate'] * 100  # Convert to percentage
        
        # Skill match impact
        skill_multiplier = 1.0 + ((skill_match - 50) / 100)  # Range: 0.5 to 1.5
        
        # Culture fit impact  
        culture_multiplier = 1.0 + ((culture_fit - 50) / 200)  # Range: 0.75 to 1.25
        
        # Infrastructure → AI transition bonus/penalty
        transition_bonus = 1.1 if skill_match > 60 else 0.9
        
        predicted_rate = base_rate * skill_multiplier * culture_multiplier * transition_bonus
        
        return min(100.0, max(5.0, predicted_rate))  # Clamp between 5% and 100%
    
    def identify_missing_skills(self, requirements: List[str]) -> List[str]:
        """Identify skills missing from user profile that are required"""
        user_skills = (self.user_profile['skills']['expert'] + 
                      self.user_profile['skills']['proficient'] +
                      self.user_profile['skills']['developing'])
        
        missing_skills = []
        
        for req in requirements:
            req_lower = req.lower()
            skill_found = False
            
            for user_skill in user_skills:
                if user_skill.lower() in req_lower or any(syn in req_lower for syn in self.get_skill_synonyms(user_skill)):
                    skill_found = True
                    break
            
            if not skill_found:
                # Extract the actual skill from requirement text
                skill = self.extract_skill_from_requirement(req)
                if skill and skill not in missing_skills:
                    missing_skills.append(skill)
        
        return missing_skills[:5]  # Limit to top 5
    
    def extract_skill_from_requirement(self, requirement: str) -> Optional[str]:
        """Extract core skill from requirement text"""
        # Common skill patterns
        skill_patterns = [
            r'experience\s+(?:with|in)\s+([^,\n]+)',
            r'knowledge\s+of\s+([^,\n]+)',
            r'proficient\s+(?:in|with)\s+([^,\n]+)',
            r'familiar\s+with\s+([^,\n]+)',
            r'(\w+(?:\s+\w+)?)\s+experience',
            r'(\w+(?:\s+\w+)?)\s+skills?'
        ]
        
        for pattern in skill_patterns:
            match = re.search(pattern, requirement, re.IGNORECASE)
            if match:
                skill = match.group(1).strip().lower()
                if len(skill) > 2 and len(skill) < 30:
                    return skill
        
        return None
    
    def identify_competitive_advantages(self, job_data: Dict[str, Any], skill_match: float) -> List[str]:
        """Identify candidate's competitive advantages for this role"""
        advantages = []
        
        # Infrastructure experience advantage
        if any(term in job_data['description'].lower() for term in ['infrastructure', 'reliability', 'uptime', 'systems']):
            advantages.append("Proven infrastructure reliability experience (99.8% uptime track record)")
        
        # Transition story advantage
        if skill_match > 50:
            advantages.append("Active Infrastructure → AI career transition demonstrates adaptability and learning agility")
        
        # Project portfolio advantage
        if any(term in job_data['description'].lower() for term in ['automation', 'python', 'projects']):
            advantages.append("Practical automation projects and bot development showcase hands-on experience")
        
        # Memory Platform relevance
        if any(term in job_data['description'].lower() for term in ['ai', 'data', 'platform', 'system']):
            advantages.append("Memory Platform project demonstrates end-to-end AI system development")
        
        # Learning mindset advantage
        advantages.append("Documented systematic learning approach and skill development methodology")
        
        # Industry timing advantage
        if job_data['industry'] in ['technology', 'ai']:
            advantages.append("Perfect timing for Infrastructure professionals entering AI field due to system integration needs")
        
        return advantages[:4]  # Limit to top 4
    
    def generate_application_strategy(self, job_data: Dict[str, Any], skill_match: float, culture_fit: float) -> str:
        """Generate strategic application approach"""
        
        if skill_match >= 80 and culture_fit >= 80:
            return "High-priority immediate application: Strong fit across skills and culture. Lead with infrastructure reliability story and AI transition progress."
            
        elif skill_match >= 60 and culture_fit >= 60:
            return "Strategic application: Good overall fit. Emphasize transferable skills and learning velocity. Highlight specific project examples."
            
        elif skill_match >= 40:
            return "Development-focused application: Address skill gaps through targeted learning before applying. Use application as learning goal motivation."
            
        else:
            return "Research and networking approach: Company culture alignment but significant skill gaps. Focus on networking and learning about role requirements."
    
    def determine_optimal_timing(self, overall_rating: float) -> str:
        """Determine optimal application timing"""
        if overall_rating >= 85:
            return "immediate"
        elif overall_rating >= 70:
            return "within_24_hours"
        elif overall_rating >= 55:
            return "within_week"
        else:
            return "after_skill_development"
    
    def generate_follow_up_strategy(self, company_intel: CompanyIntelligence) -> str:
        """Generate follow-up strategy based on company analysis"""
        
        if company_intel.growth_stage == 'startup':
            return "Fast follow-up strategy: Reach out to hiring manager within 3-5 days. Startups move quickly."
        elif company_intel.size in ['large', 'very_large']:
            return "Formal follow-up strategy: Follow standard HR process. Follow up after 1 week, then bi-weekly."
        elif company_intel.culture_match_score >= 80:
            return "Cultural alignment follow-up: Reference shared values in follow-up communications."
        else:
            return "Standard follow-up strategy: Professional follow-up after 1 week, highlighting key qualifications."
    
    def create_fallback_job_data(self, url: str) -> Dict[str, Any]:
        """Create fallback job data when scraping fails"""
        return {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'title': 'Job Position',
            'company': 'Company',
            'location': 'Location not specified',
            'description': 'Job description could not be retrieved',
            'salary': None,
            'job_type': 'unknown',
            'requirements': ['Experience in relevant technologies'],
            'preferred_qualifications': [],
            'industry': 'technology',
            'company_size': 'unknown'
        }
    
    def generate_job_id(self, url: str) -> str:
        """Generate unique job ID from URL"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def save_company_database(self):
        """Save company database for future use"""
        try:
            company_db_path = self.job_data_path / "company_database.json"
            with open(company_db_path, 'w', encoding='utf-8') as f:
                json.dump(self.company_database, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error saving company database: {e}")
    
    def save_job_analysis(self, analysis: JobAnalysis) -> str:
        """Save job analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"job_analysis_{analysis.job_id}_{timestamp}.json"
        filepath = self.job_data_path / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(analysis), f, indent=2, ensure_ascii=False, default=str)
            return str(filepath)
        except Exception as e:
            print(f"Error saving job analysis: {e}")
            return ""
    
    def analyze_job_opportunity(self, url: str) -> JobAnalysis:
        """Main method: Complete intelligent job analysis"""
        print("Starting Smart Job Hunter AI analysis...")
        
        # Step 1: Scrape job posting
        print("Extracting job information...")
        job_data = self.scrape_job_posting(url)
        
        # Step 2: Perform comprehensive analysis
        print("Performing AI-powered job fit analysis...")
        analysis = self.analyze_job_fit(job_data)
        
        # Step 3: Save results
        saved_path = self.save_job_analysis(analysis)
        print(f"Analysis complete! Saved to: {saved_path}")
        
        return analysis
    
    def batch_analyze_jobs(self, urls: List[str]) -> List[JobAnalysis]:
        """Analyze multiple job opportunities and rank them"""
        analyses = []
        
        for i, url in enumerate(urls, 1):
            print(f"Analyzing job {i}/{len(urls)}: {url}")
            try:
                analysis = self.analyze_job_opportunity(url)
                analyses.append(analysis)
            except Exception as e:
                print(f"Error analyzing job {i}: {e}")
        
        # Sort by overall rating
        analyses.sort(key=lambda x: x.overall_rating, reverse=True)
        
        return analyses


def main():
    """Test Smart Job Hunter AI"""
    hunter = SmartJobHunterAI()
    
    print("Smart Job Hunter AI - Test Mode")
    print("=" * 50)
    
    # Test with a sample URL (would need actual job posting URL)
    test_url = "https://example.com/job"
    
    # For testing, create a sample analysis
    print("Creating sample job analysis...")
    sample_analysis = JobAnalysis(
        job_id="test123",
        title="AI Engineer",
        company="TechCorp",
        url=test_url,
        description="Exciting AI role...",
        requirements=["Python", "Machine Learning", "3+ years experience"],
        preferred_qualifications=["PhD in AI", "TensorFlow"],
        salary_range="$90,000 - $120,000",
        location="Remote",
        job_type="remote",
        company_size="medium",
        industry="technology",
        skill_match_score=75.0,
        culture_fit_score=85.0,
        growth_potential_score=90.0,
        success_probability=65.0,
        overall_rating=78.8,
        required_skills_missing=["TensorFlow", "Deep Learning"],
        competitive_advantages=["Infrastructure experience", "Learning agility"],
        application_strategy="Strategic application with skill development focus",
        optimal_timing="within_week",
        follow_up_strategy="Professional follow-up after 1 week"
    )
    
    print("\nSample Analysis Results:")
    print(f"Job: {sample_analysis.title} at {sample_analysis.company}")
    print(f"Overall Rating: {sample_analysis.overall_rating:.1f}%")
    print(f"Skill Match: {sample_analysis.skill_match_score:.1f}%")
    print(f"Culture Fit: {sample_analysis.culture_fit_score:.1f}%")
    print(f"Success Probability: {sample_analysis.success_probability:.1f}%")
    print(f"Strategy: {sample_analysis.application_strategy}")
    
    print("\nSmart Job Hunter AI test completed!")


if __name__ == "__main__":
    main()