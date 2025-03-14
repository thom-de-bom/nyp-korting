import random
import time
import pyautogui
import keyboard
import datetime
import pyperclip
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to get absolute path for resource files
def get_resource_path(filename):
    return os.path.join(script_dir, filename)

# Define image paths using relative paths in the images folder
box_image = get_resource_path(os.path.join("images", "box.jpg"))
coupon_image = get_resource_path(os.path.join("images", "NOGEENCOUPON.png"))
verwijder_image = get_resource_path(os.path.join("images", "verwijder.png"))

# Define the weights for each range
weights = [1, 2, 5, 2, 1]

def gen_random():
    """Generate a random number based on weighted ranges"""
    choices = [random.randint(100, 399)] * weights[0] + \
              [random.randint(400, 500)] * weights[1] + \
              [random.randint(501, 699)] * weights[2] + \
              [random.randint(700, 800)] * weights[3] + \
              [random.randint(801, 999)] * weights[4]
    number = str(random.choice(choices))
    return number

def exists_on_screen(image, confidence=0.8): 
    """
    Check if an image exists on screen and return its position if found.
    
    Args:
        image: Path to the image file
        confidence: Confidence level for image recognition (0-1)
        
    Returns:
        False if image not found, or the position object if found
    """
    thing2find = pyautogui.locateOnScreen(image, confidence=confidence) 
    if thing2find == None: 
        return False 
    else: 
        return thing2find

def find_input_field():
    """Find and click the input field on screen"""
    print("Looking for input field...")
    try:
        input_field = pyautogui.locateCenterOnScreen(box_image, confidence=0.5)
        if input_field:
            pyautogui.click(input_field)
            print("Input field found and clicked")
            return True
        else:
            print("Input field not found. Please position the cursor manually and press Enter.")
            input("Press Enter to continue...")
            return True
    except Exception as e:
        print(f"Error finding input field: {e}")
        print("Please position the cursor manually and press Enter.")
        input("Press Enter to continue...")
        return True

def save_coupon(code):
    """Save the coupon code to file"""
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d")
    coupon_data = f"{code}|{date_time_str}"
    
    coupon_file = get_resource_path("Coupons.txt")
    try:
        with open(coupon_file, "a") as f:
            f.write(coupon_data + "\n")
        print(f"Coupon saved to {coupon_file}")
        return True
    except Exception as e:
        print(f"Error saving coupon: {e}")
        # Backup save to desktop in case of permission issues
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            backup_file = os.path.join(desktop, "Coupons_backup.txt")
            with open(backup_file, "a") as f:
                f.write(coupon_data + "\n")
            print(f"Coupon saved to backup file: {backup_file}")
            return True
        except:
            print("Failed to save coupon. Here it is:")
            print(coupon_data)
            return False

def fast_mode():
    """
    Fast Mode: Quickly find a valid coupon without saving it.
    Optimized for speed by removing pre-checks and file saving.
    Does not show popup or save coupon to file.
    """
    # Switch to the target window
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)
    
    # Find and click the input field
    if not find_input_field():
        return
    
    # Initialize a list to keep track of the used numbers
    used_numbers = []
    
    print("Running in Fast Mode - Press DELETE key to stop")
    
    # Loop until the delete key is pressed
    while not keyboard.is_pressed('delete'):
        # Generate a random number with the defined weights
        number = gen_random() 
        
        # Check if the number has been used before
        while number in used_numbers:
            # Generate a new number
            number = gen_random()
            
        # Add the number to the used numbers list
        used_numbers.append(number)
        
        # Write number
        pyautogui.typewrite(number)
        
        # Press Enter
        pyautogui.press('enter')
        
        # Small delay to allow the page to respond (reduced for speed)
        time.sleep(0.3)
        
        # Check if the code was valid
        coupon_found = exists_on_screen(coupon_image, confidence=0.6)
        if coupon_found:
            print(f"Valid coupon found: {number}")
            print("Success! Coupon found. Exiting Fast Mode.")
            # Just exit without returning the coupon code
            # This prevents the popup notification
            return
            
        # Select the entire number
        pyautogui.hotkey('ctrl', 'a')
        
        # Delete the number
        pyautogui.press('delete')
    
    print("Fast Mode stopped by user.")
    return

def continuous_mode():
    """
    Continuous Mode: Find multiple valid coupons and save them.
    Checks before and after each attempt and saves coupons to file.
    """
    # Switch to the target window
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)
    
    # Find and click the input field
    if not find_input_field():
        return
    
    # Initialize a list to keep track of the used numbers
    used_numbers = []
    
    # First check if a valid coupon is already present
    print("Checking if a valid coupon is already present...")
    if exists_on_screen(coupon_image, confidence=0.6):
        print("Valid coupon already found on screen!")
        # Try to find a way to continue to the next coupon
        # This would need to be customized based on the website
        return
    
    print("Running in Continuous Mode - Press DELETE key to stop")
    
    # Loop until the delete key is pressed
    last_tried_number = None
    found_coupons = []
    
    while not keyboard.is_pressed('delete'):
        # Check if the previous code was valid before trying a new one
        coupon_found = exists_on_screen(coupon_image, confidence=0.6)
        if coupon_found and last_tried_number:
            print(f"Valid coupon found: {last_tried_number}")
            
            # Save the coupon to file
            save_coupon(last_tried_number)
            found_coupons.append(last_tried_number)
            
            print("Success! Coupon found and saved.")
            
            # Look for the "verwijder" (remove/delete) button
            print("Looking for 'verwijder' button...")
            verwijder_button = None
            # Try a few times with a small delay between attempts
            for _ in range(5):
                verwijder_button = exists_on_screen(verwijder_image, confidence=0.6)
                if verwijder_button:
                    break
                time.sleep(0.5)
                
            if verwijder_button:
                # Click on the center of the verwijder button
                verwijder_center = pyautogui.center(verwijder_button)
                print(f"Found 'verwijder' button at {verwijder_center}, clicking it...")
                pyautogui.click(verwijder_center)
                time.sleep(1)
                
                # Try to find the input field again
                if not find_input_field():
                    print("Could not find input field after clicking 'verwijder'. Exiting.")
                    return found_coupons
            else:
                print("Could not find 'verwijder' button. Trying to continue anyway...")
                # Try to find the input field again
                if not find_input_field():
                    print("Could not find input field after finding a coupon. Exiting.")
                    return found_coupons
            
        # Generate a random number with the defined weights
        number = gen_random() 
        
        # Check if the number has been used before
        while number in used_numbers:
            # Generate a new number
            number = gen_random()
            
        # Add the number to the used numbers list
        used_numbers.append(number)
        
        # Store the number we're about to try
        last_tried_number = number
        
        # Write number
        pyautogui.typewrite(number)
        
        # Press Enter
        pyautogui.press('enter')
        
        # Small delay to allow the page to respond
        time.sleep(0.5)
        
        # Check if the code was valid immediately after entering
        coupon_found = exists_on_screen(coupon_image, confidence=0.6)
        if coupon_found:
            print(f"Valid coupon found: {number}")
            
            # Save the coupon to file
            save_coupon(number)
            found_coupons.append(number)
            
            print("Success! Coupon found and saved.")
            
            # Look for the "verwijder" (remove/delete) button
            print("Looking for 'verwijder' button...")
            verwijder_button = None
            # Try a few times with a small delay between attempts
            for _ in range(5):
                verwijder_button = exists_on_screen(verwijder_image, confidence=0.6)
                if verwijder_button:
                    break
                time.sleep(0.5)
                
            if verwijder_button:
                # Click on the center of the verwijder button
                verwijder_center = pyautogui.center(verwijder_button)
                print(f"Found 'verwijder' button at {verwijder_center}, clicking it...")
                pyautogui.click(verwijder_center)
                time.sleep(1)
                
                # Try to find the input field again
                if not find_input_field():
                    print("Could not find input field after clicking 'verwijder'. Exiting.")
                    return found_coupons
            else:
                print("Could not find 'verwijder' button. Trying to continue anyway...")
                # Try to find the input field again
                if not find_input_field():
                    print("Could not find input field after finding a coupon. Exiting.")
                    return found_coupons
            
        # Select the entire number
        pyautogui.hotkey('ctrl', 'a')
        
        # Delete the number
        pyautogui.press('delete')
    
    print("Continuous Mode stopped by user.")
    return found_coupons

def create_ui():
    """Create the UI for selecting the mode"""
    root = tk.Tk()
    root.title("Pizza Coupon Finder")
    root.geometry("400x300")
    
    # Set style
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12))
    style.configure("TLabel", font=("Arial", 12))
    style.configure("Header.TLabel", font=("Arial", 14, "bold"))
    
    # Create header
    header = ttk.Label(root, text="Pizza Coupon Finder", style="Header.TLabel")
    header.pack(pady=20)
    
    # Create mode selection frame
    mode_frame = ttk.Frame(root)
    mode_frame.pack(pady=10, fill="x", padx=20)
    
    # Mode selection variable
    mode_var = tk.StringVar(value="fast")
    
    # Create mode selection radio buttons
    fast_radio = ttk.Radiobutton(mode_frame, text="Fast Mode", variable=mode_var, value="fast")
    fast_radio.grid(row=0, column=0, sticky="w", pady=5)
    
    continuous_radio = ttk.Radiobutton(mode_frame, text="Continuous Mode", variable=mode_var, value="continuous")
    continuous_radio.grid(row=1, column=0, sticky="w", pady=5)
    
    # Create description labels
    fast_desc = ttk.Label(mode_frame, text="Quick search, exit on first find", font=("Arial", 10))
    fast_desc.grid(row=0, column=1, sticky="w", padx=10, pady=5)
    
    continuous_desc = ttk.Label(mode_frame, text="Find multiple coupons, save to file", font=("Arial", 10))
    continuous_desc.grid(row=1, column=1, sticky="w", padx=10, pady=5)
    
    # Create start button
    def start_selected_mode():
        selected_mode = mode_var.get()
        root.destroy()  # Close the UI
        
        if selected_mode == "fast":
            # Run fast mode without showing popup at the end
            fast_mode()
        else:
            results = continuous_mode()
            if results:
                messagebox.showinfo("Success", f"Found {len(results)} coupons: {', '.join(results)}")
    
    start_button = ttk.Button(root, text="Start", command=start_selected_mode)
    start_button.pack(pady=20)
    
    # Create info label
    info_label = ttk.Label(root, text="Press DELETE key anytime to stop the script", font=("Arial", 10))
    info_label.pack(pady=10)
    
    # Run the UI
    root.mainloop()

# Main entry point
if __name__ == "__main__":
    create_ui()
