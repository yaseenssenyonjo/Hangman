from hangman import Hangman

hangman = Hangman()
hangman.load_words_from_file('./words')
hangman.update_loop()
