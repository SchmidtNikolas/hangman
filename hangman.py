import requests, string, time
from bs4 import BeautifulSoup


def print_status(word, lives, guessed, correct):
    """prints out current game state"""

    # start a new line
    print_state = "\n"

    # print out each character if guessed or blank
    for i in word:
        print_state += " _ " if i not in correct else i.upper()

    # print remaining lives and uppercase characters of guessed words
    print_state += "\nLives remaining: {}".format(lives)
    if len(guessed) != 0:
        upper_guess = "".join(sorted(list(guessed))).upper()
        upper_guess = " ".join(list(upper_guess))
        print_state += "\nLetters guessed: {}".format(upper_guess)

    # print our state plus some extra spaces
    print(print_state, "\n\n")

def handle_guess(guess, word, lives, guessed, correct):

    # pause for the user
    time.sleep(.2)

    # non-alpha guesses
    if guess not in string.ascii_lowercase:
        print("Please enter a letter, not that thing.")
        return False, lives

    # repeated guesses
    if guess in guessed:
        print("You already guessed that one. Try something else.")
        return False, lives

    # miss
    if guess not in word:
        lives -= 1
        guessed.add(guess)
        print("Strike! {} is not in this word!".format(guess.upper()))

    # hit
    if guess in word:
        guessed.add(guess)
        correct.add(guess)
        print("Good one! There are {} of the letter {} in the word.".format(word.count(guess), guess.upper()))

    # if we've won, break
    if set(word) == correct:
        return True, lives

    # catch-all
    return False, lives


def do_game(lives=6):

    # set up some initial values
    victory = False
    guessed = set()
    correct = set()

    # loop while we're still alive
    while lives > 0:
        # print the current game status
        print_status(word, lives, guessed, correct)

        # get the user's guess by ripping the first character off the string
        guess = input("Please guess a letter: ")[:1].lower()

        # turn empty string into a string we can work with:
        if guess == "":
            guess = " "

        # handle that guess appropriaely and return some values
        victory, lives = handle_guess(guess, word, lives, guessed, correct)

        # break the loop if we win
        if victory:
            lives = 0

    #print out game status and the word
    print("YOU {}".format("WIN" if victory else "LOSE"))
    print("{}: {}".format("The word was" if not victory else "You got the word" ,word))


def pick_word():
    # get a random word
    r = requests.get("https://wordunscrambler.me/random-word-generator")
    soup = BeautifulSoup(r.text, features='lxml')

    # clean the request to get just the word
    word = soup.find('div', {'id': 'random-word-wrapper'}).findChildren('a')[0].text.strip()

    return word.lower()

if __name__ == "__main__":
    word = pick_word()
    do_game()
