# Img2Desmos: Image to Desmos Art Converter 🎨

Transform your favorite images into stunning Desmos "pixel art" with this Python script! `Img2Desmos` automates the process of converting images into a series of Desmos expressions that render as colored rectangles, effectively creating pixelated artwork directly in the Desmos graphing calculator.

This enhanced version features:
*   **Efficient Rectangle Merging:** Intelligently combines adjacent pixels of the same color into larger rectangles, drastically reducing the number of Desmos expressions for smoother performance.
*   **Optional Color Quantization:** Simplify complex images by reducing their color palette using k-means clustering. This creates a stylized, posterized effect and further optimizes the number of expressions for intricate images like photographs.
*   **Reliable Desmos Integration:** Utilizes a carefully tested LaTeX format (`\operatorname{polygon}`) and JavaScript command structure for compatibility with the Desmos `Calc` API.
*   **Browser Automation:** Employs Selenium to control a web browser (Chrome by default, Edge supported) for a seamless, automated experience.

## ✨ Features

*   🖼️ Convert common image formats (PNG, JPG, etc.) to Desmos art.
*   🧩 Merge same-colored pixels into larger rectangles (fewer expressions, better performance).
*   🎨 Optional color quantization to reduce and unify image colors.
*   ⚙️ Adjustable "quality" to control the resolution of the Desmos output.
*   🚀 Automates browser interaction: opens Desmos, inputs expressions, sets viewport.
*   💻 Cross-platform (Windows, macOS, Linux) with Python and Selenium.

## 🛠️ Requirements

*   Python 3.7+
*   OpenCV (`opencv-python`): For image processing.
*   Selenium (`selenium`): For browser automation.
*   NumPy (`numpy`): For numerical operations, especially with image data.
*   A compatible web browser:
    *   Google Chrome (recommended)
    *   Microsoft Edge
*   The corresponding WebDriver for your chosen browser:
    *   [ChromeDriver](https://chromedriver.chromium.org/downloads) for Google Chrome.
    *   [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) for Microsoft Edge.
    *   **Crucial:** Ensure your WebDriver version matches your browser version.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/img2desmos.git # Replace with your repo URL
cd img2desmos
Use code with caution.
Markdown
2. Set Up a Virtual Environment (Recommended)
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
Use code with caution.
Bash
3. Install Dependencies
pip install opencv-python selenium numpy
Use code with caution.
Bash
4. Set Up WebDriver
Download the WebDriver for your browser (Chrome or Edge) and ensure its version matches your browser.

Option A (Recommended): Add the directory containing the WebDriver executable (e.g., chromedriver.exe) to your system's PATH environment variable.

Option B: Specify the full path to the WebDriver executable in the script's configuration section (WEBDRIVER_PATH).

⚙️ Configuration & Usage
Open img2desmos.py and modify the configuration variables within the if __name__ == '__main__': block:

# --- Configuration ---
WEBDRIVER_PATH = None  # Example: r"C:\path\to\your\chromedriver.exe"
BROWSER_BINARY_PATH = None # Optional: if your browser isn't in the default path
BROWSER_TO_USE = "chrome"  # "chrome" (default) or "edge"

IMAGE_FILE_PATH = r"path/to/your/image.png"  # !!! CHANGE THIS !!!
QUALITY_PIXELS = 32 

NUMBER_OF_COLORS = 16  # Target colors for quantization (e.g., 8, 16, 32).
                       # Set to None to disable quantization.
Use code with caution.
Python
WEBDRIVER_PATH: Full path to WebDriver if not in system PATH.

BROWSER_BINARY_PATH: Usually None. Set if your browser is in a non-standard location.

BROWSER_TO_USE: "chrome" or "edge".

IMAGE_FILE_PATH: Essential! Path to the image you want to convert.

QUALITY_PIXELS: Defines the resolution of the output in Desmos "pixels" (largest side of the image). Higher values = more detail & expressions.

NUMBER_OF_COLORS: (Optional) If set to an integer (e.g., 16), the script will reduce the image's color palette to this many dominant colors. Set to None to use the original (resized) image colors without quantization. This is highly recommended for photographs or images with many color shades.

Running the Script
Execute from your terminal:

python img2desmos.py
Use code with caution.
Bash
The script will launch the browser, perform the conversion, and draw the art in Desmos. Press Enter in the console when done to close the browser.

🔬 How It Works
Image Preprocessing:

Loads the image using OpenCV, converts it to RGB, and flips it vertically (so array row 0 aligns with Desmos's y-axis bottom).

Color Quantization (If Enabled): Applies k-means clustering to reduce the image's color palette to NUMBER_OF_COLORS.

Resizes the image to the target QUALITY_PIXELS resolution using nearest-neighbor interpolation to maintain sharp pixel edges.

Greedy Rectangle Merging:

The core optimization: the script iterates through the (possibly quantized and resized) image.

For each unvisited pixel, it identifies the largest possible contiguous rectangle of the exact same color.

Desmos Expression Generation:

For each merged rectangle, a JavaScript command Calc.setExpression({...}); is created.

The latex field uses Desmos's polygon(...) function, formatted as \operatorname{polygon}\left(\left[ (P1x,P1y), ... \right]\right). Points are given in Clockwise order (BottomRight, TopRight, TopLeft, BottomLeft), a format found to be reliable.

Browser Automation (Selenium):

Launches and controls Chrome (or Edge).

Navigates to Desmos and disables UI updates in the expression list for faster processing.

Sends the generated JavaScript commands in chunks. The chunk size is dynamically based on the image width, mimicking a behavior that proved effective in earlier tests.

Adjusts the Desmos viewport to frame the artwork.

Re-enables UI updates in the expression list at the end.

⚠️ Troubleshooting & Notes
"Calc object not found": Desmos may not have fully loaded. Try increasing load_wait_time in the img2desmos.__init__ method (e.g., to 8 or 10 seconds).

WebDriver Errors (e.g., "session not created"):

Ensure your WebDriver version exactly matches your browser version.

Verify the WebDriver executable is in your system PATH or the WEBDRIVER_PATH in the script is correct.

Try closing all instances of the browser before running the script.

Performance: While optimized, very high QUALITY_PIXELS (e.g., 128+) or a high NUMBER_OF_COLORS on complex images can still generate many expressions, potentially making Desmos lag. Color quantization significantly helps for typical images.

Desmos API Stability: This script interacts with internal Desmos Calc object functionalities. These are not public, stable APIs and could be changed by Desmos in the future, potentially affecting the script's operation.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
Inspired by the challenge of representing images within the versatile Desmos graphing calculator.

Uses the powerful libraries OpenCV, Selenium, and NumPy.

**Key changes made to align with the example README and your project:**

*   **Catchy Title and Emojis:** Added a more engaging title and relevant emojis.
*   **Clearer Introduction:** Emphasized the core value propositions (rectangle merging, color quantization).
*   **Structured Sections:** Used similar section headings (Features, Requirements, Getting Started, Configuration, How It Works, Troubleshooting, License).
*   **Concise Language:** Tried to keep explanations clear and to the point.
*   **Emphasis on Configuration:** Clearly highlighted the user-configurable parts.
*   **Improved "How It Works":** Broke it down into more digestible steps.
*   **Enhanced Troubleshooting:** Added more common WebDriver and Desmos loading issues.
*   **Maintained Technical Accuracy:** Ensured the descriptions match your script's actual functionality.

Make sure to replace `https://github.com/your-username/img2desmos.git` with your actual repository URL once you've created it on GitHub.
Use code with caution.
