#!/usr/bin/env python
"""
Test Installation Script
Verifies that all dependencies are correctly installed
"""

import sys
import os

def test_python_version():
    """Test Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\nTesting dependencies...")
    
    dependencies = {
        'PIL': 'Pillow',
        'numpy': 'numpy',
        'yaml': 'PyYAML'
    }
    
    all_ok = True
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {package} (OK)")
        except ImportError:
            print(f"  ✗ {package} (NOT INSTALLED)")
            all_ok = False
    
    return all_ok

def test_project_structure():
    """Test project structure"""
    print("\nTesting project structure...")
    
    required_dirs = ['input', 'output', 'logos', 'src']
    required_files = ['main.py', 'config.yaml', 'requirements.txt']
    
    all_ok = True
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}/ folder (OK)")
        else:
            print(f"  ✗ {directory}/ folder (MISSING)")
            all_ok = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file} (OK)")
        else:
            print(f"  ✗ {file} (MISSING)")
            all_ok = False
    
    return all_ok

def test_imports():
    """Test importing project modules"""
    print("\nTesting project modules...")
    
    try:
        sys.path.insert(0, 'src')
        from logo_processor import LogoProcessor
        print("  ✓ LogoProcessor (OK)")
        
        from config_loader import ConfigLoader
        print("  ✓ ConfigLoader (OK)")
        
        return True
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("  LOGO PROCESSOR - INSTALLATION TEST")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Module Imports", test_imports()))
    
    print("\n" + "="*60)
    print("  TEST RESULTS")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60 + "\n")
    
    if all_passed:
        print("🎉 All tests passed! Installation is complete.")
        print("\nYou can now run the application:")
        print("  - Double-click: run.bat (Windows)")
        print("  - Command line: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Ensure Python 3.8+ is installed")
        print("  - Check that all project files are present")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
