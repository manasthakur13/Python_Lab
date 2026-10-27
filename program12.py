from PIL import Image, ImageFilter

def apply_grayscale(image):
    """
    Converts an image to grayscale by adjusting the underlying RGB color channels.
    Iterates through the raw pixel grid and applies the standard luminance formula.
    
    Args:
        image (PIL.Image.Image): The input image object.
        
    Returns:
        PIL.Image.Image: The processed grayscale image.
    """
    img_copy = image.copy().convert("RGB")
    pixels = img_copy.load()
    width, height = img_copy.size
    
    # Process the raw pixel grid
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            # Standard RGB to grayscale conversion formula
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            pixels[x, y] = (gray, gray, gray)
            
    return img_copy

def apply_threshold(image, threshold=128):
    """
    Applies image thresholding to generate a black and white image.
    Pixels brighter than the threshold become white; others become black.
    
    Args:
        image (PIL.Image.Image): The input image object.
        threshold (int): The cutoff value (0-255) for black vs. white.
        
    Returns:
        PIL.Image.Image: The processed black and white image.
    """
    img_copy = image.copy().convert("RGB")
    pixels = img_copy.load()
    width, height = img_copy.size
    
    # Process the raw pixel grid
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            # Calculate simple average brightness
            brightness = (r + g + b) // 3
            if brightness >= threshold:
                pixels[x, y] = (255, 255, 255)  # White
            else:
                pixels[x, y] = (0, 0, 0)        # Black
                
    return img_copy

def apply_spatial_blur(image):
    """
    Applies a simple spatial blur filter to the image directly.
    
    Args:
        image (PIL.Image.Image): The input image object.
        
    Returns:
        PIL.Image.Image: The spatially blurred image.
    """
    # Uses Pillow's built-in spatial convolution matrix for blurring
    return image.filter(ImageFilter.BLUR)

def main():
    """
    Main execution function that opens a JPEG or PNG image, applies 
    the transformation filters, and outputs the processed images to disk.
    """
    input_filename = "sample_image.jpg"  # Replace with a valid local JPEG/PNG path
    
    try:
        # Open the raw image file
        with Image.open(input_filename) as img:
            print(f"Successfully loaded {input_filename}")
            
            # 1. Grayscale Conversion
            grayscale_img = apply_grayscale(img)
            grayscale_img.save("output_grayscale.jpg")
            print("Saved: output_grayscale.jpg")
            
            # 2. Image Thresholding (Black and White Generation)
            bw_img = apply_threshold(img, threshold=128)
            bw_img.save("output_threshold.jpg")
            print("Saved: output_threshold.jpg")
            
            # 3. Simple Spatial Blur Filter
            blurred_img = apply_spatial_blur(img)
            blurred_img.save("output_blurred.jpg")
            print("Saved: output_blurred.jpg")
            
    except FileNotFoundError:
        print(f"Error: Could not find '{input_filename}'. "
              f"Ensure a valid JPEG or PNG file exists in the directory.")

if __name__ == "__main__":
    main()