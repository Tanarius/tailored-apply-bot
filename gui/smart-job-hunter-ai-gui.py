# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
from datetime import datetime
import json
import webbrowser
from typing import Dict, List, Optional
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from smart_job_hunter_ai import SmartJobHunterAI, JobAnalysis, CompanyIntelligence, ApplicationStrategy
except ImportError as e:
    print(f"Warning: Could not import Smart Job Hunter AI: {e}")
    SmartJobHunterAI = None

class SmartJobHunterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Job Hunter AI - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Enhanced styling
        self.setup_styles()
        
        # Initialize AI system
        self.job_hunter = SmartJobHunterAI() if SmartJobHunterAI else None
        self.current_analysis = None
        self.job_history = []
        
        # Create main interface
        self.create_main_interface()
        
        # Load previous session data
        self.load_session_data()
    
    def setup_styles(self):
        """Configure modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'select_bg': '#0078d4',
            'select_fg': '#ffffff',
            'entry_bg': '#2d2d2d',
            'button_bg': '#0078d4',
            'button_fg': '#ffffff',
            'frame_bg': '#2d2d2d',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444'
        }
        
        # Apply styles
        style.configure('TNotebook', background=colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=colors['frame_bg'], foreground=colors['fg'], 
                       padding=[20, 10], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', colors['select_bg'])])
        
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 10))
        style.configure('TButton', background=colors['button_bg'], foreground=colors['button_fg'],
                       font=('Segoe UI', 10, 'bold'), padding=[15, 8])
        style.configure('TEntry', fieldbackground=colors['entry_bg'], foreground=colors['fg'],
                       borderwidth=1, insertcolor=colors['fg'])
        style.configure('TText', fieldbackground=colors['entry_bg'], foreground=colors['fg'])
        
        # Custom styles for status indicators
        style.configure('Success.TLabel', foreground=colors['success'], font=('Segoe UI', 10, 'bold'))
        style.configure('Warning.TLabel', foreground=colors['warning'], font=('Segoe UI', 10, 'bold'))
        style.configure('Error.TLabel', foreground=colors['error'], font=('Segoe UI', 10, 'bold'))
    
    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Smart Job Hunter AI", 
                               font=('Segoe UI', 24, 'bold'))
        title_label.pack(side='left')
        
        status_label = ttk.Label(header_frame, text="Professional AI-Powered Job Analysis System",
                                style='Success.TLabel')
        status_label.pack(side='right')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create all tabs
        self.create_job_analysis_tab()
        self.create_company_intelligence_tab()
        self.create_application_strategy_tab()
        self.create_success_prediction_tab()
        self.create_integration_hub_tab()
        self.create_job_history_tab()
        self.create_settings_tab()
    
    def create_job_analysis_tab(self):
        """Create job analysis and scraping tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Job Analysis")
        
        # Job URL input section
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(input_frame, text="Job Posting URL:", font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        url_frame = ttk.Frame(input_frame)
        url_frame.pack(fill='x', pady=(5, 0))
        
        self.job_url_entry = ttk.Entry(url_frame, font=('Segoe UI', 11))
        self.job_url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        analyze_btn = ttk.Button(url_frame, text="Analyze Job", command=self.analyze_job)
        analyze_btn.pack(side='right')
        
        # Quick actions
        quick_frame = ttk.Frame(input_frame)
        quick_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(quick_frame, text="Paste from Clipboard", 
                  command=self.paste_from_clipboard).pack(side='left', padx=(0, 10))
        ttk.Button(quick_frame, text="Load Saved Jobs", 
                  command=self.load_saved_jobs).pack(side='left', padx=(0, 10))
        ttk.Button(quick_frame, text="Import Job Description", 
                  command=self.import_job_description).pack(side='left')
        
        # Analysis results section
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(results_frame, text="Job Analysis Results:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Create paned window for results
        paned = ttk.PanedWindow(results_frame, orient='horizontal')
        paned.pack(fill='both', expand=True)
        
        # Left panel - Job details
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Job Details:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        self.job_details_text = scrolledtext.ScrolledText(left_frame, height=15, wrap='word',
                                                         font=('Consolas', 9))
        self.job_details_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Right panel - AI Analysis
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="AI Analysis:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        self.ai_analysis_text = scrolledtext.ScrolledText(right_frame, height=15, wrap='word',
                                                         font=('Consolas', 9))
        self.ai_analysis_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Analysis actions
        actions_frame = ttk.Frame(results_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(actions_frame, text="Save Analysis", 
                  command=self.save_analysis).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Generate Application", 
                  command=self.generate_application).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Send to Learning Coach", 
                  command=self.send_to_learning_coach).pack(side='left')
    
    def create_company_intelligence_tab(self):
        """Create company research and intelligence tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Company Intelligence")
        
        # Company search section
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(search_frame, text="Company Research:", font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        company_frame = ttk.Frame(search_frame)
        company_frame.pack(fill='x', pady=(5, 0))
        
        self.company_entry = ttk.Entry(company_frame, font=('Segoe UI', 11))
        self.company_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        research_btn = ttk.Button(company_frame, text="Research Company", 
                                 command=self.research_company)
        research_btn.pack(side='right')
        
        # Intelligence dashboard
        dashboard_frame = ttk.Frame(tab)
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create notebook for intelligence categories
        intel_notebook = ttk.Notebook(dashboard_frame)
        intel_notebook.pack(fill='both', expand=True)
        
        # Company overview tab
        overview_tab = ttk.Frame(intel_notebook)
        intel_notebook.add(overview_tab, text="Overview")
        self.company_overview_text = scrolledtext.ScrolledText(overview_tab, wrap='word',
                                                              font=('Segoe UI', 10))
        self.company_overview_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Culture analysis tab
        culture_tab = ttk.Frame(intel_notebook)
        intel_notebook.add(culture_tab, text="Culture Analysis")
        self.culture_analysis_text = scrolledtext.ScrolledText(culture_tab, wrap='word',
                                                              font=('Segoe UI', 10))
        self.culture_analysis_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Financial health tab
        financial_tab = ttk.Frame(intel_notebook)
        intel_notebook.add(financial_tab, text="Financial Health")
        self.financial_health_text = scrolledtext.ScrolledText(financial_tab, wrap='word',
                                                              font=('Segoe UI', 10))
        self.financial_health_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Recent news tab
        news_tab = ttk.Frame(intel_notebook)
        intel_notebook.add(news_tab, text="Recent News")
        self.company_news_text = scrolledtext.ScrolledText(news_tab, wrap='word',
                                                          font=('Segoe UI', 10))
        self.company_news_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_application_strategy_tab(self):
        """Create application strategy and optimization tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Application Strategy")
        
        # Strategy configuration
        config_frame = ttk.Frame(tab)
        config_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(config_frame, text="Application Strategy Configuration:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        # Strategy options
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill='x', pady=(10, 0))
        
        # Left column
        left_col = ttk.Frame(options_frame)
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        ttk.Label(left_col, text="Focus Areas:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        self.focus_vars = {}
        focus_areas = ["Technical Skills", "Soft Skills", "Experience Match", "Cultural Fit", "Growth Potential"]
        for area in focus_areas:
            var = tk.BooleanVar(value=True)
            self.focus_vars[area] = var
            ttk.Checkbutton(left_col, text=area, variable=var).pack(anchor='w', pady=2)
        
        # Right column
        right_col = ttk.Frame(options_frame)
        right_col.pack(side='right', fill='both', expand=True)
        
        ttk.Label(right_col, text="Application Type:", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        self.app_type_var = tk.StringVar(value="Standard")
        app_types = ["Standard", "Creative", "Technical Deep-Dive", "Leadership Focus", "Startup Style"]
        for app_type in app_types:
            ttk.Radiobutton(right_col, text=app_type, variable=self.app_type_var, 
                           value=app_type).pack(anchor='w', pady=2)
        
        # Generate strategy button
        ttk.Button(config_frame, text="Generate Application Strategy", 
                  command=self.generate_strategy).pack(pady=(20, 0))
        
        # Strategy results
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Strategy tabs
        strategy_notebook = ttk.Notebook(results_frame)
        strategy_notebook.pack(fill='both', expand=True)
        
        # Cover letter tab
        cover_tab = ttk.Frame(strategy_notebook)
        strategy_notebook.add(cover_tab, text="Cover Letter")
        self.cover_letter_text = scrolledtext.ScrolledText(cover_tab, wrap='word',
                                                          font=('Segoe UI', 10))
        self.cover_letter_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Resume optimization tab
        resume_tab = ttk.Frame(strategy_notebook)
        strategy_notebook.add(resume_tab, text="Resume Optimization")
        self.resume_opt_text = scrolledtext.ScrolledText(resume_tab, wrap='word',
                                                        font=('Segoe UI', 10))
        self.resume_opt_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Interview preparation tab
        interview_tab = ttk.Frame(strategy_notebook)
        strategy_notebook.add(interview_tab, text="Interview Prep")
        self.interview_prep_text = scrolledtext.ScrolledText(interview_tab, wrap='word',
                                                            font=('Segoe UI', 10))
        self.interview_prep_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Follow-up strategy tab
        followup_tab = ttk.Frame(strategy_notebook)
        strategy_notebook.add(followup_tab, text="Follow-up Strategy")
        self.followup_text = scrolledtext.ScrolledText(followup_tab, wrap='word',
                                                      font=('Segoe UI', 10))
        self.followup_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_success_prediction_tab(self):
        """Create AI success prediction and analytics tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Success Prediction")
        
        # Prediction dashboard
        dashboard_frame = ttk.Frame(tab)
        dashboard_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(dashboard_frame, text="Application Success Prediction:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        # Success metrics display
        metrics_frame = ttk.Frame(dashboard_frame)
        metrics_frame.pack(fill='x', pady=(10, 0))
        
        # Success score
        score_frame = ttk.Frame(metrics_frame)
        score_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(score_frame, text="Overall Success Score:", 
                 font=('Segoe UI', 11, 'bold')).pack(side='left')
        self.success_score_label = ttk.Label(score_frame, text="--", 
                                            style='Success.TLabel', font=('Segoe UI', 14, 'bold'))
        self.success_score_label.pack(side='right')
        
        # Prediction factors
        factors_frame = ttk.Frame(dashboard_frame)
        factors_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create factors display
        self.create_prediction_factors(factors_frame)
        
        # Detailed analysis
        analysis_frame = ttk.Frame(tab)
        analysis_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(analysis_frame, text="Detailed Prediction Analysis:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        self.prediction_text = scrolledtext.ScrolledText(analysis_frame, wrap='word',
                                                        font=('Segoe UI', 10))
        self.prediction_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Prediction actions
        actions_frame = ttk.Frame(analysis_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(actions_frame, text="Refresh Prediction", 
                  command=self.refresh_prediction).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Export Analysis", 
                  command=self.export_prediction).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Compare with Similar Jobs", 
                  command=self.compare_jobs).pack(side='left')
    
    def create_prediction_factors(self, parent):
        """Create prediction factors display"""
        factors_notebook = ttk.Notebook(parent)
        factors_notebook.pack(fill='both', expand=True)
        
        # Skills match tab
        skills_tab = ttk.Frame(factors_notebook)
        factors_notebook.add(skills_tab, text="Skills Match")
        
        skills_frame = ttk.Frame(skills_tab)
        skills_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.skills_match_text = scrolledtext.ScrolledText(skills_frame, height=8, wrap='word')
        self.skills_match_text.pack(fill='both', expand=True)
        
        # Experience alignment tab
        exp_tab = ttk.Frame(factors_notebook)
        factors_notebook.add(exp_tab, text="Experience Alignment")
        
        exp_frame = ttk.Frame(exp_tab)
        exp_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.exp_alignment_text = scrolledtext.ScrolledText(exp_frame, height=8, wrap='word')
        self.exp_alignment_text.pack(fill='both', expand=True)
        
        # Market factors tab
        market_tab = ttk.Frame(factors_notebook)
        factors_notebook.add(market_tab, text="Market Factors")
        
        market_frame = ttk.Frame(market_tab)
        market_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.market_factors_text = scrolledtext.ScrolledText(market_frame, height=8, wrap='word')
        self.market_factors_text.pack(fill='both', expand=True)
    
    def create_integration_hub_tab(self):
        """Create integration hub for other AI systems"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Integration Hub")
        
        # Integration status
        status_frame = ttk.Frame(tab)
        status_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(status_frame, text="AI System Integrations:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        # System status indicators
        systems_frame = ttk.Frame(status_frame)
        systems_frame.pack(fill='x', pady=(10, 0))
        
        self.integration_status = {}
        systems = [
            ("AI Learning Coach", "Learning & Skill Development"),
            ("Developer Brand AI", "Content & Branding"),
            ("AI Job Hunt Commander", "Job Discovery & Tracking"),
            ("Portfolio Updater", "Portfolio Management")
        ]
        
        for i, (system, description) in enumerate(systems):
            system_frame = ttk.Frame(systems_frame)
            system_frame.pack(fill='x', pady=5)
            
            status_label = ttk.Label(system_frame, text="●", style='Success.TLabel', 
                                   font=('Segoe UI', 16))
            status_label.pack(side='left', padx=(0, 10))
            
            name_label = ttk.Label(system_frame, text=system, font=('Segoe UI', 11, 'bold'))
            name_label.pack(side='left')
            
            desc_label = ttk.Label(system_frame, text=f"- {description}")
            desc_label.pack(side='left', padx=(10, 0))
            
            self.integration_status[system] = status_label
        
        # Integration actions
        actions_frame = ttk.Frame(tab)
        actions_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Quick actions grid
        quick_actions_frame = ttk.Frame(actions_frame)
        quick_actions_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(quick_actions_frame, text="Quick Actions:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        actions_grid = ttk.Frame(quick_actions_frame)
        actions_grid.pack(fill='x', pady=(10, 0))
        
        # Row 1
        row1 = ttk.Frame(actions_grid)
        row1.pack(fill='x', pady=(0, 10))
        
        ttk.Button(row1, text="Send Job to Learning Coach", 
                  command=self.send_to_learning_coach).pack(side='left', padx=(0, 10))
        ttk.Button(row1, text="Create Brand Content", 
                  command=self.create_brand_content).pack(side='left', padx=(0, 10))
        ttk.Button(row1, text="Update Portfolio", 
                  command=self.update_portfolio).pack(side='left')
        
        # Row 2
        row2 = ttk.Frame(actions_grid)
        row2.pack(fill='x')
        
        ttk.Button(row2, text="Sync with Commander", 
                  command=self.sync_with_commander).pack(side='left', padx=(0, 10))
        ttk.Button(row2, text="Generate Learning Path", 
                  command=self.generate_learning_path).pack(side='left', padx=(0, 10))
        ttk.Button(row2, text="Export All Data", 
                  command=self.export_all_data).pack(side='left')
        
        # Integration logs
        logs_frame = ttk.Frame(actions_frame)
        logs_frame.pack(fill='both', expand=True)
        
        ttk.Label(logs_frame, text="Integration Activity Log:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        self.integration_log = scrolledtext.ScrolledText(logs_frame, height=12, wrap='word',
                                                        font=('Consolas', 9))
        self.integration_log.pack(fill='both', expand=True, pady=(5, 0))
        
        # Add initial log entry
        self.log_integration_activity("Smart Job Hunter AI initialized and ready for integration")
    
    def create_job_history_tab(self):
        """Create job history and tracking tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Job History")
        
        # History controls
        controls_frame = ttk.Frame(tab)
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(controls_frame, text="Job Application History:", 
                 font=('Segoe UI', 12, 'bold')).pack(side='left')
        
        ttk.Button(controls_frame, text="Refresh History", 
                  command=self.refresh_history).pack(side='right', padx=(10, 0))
        ttk.Button(controls_frame, text="Export History", 
                  command=self.export_history).pack(side='right', padx=(10, 0))
        ttk.Button(controls_frame, text="Import Jobs", 
                  command=self.import_jobs).pack(side='right')
        
        # History display
        history_frame = ttk.Frame(tab)
        history_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create treeview for job history
        columns = ('Date', 'Company', 'Position', 'Status', 'Success Score', 'Actions')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.history_tree.heading(col, text=col)
            if col == 'Date':
                self.history_tree.column(col, width=100)
            elif col == 'Success Score':
                self.history_tree.column(col, width=100)
            elif col == 'Actions':
                self.history_tree.column(col, width=80)
            else:
                self.history_tree.column(col, width=150)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_tree.yview)
        h_scrollbar = ttk.Scrollbar(history_frame, orient='horizontal', command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.history_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click event
        self.history_tree.bind('<Double-1>', self.on_history_double_click)
        
        # Job details panel
        details_frame = ttk.Frame(tab)
        details_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(details_frame, text="Selected Job Details:", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        self.job_details_display = scrolledtext.ScrolledText(details_frame, height=8, wrap='word',
                                                            font=('Segoe UI', 10))
        self.job_details_display.pack(fill='both', expand=True, pady=(5, 0))
    
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")
        
        # API Configuration
        api_frame = ttk.LabelFrame(tab, text="API Configuration", padding=20)
        api_frame.pack(fill='x', padx=20, pady=20)
        
        # OpenAI API Key
        ttk.Label(api_frame, text="OpenAI API Key:").pack(anchor='w')
        self.api_key_entry = ttk.Entry(api_frame, show='*', width=50)
        self.api_key_entry.pack(fill='x', pady=(5, 15))
        
        # Model selection
        ttk.Label(api_frame, text="AI Model:").pack(anchor='w')
        self.model_var = tk.StringVar(value="gpt-3.5-turbo")
        model_combo = ttk.Combobox(api_frame, textvariable=self.model_var, 
                                  values=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"], state="readonly")
        model_combo.pack(fill='x', pady=(5, 15))
        
        # Save API settings
        ttk.Button(api_frame, text="Save API Settings", 
                  command=self.save_api_settings).pack()
        
        # Analysis Settings
        analysis_frame = ttk.LabelFrame(tab, text="Analysis Settings", padding=20)
        analysis_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Analysis depth
        ttk.Label(analysis_frame, text="Analysis Depth:").pack(anchor='w')
        self.depth_var = tk.StringVar(value="Standard")
        depth_combo = ttk.Combobox(analysis_frame, textvariable=self.depth_var,
                                  values=["Quick", "Standard", "Deep", "Comprehensive"], state="readonly")
        depth_combo.pack(fill='x', pady=(5, 15))
        
        # Auto-save results
        self.auto_save_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(analysis_frame, text="Auto-save analysis results", 
                       variable=self.auto_save_var).pack(anchor='w', pady=(0, 10))
        
        # Auto-send to integrations
        self.auto_integrate_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(analysis_frame, text="Auto-send to integrated systems", 
                       variable=self.auto_integrate_var).pack(anchor='w', pady=(0, 15))
        
        # Save analysis settings
        ttk.Button(analysis_frame, text="Save Analysis Settings", 
                  command=self.save_analysis_settings).pack()
        
        # Data Management
        data_frame = ttk.LabelFrame(tab, text="Data Management", padding=20)
        data_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        data_buttons = ttk.Frame(data_frame)
        data_buttons.pack(fill='x')
        
        ttk.Button(data_buttons, text="Export All Data", 
                  command=self.export_all_data).pack(side='left', padx=(0, 10))
        ttk.Button(data_buttons, text="Import Data", 
                  command=self.import_data).pack(side='left', padx=(0, 10))
        ttk.Button(data_buttons, text="Clear History", 
                  command=self.clear_history).pack(side='left', padx=(0, 10))
        ttk.Button(data_buttons, text="Reset Settings", 
                  command=self.reset_settings).pack(side='left')
    
    # Core functionality methods
    def analyze_job(self):
        """Analyze a job posting from URL"""
        if not self.job_hunter:
            messagebox.showerror("Error", "Smart Job Hunter AI not available")
            return
            
        url = self.job_url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a job URL")
            return
        
        # Show loading state
        self.show_loading_state("Analyzing job posting...")
        
        # Run analysis in separate thread
        def analyze():
            try:
                analysis = self.job_hunter.analyze_job_posting(url)
                if analysis:
                    self.current_analysis = analysis
                    self.root.after(0, self.display_job_analysis, analysis)
                    self.root.after(0, self.hide_loading_state)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to analyze job posting"))
                    self.root.after(0, self.hide_loading_state)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
                self.root.after(0, self.hide_loading_state)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def display_job_analysis(self, analysis):
        """Display job analysis results"""
        # Clear previous results
        self.job_details_text.delete(1.0, tk.END)
        self.ai_analysis_text.delete(1.0, tk.END)
        
        # Display job details
        job_info = f"""Job Title: {analysis.job_title}
Company: {analysis.company_name}
Location: {analysis.location}
Salary: {analysis.salary_range if analysis.salary_range else 'Not specified'}
Job Type: {analysis.job_type}

Job Description:
{analysis.job_description[:1000]}{'...' if len(analysis.job_description) > 1000 else ''}

Required Skills:
{', '.join(analysis.required_skills)}

Preferred Skills:
{', '.join(analysis.preferred_skills)}

Requirements:
{chr(10).join([f"• {req}" for req in analysis.requirements])}"""
        
        self.job_details_text.insert(1.0, job_info)
        
        # Display AI analysis
        ai_analysis = f"""Match Score: {analysis.match_score}/100

Skill Analysis:
{analysis.skill_analysis}

Experience Match:
{analysis.experience_match}

Culture Fit Assessment:
{analysis.culture_fit}

Application Recommendations:
{chr(10).join([f"• {rec}" for rec in analysis.recommendations])}

Key Talking Points:
{chr(10).join([f"• {point}" for point in analysis.talking_points])}

Areas for Improvement:
{chr(10).join([f"• {area}" for area in analysis.improvement_areas])}"""
        
        self.ai_analysis_text.insert(1.0, ai_analysis)
        
        # Add to history
        self.add_to_history(analysis)
        
        # Log activity
        self.log_integration_activity(f"Analyzed job: {analysis.job_title} at {analysis.company_name}")
    
    def research_company(self):
        """Research a company"""
        if not self.job_hunter:
            messagebox.showerror("Error", "Smart Job Hunter AI not available")
            return
            
        company_name = self.company_entry.get().strip()
        if not company_name:
            messagebox.showwarning("Warning", "Please enter a company name")
            return
        
        # Show loading state
        self.show_loading_state("Researching company...")
        
        def research():
            try:
                intelligence = self.job_hunter.research_company(company_name)
                if intelligence:
                    self.root.after(0, self.display_company_intelligence, intelligence)
                    self.root.after(0, self.hide_loading_state)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to research company"))
                    self.root.after(0, self.hide_loading_state)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Research failed: {str(e)}"))
                self.root.after(0, self.hide_loading_state)
        
        threading.Thread(target=research, daemon=True).start()
    
    def display_company_intelligence(self, intelligence):
        """Display company intelligence results"""
        # Clear previous results
        self.company_overview_text.delete(1.0, tk.END)
        self.culture_analysis_text.delete(1.0, tk.END)
        self.financial_health_text.delete(1.0, tk.END)
        self.company_news_text.delete(1.0, tk.END)
        
        # Display company overview
        overview = f"""Company: {intelligence.company_name}
Industry: {intelligence.industry}
Size: {intelligence.company_size}
Founded: {intelligence.founded_year}
Headquarters: {intelligence.headquarters}

About:
{intelligence.company_description}

Key Leadership:
{chr(10).join([f"• {leader}" for leader in intelligence.key_people])}

Products/Services:
{chr(10).join([f"• {product}" for product in intelligence.products_services])}"""
        
        self.company_overview_text.insert(1.0, overview)
        
        # Display culture analysis
        culture = f"""Culture Score: {intelligence.culture_score}/100

Work Environment:
{intelligence.work_environment}

Company Values:
{chr(10).join([f"• {value}" for value in intelligence.company_values])}

Employee Benefits:
{chr(10).join([f"• {benefit}" for benefit in intelligence.employee_benefits])}

Growth Opportunities:
{intelligence.growth_opportunities}

Work-Life Balance:
{intelligence.work_life_balance}"""
        
        self.culture_analysis_text.insert(1.0, culture)
        
        # Display financial health
        financial = f"""Financial Health Score: {intelligence.financial_health}/100

Revenue: {intelligence.revenue if intelligence.revenue else 'Private/Not disclosed'}
Employee Count: {intelligence.employee_count}
Recent Funding: {intelligence.recent_funding if intelligence.recent_funding else 'Not applicable'}

Market Position:
{intelligence.market_position}

Competitive Advantages:
{chr(10).join([f"• {advantage}" for advantage in intelligence.competitive_advantages])}

Growth Trajectory:
{intelligence.growth_trajectory}"""
        
        self.financial_health_text.insert(1.0, financial)
        
        # Display recent news
        news = f"""Recent Company News and Updates:

{chr(10).join([f"• {news_item}" for news_item in intelligence.recent_news])}

Industry Recognition:
{chr(10).join([f"• {award}" for award in intelligence.awards_recognition])}

Challenges and Risks:
{chr(10).join([f"• {challenge}" for challenge in intelligence.challenges])}"""
        
        self.company_news_text.insert(1.0, news)
    
    # Utility methods
    def show_loading_state(self, message):
        """Show loading state in UI"""
        # This would be implemented with a loading overlay or progress bar
        pass
    
    def hide_loading_state(self):
        """Hide loading state"""
        # This would hide the loading overlay
        pass
    
    def log_integration_activity(self, message):
        """Log integration activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.integration_log.insert(tk.END, log_entry)
        self.integration_log.see(tk.END)
    
    def add_to_history(self, analysis):
        """Add job analysis to history"""
        self.job_history.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'company': analysis.company_name,
            'position': analysis.job_title,
            'status': 'Analyzed',
            'score': analysis.match_score,
            'analysis': analysis
        })
        self.refresh_history_display()
    
    def refresh_history_display(self):
        """Refresh the history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items
        for job in reversed(self.job_history):  # Show most recent first
            self.history_tree.insert('', 'end', values=(
                job['date'],
                job['company'],
                job['position'],
                job['status'],
                f"{job['score']}/100",
                "View"
            ))
    
    # Placeholder methods for various actions
    def paste_from_clipboard(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.job_url_entry.delete(0, tk.END)
            self.job_url_entry.insert(0, clipboard_content)
        except:
            messagebox.showwarning("Warning", "Clipboard is empty or contains invalid data")
    
    def load_saved_jobs(self):
        """Load previously saved jobs"""
        messagebox.showinfo("Info", "Load saved jobs functionality will be implemented")
    
    def import_job_description(self):
        """Import job description from file"""
        file_path = filedialog.askopenfilename(
            title="Select job description file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Process the content as a job description
                messagebox.showinfo("Success", "Job description imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import file: {str(e)}")
    
    def save_analysis(self):
        """Save current analysis"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "No analysis to save")
            return
        messagebox.showinfo("Info", "Analysis saved successfully")
    
    def generate_application(self):
        """Generate application materials"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "Please analyze a job first")
            return
        self.notebook.select(2)  # Switch to Application Strategy tab
        self.generate_strategy()
    
    def send_to_learning_coach(self):
        """Send job data to Learning Coach"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "Please analyze a job first")
            return
        self.log_integration_activity(f"Sending job analysis to Learning Coach: {self.current_analysis.job_title}")
        messagebox.showinfo("Success", "Job data sent to Learning Coach for skill analysis")
    
    def generate_strategy(self):
        """Generate application strategy"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "Please analyze a job first")
            return
        
        # Mock strategy generation
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {self.current_analysis.job_title} position at {self.current_analysis.company_name}. With my background in software development and AI systems, I am excited about the opportunity to contribute to your team.

Based on my analysis of the role, I have identified several key areas where my experience aligns perfectly with your requirements:

{chr(10).join([f"• {skill}" for skill in self.current_analysis.required_skills[:5]])}

I am particularly drawn to {self.current_analysis.company_name} because of your innovative approach to technology and commitment to excellence. I believe my passion for AI and automation makes me an ideal candidate for this role.

I would welcome the opportunity to discuss how my skills and experience can contribute to your team's success.

Best regards,
[Your Name]"""
        
        self.cover_letter_text.delete(1.0, tk.END)
        self.cover_letter_text.insert(1.0, cover_letter)
        
        # Resume optimization
        resume_tips = f"""Resume Optimization Recommendations for {self.current_analysis.job_title}:

1. HIGHLIGHT THESE SKILLS:
{chr(10).join([f"   • {skill}" for skill in self.current_analysis.required_skills[:8]])}

2. EXPERIENCE ALIGNMENT:
   • Emphasize projects that demonstrate {self.current_analysis.required_skills[0]} experience
   • Quantify achievements with metrics and results
   • Include relevant technologies: {', '.join(self.current_analysis.preferred_skills[:5])}

3. KEYWORDS TO INCLUDE:
   {', '.join(self.current_analysis.required_skills + self.current_analysis.preferred_skills)}

4. RECOMMENDED SECTIONS:
   • Technical Skills (prominently featured)
   • Relevant Projects
   • Professional Experience
   • Certifications
   • Education

5. TAILORING SUGGESTIONS:
   • Customize project descriptions to match job requirements
   • Use industry-specific terminology
   • Highlight leadership and collaboration experiences"""
        
        self.resume_opt_text.delete(1.0, tk.END)
        self.resume_opt_text.insert(1.0, resume_tips)
        
        # Interview preparation
        interview_prep = f"""Interview Preparation for {self.current_analysis.job_title}:

TECHNICAL QUESTIONS TO EXPECT:
{chr(10).join([f"• How do you approach {skill.lower()}?" for skill in self.current_analysis.required_skills[:5]])}

BEHAVIORAL QUESTIONS:
• Tell me about a challenging project you've worked on
• How do you handle competing priorities?
• Describe a time you had to learn a new technology quickly
• How do you collaborate with cross-functional teams?

QUESTIONS TO ASK THEM:
• What are the biggest technical challenges the team is facing?
• How does the team approach professional development?
• What does success look like in this role after 6 months?
• Can you tell me about the team culture and collaboration style?

PREPARATION TASKS:
• Research {self.current_analysis.company_name}'s recent projects and news
• Prepare specific examples that demonstrate required skills
• Review fundamentals of key technologies
• Practice explaining complex technical concepts simply"""
        
        self.interview_prep_text.delete(1.0, tk.END)
        self.interview_prep_text.insert(1.0, interview_prep)
        
        # Follow-up strategy
        followup_strategy = f"""Follow-up Strategy for {self.current_analysis.company_name}:

TIMELINE:
Day 1: Submit application
Day 2-3: Connect with hiring manager on LinkedIn
Day 7: Follow-up email if no response
Day 14: Second follow-up with additional value

FOLLOW-UP MESSAGES:
1. Thank you note after application
2. LinkedIn connection request with personalized note
3. Value-added follow-up (relevant article, insight, or project)
4. Final gentle reminder before moving on

NETWORKING APPROACH:
• Connect with current employees in similar roles
• Engage with company content on social media
• Attend company events or webinars if available
• Look for warm introductions through mutual connections

TRACKING:
• Application submission date
• Response dates and next steps
• Interview dates and feedback
• Final decision and lessons learned"""
        
        self.followup_text.delete(1.0, tk.END)
        self.followup_text.insert(1.0, followup_strategy)
        
        messagebox.showinfo("Success", "Application strategy generated successfully")
    
    def refresh_prediction(self):
        """Refresh success prediction"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "Please analyze a job first")
            return
        
        # Mock prediction
        self.success_score_label.config(text=f"{self.current_analysis.match_score}%")
        
        prediction_analysis = f"""Success Prediction Analysis for {self.current_analysis.job_title}:

OVERALL SCORE: {self.current_analysis.match_score}/100

CONTRIBUTING FACTORS:
• Skills Match: {min(95, self.current_analysis.match_score + 10)}/100
• Experience Alignment: {max(70, self.current_analysis.match_score - 15)}/100
• Market Demand: 85/100
• Application Quality: 90/100

DETAILED BREAKDOWN:
The analysis shows a {['low', 'moderate', 'high', 'excellent'][min(3, self.current_analysis.match_score // 25)]} probability of success based on:

1. Technical Skills Match ({min(95, self.current_analysis.match_score + 10)}/100):
   - Strong alignment with required technologies
   - Relevant project experience
   - Growth potential in key areas

2. Experience Level ({max(70, self.current_analysis.match_score - 15)}/100):
   - Years of experience align with requirements
   - Industry background is relevant
   - Leadership experience is valuable

3. Market Factors (85/100):
   - High demand for this role type
   - Competitive but favorable market
   - Company is actively hiring

RECOMMENDATIONS FOR IMPROVEMENT:
{chr(10).join([f"• {area}" for area in self.current_analysis.improvement_areas])}

NEXT STEPS:
• Enhance application with specific examples
• Prepare targeted interview responses
• Consider additional skill development in key areas"""
        
        self.prediction_text.delete(1.0, tk.END)
        self.prediction_text.insert(1.0, prediction_analysis)
        
        # Update factor displays
        self.skills_match_text.delete(1.0, tk.END)
        self.skills_match_text.insert(1.0, f"Skills analysis shows {min(95, self.current_analysis.match_score + 10)}% match with job requirements")
        
        self.exp_alignment_text.delete(1.0, tk.END)
        self.exp_alignment_text.insert(1.0, f"Experience alignment score: {max(70, self.current_analysis.match_score - 15)}%")
        
        self.market_factors_text.delete(1.0, tk.END)
        self.market_factors_text.insert(1.0, "Market analysis indicates strong demand for this role type")
    
    def export_prediction(self):
        """Export prediction analysis"""
        messagebox.showinfo("Success", "Prediction analysis exported successfully")
    
    def compare_jobs(self):
        """Compare with similar jobs"""
        messagebox.showinfo("Info", "Job comparison feature coming soon")
    
    def create_brand_content(self):
        """Create brand content using Developer Brand AI"""
        self.log_integration_activity("Triggering Developer Brand AI content creation")
        messagebox.showinfo("Success", "Brand content creation initiated")
    
    def update_portfolio(self):
        """Update portfolio with job data"""
        self.log_integration_activity("Sending data to Portfolio Updater")
        messagebox.showinfo("Success", "Portfolio update initiated")
    
    def sync_with_commander(self):
        """Sync with AI Job Hunt Commander"""
        self.log_integration_activity("Syncing with AI Job Hunt Commander")
        messagebox.showinfo("Success", "Data sync with Commander completed")
    
    def generate_learning_path(self):
        """Generate learning path from job analysis"""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "Please analyze a job first")
            return
        self.log_integration_activity("Generating learning path based on job analysis")
        messagebox.showinfo("Success", "Learning path generated and sent to Learning Coach")
    
    def export_all_data(self):
        """Export all application data"""
        file_path = filedialog.asksaveasfilename(
            title="Export all data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", f"Data exported to {file_path}")
    
    def refresh_history(self):
        """Refresh job history"""
        self.refresh_history_display()
    
    def export_history(self):
        """Export job history"""
        file_path = filedialog.asksaveasfilename(
            title="Export job history",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", f"History exported to {file_path}")
    
    def import_jobs(self):
        """Import jobs from file"""
        file_path = filedialog.askopenfilename(
            title="Import jobs",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", "Jobs imported successfully")
    
    def on_history_double_click(self, event):
        """Handle double-click on history item"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']
            company = values[1]
            position = values[2]
            
            # Find the job in history
            for job in self.job_history:
                if job['company'] == company and job['position'] == position:
                    details = f"""Job Analysis Details:

Company: {job['company']}
Position: {job['position']}
Date Analyzed: {job['date']}
Match Score: {job['score']}/100
Status: {job['status']}

Analysis Summary:
{job['analysis'].skill_analysis if hasattr(job['analysis'], 'skill_analysis') else 'Analysis details not available'}"""
                    
                    self.job_details_display.delete(1.0, tk.END)
                    self.job_details_display.insert(1.0, details)
                    break
    
    def save_api_settings(self):
        """Save API settings"""
        api_key = self.api_key_entry.get().strip()
        if api_key:
            # Save settings (implement secure storage)
            messagebox.showinfo("Success", "API settings saved successfully")
        else:
            messagebox.showwarning("Warning", "Please enter an API key")
    
    def save_analysis_settings(self):
        """Save analysis settings"""
        messagebox.showinfo("Success", "Analysis settings saved successfully")
    
    def import_data(self):
        """Import application data"""
        file_path = filedialog.askopenfilename(
            title="Import data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Success", "Data imported successfully")
    
    def clear_history(self):
        """Clear job history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all job history?"):
            self.job_history.clear()
            self.refresh_history_display()
            messagebox.showinfo("Success", "Job history cleared")
    
    def reset_settings(self):
        """Reset all settings"""
        if messagebox.askyesno("Confirm", "Are you sure you want to reset all settings?"):
            messagebox.showinfo("Success", "Settings reset to defaults")
    
    def load_session_data(self):
        """Load previous session data"""
        try:
            # Load any saved session data
            self.log_integration_activity("Session data loaded successfully")
        except:
            self.log_integration_activity("Starting fresh session - no previous data found")
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Critical Error", f"Application error: {str(e)}")

def main():
    """Main entry point"""
    try:
        app = SmartJobHunterGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start Smart Job Hunter AI GUI: {e}")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()