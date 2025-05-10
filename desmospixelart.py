# desmospixelart.py
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
#from selenium.webdriver.edge.service import Service as EdgeService
#from selenium.webdriver.edge.options import Options as EdgeOptions
import time
import numpy as np
import traceback

class _Utils:
    """Helper class for utility functions."""
    @staticmethod
    def RGBToHex(rgb_tuple):
        """Converts an (R, G, B) tuple to a hex color string."""
        return '%02x%02x%02x' % (int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2]))

    @staticmethod
    def ConvertToExpression(rgb, x, y, rect_width, rect_height):
        """
        Creates the JavaScript string for a Calc.setExpression call to draw a colored rectangle.
        """
        x, y, rect_width, rect_height = int(x), int(y), int(rect_width), int(rect_height)
        expression_id = f"rect_{x}_{y}_{rect_width}_{rect_height}"

        expression_js = (
            "Calc.setExpression({"
            f"color: '#{_Utils.RGBToHex(rgb)}', "
            f"id: '{expression_id}', "
            "lineOpacity:'1', lineWidth: '1', "
            f"latex: {_Utils.CoordToLatex(x, y, rect_width, rect_height)}, "
            "pointOpacity: '', fillOpacity: '1'"
            "});\n" 
        )
        return str(expression_js)

    @staticmethod
    def CoordToLatex(x, y, rect_width, rect_height):
        """
        Generates the LaTeX string for a polygon representing the rectangle.
        Matches the specific LaTeX format of the original working base code:
        '\\operatorname{polygon}\\left(\\left[ (BRx, BRy),(TRx, TRy),(TLx, TLy),(BLx, BLy) \\right]\\right)'
        Points are in Clockwise order: BottomRight, TopRight, TopLeft, BottomLeft.
        """
        br_x, br_y = x + rect_width, y
        tr_x, tr_y = x + rect_width, y + rect_height
        tl_x, tl_y = x, y + rect_height
        bl_x, bl_y = x, y

        points = [(br_x, br_y), (tr_x, tr_y), (tl_x, tl_y), (bl_x, bl_y)]
        points_str_list = [str(p) for p in points]
        
        latex = r"'\\operatorname{polygon}\\left(\\left[ " + ",".join(points_str_list) + r" \\right]\\right)'"
        return latex

    @staticmethod
    def quantize_colors(image, num_colors=16):
        """
        Reduces the number of unique colors in an image using k-means clustering.
        :param image: Input image (NumPy array, expected in RGB).
        :param num_colors: The target number of dominant colors.
        :return: Image with quantized colors.
        """
        pixels = image.reshape((-1, 3)); pixels = np.float32(pixels)
        # criteria: (type, max_iter, epsilon)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        # attempts: number of times algorithm is run with different initial labellings
        _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers) # Convert centers to uint8 for image display/saving
        quantized_pixels = centers[labels.flatten()]
        quantized_image = quantized_pixels.reshape(image.shape)
        return quantized_image

class img2desmos:
    """
    Converts images into Desmos-style pixel art, with optional color quantization,
    by generating and executing JavaScript commands to draw merged rectangles.
    """
    def __init__(self, driver_path=None, browser_binary_location=None, 
                 browser_type="chrome", window_width=1000, window_height=800, 
                 desmos_url=r'https://www.desmos.com/calculator', 
                 load_wait_time=6):
        self.driver = None
        browser_type = browser_type.lower()
        
        if browser_type == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized") 
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # options.add_argument("--headless") # Uncomment for headless operation

            if browser_binary_location: 
                options.binary_location = browser_binary_location
            if driver_path:
                service = ChromeService(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                # Assumes chromedriver is in PATH
                self.driver = webdriver.Chrome(options=options)
        elif browser_type == "edge":
            options = EdgeOptions()
            if browser_binary_location: 
                options.binary_location = browser_binary_location
            if driver_path:
                service = EdgeService(executable_path=driver_path)
                self.driver = webdriver.Edge(service=service, options=options)
            else:
                # Assumes msedgedriver is in PATH
                self.driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser_type: {browser_type}. Choose 'chrome' or 'edge'.")

        # Setting window size after initialization for some drivers
        if browser_type == "chrome" and "--headless" not in options.arguments:
             # For non-headless Chrome, set_window_size might work better here
             # or rely on --start-maximized. Headless often needs size set in options.
             pass # Rely on --start-maximized or set if needed
        self.driver.set_window_size(window_width, window_height) 
        
        try:
            self.driver.get(desmos_url)
            print(f"Waiting {load_wait_time}s for Desmos to load ({browser_type.capitalize()})...")
            time.sleep(load_wait_time)
            
            calc_exists = self.driver.execute_script("return typeof Calc !== 'undefined' && Calc !== null;")
            if not calc_exists:
                raise RuntimeError(f"Desmos 'Calc' object not found on {desmos_url}. Increase load_wait_time or check URL.")
            print("'Calc' object found.")

            self.driver.execute_script('Calc.updateSettings({"expressions": false});')
            print("Connected to Desmos and disabled expression list UI updates for performance.")
        except Exception as e:
            print(f"Error initializing Desmos session with {browser_type.capitalize()}: {e}")
            traceback.print_exc()
            if self.driver:
                self.driver.quit()
            raise

    def draw_image(self, image_path, quality_target_pixels, num_quantized_colors=None):
        """
        Processes an image, optionally quantizes colors, converts to Desmos expressions, and draws it.
        :param image_path: Path to the input image file.
        :param quality_target_pixels: The target size (in Desmos "pixels") for the largest side of the image.
        :param num_quantized_colors: Optional. If set (e.g., 8, 16, 32), reduces image colors to this number.
        """
        if not self.driver:
            print("WebDriver not initialized. Cannot draw image.")
            return

        input_image = cv2.imread(image_path)
        if input_image is None:
            print(f"Error: Could not read image from path: {image_path}")
            return
        
        input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # --- Optional Color Quantization Step ---
        if num_quantized_colors is not None and num_quantized_colors > 0:
            print(f"Quantizing image colors to {num_quantized_colors} dominant colors...")
            start_quant_time = time.time()
            processed_image = _Utils.quantize_colors(input_image_rgb, num_quantized_colors)
            print(f"Color quantization took {time.time() - start_quant_time:.2f} seconds.")
        else:
            processed_image = input_image_rgb # Use original RGB if no quantization

        # Flip vertically so array row 0 is bottom of image in Desmos
        input_image_flipped = cv2.flip(processed_image, 0) 
        
        img_h_orig, img_w_orig = input_image_flipped.shape[:2]
        
        if img_w_orig == 0 or img_h_orig == 0:
            print("Error: Image (possibly after processing) has zero width or height.")
            return
        aspect_ratio = img_w_orig / img_h_orig
        
        # Determine dimensions of the "pixel grid" in Desmos units
        if img_w_orig > img_h_orig:
            desmos_pixel_grid_w = int(quality_target_pixels) 
            desmos_pixel_grid_h = int(desmos_pixel_grid_w / aspect_ratio) or 1 # Ensure at least 1
        else:
            desmos_pixel_grid_h = int(quality_target_pixels)
            desmos_pixel_grid_w = int(desmos_pixel_grid_h * aspect_ratio) or 1 # Ensure at least 1
        
        if desmos_pixel_grid_w == 0 or desmos_pixel_grid_h == 0:
            print(f"Error: Calculated pixel grid is zero size ({desmos_pixel_grid_w}x{desmos_pixel_grid_h}).")
            return

        print(f"Resizing image to a {desmos_pixel_grid_w}x{desmos_pixel_grid_h} pixel grid for Desmos.")
        
        temp_resized_img = cv2.resize(input_image_flipped, (desmos_pixel_grid_w, desmos_pixel_grid_h), 
                                      interpolation=cv2.INTER_NEAREST)

        visited = np.zeros((desmos_pixel_grid_h, desmos_pixel_grid_w), dtype=bool) # (rows, cols)
        expressions_list = []

        # Greedy rectangle merging algorithm
        for r_idx in range(desmos_pixel_grid_h):  # y-coordinate in image array
            for c_idx in range(desmos_pixel_grid_w): # x-coordinate in image array
                if not visited[r_idx, c_idx]:
                    current_color = temp_resized_img[r_idx, c_idx]
                    rect_w = 1 
                    for c_offset in range(1, desmos_pixel_grid_w - c_idx):
                        if visited[r_idx, c_idx + c_offset] or \
                           not np.array_equal(temp_resized_img[r_idx, c_idx + c_offset], current_color):
                            break
                        rect_w += 1
                    rect_h = 1
                    for r_offset in range(1, desmos_pixel_grid_h - r_idx):
                        can_extend_row = True
                        for c_check_in_row in range(rect_w):
                            if visited[r_idx + r_offset, c_idx + c_check_in_row] or \
                               not np.array_equal(temp_resized_img[r_idx + r_offset, c_idx + c_check_in_row], current_color):
                                can_extend_row = False; break
                        if not can_extend_row: break
                        rect_h += 1
                    expressions_list.append(
                        _Utils.ConvertToExpression(current_color, c_idx, r_idx, rect_w, rect_h)
                    )
                    for r_v in range(r_idx, r_idx + rect_h):
                        for c_v in range(c_idx, c_idx + rect_w):
                            visited[r_v, c_v] = True
        
        if not expressions_list:
            print("No Desmos expressions were generated (e.g., image might be blank or too small).")
            return
        
        print(f"Generated {len(expressions_list)} Desmos expressions (merged rectangles).")
        if expressions_list:
             print(f"Sample JS command: {expressions_list[0].strip()}")
        
        output_js_string = "".join(expressions_list)
        
        img_center_x = desmos_pixel_grid_w / 2
        img_center_y = desmos_pixel_grid_h / 2
        margin_factor = 0.1
        view_padding_x = max(desmos_pixel_grid_w * margin_factor, 2)
        view_padding_y = max(desmos_pixel_grid_h * margin_factor, 2)
        viewport_width = desmos_pixel_grid_w + 2 * view_padding_x
        viewport_height = desmos_pixel_grid_h + 2 * view_padding_y

        zoom_script = f"""
            Calc.setViewport([
                {img_center_x - viewport_width / 2}, {img_center_x + viewport_width / 2},
                {img_center_y - viewport_height / 2}, {img_center_y + viewport_height / 2}
            ]);"""
        
        print("Sending expressions to Desmos..."); start_time_desmos = time.time()
        try: 
            self.driver.execute_script(zoom_script)
            print("Viewport set.")
        except Exception as e: 
            print(f"Error setting viewport: {e}"); traceback.print_exc()

        lines_per_chunk = desmos_pixel_grid_w 
        if lines_per_chunk <= 0 : lines_per_chunk = 10 # Safety fallback
        print(f"Sending expressions in chunks of {lines_per_chunk} commands.")

        script_lines = output_js_string.strip().split('\n')
        for i in range(0, len(script_lines), lines_per_chunk):
            chunk = '\n'.join(script_lines[i : i + lines_per_chunk])
            if chunk.strip():
                try:
                    self.driver.execute_script(chunk)
                except Exception as e:
                    print(f"Error executing Desmos script chunk (lines ~{i+1}-{i+lines_per_chunk}): {e}")
                    traceback.print_exc()
        
        try:
            self.driver.execute_script('Calc.updateSettings({"expressions": true});')
            print("Expression list UI updates re-enabled.")
        except Exception as e: 
            print(f"Error re-enabling expression list UI: {e}"); traceback.print_exc()
        
        print(f"Drawing in Desmos took {time.time() - start_time_desmos:.2f} seconds.")

    def close(self):
        """Closes the WebDriver session."""
        if self.driver:
            try:
                print("You can now close the browser manually or press Enter here to quit script and close it.")
                input("Press Enter to close browser and exit script...")
            except EOFError:
                print("Auto-closing browser in 5 seconds...")
                time.sleep(5)
            finally:
                self.driver.quit()
                print("Browser closed.")

# --- Example Usage ---
if __name__ == '__main__':
    # --- Configuration ---
    # Path to your WebDriver (chromedriver.exe or msedgedriver.exe)
    # Set to None if the driver is in your system's PATH.
    WEBDRIVER_PATH = None 
    # Example: WEBDRIVER_PATH = r"C:\path\to\your\chromedriver.exe" 
    
    # Optional: Path to your browser's binary (if not in default location)
    BROWSER_BINARY_PATH = None
    # Example: BROWSER_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # Choose browser: "chrome" (default) or "edge"
    BROWSER_TO_USE = "chrome" 

    # Path to the image you want to convert
    IMAGE_FILE_PATH = r"your_image.png"  # <--- !!! CHANGE THIS !!!

    # Target size for the largest side of the image in Desmos "pixels".
    QUALITY_PIXELS = 64  # <--- !!! CHANGE THIS !!!
    
    # Optional: Target number of colors after quantization.
    # Set to an integer (e.g., 8, 16, 32) or None to disable quantization.
    NUMBER_OF_COLORS = None  # <--- !!! CHANGE THIS !!!
    # Example: Reduce to 16 dominant colors
    # NUMBER_OF_COLORS = None # To use original image colors without quantization

    # --- Run the conversion ---
    converter_instance = None
    try:
        print(f"Initializing img2desmos (Browser: {BROWSER_TO_USE.capitalize()})...")
        converter_instance = img2desmos(
            driver_path=WEBDRIVER_PATH,
            browser_binary_location=BROWSER_BINARY_PATH,
            browser_type=BROWSER_TO_USE
        )
        
        print(f"Starting image conversion for: {IMAGE_FILE_PATH}")
        converter_instance.draw_image(
            IMAGE_FILE_PATH, 
            QUALITY_PIXELS,
            num_quantized_colors=NUMBER_OF_COLORS
        )

    except FileNotFoundError:
        print(f"ERROR: Image file not found at '{IMAGE_FILE_PATH}'. Please check path.")
    except RuntimeError as e: 
        print(f"A runtime error occurred: {e}")
    except Exception as e:
        print(f"An unexpected critical error occurred: {e}")
        traceback.print_exc()
    finally:
        if converter_instance:
            converter_instance.close()
        print("Script finished.")
