# 📊 PDP Tracker - Post Dated Payment Analysis Tool

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A comprehensive tool designed to help sales teams track and analyze the performance of Post Dated Payments (PDP) and payfile improvements when implementing long-term payment arrangements.

![PDP Tracker Interface](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=PDP+Tracker+Dashboard)

> **Perfect for**: Sales teams implementing new payment strategies and need to track ROI and performance improvements over time.

## 🎯 Purpose

This tool helps you:
- **Track baseline performance** - Remember where you started on specific dates
- **Import Excel reports** - Automatically process your collector performance reports
- **Monitor improvements** - See if your new payment strategy is working
- **Compare progress** - Track changes between different time periods
- **Generate visualizations** - Create charts and graphs for presentations
- **Analyze trends** - Understand which agents and offices are performing best

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/pdp-tracker.git
cd pdp-tracker

# Run automated setup
python setup.py
```

### Option 2: Manual Setup

1. **Download or Clone**:
   ```bash
   git clone https://github.com/yourusername/pdp-tracker.git
   cd pdp-tracker
   ```

2. **Install Python** (if not already installed):
   - Download from [python.org](https://python.org/downloads/)
   - ✅ **Important**: Check "Add Python to PATH" during installation

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Tool**:
   ```bash
   python pdp_gui.py
   ```
   
   Or on Windows, double-click: `run_pdp_tracker.bat`

## 📊 How to Use

### Step 1: Create Your First Baseline
1. Open the GUI (`python pdp_gui.py`)
2. Go to the "📁 Import Reports" tab
3. Enter a meaningful baseline name (e.g., "July 2024 Start")
4. Add a description (e.g., "Starting point for new payment arrangement strategy")

### Step 2: Import Your Excel Report
1. Click "Browse..." to select your Excel file
2. The tool will automatically detect columns for:
   - Agent/Collector names
   - Office/Location
   - Current month promised payments
   - Following month promised payments
3. Click "Import Data"

### Step 3: View Your Progress
1. Go to the "📊 View Progress" tab
2. Select your baseline from the dropdown
3. Click "Generate Report" to see current totals and metrics

### Step 4: Track Improvements Over Time
1. Import new reports as the month progresses
2. Use the "📈 Compare Performance" tab to compare different time periods
3. See exactly how much your numbers have improved

### Step 5: Create Visualizations
1. Go to the "📊 Charts & Graphs" tab
2. Select a baseline and click "Create Charts"
3. Charts are saved as PNG files and include:
   - Office performance comparison
   - Current vs Following month breakdown
   - Top performing agents
   - Agent count by office

## 📁 File Structure

```
PDC Builder/
├── pdp_tracker.py          # Main tracking engine
├── pdp_gui.py              # User-friendly GUI interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── pdp_tracker.db         # Database (created automatically)
└── your_excel_files.xlsx  # Your collector reports
```

## 🔍 Features Explained

### Baseline Tracking
- **Purpose**: Remember your starting point on any given date
- **Example**: "On 7/28 you started with $50,000 promised payments, now you have $65,000"
- **Benefit**: Measure actual improvement, not just current numbers

### Automatic Excel Import
- **Supported formats**: .xlsx, .xls
- **Smart column detection**: Finds agent names, offices, and payment amounts automatically
- **Flexible structure**: Works with different report layouts

### Progress Comparison
- **Time-based tracking**: Compare any two baselines/dates
- **Percentage improvements**: See growth rates, not just dollar amounts
- **Agent-level details**: Identify top performers and areas needing attention

### Visual Reports
- **Office performance**: See which locations are excelling
- **Payment distribution**: Current vs future month breakdown
- **Top performers**: Identify your best agents
- **Trend analysis**: Understand patterns in your data

## 💡 Best Practices

### Creating Baselines
- **Use descriptive names**: "Month_Start_July2024" instead of "Baseline1"
- **Include context**: Note any special circumstances or changes
- **Regular snapshots**: Create baselines weekly or bi-weekly

### Data Import Tips
- **Consistent format**: Keep your Excel reports in the same structure
- **Clean data**: Remove any totally empty rows or summary rows at the bottom
- **Regular updates**: Import new data as payments are processed

### Comparing Performance
- **Meaningful timeframes**: Compare similar periods (week to week, month to month)
- **Account for external factors**: Note holidays, policy changes, etc.
- **Focus on trends**: Look for patterns, not just individual data points

## 🛠️ Troubleshooting

### Common Issues

**"Could not read Excel file"**
- Check that the file is not open in Excel
- Ensure the file format is .xlsx or .xls
- Verify the file is not corrupted

**"Could not identify agent column"**
- Make sure your Excel file has a column with agent/collector names
- Check that the column header contains words like "agent", "collector", or "name"

**"No baselines found"**
- You need to import at least one Excel file first
- Each import creates a baseline automatically

**Charts not displaying**
- Make sure matplotlib is installed: `pip install matplotlib`
- Check that you have data imported for the selected baseline

### Getting Help
1. **Check the status messages** in each tab for detailed error information
2. **Verify your Excel file structure** - it should have columns for agents and payment amounts
3. **Try a simple test** with a small Excel file first

## 📈 Understanding Your Results

### Key Metrics
- **Current Month Promised**: Payments expected this month
- **Following Month Promised**: Payments arranged for next month
- **Grand Total**: Sum of current and following month
- **Improvement Percentage**: How much you've grown from baseline

### Success Indicators
- **Increasing total promised payments**
- **Higher following month commitments** (indicates successful long-term arrangements)
- **Consistent agent performance** across time periods
- **Growing payfile** month over month

## 🎯 Strategic Use

### For Management
- Track ROI of new payment arrangement strategy
- Identify which offices/agents are adapting best
- Present clear before/after comparisons
- Make data-driven decisions about program expansion

### For Sales Teams
- See individual and team progress
- Understand impact of long-term payment strategies
- Motivate agents with clear improvement metrics
- Identify coaching opportunities

### For Analysis
- Export data for further analysis if needed
- Create custom date ranges for reporting
- Combine with other business metrics
- Track seasonal patterns and trends

---

## 📞 Support

This tool was designed specifically for your Post Dated Payment tracking needs. The database stores all your historical data safely, so you can always go back and analyze previous periods or create new comparisons as your strategy evolves.

**Remember**: The goal is to see if your new long-term payment arrangement strategy is working. Look for increasing "Following Month" commitments and overall payfile growth over time!

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Guide
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If this tool helps your sales team track PDP performance, please give it a ⭐️ on GitHub!

## 📞 Contact & Support

- 🐛 **Bug Reports**: [Create an Issue](../../issues)
- 💡 **Feature Requests**: [Create an Issue](../../issues)
- 📧 **Questions**: Open a [Discussion](../../discussions)

## 📊 Project Status

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/pdp-tracker)
![GitHub issues](https://img.shields.io/github/issues/yourusername/pdp-tracker)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/pdp-tracker)

---

<div align="center">
  <strong>Built with ❤️ for sales teams implementing innovative payment strategies</strong>
</div> 