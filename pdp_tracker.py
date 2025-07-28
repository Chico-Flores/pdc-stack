#!/usr/bin/env python3
"""
Post Dated Payment (PDP) Tracker Tool
=====================================

A comprehensive tool to track and analyze the performance of post-dated payments
and payfile improvements for sales teams implementing long-term payment arrangements.

Features:
- Import Excel reports automatically
- Track historical baselines with timestamps
- Calculate improvement metrics
- Generate visualizations and reports
- Monitor agent and office performance
"""

import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import datetime, date
import os
import glob
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class PDPTracker:
    """Main class for tracking Post Dated Payment performance"""
    
    def __init__(self, db_path: str = "pdp_tracker.db"):
        """Initialize the PDP Tracker with database connection"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
    def create_tables(self):
        """Create database tables for storing PDP data"""
        cursor = self.conn.cursor()
        
        # Historical baselines table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline_date DATE NOT NULL,
            baseline_name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Agent performance data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline_id INTEGER,
            agent_name TEXT NOT NULL,
            office TEXT,
            current_month_promised REAL DEFAULT 0,
            following_month_promised REAL DEFAULT 0,
            total_promised REAL DEFAULT 0,
            import_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (baseline_id) REFERENCES baselines (id)
        )
        ''')
        
        # Office totals
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS office_totals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline_id INTEGER,
            office TEXT NOT NULL,
            current_month_total REAL DEFAULT 0,
            following_month_total REAL DEFAULT 0,
            grand_total REAL DEFAULT 0,
            agent_count INTEGER DEFAULT 0,
            import_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (baseline_id) REFERENCES baselines (id)
        )
        ''')
        
        # Overall company totals
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_totals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline_id INTEGER,
            total_current_month REAL DEFAULT 0,
            total_following_month REAL DEFAULT 0,
            grand_total REAL DEFAULT 0,
            total_agents INTEGER DEFAULT 0,
            total_offices INTEGER DEFAULT 0,
            import_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (baseline_id) REFERENCES baselines (id)
        )
        ''')
        
        self.conn.commit()
    
    def create_baseline(self, name: str, description: str = "") -> int:
        """Create a new baseline for tracking progress"""
        cursor = self.conn.cursor()
        baseline_date = date.today()
        
        cursor.execute('''
        INSERT INTO baselines (baseline_date, baseline_name, description)
        VALUES (?, ?, ?)
        ''', (baseline_date, name, description))
        
        baseline_id = cursor.lastrowid
        self.conn.commit()
        
        print(f"✅ Created baseline '{name}' with ID {baseline_id} on {baseline_date}")
        return baseline_id
    
    def import_excel_report(self, file_path: str, baseline_id: Optional[int] = None) -> bool:
        """Import data from Excel report file"""
        try:
            # Read the Excel file - try different sheet names commonly used
            possible_sheets = ['Sheet1', 'Data', 'Report', 'CollectorPerformance', 0]
            df = None
            
            for sheet in possible_sheets:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    break
                except:
                    continue
            
            if df is None:
                print(f"❌ Could not read Excel file: {file_path}")
                return False
            
            # If no baseline_id provided, create one automatically
            if baseline_id is None:
                baseline_name = f"Import_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                baseline_id = self.create_baseline(baseline_name, f"Auto-imported from {os.path.basename(file_path)}")
            
            return self._process_dataframe(df, baseline_id, file_path)
            
        except Exception as e:
            print(f"❌ Error importing Excel file: {e}")
            return False
    
    def _process_dataframe(self, df: pd.DataFrame, baseline_id: int, file_path: str) -> bool:
        """Process the dataframe and extract PDP data"""
        try:
            import_date = date.today()
            cursor = self.conn.cursor()
            
            # Print dataframe info for debugging
            print(f"📊 Processing data with {len(df)} rows and {len(df.columns)} columns")
            print(f"Columns: {list(df.columns)}")
            
            # Try to identify relevant columns (flexible column name matching)
            agent_col = self._find_column(df, ['agent', 'collector', 'name', 'employee'])
            office_col = self._find_column(df, ['office', 'location', 'branch', 'dept'])
            current_col = self._find_column(df, ['current', 'this month', 'current month'])
            following_col = self._find_column(df, ['following', 'next month', 'following month'])
            
            if not agent_col:
                print("❌ Could not identify agent column")
                return False
            
            # Process agent-level data
            agent_count = 0
            office_totals = {}
            
            for _, row in df.iterrows():
                agent_name = str(row[agent_col]).strip()
                if agent_name.lower() in ['nan', 'total', 'grand total', '']:
                    continue
                
                office = str(row[office_col]).strip() if office_col else 'Unknown'
                current_promised = self._safe_float(row[current_col]) if current_col else 0
                following_promised = self._safe_float(row[following_col]) if following_col else 0
                total_promised = current_promised + following_promised
                
                # Insert agent performance
                cursor.execute('''
                INSERT INTO agent_performance 
                (baseline_id, agent_name, office, current_month_promised, 
                 following_month_promised, total_promised, import_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (baseline_id, agent_name, office, current_promised, 
                     following_promised, total_promised, import_date))
                
                agent_count += 1
                
                # Accumulate office totals
                if office not in office_totals:
                    office_totals[office] = {
                        'current': 0, 'following': 0, 'agents': 0
                    }
                office_totals[office]['current'] += current_promised
                office_totals[office]['following'] += following_promised
                office_totals[office]['agents'] += 1
            
            # Insert office totals
            for office, totals in office_totals.items():
                cursor.execute('''
                INSERT INTO office_totals 
                (baseline_id, office, current_month_total, following_month_total, 
                 grand_total, agent_count, import_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (baseline_id, office, totals['current'], totals['following'],
                     totals['current'] + totals['following'], totals['agents'], import_date))
            
            # Insert company totals
            total_current = sum(t['current'] for t in office_totals.values())
            total_following = sum(t['following'] for t in office_totals.values())
            grand_total = total_current + total_following
            
            cursor.execute('''
            INSERT INTO company_totals 
            (baseline_id, total_current_month, total_following_month, 
             grand_total, total_agents, total_offices, import_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (baseline_id, total_current, total_following, grand_total,
                 agent_count, len(office_totals), import_date))
            
            self.conn.commit()
            
            print(f"✅ Successfully imported data for {agent_count} agents across {len(office_totals)} offices")
            print(f"💰 Total Current Month: ${total_current:,.2f}")
            print(f"💰 Total Following Month: ${total_following:,.2f}")
            print(f"💰 Grand Total: ${grand_total:,.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing dataframe: {e}")
            return False
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Find a column that matches one of the possible names (case-insensitive)"""
        for col in df.columns:
            col_lower = str(col).lower()
            for name in possible_names:
                if name.lower() in col_lower:
                    return col
        return None
    
    def _safe_float(self, value) -> float:
        """Safely convert value to float"""
        try:
            if pd.isna(value):
                return 0.0
            return float(str(value).replace('$', '').replace(',', ''))
        except:
            return 0.0
    
    def get_baselines(self) -> pd.DataFrame:
        """Get all available baselines"""
        return pd.read_sql_query('''
        SELECT id, baseline_date, baseline_name, description, created_at
        FROM baselines
        ORDER BY baseline_date DESC
        ''', self.conn)
    
    def compare_baselines(self, baseline1_id: int, baseline2_id: int) -> Dict:
        """Compare two baselines to show improvement"""
        cursor = self.conn.cursor()
        
        # Get baseline info
        baseline1 = cursor.execute('SELECT * FROM baselines WHERE id = ?', (baseline1_id,)).fetchone()
        baseline2 = cursor.execute('SELECT * FROM baselines WHERE id = ?', (baseline2_id,)).fetchone()
        
        if not baseline1 or not baseline2:
            return {"error": "One or both baselines not found"}
        
        # Get company totals for comparison
        totals1 = cursor.execute('SELECT * FROM company_totals WHERE baseline_id = ?', (baseline1_id,)).fetchone()
        totals2 = cursor.execute('SELECT * FROM company_totals WHERE baseline_id = ?', (baseline2_id,)).fetchone()
        
        if not totals1 or not totals2:
            return {"error": "Company totals not found for one or both baselines"}
        
        # Calculate improvements
        current_improvement = totals2[2] - totals1[2]  # total_current_month
        following_improvement = totals2[3] - totals1[3]  # total_following_month
        grand_improvement = totals2[4] - totals1[4]  # grand_total
        agent_change = totals2[5] - totals1[5]  # total_agents
        
        return {
            "baseline1": {"name": baseline1[2], "date": baseline1[1], "grand_total": totals1[4]},
            "baseline2": {"name": baseline2[2], "date": baseline2[1], "grand_total": totals2[4]},
            "improvements": {
                "current_month": current_improvement,
                "following_month": following_improvement,
                "grand_total": grand_improvement,
                "agent_change": agent_change,
                "current_month_percent": (current_improvement / totals1[2] * 100) if totals1[2] > 0 else 0,
                "following_month_percent": (following_improvement / totals1[3] * 100) if totals1[3] > 0 else 0,
                "grand_total_percent": (grand_improvement / totals1[4] * 100) if totals1[4] > 0 else 0
            }
        }
    
    def generate_progress_report(self, baseline_id: Optional[int] = None) -> str:
        """Generate a comprehensive progress report"""
        if baseline_id is None:
            # Get the most recent baseline
            baseline = self.conn.execute('SELECT id FROM baselines ORDER BY created_at DESC LIMIT 1').fetchone()
            if not baseline:
                return "❌ No baselines found. Please import data first."
            baseline_id = baseline[0]
        
        # Get baseline info
        baseline_info = self.conn.execute('SELECT * FROM baselines WHERE id = ?', (baseline_id,)).fetchone()
        company_total = self.conn.execute('SELECT * FROM company_totals WHERE baseline_id = ?', (baseline_id,)).fetchone()
        
        report = f"""
📊 POST DATED PAYMENT (PDP) PROGRESS REPORT
{'='*50}

📅 Baseline: {baseline_info[2]}
📅 Date: {baseline_info[1]}
📝 Description: {baseline_info[3]}

💰 CURRENT TOTALS:
• Current Month Promised: ${company_total[2]:,.2f}
• Following Month Promised: ${company_total[3]:,.2f}
• Grand Total: ${company_total[4]:,.2f}

👥 TEAM METRICS:
• Total Agents: {company_total[5]}
• Total Offices: {company_total[6]}
• Average per Agent: ${company_total[4]/company_total[5]:,.2f}

"""
        
        # Get office breakdown
        office_data = pd.read_sql_query('''
        SELECT office, current_month_total, following_month_total, 
               grand_total, agent_count
        FROM office_totals 
        WHERE baseline_id = ?
        ORDER BY grand_total DESC
        ''', self.conn, params=(baseline_id,))
        
        if not office_data.empty:
            report += "🏢 OFFICE BREAKDOWN:\n"
            for _, office in office_data.iterrows():
                report += f"• {office['office']}: ${office['grand_total']:,.2f} ({office['agent_count']} agents)\n"
        
        return report
    
    def create_visualizations(self, baseline_id: Optional[int] = None):
        """Create visualizations for the PDP data"""
        if baseline_id is None:
            baseline = self.conn.execute('SELECT id FROM baselines ORDER BY created_at DESC LIMIT 1').fetchone()
            if not baseline:
                print("❌ No baselines found")
                return
            baseline_id = baseline[0]
        
        # Set up the plotting style
        plt.style.use('default')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Post Dated Payment (PDP) Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Office Totals Bar Chart
        office_data = pd.read_sql_query('''
        SELECT office, grand_total, agent_count
        FROM office_totals 
        WHERE baseline_id = ?
        ORDER BY grand_total DESC
        ''', self.conn, params=(baseline_id,))
        
        if not office_data.empty:
            ax1.bar(office_data['office'], office_data['grand_total'])
            ax1.set_title('Total Promised Payments by Office')
            ax1.set_ylabel('Total Amount ($)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Format y-axis as currency
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # 2. Current vs Following Month Comparison
        company_data = pd.read_sql_query('''
        SELECT total_current_month, total_following_month
        FROM company_totals 
        WHERE baseline_id = ?
        ''', self.conn, params=(baseline_id,))
        
        if not company_data.empty:
            categories = ['Current Month', 'Following Month']
            values = [company_data.iloc[0]['total_current_month'], 
                     company_data.iloc[0]['total_following_month']]
            
            ax2.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Current vs Following Month Distribution')
        
        # 3. Agent Performance (Top 10)
        agent_data = pd.read_sql_query('''
        SELECT agent_name, total_promised, office
        FROM agent_performance 
        WHERE baseline_id = ?
        ORDER BY total_promised DESC
        LIMIT 10
        ''', self.conn, params=(baseline_id,))
        
        if not agent_data.empty:
            ax3.barh(agent_data['agent_name'], agent_data['total_promised'])
            ax3.set_title('Top 10 Agents by Total Promised')
            ax3.set_xlabel('Total Amount ($)')
            ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # 4. Office Agent Count
        if not office_data.empty:
            ax4.bar(office_data['office'], office_data['agent_count'])
            ax4.set_title('Number of Agents by Office')
            ax4.set_ylabel('Agent Count')
            ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save the plot
        filename = f'pdp_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Visualizations saved as: {filename}")
        plt.show()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function to demonstrate usage"""
    print("🚀 PDP Tracker Tool - Post Dated Payment Analysis")
    print("=" * 50)
    
    tracker = PDPTracker()
    
    # Example usage
    print("\n📋 Available Commands:")
    print("1. Import Excel report")
    print("2. Create baseline")
    print("3. View baselines")
    print("4. Generate progress report")
    print("5. Create visualizations")
    print("6. Compare baselines")
    
    # Auto-import any Excel files in current directory
    excel_files = glob.glob("*.xlsx")
    if excel_files:
        print(f"\n📁 Found {len(excel_files)} Excel files:")
        for i, file in enumerate(excel_files):
            print(f"   {i+1}. {file}")
        
        # For demo purposes, let's create a baseline and try to import the first file
        if len(excel_files) > 0:
            baseline_id = tracker.create_baseline(
                "Initial Analysis", 
                "Starting point for PDP tracking analysis"
            )
            
            success = tracker.import_excel_report(excel_files[0], baseline_id)
            if success:
                print(tracker.generate_progress_report(baseline_id))
                tracker.create_visualizations(baseline_id)
    
    tracker.close()

if __name__ == "__main__":
    main() 