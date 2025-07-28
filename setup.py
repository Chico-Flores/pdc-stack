#!/usr/bin/env python3
"""
Setup script for PDP Tracker
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    required_modules = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'sqlite3', 'tkinter', 'openpyxl'
    ]
    
    failed_imports = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ All modules imported successfully!")
        return True

def create_test_data():
    """Create a sample Excel file for testing"""
    print("📊 Creating sample test data...")
    try:
        import pandas as pd
        
        # Sample data
        sample_data = {
            'Agent Name': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson', 'Tom Brown'],
            'Office': ['Downtown', 'Downtown', 'Uptown', 'Uptown', 'West Side'],
            'Current Month Promised': [5000, 7500, 6200, 8900, 4300],
            'Following Month Promised': [3200, 4100, 5500, 6700, 2800]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel('sample_collector_report.xlsx', index=False)
        print("✅ Sample data created: sample_collector_report.xlsx")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 PDP Tracker Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Setup failed during import testing")
        sys.exit(1)
    
    # Create sample data
    create_test_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the GUI: python pdp_gui.py")
    print("2. Import your Excel files or use the sample: sample_collector_report.xlsx")
    print("3. Start tracking your PDP performance!")
    
    # Offer to launch GUI
    try:
        response = input("\n🚀 Launch the GUI now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("Launching PDP Tracker GUI...")
            import pdp_gui
            pdp_gui.main()
    except KeyboardInterrupt:
        print("\n👋 Setup complete! Launch when ready with: python pdp_gui.py")

if __name__ == "__main__":
    main() 