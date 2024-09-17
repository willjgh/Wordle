'''Module to play wordle in the terminal.'''

import random

# load lists of words that are allowed as guesses and as answers
with open('./Data/allowed_guesses.txt', 'r') as file:
    allowed_guesses = file.read().splitlines()
with open('./Data/answers.txt', 'r') as file:
    answers = file.read().splitlines()

def wordle():
    '''Run a game of wordle.'''

    # choose answer
    answer = random.choice(answers)

    # state of the alphabet
    # 0: not yet used (grey)
    # 1: not in answer (black)
    # 2: in answer (yellow)
    # 3: exactly matched (green)
    alphabet = {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}

    # loop while playing
    playing = True
    while playing:

        # prompt for input until valid guess
        guessing = True
        while guessing:

            # input
            guess = input(f"Guess a 5 letter word: ")

            # check valid
            if (guess in allowed_guesses) or (guess in answers):
                guessing = False
            else:
                print("Invalid guess \n")

        # compare guess and answer character by character
        guess_chars = [char for char in guess]
        answer_chars = [char for char in answer]

        # result to print
        output_text = ""

        # count of correct characters
        correct_count = 0
        
        # examine character by character
        for i in range(5):

            # exact match: green
            if guess_chars[i] == answer_chars[i]:
                output_text += "\x1b[5;30;42m" + guess_chars[i] + "\x1b[0m "
                correct_count += 1

                # replace match in answer to prevent multiple greens and yellows
                # for the same character present in an answer
                # e.g. guess "aa___" should only be given 1 green for an answer
                # of "a____"
                j = answer_chars.index(guess_chars[i])
                answer_chars[j] = None

                # update letter to green if not already green
                if alphabet[guess_chars[i]] < 3:
                    alphabet[guess_chars[i]] = 3

            # in answer: yellow
            elif guess_chars[i] in answer_chars:

                # unless already an exact match elsewhere
                j = answer_chars.index(guess_chars[i])
                if guess_chars[j] == answer_chars[j]:
                    output_text += "\x1b[6;30;40m" + guess_chars[i] + "\x1b[0m "
                    continue

                # otherwise yellow
                output_text += "\x1b[6;30;43m" + guess_chars[i] + "\x1b[0m "

                # replace match in answer
                answer_chars[j] = None

                # update letter to yellow if not already yellow or green
                if alphabet[guess_chars[i]] < 2:
                    alphabet[guess_chars[i]] = 2

            # not in answer: black
            else:
                output_text += "\x1b[6;30;40m" + guess_chars[i] + "\x1b[0m "

                # update letter to grey if hasn't been used before
                if alphabet[guess_chars[i]] < 1:
                    alphabet[guess_chars[i]] = 1

        # print output
        print(output_text + "\n")

        # correct guess: end game
        if correct_count == 5:
            print("You win!")
            playing = False

        # print alphabet: letters coloured by information
        else:

            alphabet_output = ""
            for letter, colour in alphabet.items():
                if colour == 0:
                    alphabet_output += letter + " "
                elif colour == 1:
                    alphabet_output += "\x1b[6;30;40m" + letter + "\x1b[0m "
                elif colour == 2:
                    alphabet_output += "\x1b[6;30;43m" + letter + "\x1b[0m "
                else:
                    alphabet_output += "\x1b[5;30;42m" + letter + "\x1b[0m "

            print(alphabet_output + "\n")


if __name__ == "__main__":
    wordle()