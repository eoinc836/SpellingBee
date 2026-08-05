from scrape_bee.scrape_bee import scrape_bee
from datetime import datetime
import json
from gpiozero import Button
from signal import pause

scrape_bee('https://www.nytimes.com/puzzles/spelling-bee')
game_data_file_name = datetime.today().strftime('%Y-%m-%d') + '.json'
global word
with open('data/'+game_data_file_name) as game_data:
    data = json.load(game_data)
    centerLetter = data['today']['centerLetter']
    outerLetters = data['today']['outerLetters']


def addLetterToWord(letter):
    word += letter
    print(word)

centerLetter_button = Button(27)
outer_letter_1 = Button(22)

centerLetter_button.when_pressed = lambda: addLetterToWord(centerLetter)
outer_letter_1.when_pressed = lambda: addLetterToWord(outerLetters[0])

pause()


