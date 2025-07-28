#!/usr/bin/env python3
"""
PDP Tracker GUI - User-friendly interface for Post Dated Payment tracking
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from datetime import datetime
import os
from pdp_tracker import PDPTracker
import pandas as pd

class PDPTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDP Tracker - Post Dated Payment Analysis Tool")
        self.root.geometry("800x600")
        
        # Initialize tracker
        self.tracker = PDPTracker()
        
        # Create GUI elements
        self.create_widgets()
        
        # Refresh baselines on startup
        self.refresh_baselines()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Import Data
        self.import_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.import_frame, text="📁 Import Reports")
        self.create_import_tab()
        
        # Tab 2: View Progress
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="📊 View Progress")
        self.create_progress_tab()
        
        # Tab 3: Compare Baselines
        self.compare_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compare_frame, text="📈 Compare Performance")
        self.create_compare_tab()
        
        # Tab 4: Visualizations
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="📊 Charts & Graphs")
        self.create_viz_tab()
    
    def create_import_tab(self):
        """Create the import data tab"""
        # Title
        title_label = tk.Label(self.import_frame, text="Import Excel Reports", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.import_frame, 
                               text="1. Create a baseline name\n2. Select your Excel report file\n3. Click Import",
                               font=("Arial", 10), justify=tk.LEFT)
        instructions.pack(pady=5)
        
        # Baseline creation frame
        baseline_frame = ttk.LabelFrame(self.import_frame, text="Create New Baseline")
        baseline_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(baseline_frame, text="Baseline Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.baseline_name_entry = tk.Entry(baseline_frame, width=30)
        self.baseline_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(baseline_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.baseline_desc_entry = tk.Entry(baseline_frame, width=50)
        self.baseline_desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.import_frame, text="Select Excel File")
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.file_path_var = tk.StringVar()
        tk.Label(file_frame, text="Selected File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        file_label = tk.Label(file_frame, textvariable=self.file_path_var, 
                             wraplength=400, justify=tk.LEFT)
        file_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        tk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(file_frame, text="Import Data", command=self.import_data, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)
        
        # Status area
        self.import_status = scrolledtext.ScrolledText(self.import_frame, height=10, width=70)
        self.import_status.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add current date/time as default baseline name
        default_name = f"Baseline_{datetime.now().strftime('%Y%m%d_%H%M')}"
        self.baseline_name_entry.insert(0, default_name)
    
    def create_progress_tab(self):
        """Create the progress viewing tab"""
        title_label = tk.Label(self.progress_frame, text="Progress Reports", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Baseline selection
        selection_frame = ttk.LabelFrame(self.progress_frame, text="Select Baseline")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(selection_frame, text="Baseline:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.progress_baseline_var = tk.StringVar()
        self.progress_baseline_combo = ttk.Combobox(selection_frame, textvariable=self.progress_baseline_var, 
                                                   width=40, state="readonly")
        self.progress_baseline_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(selection_frame, text="Generate Report", command=self.generate_progress_report,
                 bg="#2196F3", fg="white").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(selection_frame, text="Refresh List", command=self.refresh_baselines,
                 bg="#FF9800", fg="white").grid(row=0, column=3, padx=5, pady=5)
        
        # Report display
        self.progress_report = scrolledtext.ScrolledText(self.progress_frame, height=20, width=80)
        self.progress_report.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_compare_tab(self):
        """Create the comparison tab"""
        title_label = tk.Label(self.compare_frame, text="Compare Baselines", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Baseline selection frame
        selection_frame = ttk.LabelFrame(self.compare_frame, text="Select Baselines to Compare")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(selection_frame, text="Baseline 1 (Starting):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.compare_baseline1_var = tk.StringVar()
        self.compare_baseline1_combo = ttk.Combobox(selection_frame, textvariable=self.compare_baseline1_var, 
                                                   width=30, state="readonly")
        self.compare_baseline1_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(selection_frame, text="Baseline 2 (Current):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.compare_baseline2_var = tk.StringVar()
        self.compare_baseline2_combo = ttk.Combobox(selection_frame, textvariable=self.compare_baseline2_var, 
                                                   width=30, state="readonly")
        self.compare_baseline2_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(selection_frame, text="Compare", command=self.compare_baselines,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=2, padx=5, pady=5)
        
        # Comparison results
        self.compare_results = scrolledtext.ScrolledText(self.compare_frame, height=20, width=80)
        self.compare_results.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_viz_tab(self):
        """Create the visualization tab"""
        title_label = tk.Label(self.viz_frame, text="Charts & Visualizations", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Baseline selection
        selection_frame = ttk.LabelFrame(self.viz_frame, text="Select Baseline for Charts")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(selection_frame, text="Baseline:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.viz_baseline_var = tk.StringVar()
        self.viz_baseline_combo = ttk.Combobox(selection_frame, textvariable=self.viz_baseline_var, 
                                              width=40, state="readonly")
        self.viz_baseline_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(selection_frame, text="Create Charts", command=self.create_visualizations,
                 bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        
        # Instructions
        instructions_text = """
Instructions for Charts:
• Select a baseline from the dropdown
• Click 'Create Charts' to generate visualizations
• Charts will be saved as PNG files and displayed
• Charts include: Office totals, Current vs Following month, Top agents, Agent counts
        """
        
        instructions_label = tk.Label(self.viz_frame, text=instructions_text, 
                                     justify=tk.LEFT, font=("Arial", 10))
        instructions_label.pack(padx=20, pady=10)
        
        # Status area
        self.viz_status = scrolledtext.ScrolledText(self.viz_frame, height=15, width=80)
        self.viz_status.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def browse_file(self):
        """Browse for Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel Report File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(os.path.basename(file_path))
            self.selected_file_path = file_path
    
    def import_data(self):
        """Import data from selected Excel file"""
        if not hasattr(self, 'selected_file_path'):
            messagebox.showerror("Error", "Please select an Excel file first")
            return
        
        baseline_name = self.baseline_name_entry.get().strip()
        if not baseline_name:
            messagebox.showerror("Error", "Please enter a baseline name")
            return
        
        baseline_desc = self.baseline_desc_entry.get().strip()
        
        # Clear status
        self.import_status.delete(1.0, tk.END)
        self.import_status.insert(tk.END, "Starting import...\n")
        self.import_status.update()
        
        def import_thread():
            try:
                # Create baseline
                baseline_id = self.tracker.create_baseline(baseline_name, baseline_desc)
                self.import_status.insert(tk.END, f"✅ Created baseline: {baseline_name}\n")
                self.import_status.update()
                
                # Import data
                success = self.tracker.import_excel_report(self.selected_file_path, baseline_id)
                
                if success:
                    self.import_status.insert(tk.END, "✅ Data imported successfully!\n")
                    self.refresh_baselines()
                    
                    # Generate initial report
                    report = self.tracker.generate_progress_report(baseline_id)
                    self.import_status.insert(tk.END, "\n" + report)
                else:
                    self.import_status.insert(tk.END, "❌ Import failed. Check file format.\n")
                
                self.import_status.see(tk.END)
                
            except Exception as e:
                self.import_status.insert(tk.END, f"❌ Error: {str(e)}\n")
                self.import_status.see(tk.END)
        
        # Run import in separate thread to prevent GUI freezing
        thread = threading.Thread(target=import_thread)
        thread.daemon = True
        thread.start()
    
    def refresh_baselines(self):
        """Refresh the baseline dropdown lists"""
        try:
            baselines_df = self.tracker.get_baselines()
            baseline_options = []
            self.baseline_dict = {}
            
            for _, row in baselines_df.iterrows():
                display_text = f"{row['baseline_name']} ({row['baseline_date']})"
                baseline_options.append(display_text)
                self.baseline_dict[display_text] = row['id']
            
            # Update all combo boxes
            self.progress_baseline_combo['values'] = baseline_options
            self.compare_baseline1_combo['values'] = baseline_options
            self.compare_baseline2_combo['values'] = baseline_options
            self.viz_baseline_combo['values'] = baseline_options
            
            # Select most recent by default
            if baseline_options:
                self.progress_baseline_combo.set(baseline_options[0])
                self.viz_baseline_combo.set(baseline_options[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh baselines: {str(e)}")
    
    def generate_progress_report(self):
        """Generate progress report for selected baseline"""
        selected = self.progress_baseline_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a baseline")
            return
        
        baseline_id = self.baseline_dict[selected]
        
        try:
            report = self.tracker.generate_progress_report(baseline_id)
            self.progress_report.delete(1.0, tk.END)
            self.progress_report.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def compare_baselines(self):
        """Compare two selected baselines"""
        baseline1 = self.compare_baseline1_var.get()
        baseline2 = self.compare_baseline2_var.get()
        
        if not baseline1 or not baseline2:
            messagebox.showerror("Error", "Please select both baselines")
            return
        
        if baseline1 == baseline2:
            messagebox.showerror("Error", "Please select different baselines")
            return
        
        baseline1_id = self.baseline_dict[baseline1]
        baseline2_id = self.baseline_dict[baseline2]
        
        try:
            comparison = self.tracker.compare_baselines(baseline1_id, baseline2_id)
            
            if "error" in comparison:
                messagebox.showerror("Error", comparison["error"])
                return
            
            # Format comparison report
            report = f"""
🔍 BASELINE COMPARISON REPORT
{'='*50}

📊 BASELINE 1 (Starting Point):
• Name: {comparison['baseline1']['name']}
• Date: {comparison['baseline1']['date']}
• Grand Total: ${comparison['baseline1']['grand_total']:,.2f}

📊 BASELINE 2 (Current):
• Name: {comparison['baseline2']['name']}
• Date: {comparison['baseline2']['date']}
• Grand Total: ${comparison['baseline2']['grand_total']:,.2f}

📈 IMPROVEMENTS:
• Current Month Change: ${comparison['improvements']['current_month']:,.2f} ({comparison['improvements']['current_month_percent']:.1f}%)
• Following Month Change: ${comparison['improvements']['following_month']:,.2f} ({comparison['improvements']['following_month_percent']:.1f}%)
• Grand Total Change: ${comparison['improvements']['grand_total']:,.2f} ({comparison['improvements']['grand_total_percent']:.1f}%)
• Agent Count Change: {comparison['improvements']['agent_change']}

{'🎉 POSITIVE IMPROVEMENT!' if comparison['improvements']['grand_total'] > 0 else '⚠️ NEEDS ATTENTION' if comparison['improvements']['grand_total'] < 0 else '➡️ NO CHANGE'}
"""
            
            self.compare_results.delete(1.0, tk.END)
            self.compare_results.insert(tk.END, report)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare baselines: {str(e)}")
    
    def create_visualizations(self):
        """Create visualizations for selected baseline"""
        selected = self.viz_baseline_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a baseline")
            return
        
        baseline_id = self.baseline_dict[selected]
        
        self.viz_status.delete(1.0, tk.END)
        self.viz_status.insert(tk.END, "Creating visualizations...\n")
        self.viz_status.update()
        
        def viz_thread():
            try:
                # Redirect print statements to GUI
                import sys
                from io import StringIO
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                self.tracker.create_visualizations(baseline_id)
                
                # Get output and restore stdout
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                self.viz_status.insert(tk.END, "✅ Visualizations created successfully!\n")
                self.viz_status.insert(tk.END, output)
                self.viz_status.see(tk.END)
                
            except Exception as e:
                self.viz_status.insert(tk.END, f"❌ Error creating visualizations: {str(e)}\n")
                self.viz_status.see(tk.END)
        
        thread = threading.Thread(target=viz_thread)
        thread.daemon = True
        thread.start()
    
    def on_closing(self):
        """Handle window closing"""
        self.tracker.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PDPTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 