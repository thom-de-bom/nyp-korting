# Pizza Coupon Finder

This script automates the process of finding valid coupon codes for New York Pizza (Netherlands). It uses image recognition to detect when a valid coupon has been found and can operate in two different modes.

## Dependencies

Before using this script, you need to install the following Python packages:

```bash
pip install pyautogui
pip install keyboard
pip install pyperclip
```

You also need to have the following files in the `images` folder (which should be in the same directory as the script):
- `images/box.jpg` - Image of the coupon input field
- `images/NOGEENCOUPON.png` - Image that appears when a valid coupon is found
- `images/verwijder.png` - Image of the "verwijder" (remove) button for continuous mode

## How to Use

### Step 1: Prepare Your Order

1. Go to [New York Pizza](https://www.newyorkpizza.nl/)
2. Add the pizzas you want to your cart
   - **Important**: Add at least 2 pizzas to benefit from the "2nd pizza free" promotions
   - **Note**: Action pizzas and special items typically don't work with coupon codes

### Step 2: Go to Checkout

1. Proceed to the checkout page
2. Click on the button labeled "Do you have a coupon code or membership discount?"
3. This will open the coupon code input field

### Step 3: Prepare the Script

1. Make sure the New York Pizza checkout page is open and visible
2. The coupon input field should be visible on screen

### Step 4: Run the Script

1. Run the script: `python pizzakorting-nyp.py`
2. A GUI will appear with two mode options
3. Select your preferred mode (see below for details)
4. Click "Start"
5. The script will automatically:
   - Switch to the New York Pizza tab (using Alt+Tab)
   - Find the coupon input field
   - Start trying coupon codes

### Step 5: Using the Results

- If a valid coupon is found, it will be applied to your order
- In Continuous Mode, the coupon will also be saved to `Coupons.txt`
- You can press and hold the DELETE key at any time to stop the script

## Operating Modes

### Fast Mode

**Description**: Quickly finds a valid coupon without saving it or showing notifications.

**Advantages**:
- Faster operation (fewer checks, shorter delays)
- Simpler process (just find a coupon and stop)
- No popup notifications to interrupt the flow

**Disadvantages**:
- Doesn't save found coupons
- May not be as accurate in identifying which exact code worked
- Exits immediately after finding a coupon

**When to use**:
- When you just need a quick discount for your current order
- When you don't care about saving coupons for later
- When speed is more important than collecting multiple coupons

### Continuous Mode

**Description**: Finds multiple valid coupons, saves them to a file, and continues searching.

**Advantages**:
- Saves all found coupons to `Coupons.txt` with dates
- Can find multiple coupons in one session
- More thorough verification of valid coupons
- Automatically continues after finding a coupon by clicking the "verwijder" button

**Disadvantages**:
- Slower operation (more checks, longer delays)
- More complex process
- Shows popup notifications at the end

**When to use**:
- When you want to collect multiple coupons for future use
- When accuracy of saved coupons is important
- When you want to build a database of working coupons

## Project Structure

```
pizza-coupon-finder/
├── pizzakorting-nyp.py  # Main script
├── README.md            # This documentation
├── Coupons.txt          # Saved coupons (created automatically)
└── images/              # Folder containing reference images
    ├── box.jpg          # Image of the coupon input field
    ├── NOGEENCOUPON.png # Image that appears when a valid coupon is found
    └── verwijder.png    # Image of the "verwijder" (remove) button
```

## Troubleshooting

- **Script can't find the input field**: Make sure the coupon input field is clearly visible on screen and the `images/box.jpg` file matches what's on screen
- **Script doesn't recognize valid coupons**: Try adjusting the confidence level in the script
- **Script stops unexpectedly**: Check if the website layout has changed
- **"verwijder" button not found**: Make sure the button is visible and matches the `images/verwijder.png` image

## Technical Notes

- The script uses weighted random number generation to focus on ranges that are more likely to contain valid coupons
- Image recognition is used to detect the input field, valid coupons, and navigation buttons
- The script keeps track of tried numbers to avoid duplicates
- In Continuous Mode, found coupons are saved in the format `code|YYYY-MM-DD`

## Limitations

- The script relies on image recognition, so changes to the website layout may break functionality
- Some valid coupons may be missed if the confidence level is set too high
- Some invalid coupons may be incorrectly identified as valid if the confidence level is set too low
- The script cannot bypass website security measures or generate valid coupons; it only tries random codes

## Legal Disclaimer

This script is provided for educational purposes only. Use it responsibly and in accordance with New York Pizza's terms of service. The authors are not responsible for any misuse of this script.
