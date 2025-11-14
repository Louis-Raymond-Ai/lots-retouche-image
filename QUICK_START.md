# 🚀 Quick Start Guide

Get started with Logo Processor in 3 simple steps!

## Step 1: Install Python (if not already installed)

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. **IMPORTANT**: During installation, check ☑️ "Add Python to PATH"
4. Click "Install Now"

## Step 2: Install Dependencies

Open Command Prompt in the project folder and run:

```cmd
pip install -r requirements.txt
```

**Or simply double-click `run.bat`** - it will install dependencies automatically!

## Step 3: Prepare and Run

### Prepare Files

1. **Add your logo files** to the `logos` folder:
   - `logo_x6.png`
   - `logo_x8.png`
   - `logo_x12.png`

2. **Add images to process** to the `input` folder:
   - Any JPG, JPEG, or PNG files
   - As many as you want!

### Run the Application

**Easiest way (Windows):**
- Double-click `run.bat`

**Alternative:**
- Double-click `main.py`
- Or run in Command Prompt: `python main.py`

### Follow the Prompts

1. Select which logo to apply (1, 2, or 3)
2. Confirm processing (press 'y')
3. Wait for completion
4. Find your processed images in the `output` folder!

## 📁 Folder Structure

```
logo_project/
├── input/          ← Put your images HERE
├── output/         ← Processed images appear HERE
├── logos/          ← Put your logo files HERE
├── main.py         ← RUN THIS (or run.bat)
└── config.yaml     ← Edit settings here
```

## ⚙️ Basic Configuration

Edit `config.yaml` to change:

- **Logo position**: Adjust `margins.right` and `margins.top`
- **Output quality**: Change `processing.jpeg_quality` (1-100)
- **File suffixes**: Modify `output.suffix_x6`, etc.

## 🆘 Common Issues

### "Python is not recognized"
→ Reinstall Python and check "Add Python to PATH"

### "No images found"
→ Make sure images are directly in the `input` folder

### "Logo not found"
→ Check that logo files are in `logos` folder with correct names

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`

## 💡 Tips

- **Large batches**: The tool can handle 1000+ images
- **Multiple runs**: You can run the tool multiple times with different logos
- **Original files**: Your original images in `input` are never modified
- **Quality**: Default quality (95) is excellent for most uses

## 📖 Need More Help?

See the full `README.md` for:
- Detailed configuration options
- Advanced usage
- Troubleshooting guide
- Performance tips

---

**That's it! You're ready to process images! 🎉**
