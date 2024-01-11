import tkinter as tk
from tkinter import messagebox
import random
import functools

class KlooDoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Kloo-Do Game")
        self.round_counter = 1

        # Set the initial window size
        self.master.geometry("800x600")
        # Allow both width and height to be resizable
        self.master.resizable(width=True, height=True)

        self.original_characters = ["Budi", "Bambang", "Jevon", "Aladdin", "Charlotte"]
        self.original_weapons = ["Keris", "Lifebuoy", "Gun", "Carpet", "Broomstick"]
        self.original_locations = ["Beach", "Bathroom", "Sea", "Sky", "Bar"]
        self.actions = ["Massaging", "Party", "Sleeping", "Sweeping", "Singing"]
        self.distance = ["10", "500", "3", "100", "20"]

        # Add the characters attribute
        self.characters = self.original_characters.copy()
        self.weapons = self.original_weapons.copy()
        self.locations = self.original_locations.copy()
        self.storyline_count = 1
        self.current_storyline = 0
        self.max_incorrect_guesses = 3
        self.incorrect_guesses = 0
        self.user_score = 0
        self.system_score = 0

        # Create knowledge base using First Order Logic
        self.knowledge_base = []
        for character in self.original_characters:
            for location in self.original_locations:
                for weapon in self.original_weapons:
                    knowledge = {
                        "character": character,
                        "location": location,
                        "weapon": weapon,
                        "sentence": f"The Killer: {character}\nThe location: {location}\nThe weapon: {weapon}\n"
                    }
                    self.knowledge_base.append(knowledge)

        self.create_widgets()

        # Generate the first storyline and clues
        self.generate_storyline()
        # Directly set the correct_answer attribute based on the current storyline
        self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
        self.round_counter += 1

        # Update the score display initially
        self.update_score_display()

    def create_widgets(self):
        self.user_score_label = tk.Label(self.master, text="User Score: 0", font=("Helvetica", 12, "italic"), bg="pink")
        self.user_score_label.pack(pady=5)

        self.system_score_label = tk.Label(self.master, text="System Score: 0", font=("Helvetica", 12, "italic"), bg="pink")
        self.system_score_label.pack(pady=5)
        self.story_label = tk.Label(self.master, text="Storyline", font=("Helvetica", 16, "bold"), bg="lightblue")
        self.story_label.pack(pady=10)

        self.story_text = tk.Text(self.master, height=8, width=80, wrap=tk.WORD, font=("Helvetica", 12), bg="lightyellow")
        self.story_text.pack(pady=10)

        self.clue_button = tk.Button(self.master, text="Clue", command=self.show_clues, font=("Helvetica", 12), bg="lightgreen")
        self.clue_button.pack(pady=5)

        self.name_label = tk.Label(self.master, text="Guess killer's name:", font=("Helvetica", 12), bg="lightblue")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        self.location_label = tk.Label(self.master, text="Guess murder location:", font=("Helvetica", 12), bg="lightblue")
        self.location_label.pack()

        self.location_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.location_entry.pack(pady=5)

        self.weapon_label = tk.Label(self.master, text="Guess murder weapon:", font=("Helvetica", 12), bg="lightblue")
        self.weapon_label.pack()

        self.weapon_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.weapon_entry.pack(pady=5)

        # Modify the 'Submit' button to use functools.partial
        self.submit_button = tk.Button(self.master, text="Submit", command=functools.partial(self.check_answer, True),
                                       font=("Helvetica", 12, "bold"), bg="orange", fg="white")
        self.submit_button.pack(pady=10)

    def generate_order(self, original_list):
    # Generate a deterministic order based on the original order
        order = list(range(len(original_list)))
        random.shuffle(order)  # You can replace this line with a deterministic shuffling logic if needed
        return [original_list[i] for i in order]

    def shuffle_characters(self):
        # Generate deterministic orders for characters, weapons, and locations
        self.characters = self.generate_order(self.original_characters)
        self.weapons = self.generate_order(self.original_weapons)
        self.locations = self.generate_order(self.original_locations)

        # Set the victim as the first character in the new order
        victim_index = self.characters.index(self.original_characters[0])

        # Place the victim at a random position in the new order
        random_position = random.randint(0, len(self.characters) - 1)
        self.characters.insert(random_position, self.characters.pop(victim_index))

    def generate_storyline(self):
        self.story_text.delete(1.0, tk.END)

        # Shuffle the characters list
        random.shuffle(self.characters)

        # Use the characters list without shuffling
        victim = self.characters[0]

        # Ensure that the killer is not the same as the victim
        potential_killers = [char for char in self.characters[1:] if char != victim]
        killer = random.choice(potential_killers)

        weapon = self.weapons[0]

        storyline = f"{victim} is killed at the {self.locations[0]} and a {self.weapons[0]} is found beside him. "
        storyline += f"\nThe characters at that place:\n"

        # Initialize variables for current weapon, location, and distance
        current_weapon = self.weapons[1:]
        current_location = self.locations[1:]
        current_distance = self.distance[1:]

        for char, act, weap, loc, dist in zip(self.characters[1:], self.actions, current_weapon, current_location, current_distance):
            storyline += f"- {char} is {act} and bringing {weap} {dist} meters from the murder location in {loc}.\n"

        self.story_text.insert(tk.END, storyline)

        self.correct_answer = f"The Killer: {killer}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"

        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.weapon_entry.delete(0, tk.END)


    def show_clues(self):
        actor_clue = self.generate_clue(self.characters[0])
        location_clue = self.generate_clue(self.locations[self.current_storyline])
        weapon_clue = self.generate_clue(self.weapons[0])

        messagebox.showinfo("Clues", f"Clue for Actor:\n{actor_clue}\n\nClue for Location:\n{location_clue}\n\nClue for Weapon:\n{weapon_clue}")

    def generate_clue(self, correct_answer):
        correct_answer = correct_answer.upper()

        grid_size = (10, 10)
        grid = [[' ' for _ in range(grid_size[1])] for _ in range(grid_size[0])]

        # Determine the starting position based on the length of the correct answer
        start_row = random.randint(0, grid_size[0] - 1)
        start_col = random.randint(0, grid_size[1] - len(correct_answer))

        # Embed the correct answer into the grid based on a rule (show only consonants)
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
        for i, char in enumerate(correct_answer):
            if char in consonants:
                grid[start_row][start_col + i] = f'{char}'

        # Fill the remaining grid with random vowels or spaces
        vowels = "AEIOU"
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                if grid[row][col] == ' ':
                    # Use '_' to represent empty spaces in the crossword
                    grid[row][col] = f'{random.choice(vowels)}'

        clue_text = '\n'.join([' '.join(row) for row in grid])

        return clue_text

    def check_answer(self, is_submit):
        name_guess = self.name_entry.get().lower()
        location_guess = self.location_entry.get().lower()
        weapon_guess = self.weapon_entry.get().lower()

        if not name_guess or not location_guess or not weapon_guess:
            messagebox.showinfo("Error", "Please fill in all guess boxes.")
            return

        if name_guess == self.characters[0].lower() and \
            location_guess == self.locations[self.current_storyline].lower() and \
            weapon_guess == self.weapons[0].lower():
            self.user_score += 1
            self.update_score_display()
            messagebox.showinfo("Correct", "Congratulations! You solved the mystery. You got 1 score!")

            self.knowledge_base.append({
                "character": self.characters[0],
                "location": self.locations[self.current_storyline],
                "weapon": self.weapons[0],
                "sentence": f"The user guessed correctly: {self.characters[0]}, {self.locations[self.current_storyline]}, {self.weapons[0]}\n"
            })

            if self.user_score >= 3 or self.current_storyline == len(self.original_locations) - 1:
                self.end_game()
            else:
                self.current_storyline += 1
                self.generate_storyline()
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
        else:
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.max_incorrect_guesses:
                self.system_score += 1
                self.update_score_display()
                messagebox.showinfo("Game Over", f"Sorry, you've reached the maximum incorrect guesses.\n"
                                                f"The correct answer is:\n {self.correct_answer}\n The system got 1 score! You defeated :p")
                self.reset_game()
            elif is_submit:
                messagebox.showinfo("Incorrect", "Sorry, your answer is incorrect. Keep investigating!")

    def update_score_display(self):
        self.user_score_label.config(text=f"User Score: {self.user_score}")
        self.system_score_label.config(text=f"System Score: {self.system_score}")

    def end_game(self):
        if self.user_score >= 3:
            messagebox.showinfo("Game Over", "Congratulations! You are the winner with a score of 3.")
        else:
            messagebox.showinfo("Game Over", "Game over! It's a draw.")
        self.master.destroy()

    def reset_game(self):
        self.story_text.delete(1.0, tk.END)
        self.incorrect_guesses = 0

        if self.user_score >= 3:
            messagebox.showinfo("Game Over", "Congratulations! You are the winner with a score of 3.")
            self.master.destroy()
        elif self.system_score >= 3:
            messagebox.showinfo("Game Over", "Sorry, the system is the winner with a score of 3.")
            self.master.destroy()
        else:
            if self.user_score < 3 and self.system_score < 3 and self.current_storyline < len(self.original_locations) - 1:
                self.current_storyline += 1
                self.generate_storyline()
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}"
            elif self.user_score < 3 and self.system_score < 3 and self.current_storyline == len(self.original_locations) - 1:
                self.generate_storyline()
                self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
            else:
                messagebox.showinfo("Game Over", "Game over! It's a draw.")
                self.master.destroy()

def main():
    root = tk.Tk()
    game = KlooDoGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
