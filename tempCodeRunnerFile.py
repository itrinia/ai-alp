     # Clear the existing storyline
        self.story_text.delete(1.0, tk.END)

        # Reset the characters, locations, and weapons lists to their original state
        self.characters = self.original_characters.copy()
        self.weapons = self.original_weapons.copy()
        self.locations = self.original_locations.copy()

        # Randomly select the killed character from the list
        victim = random.choice(self.characters)
        self.characters.remove(victim)  # Remove the killed character from the list

        # Randomly select the killer from the remaining characters
        remaining_characters = [char for char in self.characters if char != victim]
        random.shuffle(remaining_characters)

        killer = remaining_characters[0]
        weapon = self.weapons[0]

        # Shuffle weapons and locations
        random.shuffle(self.weapons)
        random.shuffle(self.locations)

        # Set the correct answer after shuffling
        self.correct_answer = f"The Killer: {killer}\n The weapon: {self.weapons[0]}\n The location: {self.locations[self.current_storyline]}"

        storyline = f"{victim} is killed at the {self.locations[1]} and a {self.weapons[1]} is found beside him. "
        storyline += f"\nThe characters at that place:\n"

        # Assign random actions and locations to other characters
        for char, act, weap, loc, dist in zip(self.characters, self.actions, self.weapons[1:], self.locations[1:], self.distance[1:]):
            storyline += f"- {char} is {act} and bringing {weap} {dist} meters from the murder location in {loc}.\n"

        self.story_text.insert(tk.END, storyline)
