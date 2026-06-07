import random

def main():
    # 1. Predefined dictionary of 5 words with their clues
    WORD_BANK = {
        "python": "A popular programming language named after a snake.",
        "coding": "The act of writing instructions for a computer.",
        "program": "A set of instructions that a computer executes.",
        "laptop": "A portable computer that fits on your lap.",
        "keyboard": "The device you use to type letters and numbers."
    }
    
    # Select a random word and pull its clue
    secret_word = random.choice(list(WORD_BANK.keys()))
    clue = WORD_BANK[secret_word]
    
    # Track game states
    guessed_letters = set()
    incorrect_guesses_left = 6
    
    # --- ATTRACTIVE WELCOME SCREEN ---
    print("\n" + "═" * 50)
    print(" 🎮  WELCOME TO THE ULTIMATE HANGMAN CHALLENGE  🎮 ")
    print("═" * 50)
    print(f" 💡  CLUE: {clue}")
    print("═" * 50 + "\n")
    
    # 3. Main Game Loop
    while incorrect_guesses_left > 0:
        # Build the hidden word display (e.g., p _ t h _ n)
        displayed_word = []
        for letter in secret_word:
            if letter in guessed_letters:
                displayed_word.append(letter.upper())  # Uppercase makes it stand out
            else:
                displayed_word.append("_")
        
        # --- ATTRACTIVE STATUS DASHBOARD ---
        print("┌────────────────────────────────────────────────┐")
        print(f"  📝  WORD TO GUESS:  {' '.join(displayed_word)}")
        print(f"  ❤️   LIVES REMAINING: {'❤️ ' * incorrect_guesses_left}{'🖤 ' * (6 - incorrect_guesses_left)}")
        
        # Show guessed letters nicely
        if guessed_letters:
            sorted_guesses = ", ".join(sorted(guessed_letters)).upper()
            print(f"  🧠  GUESSED SO FAR:  [ {sorted_guesses} ]")
        else:
            print("  🧠  GUESSED SO FAR:  [ None ]")
        print("└────────────────────────────────────────────────┘")
        
        # Check Win Condition
        if "_" not in displayed_word:
            print("\n" + "✨" * 25)
            print(f" 🎉 CONGRATULATIONS! You guessed it: '{secret_word.upper()}'!")
            print("✨" * 25 + "\n")
            break
            
        # 3. Basic console input
        guess = input(" 👉 Guess a letter: ").lower().strip()
        
        # Input Validation (if-else logic)
        if len(guess) != 1 or not guess.isalpha():
            print("\n❌ Invalid entry! Please type a single alphabetical letter.\n")
            continue
            
        if guess in guessed_letters:
            print(f"\n⚠️  You've already tried '{guess.upper()}'. Pick another one!\n")
            continue
            
        # Add the valid guess
        guessed_letters.add(guess)
        
        # Check if the letter is correct
        if guess in secret_word:
            print(f"\n✅ Nice shot! '{guess.upper()}' is in the word.\n")
        else:
            print(f"\n💥 Ouch! '{guess.upper()}' is not in the word.\n")
            incorrect_guesses_left -= 1

    # Check Loss Condition
    if incorrect_guesses_left == 0:
        print("\n" + "❌" * 25)
        print(" 💀 GAME OVER! You ran out of lives. 💀")
        print(f" The secret word was: '{secret_word.upper()}'")
        print("" + "❌" * 25 + "\n")

if __name__ == "__main__":
    main()