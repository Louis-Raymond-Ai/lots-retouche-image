# Logo Processor - Batch Logo Application Tool

A professional Python tool for applying logos (x6, x8, x12, etc.) to product images in batch. Designed for Windows and VS Code with easy configuration and folder-based processing.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

- **Batch Processing**: Process hundreds or thousands of images at once
- **Multiple Logo Types**: Support for x6, x8, x12, and custom logos
- **Folder-Based Workflow**: Simply drop images in the `input` folder
- **Configurable**: Easy YAML configuration for margins, quality, and paths
- **Transparent Logos**: Automatic transparency handling for seamless integration
- **High Quality**: LANCZOS resampling for best image quality
- **Windows Optimized**: Designed specifically for Windows and VS Code
- **User-Friendly**: Interactive command-line interface with progress feedback

## 📦 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (also compatible with macOS and Linux)
- **IDE**: Visual Studio Code (recommended) or any Python IDE

## 🚀 Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation by opening Command Prompt and typing:
   ```cmd
   python --version
   ```

### Step 2: Extract Project

1. Extract the `logo_project` folder to your desired location
2. Example: `C:\Users\YourName\Documents\logo_project`

### Step 3: Install Dependencies

Open Command Prompt or PowerShell in the project folder and run:

```cmd
cd path\to\logo_project
python -m pip install -r requirements.txt
```

**Alternative using VS Code:**
1. Open the project folder in VS Code
2. Open Terminal (Ctrl + `)
3. Run: `pip install -r requirements.txt`

## 🎯 Quick Start

### 1. Prepare Your Files

**Add Logo Files:**
- Place your logo files in the `logos` folder:
  - `logo_x6.png` - Logo with "x6" text
  - `logo_x8.png` - Logo with "x8" text
  - `logo_x12.png` - Logo with "x12" text

**Add Images to Process:**
- Place all product images in the `input` folder
- Supported formats: JPG, JPEG, PNG
- You can add as many images as needed

### 2. Run the Application

**Option A: Double-click (Windows)**
- Simply double-click `main.py`
- Windows will run it with Python automatically

**Option B: Command Line**
```cmd
python main.py
```

**Option C: VS Code**
1. Open `main.py` in VS Code
2. Press F5 or click "Run" → "Start Debugging"

### 3. Follow the Prompts

1. The application will show:
   - Number of images found
   - Available logos
2. Select which logo to apply (1, 2, or 3)
3. Confirm processing
4. Wait for completion
5. Find processed images in the `output` folder

## 📁 Project Structure

```
logo_project/
│
├── input/                  # Place your images here
│   ├── product1.jpg
│   ├── product2.jpg
│   └── ...
│
├── output/                 # Processed images appear here
│   ├── product1_x6.jpg
│   ├── product2_x6.jpg
│   └── ...
│
├── logos/                  # Place your logo files here
│   ├── logo_x6.png
│   ├── logo_x8.png
│   └── logo_x12.png
│
├── src/                    # Source code (don't modify)
│   ├── __init__.py
│   ├── logo_processor.py
│   └── config_loader.py
│
├── docs/                   # Additional documentation
│
├── main.py                 # Main script - RUN THIS
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## ⚙️ Configuration

Edit `config.yaml` to customize settings:

### Margins
```yaml
margins:
  right: 21  # Distance from right edge (pixels)
  top: 22    # Distance from top edge (pixels)
```

### Directories
```yaml
directories:
  input: "input"      # Input folder name
  output: "output"    # Output folder name
  logos: "logos"      # Logos folder name
```

### Processing Settings
```yaml
processing:
  jpeg_quality: 95           # Output quality (1-100)
  white_threshold: 250       # Logo detection threshold
  logo_padding: 3            # Padding around logo
```

### Output Settings
```yaml
output:
  format: "JPEG"             # Output format
  suffix_x6: "_x6"           # Suffix for x6 files
  suffix_x8: "_x8"           # Suffix for x8 files
  suffix_x12: "_x12"         # Suffix for x12 files
  preserve_original: true    # Keep original filename
```

## 📖 Usage

### Basic Usage

1. **Add images** to the `input` folder
2. **Run** `python main.py`
3. **Select** logo type
4. **Confirm** processing
5. **Check** `output` folder for results

### Processing Large Batches

The tool is optimized for large batches:
- ✅ 10 images: ~5 seconds
- ✅ 100 images: ~30 seconds
- ✅ 1000 images: ~5 minutes

### Using Different Logos

To use a different logo:
1. Create your logo as PNG with transparent background
2. Save it in the `logos` folder (e.g., `logo_x24.png`)
3. Add configuration in `config.yaml`:
   ```yaml
   logos:
     x24: "logos/logo_x24.png"
   output:
     suffix_x24: "_x24"
   ```

### Extracting Logo from Existing Image

If you have an image with a logo and want to extract it:

```python
from src.logo_processor import LogoProcessor

processor = LogoProcessor(margin_right=21, margin_top=22)
processor.extract_logo_from_image(
    image_path='example_with_logo.jpg',
    output_path='logos/logo_extracted.png'
)
```

## 🔧 Troubleshooting

### "No images found in input folder"
- **Solution**: Make sure images are directly in the `input` folder, not in subfolders
- Supported formats: .jpg, .jpeg, .png (case-insensitive)

### "Logo not found"
- **Solution**: Check that logo files are in the `logos` folder with correct names
- Required names: `logo_x6.png`, `logo_x8.png`, `logo_x12.png`
- Logos must be PNG format with transparent background

### "ModuleNotFoundError: No module named 'PIL'"
- **Solution**: Install dependencies: `pip install -r requirements.txt`

### Logo appears in wrong position
- **Solution**: Adjust margins in `config.yaml`:
  ```yaml
  margins:
    right: 25  # Increase to move logo left
    top: 30    # Increase to move logo down
  ```

### Output images are low quality
- **Solution**: Increase JPEG quality in `config.yaml`:
  ```yaml
  processing:
    jpeg_quality: 98  # Higher = better quality (max 100)
  ```

### Python not recognized
- **Solution**: Reinstall Python and check "Add Python to PATH" during installation
- Or use full path: `C:\Python311\python.exe main.py`

### Permission denied error
- **Solution**: Run Command Prompt as Administrator
- Or move project to a folder where you have write permissions

## 🎨 Creating Logo Files

### Requirements for Logo Files

1. **Format**: PNG with transparent background
2. **Content**: Black text on transparent background
3. **Size**: Approximately 93×97 pixels (will be auto-resized)
4. **Font**: Bold sans-serif font (e.g., Arial Bold, Helvetica Bold)

### Recommended Tools

- **Adobe Photoshop**: Professional option
- **GIMP**: Free alternative to Photoshop
- **Paint.NET**: Simple and free (Windows)
- **Canva**: Online tool with transparency support

### Example Logo Creation (GIMP)

1. Create new image: 100×100 pixels
2. Add transparent layer
3. Add text: "x6" in Arial Bold, 72pt
4. Color: Black (#000000)
5. Export as PNG with transparency

## 📊 Performance Tips

### For Large Batches (1000+ images)

1. **Close other applications** to free up RAM
2. **Use SSD** for input/output folders if possible
3. **Process in smaller batches** if memory is limited
4. **Disable antivirus scanning** for project folders temporarily

### Optimal Settings

```yaml
processing:
  jpeg_quality: 95  # Good balance of quality/size
  
advanced:
  batch_size: 10    # Process 10 at a time
  verbose: false    # Reduce console output
```

## 🆘 Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review `config.yaml` settings
3. Ensure all dependencies are installed
4. Check that Python version is 3.8+

## 📄 License

This project is proprietary software developed for internal use.

## 🔄 Version History

- **v1.0.0** (2025-01-13)
  - Initial release
  - Support for x6, x8, x12 logos
  - Batch processing
  - YAML configuration
  - Windows optimization

---

**Made with ❤️ for efficient product image processing**
