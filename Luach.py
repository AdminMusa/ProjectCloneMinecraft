import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import os
import random
import subprocess


# List of icon files (textures) to choose from randomly
icon_files = [
    'grass.png', 'stone.png', 'wood.png', 'leaves.png', 'bedrock.png',
    'brick.png', 'coal ore.png', 'diamond ore.png', 'furnace.png', 'obsidian.png',
    'sand.png', 'sandstone.png', 'stoneBricks.png', 'tnt.png', 'woodenplanks.png'
]

class TextureLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project MoonCraft Launcher")
        self.geometry("400x400")
        self.resizable(False, False)

        # Set the background image (Sky0)
        sky_image = Image.open("Sky0.png")
        sky_image = sky_image.resize((400, 400))  # Resize to fit window
        self.bg_image = ImageTk.PhotoImage(sky_image)
        bg_label = Label(self, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Randomize the icon
        self.random_icon = random.choice(icon_files)

        # Display random icon with "MOONCRAFT" text
        self.icon_image = Image.open(self.random_icon)
        self.icon_image = self.icon_image.resize((100, 100))
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.icon_label = Label(self, image=self.icon_photo, text="MOONCRAFT", font=("Arial", 24, "bold"), bg="white", fg="black", compound="top")
        self.icon_label.pack(pady=20)

        # "Start Now" Button
        self.start_button = tk.Button(self, text="Start Now", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        # Run the MoonCraft.py script when the "Start Now" button is clicked
        try:
            subprocess.run(['python', 'MoonCraft.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the game: {e}")
        finally:
            # Close the launcher window after running the game
            self.destroy()

if __name__ == "__main__":
    app = TextureLauncher()
    app.mainloop()
