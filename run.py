from os import name
from sys import stdout
from random import randint
from collections import OrderedDict

# todo: add forward compatibility for python 3.
# todo: move to a separate module
# todo: load add a method to load words from a file.
# todo: add a method to load from a list.
# todo: update the readme to reflect those changes.


class Hangman(object):
    def __init__(self):
        self._words = ['hello']
        self._guessed_letters = {'correct': [], 'incorrect': []}
        self._platform_to_implementation = {
            'nt': self._get_character_windows,
            'posix': self._get_character_unix
        }

        self._difficulty_to_settings = OrderedDict()
        self._difficulty_to_settings['Easy'] = {'percentage': 50, 'no_of_turns': 10}
        self._difficulty_to_settings['Hard'] = {'percentage': 10, 'no_of_turns': 5}

    def _supports_current_os(self):
        if name not in self._platform_to_implementation:
            print 'Sorry, this operating system is not supported!'
            return False

        return True

    def _select_difficulty(self):
        # Get the dictionary as items.
        items = self._difficulty_to_settings.items()

        # Iterate over the items and output them as options.
        for i in xrange(len(items)):
            print '[{}]: {}'.format(i + 1, items[i][0])

        # Keep asking for the desired difficulty until a valid answer is given.
        while True:
            # Get user input.
            stdout.write('Select the desired difficulty by entering corresponding number: ')
            difficulty = self._get_character()
            stdout.write(difficulty + '\r\n')

            # Retry if the input if it is not a number
            if not difficulty.isdigit():
                continue

            # Subtract from the difficulty as lists begin from zero.
            difficulty = int(difficulty) - 1

            # Check the desired difficulty is within the range of the items.
            if 0 <= difficulty < len(items):
                # Set the difficulty and the number of available turns
                self._difficulty = items[difficulty][0]
                self._no_of_turns = items[difficulty][1]['no_of_turns']
                # Output the difficulty chosen.
                print 'You have chosen {} mode, you have {} attempts to guess the word.\n'.format(self._difficulty.lower(), self._no_of_turns)
                # Break out of the loop.
                break

    def _select_random_word(self):
        # Get a random word from the list of words.
        word = self._words[randint(0, len(self._words) - 1)]

        # Get the percentage of letters to display using the difficulty.
        percentage_of_letters_to_display = self._difficulty_to_settings[self._difficulty]['percentage']
        # Get the number of letters to display using the percentage.
        no_letters_to_display = int(len(word) * (percentage_of_letters_to_display / 100.0))

        for i in xrange(no_letters_to_display):
            # Keep trying to get a letter than hasn't been already added.
            while True:
                # Select a random valid letter from the word.
                letter = word[randint(0, len(word) - 1)]
                # If the letter appears more than once in the word, select a different letter.
                if word.count(letter) > 1:
                    continue
                # If the word has not been added to guessed letters, break.
                if letter not in self._guessed_letters['correct']:
                    break
            # Add the letter to the correct letters.
            self._guessed_letters['correct'].append(letter)

        return word

    def _output_partial_word(self, word):
        partial_word = ''

        for letter in word:
            partial_word += letter if letter in self._guessed_letters['correct'] else '_'

        print partial_word

    def _output_incorrect_guesses(self):
        print 'Misses: ' + ', '.join(self._guessed_letters['incorrect'])

    def _check_user_input(self, word, letter):
        # Get the target list by determining if the letter is in the word or not.
        target = self._guessed_letters['correct'] if letter in word else self._guessed_letters['incorrect']

        # If the letter is already within the target list the user input is invalid.
        if letter in target:
            return False

        # If the letter is not within the word, reduce the number of turns.
        if letter not in word:
            self._no_of_turns -= 1

        # Otherwise, add the letter to the target list.
        target.append(letter)
        return True

    def _is_word_completed(self, word):
        # Iterate through each letter in the word.
        for letter in word:
            # If the letter has not been guessed, the word is not completed.
            if letter not in self._guessed_letters['correct']:
                return False

        # Otherwise, it has been completely guessed!
        return True

    def _get_character(self):
        return self._platform_to_implementation[name]()

    @staticmethod
    def _get_character_windows():
        from msvcrt import getch
        return getch()

    @staticmethod
    def _get_character_unix():
        from sys import stdin
        from tty import setraw
        import termios

        # Get the file descriptor for standard input.
        fd = stdin.fileno()
        # Store the current settings of the terminal for standard input.
        old_settings = termios.tcgetattr(fd)
        try:
            # Set the file descriptor to raw which prevents it from being buffered.
            setraw(fd)
            # Read a single character.
            ch = stdin.read(1)
        finally:
            # Set the terminal settings back to the original settings.
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

    def update_loop(self):
        # If this operating system is not supported, return.
        if not self._supports_current_os():
            return

        self._select_difficulty()

        # Select a random word.
        word = self._select_random_word()

        while True:
            # Output the word partially.
            self._output_partial_word(word)
            # Output the incorrect guesses.
            self._output_incorrect_guesses()

            # Check if the word is completed.
            if self._is_word_completed(word):
                print 'You win!'
                print 'Waiting for input before closing...'
                self._get_character()
                break

            # Check if there no turns left.
            if self._no_of_turns == 0:
                print 'You lose!'
                print 'Waiting for input before closing...'
                self._get_character()
                break

            print 'You have {} turns left to guess the word.'.format(self._no_of_turns)

            # Keeping to try to get a character until it is valid.
            while True:
                character = self._get_character()
                if self._check_user_input(word, character):
                    break


hangman = Hangman()
hangman.update_loop()
