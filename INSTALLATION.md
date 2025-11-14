# 📥 Installation Guide for Windows

Complete step-by-step installation guide for Logo Processor on Windows with VS Code.

## Prerequisites

- Windows 10 or Windows 11
- Administrator access (for Python installation)
- Internet connection (for downloading Python and packages)

## Step-by-Step Installation

### 1. Install Python

#### Download Python

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click on "Download Python 3.11.x" (or latest 3.x version)
3. Save the installer to your Downloads folder

#### Install Python

1. **Run the installer** (double-click the downloaded file)
2. **IMPORTANT**: ☑️ Check "Add Python to PATH" at the bottom
3. Click "Install Now"
4. Wait for installation to complete
5. Click "Close" when finished

#### Verify Python Installation

1. Press `Win + R` to open Run dialog
2. Type `cmd` and press Enter
3. In the Command Prompt, type:
   ```cmd
   python --version
   ```
4. You should see: `Python 3.11.x` (or your version)
5. If you see an error, restart your computer and try again

### 2. Install Visual Studio Code (Optional but Recommended)

#### Download VS Code

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click "Download for Windows"
3. Run the installer
4. Follow the installation wizard (use default settings)

#### Install Python Extension for VS Code

1. Open VS Code
2. Click on Extensions icon (or press `Ctrl+Shift+X`)
3. Search for "Python"
4. Click "Install" on the official Python extension by Microsoft

### 3. Extract the Project

1. **Locate the ZIP file**: `logo_project_windows.zip`
2. **Right-click** on the ZIP file
3. Select **"Extract All..."**
4. Choose a location, for example:
   - `C:\Users\YourName\Documents\logo_project`
   - Or anywhere you have write permissions
5. Click **"Extract"**

### 4. Install Project Dependencies

#### Method A: Using the Batch File (Easiest)

1. Open the extracted `logo_project` folder
2. **Double-click** `run.bat`
3. It will automatically install dependencies and run the application

#### Method B: Using Command Prompt

1. Open the `logo_project` folder
2. Hold `Shift` and **right-click** in the folder
3. Select **"Open PowerShell window here"** or **"Open Command window here"**
4. Type:
   ```cmd
   pip install -r requirements.txt
   ```
5. Press Enter and wait for installation to complete

#### Method C: Using VS Code

1. Open VS Code
2. Click **File** → **Open Folder**
3. Select the `logo_project` folder
4. Press `` Ctrl+` `` to open Terminal
5. Type:
   ```cmd
   pip install -r requirements.txt
   ```
6. Press Enter

### 5. Verify Installation

1. In the `logo_project` folder, **double-click** `test_installation.py`
2. A window will open showing test results
3. All tests should show "✓ PASS"
4. If any test fails, see [Troubleshooting](#troubleshooting) below

## Folder Setup

After installation, set up your folders:

### 1. Add Logo Files

1. Open the `logos` folder
2. Add your logo files:
   - `logo_x6.png` - Logo with "x6" text
   - `logo_x8.png` - Logo with "x8" text  
   - `logo_x12.png` - Logo with "x12" text
3. Logos must be PNG format with transparent background

### 2. Add Images to Process

1. Open the `input` folder
2. Copy all product images you want to process
3. Supported formats: JPG, JPEG, PNG
4. You can add hundreds or thousands of images

## Running the Application

### Method 1: Double-Click (Easiest)

- Double-click `run.bat` in the project folder
- Follow the on-screen prompts

### Method 2: From Command Prompt

1. Open Command Prompt in the project folder
2. Type:
   ```cmd
   python main.py
   ```
3. Press Enter

### Method 3: From VS Code

1. Open the project in VS Code
2. Open `main.py`
3. Press `F5` or click **Run** → **Start Debugging**
4. Or press `Ctrl+F5` for **Run Without Debugging**

## Troubleshooting

### "Python is not recognized as an internal or external command"

**Solution:**
1. Reinstall Python
2. **Make sure to check** ☑️ "Add Python to PATH" during installation
3. Restart your computer after installation

### "pip is not recognized"

**Solution:**
```cmd
python -m pip install -r requirements.txt
```

### "Access is denied" or "Permission denied"

**Solution:**
1. Run Command Prompt as Administrator:
   - Search for "cmd" in Start Menu
   - Right-click "Command Prompt"
   - Select "Run as administrator"
2. Or move the project to a folder where you have write permissions

### "ModuleNotFoundError: No module named 'PIL'"

**Solution:**
```cmd
pip install Pillow
```

### Dependencies won't install

**Solution:**
1. Update pip:
   ```cmd
   python -m pip install --upgrade pip
   ```
2. Try installing dependencies again:
   ```cmd
   pip install -r requirements.txt
   ```

### VS Code doesn't recognize Python

**Solution:**
1. Press `Ctrl+Shift+P` in VS Code
2. Type "Python: Select Interpreter"
3. Select your Python installation
4. Restart VS Code

## Uninstallation

To uninstall the project:

1. Delete the `logo_project` folder
2. (Optional) Uninstall Python from Windows Settings → Apps
3. (Optional) Uninstall VS Code from Windows Settings → Apps

## System Requirements

### Minimum Requirements

- **OS**: Windows 10 (64-bit)
- **RAM**: 4 GB
- **Disk Space**: 500 MB for project + dependencies
- **Python**: 3.8 or higher

### Recommended Requirements

- **OS**: Windows 11 (64-bit)
- **RAM**: 8 GB or more
- **Disk Space**: 2 GB free space
- **Python**: 3.11 or higher
- **SSD**: For faster processing of large batches

## Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](README.md) file
2. Read the [QUICK_START.md](QUICK_START.md) guide
3. Run `test_installation.py` to diagnose issues
4. Check that all files are present and not corrupted

## Next Steps

After successful installation:

1. Read [QUICK_START.md](QUICK_START.md) for basic usage
2. Review [README.md](README.md) for detailed documentation
3. Edit `config.yaml` to customize settings
4. Add your logos and images
5. Run the application!

---

**Installation complete! You're ready to process images! 🎉**
