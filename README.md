# Pygame Block Breaker

A simple block-breaker game made with Pygame. This was created as a practice project to learn about game loops, sprite management, and collision detection.

## Description

The player controls a paddle at the bottom of the screen and must use a ball to break all the blocks at the top. If the ball falls past the paddle, it resets to the center of the screen.

## How to Run

### Prerequisites

- Python 3.x
- Pygame

### Installation

1.  Make sure Python is installed.
2.  Install Pygame:
    ```sh
    pip install pygame
    ```
3.  Run the script from your terminal:
    ```sh
    python your_game_name.py
    ```

## Controls

-   **A**: Move paddle left
-   **D**: Move paddle right

## Packaging for Distribution

To create a standalone `.exe` file that can be run on other Windows computers without needing Python or Pygame installed:

1.  Install PyInstaller:
    ```sh
    pip install pyinstaller
    ```
2.  Run the packaging command from the script's directory:
    ```sh
    pyinstaller --onefile --windowed your_game_name.py
    ```
3.  The final `.exe` will be located in the `dist` folder.


