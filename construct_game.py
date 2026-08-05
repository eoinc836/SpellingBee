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


class GameState:
    def __init__(self):
        self.word = ""

    def add_letter(self, letter):
        self.word += letter
        print(self.word)

    def clear(self):
        self.word = ""

state = GameState()

centerLetter_button = Button(27)
outer_letter_1 = Button(22)

centerLetter_button.when_pressed = lambda: state.add_letter(centerLetter)
outer_letter_1.when_pressed = lambda: state.add_letter(outerLetters[0])

pause()


