# Hangman
An implementation of the popular hangman game in **Python** with cross-platform support for Windows and UNIX.

Cross-compatible with Python 2.x and Python 3.x.

## Usage
### Load from a file.
    from hangman import Hangman
    
    hangman = Hangman()
    hangman.load_words_from_file('./words')
    hangman.update_loop()
### Load from an array.
    from hangman import Hangman
    
    hangman = Hangman()
    hangman.load_words_from_array(['python', 'hangman', 'word'])
    hangman.update_loop()