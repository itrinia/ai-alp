import tkinter as tk
from tkinter import messagebox
import random
import functools

class KlooDoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Kloo-Do Game")

        # Set the initial window size
        self.master.geometry("800x500")
        # Allow both width and height to be resizable
        self.master.resizable(width=True, height=True)

        self.original_characters = ["Budi", "Bambang", "Jevon", "Aladdin", "Charlotte"]
        self.original_weapons = ["Keris", "Lifebuoy", "Gun", "Carpet", "Broomstick"]
        self.original_locations = ["Beach", "Bathroom", "Sea", "Sky", "Bar"]
        self.actions = ["Massaging", "Party", "Sleeping", "Sweeping", "Singing"]
        self.distance = ["10", "500", "3", "100", "20"]

        # Add the characters attribute
        self.characters = self.original_characters.copy()
        self.storyline_count = 1
        self.current_storyline = 0
        self.max_incorrect_guesses = 3
        self.incorrect_guesses = 0
        self.user_score = 0
        self.system_score = 0

        self.create_widgets()

        # Generate the first storyline and clues
        self.generate_storyline()
        # Directly set the correct_answer attribute based on the current storyline
        self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"

        # Update the score display initially
        self.update_score_display()

    def create_widgets(self):
        self.story_label = tk.Label(self.master, text="Storyline", font=("Helvetica", 16, "bold"))
        self.story_label.pack(pady=10)

        self.story_text = tk.Text(self.master, height=8, width=80, wrap=tk.WORD, font=("Helvetica", 12))
        self.story_text.pack(pady=10)

        self.clue_button = tk.Button(self.master, text="Clue", command=self.show_clues, font=("Helvetica", 12))
        self.clue_button.pack(pady=5)

        self.name_label = tk.Label(self.master, text="Your Guess - Name:", font=("Helvetica", 12))
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        self.location_label = tk.Label(self.master, text="Your Guess - Location:", font=("Helvetica", 12))
        self.location_label.pack()

        self.location_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.location_entry.pack(pady=5)

        self.weapon_label = tk.Label(self.master, text="Your Guess - Weapon:", font=("Helvetica", 12))
        self.weapon_label.pack()

        self.weapon_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.weapon_entry.pack(pady=5)

        # Modify the 'Submit' button to use functools.partial
        self.submit_button = tk.Button(self.master, text="Submit", command=functools.partial(self.check_answer, True),
                                       font=("Helvetica", 12, "bold"))
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.master, text=f"User Score: {self.user_score} | System Score: {self.system_score}",
                                    font=("Helvetica", 12, "italic"))
        self.score_label.pack(pady=10)

    def shuffle_characters(self):
        # Shuffle the characters once before each game
        random.shuffle(self.original_characters)

    def generate_storyline(self):
        # Clear the existing storyline
        self.story_text.delete(1.0, tk.END)

        # Reset the locations and weapons lists to their original state
        self.weapons = self.original_weapons.copy()
        self.locations = self.original_locations.copy()

        # Reset characters in each storyline
        self.characters = self.original_characters.copy()

        # Shuffle characters before each storyline
        self.shuffle_characters()

        # Randomly select the killed character from the list
        victim = random.choice(self.characters)
        self.characters.remove(victim)  # Remove the killed character from the list

        # Randomly select the killer from the shuffled list
        killer = self.characters[0]
        weapon = self.weapons[0]

        # Shuffle weapons and locations
        random.shuffle(self.weapons)
        random.shuffle(self.locations)

        storyline = f"{victim} is killed at the {self.locations[1]} and a {self.weapons[1]} is found beside him. "
        storyline += f"\nThe characters at that place:\n"

        # Assign random actions and locations to other characters
        for char, act, weap, loc, dist in zip(self.characters, self.actions, self.weapons[1:], self.locations[1:], self.distance[1:]):
            storyline += f"- {char} is {act} and bringing {weap} {dist} meters from the murder location in {loc}.\n"

        self.story_text.insert(tk.END, storyline)

        # Set the correct answer after shuffling (move this line here)
        self.correct_answer = f"The Killer: {killer}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {weapon}\n"

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

    def check_answer(self, is_submit):
        name_guess = self.name_entry.get().lower()
        location_guess = self.location_entry.get().lower()
        weapon_guess = self.weapon_entry.get().lower()

        if name_guess == self.characters[0].lower() and \
                location_guess == self.locations[self.current_storyline].lower() and \
                weapon_guess == self.weapons[0].lower():
            self.user_score += 1
            self.update_score_display()  # Move the update_score_display() call here
            messagebox.showinfo("Correct", "Congratulations! You solved the mystery. You got 1 score!")

            # If the user has reached a score of 3 or it's the last storyline, end the game
            if self.user_score >= 3 or self.current_storyline == len(self.original_locations) - 1:
                self.end_game()
            else:
                # Move to the next storyline
                self.current_storyline += 1
                self.generate_storyline()
                # Directly set the correct_answer attribute based on the current storyline
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
        else:
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.max_incorrect_guesses:
                self.system_score += 1
                self.update_score_display()  # Add this line to update the score display
                messagebox.showinfo("Game Over", f"Sorry, you've reached the maximum incorrect guesses.\n"
                                                f"The correct answer is:\n {self.correct_answer}\n The system got 1 score! You defeated :p")
                self.reset_game()
            elif is_submit:  # Check if it's a submit action
                messagebox.showinfo("Incorrect", "Sorry, your answer is incorrect. Keep investigating!")

    def end_game(self):
        if self.user_score >= 3:
            messagebox.showinfo("Game Over", "Congratulations! You are the winner with a score of 3.")
        else:
            messagebox.showinfo("Game Over", "Game over! It's a draw.")
        self.master.destroy()  # Close the application when the game is over

    def reset_game(self):
        self.story_text.delete(1.0, tk.END)
        self.incorrect_guesses = 0  # Reset the incorrect guesses to zero

        # Check if the user has reached a score of 3
        if self.user_score >= 3:
            messagebox.showinfo("Game Over", "Congratulations! You are the winner with a score of 3.")
            self.master.destroy()  # Close the application when the game is over
        elif self.system_score >= 3:  # Check if the system has reached a score of 3
            messagebox.showinfo("Game Over", "Sorry, the system is the winner with a score of 3.")
            self.master.destroy()  # Close the application when the game is over
        else:  # Check if the game should continue or if someone has won
            if self.user_score < 3 and self.system_score < 3 and self.current_storyline < len(self.original_locations) - 1:
                self.current_storyline += 1  # Move to the next storyline
                self.generate_storyline()
                # Directly set the correct_answer attribute based on the current storyline
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}"
            elif self.user_score < 3 and self.system_score < 3 and self.current_storyline == len(self.original_locations) - 1:
                self.generate_storyline()
                # Directly set the correct_answer attribute based on the current storyline
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
            else:
                messagebox.showinfo("Game Over", "Game over! It's a draw.")
                self.master.destroy()  # Close the application when the game is over

    def update_score_display(self):
        self.score_label.config(text=f"User Score: {self.user_score} | System Score: {self.system_score}", font=("Helvetica", 12, "italic"))


def main():
    root = tk.Tk()
    game = KlooDoGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
