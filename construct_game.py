from scrape_bee.scrape_bee import scrape_bee
from datetime import datetime
import json
from gpiozero import Button
from signal import pause

scrape_bee('https://www.nytimes.com/puzzles/spelling-bee')
game_data_file_name = datetime.today().strftime('%Y-%m-%d') + '.json'
with open('data/'+game_data_file_name) as game_data:
    data = json.load(game_data)
    centerLetter = data['today']['centerLetter']
    outerLetters = data['today']['outerLetters']
    answers = data['today']['answers']
    pangrams = data['today']['pangram']

class GameState:
    def __init__(self):
        self.word = ""
        self.score = 0
    def add_letter(self, letter):
        self.word += letter
        print(self.word)

    def clear(self):
        self.word = ""

    def guess(self):
        if self.word in answers:
            if len(self.word) == 4:
                points = 1
            elif self.word not in pangrams:
                points = len(self.word) - 3
            self.score += points
            print("Correct. Your score is now", self.score)
        else:
            print("Not a valid word",self.word)


state = GameState()

centerLetter_button = Button(27)
outer_letter_1 = Button(22)
outer_letter_2 = Button(23)
outer_letter_3 = Button(24)
outer_letter_4 = Button(21)
outer_letter_5 = Button(20)
outer_letter_6 = Button(25)
clear_button = Button(16)
enter_button = Button(12)

centerLetter_button.when_pressed = lambda: state.add_letter(centerLetter)
outer_letter_1.when_pressed = lambda: state.add_letter(outerLetters[0])
outer_letter_2.when_pressed = lambda: state.add_letter(outerLetters[1])
outer_letter_3.when_pressed = lambda: state.add_letter(outerLetters[2])
outer_letter_4.when_pressed = lambda: state.add_letter(outerLetters[3])
outer_letter_5.when_pressed = lambda: state.add_letter(outerLetters[4])
outer_letter_6.when_pressed = lambda: state.add_letter(outerLetters[5])
clear_button.when_pressed = lambda: state.clear()
enter_button.when_pressed = lambda: state.guess()

pause()


