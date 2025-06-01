# DesmosPixelArt: Image to Desmos Art Converter

Convert your images into pixel art displayed in the Desmos graphing calculator using this Python script.

---

## Requirements

- Python 3.7+
- Packages: `opencv-python`, `selenium`, `numpy`
- Google Chrome or Microsoft Edge browser
- Corresponding WebDriver (ChromeDriver or Edge WebDriver) matching your browser version

---

## Installation

1. **Download the script**

```bash
git clone https://github.com/zmtrxq/desmos-pixel-art.git
cd desmos-pixel-art
````

Or download `desmospixelart.py` directly.

2. **Set up a Python virtual environment (optional but recommended)**

```bash
python -m venv venv
# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install opencv-python selenium numpy
```

4. **Download and set up WebDriver**

Download ChromeDriver or Edge WebDriver matching your browser version and either add it to your system PATH or note its location.

---

## Configuration

Edit `desmospixelart.py` and set these variables at the bottom:

```python
WEBDRIVER_PATH = None  # Full path if WebDriver is not in PATH
BROWSER_TO_USE = "chrome"  # "chrome" or "edge"
IMAGE_FILE_PATH = r"path/to/your/image.png"  # Path to your image file
QUALITY_PIXELS = 32  # Output resolution (higher = more detail)
NUMBER_OF_COLORS = 16  # Number of colors for quantization; set to None to disable
```

* `QUALITY_PIXELS` controls the pixelation level.
* `NUMBER_OF_COLORS` applies color quantization to simplify colors.

---

## Usage

Run the script:

```bash
python desmospixelart.py
```

The browser will open, load Desmos, and render your image as pixel art automatically.
