# DesmosPixelArt: Image to Desmos Art Converter 🎨

Transform your favorite images into stunning Desmos "pixel art" with this Python script! `DesmosPixelArt` automates the process of converting images into a series of Desmos expressions that render as colored rectangles, effectively creating pixelated artwork directly in the Desmos graphing calculator.

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
    *   Google Chrome (recommended default)
    *   Microsoft Edge
*   The corresponding WebDriver for your chosen browser:
    *   [ChromeDriver](https://chromedriver.chromium.org/downloads) for Google Chrome.
    *   [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) for Microsoft Edge.
    *   **Crucial:** Ensure your WebDriver version matches your browser version.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/DesmosPixelArt.git # Replace with your repo URL
cd DesmosPixelArt
```
(Or download `desmospixelart.py` directly if you prefer.)

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
```
Activate it:
*   Windows:
    ```bash
    venv\Scripts\activate
    ```
*   macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies

```bash
pip install opencv-python selenium numpy
```

### 4. Set Up WebDriver

Download the WebDriver for your browser (Chrome or Edge) and ensure its version matches your browser.

*   **Option A (Recommended):** Add the directory containing the WebDriver executable (e.g., `chromedriver.exe`) to your system's PATH environment variable.
*   **Option B:** Specify the full path to the WebDriver executable in the script's configuration section (`WEBDRIVER_PATH`).

## ⚙️ Configuration & Usage

Open `desmospixelart.py` and modify the configuration variables found within the `if __name__ == '__main__':` block at the bottom of the script:

```python
# --- Configuration ---
WEBDRIVER_PATH = None  # Example: r"C:\path\to\your\chromedriver.exe"
BROWSER_BINARY_PATH = None # Optional: if your browser isn't in the default path
BROWSER_TO_USE = "chrome"  # "chrome" (default) or "edge"

IMAGE_FILE_PATH = r"path/to/your/image.png"  # !!! CHANGE THIS !!!
QUALITY_PIXELS = 32 

NUMBER_OF_COLORS = 16  # Target colors for quantization (e.g., 8, 16, 32).
                       # Set to None to disable quantization.
```

*   `WEBDRIVER_PATH`: Full path to your WebDriver executable if it's not in your system PATH. Leave as `None` if it is.
*   `BROWSER_BINARY_PATH`: Usually `None`. Only set this if your browser executable is installed in a non-standard location.
*   `BROWSER_TO_USE`: Choose between `"chrome"` or `"edge"`.
*   `IMAGE_FILE_PATH`: **Essential!** Update this to the correct path of the image you want to convert.
*   `QUALITY_PIXELS`: Defines the resolution of the output in Desmos "pixels." This refers to the number of pixels along the largest dimension of the image after resizing. Higher values yield more detail but also more Desmos expressions.
*   `NUMBER_OF_COLORS`: (Optional) If set to an integer (e.g., `16`), the script will reduce the image's color palette to this many dominant colors using k-means clustering. Set to `None` to use the original (resized) image colors without quantization. This is highly recommended for photographs or images with many subtle color variations.

### Running the Script

Execute from your terminal:

```bash
python desmospixelart.py
```

The script will launch the configured browser, navigate to Desmos, process the image, and render the artwork. After completion, it will wait for you to press Enter in the console before automatically closing the browser.

## 🔬 How It Works

The script follows these main steps:

1.  **Image Preprocessing:**
    *   The input image is loaded using OpenCV.
    *   It's converted to the RGB color space.
    *   The image is flipped vertically, so array row 0 aligns with the bottom of the y-axis in Desmos's coordinate system.
    *   **Color Quantization (If Enabled):** If `NUMBER_OF_COLORS` is specified, k-means clustering is applied to reduce the image's color palette to the desired number of dominant colors. This helps group similar shades.
    *   The image (either original or quantized) is then resized to the target `QUALITY_PIXELS` resolution (for its largest dimension) using nearest-neighbor interpolation. This method preserves sharp pixel edges, which is ideal for pixel art.

2.  **Greedy Rectangle Merging:**
    *   This is the core optimization. The script iterates through the resized image pixel by pixel.
    *   For each pixel that hasn't been included in a rectangle yet ("unvisited"), it identifies the largest possible contiguous rectangle composed of pixels of the *exact same color*. This rectangle is found by first extending horizontally and then extending that strip vertically.

3.  **Desmos Expression Generation:**
    *   For each merged rectangle identified, a JavaScript command `Calc.setExpression({...});` is constructed.
    *   The `latex` field within this command uses Desmos's `polygon(...)` function. The specific format used is `\operatorname{polygon}\left(\left[ (P1x,P1y), ... \right]\right)`.
    *   The points (vertices) of the rectangle are provided in Clockwise order (BottomRight, TopRight, TopLeft, BottomLeft), as this particular sequence and LaTeX structure was found to be reliable with the Desmos API.

4.  **Browser Automation (Selenium):**
    *   Selenium launches and controls an instance of the specified web browser (Chrome or Edge).
    *   It navigates to the Desmos graphing calculator.
    *   To improve performance during the bulk addition of expressions, UI updates for the expression list in Desmos are temporarily disabled via `Calc.updateSettings({"expressions": false});`.
    *   The generated JavaScript commands are sent to Desmos in chunks. The size of these chunks is dynamically based on the width (in pixels) of the processed image, a behavior that mirrored an earlier, simpler script which worked effectively without needing explicit refresh calls between chunks.
    *   The Desmos viewport is automatically adjusted to center and fit the generated artwork.
    *   Finally, UI updates for the expression list are re-enabled.

## ⚠️ Troubleshooting & Notes

*   **"Calc object not found":** This usually means Desmos didn't fully load before the script tried to interact with it. Try increasing the `load_wait_time` parameter in the `img2desmos.__init__` method (e.g., to 8 or 10 seconds) inside `desmospixelart.py`.
*   **WebDriver Errors (e.g., "session not created", "executable needs to be in PATH"):**
    *   Ensure your WebDriver version *exactly* matches your installed browser version.
    *   Verify that the WebDriver executable is either in a directory listed in your system's PATH environment variable, or that the `WEBDRIVER_PATH` in the script points to the correct file location.
    *   Try closing all existing instances of the browser before running the script.
*   **Performance in Desmos:** While optimized by rectangle merging and optional color quantization, using very high `QUALITY_PIXELS` (e.g., 128+) or a high `NUMBER_OF_COLORS` on highly complex images can still generate a substantial number of Desmos expressions. This may lead to some lag within Desmos. Color quantization is particularly helpful for improving performance with typical photographic images.
*   **Desmos API Stability:** This script interacts with internal functionalities of the Desmos `Calc` object. These are not officially public or guaranteed stable APIs. Future updates to the Desmos platform could potentially change these functionalities and affect the script's operation.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for full details.
