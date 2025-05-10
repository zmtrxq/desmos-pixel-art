# desmos-pixel-art
This Python script converts images into Desmos-style "pixel art" by generating and executing JavaScript commands to draw colored rectangles in the Desmos graphing calculator. It features:

*   **Efficient Rectangle Merging:** Combines adjacent pixels of the same color into larger rectangles, significantly reducing the number of Desmos expressions for better performance.
*   **Optional Color Quantization:** Can reduce the image's color palette using k-means clustering. This is highly effective for photographs or images with gradients, leading to a stylized output and even fewer Desmos expressions.
*   **Reliable Desmos Integration:** Uses a LaTeX format and JavaScript command structure carefully tested for compatibility with the Desmos `Calc` API.
*   **Browser Automation:** Leverages Selenium to automate a web browser (Chrome by default, Edge supported) to interact with the Desmos calculator.

## Features

*   Converts common image formats (PNG, JPG, etc.).
*   Merges same-colored pixels into larger rectangles.
*   Optional k-means color quantization to simplify color palettes.
*   Adjustable "quality" setting for Desmos output resolution.
*   Automates opening Desmos, inputting expressions, and setting the viewport.

## Requirements

*   Python 3.7+
*   OpenCV (`opencv-python`)
*   Selenium (`selenium`)
*   NumPy (`numpy`)
*   A compatible web browser:
    *   Google Chrome (recommended default)
    *   Microsoft Edge
*   The corresponding WebDriver for your chosen browser:
    *   ChromeDriver for Google Chrome
    *   msedgedriver for Microsoft Edge

## Installation

1.  **Clone the repository (or download `img2desmos.py`):**
    ```bash
    # Replace with your actual repository URL after creation
    git clone https://github.com/your-username/img2desmos.git 
    cd img2desmos
    ```

2.  **Install Python dependencies:**
    Using a virtual environment is recommended:
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```
    Install packages:
    ```bash
    pip install opencv-python selenium numpy
    ```

3.  **Set up WebDriver:**
    *   **Download WebDriver:**
        *   For Google Chrome: [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
        *   For Microsoft Edge: [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
        *   **Important:** Ensure the WebDriver version matches your installed browser version.
    *   **Make WebDriver Accessible:**
        *   **Option A (Recommended):** Add the directory containing the WebDriver executable (e.g., `chromedriver.exe` or `msedgedriver.exe`) to your system's PATH environment variable.
        *   **Option B:** Alternatively, specify the full path to the WebDriver executable directly in the script's configuration section (see `WEBDRIVER_PATH`).

## Usage

1.  **Configure the script (`img2desmos.py`):**
    Modify the variables in the `if __name__ == '__main__':` block:

    ```python
    # --- Configuration ---
    WEBDRIVER_PATH = None  # Or r"C:\path\to\your\chromedriver.exe"
    BROWSER_BINARY_PATH = None # Optional: if your browser isn't in the default path
    BROWSER_TO_USE = "chrome"  # "chrome" or "edge"

    IMAGE_FILE_PATH = r"path/to/your/image.png"  # !!! CHANGE THIS !!!
    QUALITY_PIXELS = 64
    
    NUMBER_OF_COLORS = None  # Target colors for quantization (e.g., 8, 16, 32).
                           # Set to None to disable quantization.
    ```
    *   `WEBDRIVER_PATH`: Set to your WebDriver's full path if not in system PATH.
    *   `BROWSER_BINARY_PATH`: Usually `None`.
    *   `BROWSER_TO_USE`: Change to `"edge"` if you prefer Microsoft Edge.
    *   `IMAGE_FILE_PATH`: **Crucial!** Update to your image's path.
    *   `QUALITY_PIXELS`: Controls Desmos output resolution (largest side).
    *   `NUMBER_OF_COLORS`: For color quantization. `None` uses original (resized) image colors.

2.  **Run the script from your terminal:**
    ```bash
    python img2desmos.py 
    ```

3.  **Observe:**
    The script will launch the browser, navigate to Desmos, process the image, and draw the art. After completion, it will wait for you to press Enter in the console before closing the browser.

## How It Works

1.  **Image Loading & Preprocessing:**
    *   Loads image with OpenCV, converts to RGB, flips vertically.
    *   **Color Quantization (Optional):** If `NUMBER_OF_COLORS` is set, k-means clustering reduces the image to the specified dominant colors.
    *   Resizes image to `QUALITY_PIXELS` (for its largest side) using `cv2.INTER_NEAREST` to maintain sharp pixel edges.

2.  **Greedy Rectangle Merging:**
    *   Iterates through the (possibly quantized and resized) image.
    *   For each unvisited pixel, it finds the largest possible contiguous rectangle of the exact same color.

3.  **Desmos Expression Generation:**
    *   Generates a `Calc.setExpression({...});` JavaScript command for each merged rectangle.
    *   The `latex` field uses Desmos's `polygon(...)` function with the specific format: `\operatorname{polygon}\left(\left[ (P1x,P1y), ... \right]\right)`. Points are specified in Clockwise order (BottomRight, TopRight, TopLeft, BottomLeft) as this was found to be reliable.

4.  **Browser Automation (Selenium):**
    *   Launches and controls the specified browser (Chrome or Edge).
    *   Navigates to Desmos and temporarily disables expression list UI updates for faster bulk command execution.
    *   Sends the generated JavaScript commands in chunks (chunk size is dynamically based on the image width, a behavior that proved effective).
    *   Adjusts the Desmos viewport to fit the generated image.
    *   Re-enables expression UI updates at the end.

## Troubleshooting / Notes

*   **"Calc object not found":** Desmos might not have fully loaded. Try increasing `load_wait_time` in `img2desmos.__init__`.
*   **WebDriver Errors:** Ensure your WebDriver version matches your browser version and that it's correctly placed (in PATH or path specified).
*   **Performance:** Very high `QUALITY_PIXELS` or a large `NUMBER_OF_COLORS` (if quantization is used inefficiently) on complex images can still generate many expressions, potentially making Desmos lag. The color quantization helps significantly for typical images.
*   **Desmos API Stability:** This script relies on the internal `Calc` object of Desmos, which is not a public, stable API. Future changes by Desmos could potentially break the script.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
