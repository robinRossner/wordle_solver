import pyautogui
import time
from PIL import Image
import numpy as np
import random

directory = ""

time.sleep(5)

def first_row():
    x, y, width, height = 1420, 440, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot1.png")
    return screenshot

def second_row():
    x, y, width, height = 1420, 565, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot2.png")
    return screenshot

def third_row():
    x, y, width, height = 1420, 685, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot3.png")
    return screenshot

def fourth_row():
    x, y, width, height = 1420, 805, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot4.png")
    return screenshot

def fifth_row():
    x, y, width, height = 1420, 925, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot5.png")
    return screenshot

def sixth_row():
    x, y, width, height = 1420, 1045, 615, 100
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(directory, "shot6.png")
    return screenshot

def closest_color(rgb):
    # Predefined colors with their labels
    colors = {
        "g": (135, 182, 94),  # Green
        "w": (254, 254, 254), # White
        "y": (235, 196, 84),  # Yellow
        "b": (168, 176, 193)  # Gray
    }
    
    # Function to calculate the distance between two colors
    def color_distance(c1, c2):
        return sum((a-b)**2 for a, b in zip(c1, c2))**0.5
    
    # Find the closest color based on distance
    closest = min(colors, key=lambda color: color_distance(colors[color], rgb))
    return closest

def map_colors_to_code_adjusted(image):
    # Convert image to numpy array
    img_array = np.array(image)

    # Check for alpha channel and remove it
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    # Adjusted color thresholds to be more permissive
    color_thresholds = {
        'b': ([160, 160, 180], [190, 190, 210]),  # Broadened Gray
        'y': ([140, 140, 0], [255, 255, 160]), # Broadened Yellow
        'g': ([66, 140, 2], [243, 247, 238]),    # Broadened Green
        'w': ([200, 200, 200], [255, 255, 255])# Broadened White
    }

    # Define a function to determine the color of a pixel
    def get_color(pixel):
        for color_code, (low, high) in color_thresholds.items():
            if all(low[i] <= pixel[i] <= high[i] for i in range(3)):
                return color_code
        return 'x'  # 'x' will be used for any color not in the predefined set

    # Divide the image width by 5 to get the width of each vertical section
    section_width = image.width // 5
    color_code_result = []

    # Process each section to determine the majority color
    for section in range(5):
        # Get all the pixels in the current section
        section_pixels = img_array[:, section*section_width:(section+1)*section_width].reshape(-1, 3)
        # Map each pixel to its color code
        color_codes = [get_color(pixel) for pixel in section_pixels]
        # Find the most common color code in this section
        most_common_color = max(set(color_codes), key=color_codes.count)
        color_code_result.append(most_common_color)

    return ''.join(color_code_result)

def classify_and_condense_rgb(rgb_values):
    classified_rgb_values = [closest_color(rgb) for rgb in rgb_values]
    condensed_rgb_values = [classified_rgb_values[0]]
    for color in classified_rgb_values[1:]:
        if color != condensed_rgb_values[-1]:
            condensed_rgb_values.append(color)
    # Exclude 'w' and limit to the first 5 colors
    filtered_colors = [color for color in condensed_rgb_values if color != 'w'][:6]
    return filtered_colors

count = 0
image_path = [
    directory, "shot1.png",
    directory, "shot2.png",
    directory, "shot3.png",
    directory, "shot4.png",
    directory, "shot5.png",
    directory, "shot6.png"
]

# Define the mapping of attempt numbers to screenshot functions
screenshot_function_mapping = {
    0: first_row,
    1: second_row,
    2: third_row,
    3: fourth_row,
    4: fifth_row,  # Corrected the typo here from 'fifth_row' to 'fifth_row'
    5: sixth_row
}

row0=[]
row1=[]
row2=[]
row3=[]
row4=[]
row5=[]

l1=[row0,row1,row2,row3,row4,row5]
# Adjust the loop condition to match the number of images
# Define new helper functions
def load_word_list(filepath):
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file.readlines() if len(line.strip()) == 5]
    return words

def refine_word_list(words, guess, feedback):
    for i, feedback_code in enumerate(feedback):
        if feedback_code == 'g':
            words = [word for word in words if word[i] == guess[i]]
        elif feedback_code == 'y':
            words = [word for word in words if guess[i] in word and word[i] != guess[i]]
        elif feedback_code == 'b':
            words = [word for word in words if guess[i] not in word]
    return words

def make_a_guess(word_list):
    return random.choice(word_list) if word_list else None

def type_guess(guess):
    for char in guess:
        pyautogui.press(char)
    pyautogui.press('enter')

def delete_last_guess():
    for _ in range(5):
        pyautogui.press('backspace')

# Load your word list from file
wordlist_path = directory, "five_letter_words.txt"

# Define the coordinates where to click for a win or a loss
win_click_position = (872, 389)  # Replace with actual coordinates for win action
loss_click_position = (868, 474)  # Replace with actual coordinates for loss action


while True:  # Change to an infinite loop

    attempt = 0
    word_list = load_word_list(wordlist_path)  # Ensure word_list is reset for each game
    guesses_made = []  # Reset for each game
    feedback_list = []  # Reset for each game
    count=0
    while attempt < 6:
        if not word_list:
            print("No more words left to guess.")
            break
        
        guess = make_a_guess(word_list) if attempt == 0 else make_a_guess(refine_word_list(word_list, guesses_made[-1], feedback_list[-1]))
        
        type_guess(guess)
        time.sleep(2)

        img = screenshot_function_mapping[attempt]()
        feedback = map_colors_to_code_adjusted(img)
        
        if 'w' in feedback:
            delete_last_guess()
            count -= 1
            word_list = load_word_list(wordlist_path)
            time.sleep(2)
            continue

        guesses_made.append(guess)
        feedback_list.append(feedback)
        print(f"Attempt {attempt + 1}: Guess '{guess}' gave feedback '{feedback}'")
        
        word_list = refine_word_list(word_list, guess, feedback)
        time.sleep(2)

        if feedback == 'ggggg':
            print(f"Word guessed correctly: {guess}")
            pyautogui.click(*win_click_position)
            break

        attempt += 1

    if feedback_list and feedback_list[-1] != 'ggggg':
        print("Failed to guess the correct word after 6 attempts.")
        pyautogui.click(*loss_click_position)
    
    time.sleep(5)  # Wait a bit before starting the next game or checking for the '5' key again