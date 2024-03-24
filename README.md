# wordle_solver
Overview
dscord:L is a Python-based automation tool designed to interact with word puzzle games, like Wordle, by taking screenshots of the game's rows, analyzing the colors to interpret feedback, and making subsequent guesses based on a predefined list of words. It automates the process of playing these games by simulating keyboard inputs for guesses and navigating through the game's feedback.

Features
Automated Guessing: Automatically types guesses into the game based on analysis and a predefined word list.
Feedback Interpretation: Interprets the color-coded feedback from the game to refine future guesses.
Screenshot Analysis: Takes and analyzes screenshots of the game at various stages to determine the game's feedback.
Adaptive Strategy: Adapts the guessing strategy based on the game's feedback using color mapping and list refinement techniques.
Requirements
Python 3.x
pyautogui
PIL (Python Imaging Library)
NumPy
Setup
Ensure Python 3.x is installed on your system.
Install required Python packages:
