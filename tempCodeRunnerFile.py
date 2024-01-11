     self.story_text.delete(1.0, tk.END)

        # Use the characters list without shuffling
        victim = self.characters[0]

        # Ensure that the killer is not the same as the victim
        potential_killers = [char for char in self.characters if char != victim]
        killer = random.choice(potential_killers)

        # Swap the victim and killer in the characters list
        victim_index = self.characters.index(victim)
        killer_index = self.characters.index(killer)
        self.characters[victim_index], self.characters[killer_index] = self.characters[killer_index], self.characters[victim_index]

        # Select a random location and weapon
        location = random.choice(self.locations)
        weapon = random.choice(self.weapons)

        storyline = f"{victim} is killed at the {location} and a {weapon} is found beside him. "
        storyline += f"\nThe characters at that place:\n"

        # Initialize variables for current weapon, location, and distance
        current_weapon = self.weapons[1:]
        current_location = self.locations[1:]
        current_distance = self.distance[1:]

        # Create a list of characters excluding the victim
        characters_at_scene = [char for char in self.characters if char != victim]

        for char, act, weap, loc, dist in zip(characters_at_scene, self.actions, current_weapon, current_location, current_distance):
            storyline += f"- {char} is {act} and bringing {weap} {dist} meters from the murder location in {loc}.\n"

        self.story_text.insert(tk.END, storyline)

        self.correct_answer = f"The Killer: {killer}\nThe location: {location}\nThe weapon: {weapon}\n"

        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.weapon_entry.delete(0, tk.END)
        self.current_storyline += 1
