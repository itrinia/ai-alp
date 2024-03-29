import tkinter as tk
from tkinter import messagebox
import random
import functools
from transformers import pipeline

class KlooDoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Kloo-Do Game")
        self.round_counter = 1
        
        # Initialize the NLP model for text generation
        self.text_generator = pipeline("text-generation")

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
        
        # old code
        # # Add the characters attribute
        # self.characters = self.original_characters.copy()
        # self.storyline_count = 1
        # self.current_storyline = 0
        # self.max_incorrect_guesses = 3
        # self.incorrect_guesses = 0
        # self.user_score = 0
        # self.system_score = 0

        # self.create_widgets()

        # Generate the first storyline and clues
        self.generate_storyline()
        # Directly set the correct_answer attribute based on the current storyline
        self.correct_answer = f"The Killer: {self.characters[0]}\nThe location: {self.locations[self.current_storyline]}\nThe weapon: {self.weapons[0]}\n"
        self.round_counter += 1

        # Update the score display initially
        self.update_score_display()
        
    def generate_dynamic_storyline(self):
        # Use the NLP model to generate a dynamic storyline
        prompt = "In a mysterious place, "
        generated_text = self.text_generator(prompt, max_length=200, num_return_sequences=1, temperature=0.8)[0]['generated_text']

        # Extract relevant information from the generated text (character, location, weapon)
        # You may need to fine-tune this based on the output of your specific model
        character, location, weapon = self.extract_information(generated_text)

        # Update game attributes
        self.characters[0] = character
        self.locations[self.current_storyline] = location
        self.weapons[0] = weapon

        # Display the generated storyline
        self.story_text.delete(1.0, tk.END)
        storyline = f"{character} is killed at the {location} and a {weapon} is found beside him."
        self.story_text.insert(tk.END, storyline)

        # Set the correct answer after dynamic generation
        self.correct_answer = f"The Killer: {character}\nThe location: {location}\nThe weapon: {weapon}\n"

    def extract_information(self, generated_text):
        # Extract relevant information using custom logic
        # This function needs to be adapted based on the output of your specific model
        # For simplicity, we assume that the generated text follows a certain pattern
        # You may need to use more sophisticated techniques for a real-world application
        character = "Budi"
        location = "Beach"
        weapon = "Keris"

        return character, location, weapon

    def create_widgets(self):
        self.story_label = tk.Label(self.master, text="Storyline", font=("Helvetica", 16, "bold"), bg="lightblue")
        self.story_label.pack(pady=10)

        self.story_text = tk.Text(self.master, height=8, width=80, wrap=tk.WORD, font=("Helvetica", 12), bg="lightyellow")
        self.story_text.pack(pady=10)

        self.clue_button = tk.Button(self.master, text="Clue", command=self.show_clues, font=("Helvetica", 12), bg="lightgreen")
        self.clue_button.pack(pady=5)

        self.name_label = tk.Label(self.master, text="Your Guess - Name:", font=("Helvetica", 12), bg="lightblue")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        self.location_label = tk.Label(self.master, text="Your Guess - Location:", font=("Helvetica", 12), bg="lightblue")
        self.location_label.pack()

        self.location_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.location_entry.pack(pady=5)

        self.weapon_label = tk.Label(self.master, text="Your Guess - Weapon:", font=("Helvetica", 12), bg="lightblue")
        self.weapon_label.pack()

        self.weapon_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.weapon_entry.pack(pady=5)

        # Modify the 'Submit' button to use functools.partial
        self.submit_button = tk.Button(self.master, text="Submit", command=functools.partial(self.check_answer, True),
                                       font=("Helvetica", 12, "bold"), bg="orange", fg="white")
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.master, text=f"User Score: {self.user_score} | System Score: {self.system_score}",
                                    font=("Helvetica", 12, "italic"), bg="lightblue")
        self.score_label.pack(pady=10)

    def shuffle_characters(self):
    # Shuffle the characters, weapons, and locations once before each game
        random.shuffle(self.original_characters)
        random.shuffle(self.original_weapons)
        random.shuffle(self.original_locations)

    # Find the index of the killed character in the original list
        victim_index = self.original_characters.index(self.characters[0])

    # Move the killed character to a random position in the list
        random_position = random.randint(0, len(self.original_characters) - 1)
        self.original_characters.insert(random_position, self.original_characters.pop(victim_index))

    # Reset characters attribute to the shuffled list
        self.characters = self.original_characters.copy()
        self.weapons = self.original_weapons.copy()
        self.locations = self.original_locations.copy()


    def generate_storyline(self):
        self.story_text.delete(1.0, tk.END)
        self.shuffle_characters()
        self.generate_dynamic_storyline()  # Use the dynamic storyline generation
        self.clear_entry_fields()
        self.round_counter += 1

    # Randomly select the killed character from the list
        victim = random.choice(self.characters)
        self.characters.remove(victim)  # Remove the killed character from the list

    # Set the killer as the first character in the list
        killer = self.characters[0]
        weapon = self.weapons[0]

    # Shuffle weapons and locations
        random.shuffle(self.weapons)
        random.shuffle(self.locations)

        storyline = f"{victim} is killed at the {self.locations[0]} and a {self.weapons[0]} is found beside him. "
        storyline += f"\nThe characters at that place:\n"

    # Assign random actions and locations to other characters
        for char, act, weap, loc, dist in zip(self.characters, self.actions, self.weapons[1:], self.locations[1:], self.distance[1:]):
            storyline += f"- {char} is {act} and bringing {weap} {dist} meters from the murder location in {loc}.\n"

        self.story_text.insert(tk.END, storyline)

    # Set the correct answer after shuffling (move this line here)
        self.correct_answer = f"The Killer: {killer}\nThe location: {self.locations[0]}\nThe weapon: {weapon}\n"

    def clear_entry_fields(self):
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.weapon_entry.delete(0, tk.END)


# -------STORYLINE---------

    def show_clues(self):
        # Pass correct answers for each clue
        actor_clue = self.generate_clue(self.characters[0])
        location_clue = self.generate_clue(self.locations[self.current_storyline])
        weapon_clue = self.generate_clue(self.weapons[0])

        messagebox.showinfo("Clues", f"Clue for Actor:\n{actor_clue}\n\nClue for Location:\n{location_clue}\n\nClue for Weapon:\n{weapon_clue}")

    # start TTS
    def generate_clue(self, correct_answer):
        correct_answer = correct_answer.upper()

        grid_size = (10, 10)
        grid = [[' ' for _ in range(grid_size[1])] for _ in range(grid_size[0])]

        # Determine the starting position based on the length of the correct answer
        start_row = grid_size[0] // 2
        start_col = (grid_size[1] - len(correct_answer)) // 2

        # Embed the correct answer into the grid horizontally
        for i, char in enumerate(correct_answer):
            grid[start_row][start_col + i] = f'{char}'

        # Fill the remaining grid with random alphabets
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                if grid[row][col] == ' ':
                    grid[row][col] = f'{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}'

        clue_text = '\n'.join([' '.join(row) for row in grid])

        return clue_text


    def check_answer(self, is_submit):
        name_guess = self.name_entry.get().lower()
        location_guess = self.location_entry.get().lower()
        weapon_guess = self.weapon_entry.get().lower()

        # Check if any of the guess boxes is empty
        if not name_guess or not location_guess or not weapon_guess:
            messagebox.showinfo("Error", "Please fill in all guess boxes.")
            return

        if name_guess == self.characters[0].lower() and \
                location_guess == self.locations[self.current_storyline].lower() and \
                weapon_guess == self.weapons[0].lower():
            self.user_score += 1
            self.update_score_display()
            messagebox.showinfo("Correct", "Congratulations! You solved the mystery. You got 1 score!")

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
        self.score_label.config(text=f"Round: {self.round_counter} | User Score: {self.user_score} | System Score: {self.system_score}", font=("Helvetica", 12, "italic"))


    def end_game(self):
        if self.user_score >= 3:
            messagebox.showinfo("Game Over", "Congratulations! You are the winner with a score of 3.")
        else:
            messagebox.showinfo("Game Over", "Game over! It's a draw.")
        self.master.destroy()  # Close the application when the game is over

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

    def update_score_display(self):
        self.score_label.config(text=f"User Score: {self.user_score} | System Score: {self.system_score}",
                                font=("Helvetica", 12, "italic"))
def main():
    root = tk.Tk()
    game = KlooDoGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
