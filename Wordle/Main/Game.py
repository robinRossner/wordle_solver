import time

def determine_win():
    pass

directory = ""

filename = (directory,'main.py')

while True:
    with open(filename) as file:
        exec(file.read())
    time.sleep(5)  # Wait a bit before starting the next game or checking for the '5' key againmudra
    