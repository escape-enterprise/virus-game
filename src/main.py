# Virus Escape Room PC Puzzle
# by Caleb "fivesixfive" North

# Constants
RESOLUTION = (1920, 1080)

# Imports
import pygame as g

def main():
    # Initialize PyGame
    g.init()
    # Create Window
    g.display.set_mode(RESOLUTION, g.FULLSCREEN)
    g.display.set_caption("Virus Game")

def loop():
    while True:
        for event in g.event.get():
            
        g.display.update()

# Execute
if __name__ == "__main__":
    main()
    loop()
