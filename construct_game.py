from scrape_bee.scrape_bee import scrape_bee
from datetime import datetime
import json
from gpiozero import Button
from signal import pause
from start_screen import GC9A01
from image_tools import to_rgb565, prepare
from PIL import Image, ImageDraw, ImageFont
import math


scrape_bee('https://www.nytimes.com/puzzles/spelling-bee')
game_data_file_name = datetime.today().strftime('%Y-%m-%d') + '.json'
with open('data/'+game_data_file_name) as game_data:
    data = json.load(game_data)
    centerLetter = data['today']['centerLetter']
    outerLetters = data['today']['outerLetters']
    answers = data['today']['answers']
    pangrams = data['today']['pangrams']

class GameState:
    def __init__(self):
        self.word = ""
        self.score = 0
        self.guessed_words = []

    def add_letter(self, letter):
        self.word += letter
        print(self.word)

    def clear(self):
        self.word = ""
        print('Cleared current selection')

    def guess(self):
        if self.word in answers and self.word not in self.guessed_words:
            self.guessed_words.append(self.word)
            if len(self.word) == 4:
                points = 1
            elif self.word not in pangrams:
                points = len(self.word)
            elif self.word in pangrams:
                points = len(self.word) + 7
            self.score += points
            print("Correct. Your score is now", self.score)
        else:
            print("Not a valid word",self.word)
        self.clear()


state = GameState()
tft = GC9A01()

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



def hex_at(d, cx, cy, r, fill, outline="black"):
    pts = [(cx + r * math.cos(math.radians(60 * i - 90)),
            cy + r * math.sin(math.radians(60 * i - 90))) for i in range(6)]
    d.polygon(pts, fill=fill, outline=outline)

img = Image.new("RGB", (240, 240), "black")
d = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)

hex_at(d, 120, 120, 34, "#f7da21")                    # centre letter
d.text((120, 120), centerLetter.upper(), font=font, fill="black", anchor="mm")

for i, letter in enumerate(outerLetters):
    a = math.radians(60 * i)
    x, y = 120 + 62 * math.cos(a), 120 + 62 * math.sin(a)
    hex_at(d, x, y, 34, "#e6e6e6")
    d.text((x, y), letter.upper(), font=font, fill="black", anchor="mm")

tft.blit(to_rgb565(img))

try:
    pause()
except KeyboardInterrupt:
    pass
finally:
    tft.close()


