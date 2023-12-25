import tkinter as tk
from tkinter import messagebox
import random

class KlooDoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Kloo-Do Game")

        self.characters = ["Budi", "Bambang", "Jevon", "Aladdin", "Charlotte"]
        self.weapons = ["Keris", "Lifebuoy", "Gun", "Carpet", "Bag with Bullets"]
        self.locations = ["Beach", "Bathroom", "Sea", "Sky", "Bar"]

        self.storyline_count = 1
        self.current_storyline = 0
        self.max_incorrect_guesses = 3
        self.incorrect_guesses = 0

        self.create_widgets()

        # Generate the first storyline and clues
        self.generate_storyline()
        self.correct_answer = self.get_correct_answer()  # Store the correct answer

    def create_widgets(self):
        self.story_label = tk.Label(self.master, text="Storyline")
        self.story_label.pack()

        self.story_text = tk.Text(self.master, height=5, width=80)
        self.story_text.pack()

        self.clue_button = tk.Button(self.master, text="Clue", command=self.show_clues)
        self.clue_button.pack()

        self.name_label = tk.Label(self.master, text="Your Guess - Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack()

        self.location_label = tk.Label(self.master, text="Your Guess - Location:")
        self.location_label.pack()

        self.location_entry = tk.Entry(self.master)
        self.location_entry.pack()

        self.weapon_label = tk.Label(self.master, text="Your Guess - Weapon:")
        self.weapon_label.pack()

        self.weapon_entry = tk.Entry(self.master)
        self.weapon_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer)
        self.submit_button.pack()

    def generate_storyline(self):
        # Clear the existing storyline
        self.story_text.delete(1.0, tk.END)

        characters = random.sample(self.characters, 5)
        weapons = random.sample(self.weapons, 5)
        locations = random.sample(self.locations, 5)

        self.correct_answer = f"{characters[0]} {locations[self.current_storyline]} {weapons[0]}"  # Set the correct answer

        storyline = f"In the {locations[self.current_storyline]}, there is a murder case. "
        storyline += f"{characters[0]} was killed and found dead below the coconut tree. "
        storyline += f"In the {locations[self.current_storyline]}, there are only 5 people:\n"
        for char, weap in zip(characters[1:], weapons[1:]):
            storyline += f"{char} is in the {locations[self.characters.index(char)]}, "
            storyline += f"carrying a {weap} and doing something specific. "
        storyline += f"{characters[-1]} is in the corner of the {locations[self.current_storyline]}, "
        storyline += f"carrying a {weapons[-1]} and sleeping."

        self.story_text.insert(tk.END, storyline)

    def show_clues(self):
        # Pass correct answers for each clue
        actor_clue = self.generate_clue(self.characters[0])
        location_clue = self.generate_clue(self.locations[self.current_storyline])
        weapon_clue = self.generate_clue(self.weapons[0])

        messagebox.showinfo("Clues", f"Clue for Actor:\n{actor_clue}\n\nClue for Location:\n{location_clue}\n\nClue for Weapon:\n{weapon_clue}")

    def generate_clue(self, correct_answer):
        # Convert the correct answer to uppercase
        correct_answer = correct_answer.upper()

        # Create a grid for the crossword puzzle
        grid_size = (10, 10)
        grid = [[' ' for _ in range(grid_size[1])] for _ in range(grid_size[0])]

        # Ensure the range for start_row is valid
        max_start_row = max(0, grid_size[0] - len(correct_answer))
        start_row = random.randint(0, max_start_row)

        # Ensure the range for start_col is valid
        max_start_col = max(0, grid_size[1] - len(correct_answer))
        start_col = random.randint(0, max_start_col)

        # Embed the correct answer into the grid horizontally
        for i, char in enumerate(correct_answer):
            grid[start_row][start_col + i] = char

        # Fill the remaining grid with random alphabets
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                if grid[row][col] == ' ':
                    grid[row][col] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # Convert the grid to a string
        clue_text = '\n'.join([' '.join(row) for row in grid])

        return clue_text



    def check_answer(self):
        name_guess = self.name_entry.get().lower()
        location_guess = self.location_entry.get().lower()
        weapon_guess = self.weapon_entry.get().lower()

        if name_guess == self.characters[0].lower() and \
           location_guess == self.locations[self.current_storyline].lower() and \
           weapon_guess == self.weapons[0].lower():
            messagebox.showinfo("Correct", "Congratulations! You solved the mystery.")
            self.reset_game()
        else:
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.max_incorrect_guesses:
                messagebox.showinfo("Game Over", f"Sorry, you've reached the maximum incorrect guesses.\n"
                                                 f"The correct answer is: {self.correct_answer}")
                self.reset_game()
            else:
                messagebox.showinfo("Incorrect", "Sorry, your answer is incorrect. Keep investigating!")

    def reset_game(self):
        self.story_text.delete(1.0, tk.END)
        self.current_storyline = 0
        self.incorrect_guesses = 0
        self.generate_storyline()
        self.correct_answer = self.get_correct_answer()  # Store the correct answer

    def get_correct_answer(self):
         return self.correct_answer

def main():
    root = tk.Tk()
    game = KlooDoGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
