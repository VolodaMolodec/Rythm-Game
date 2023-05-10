import arcade
from Settings import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH

class Redactor(arcade.Window):
    def __init__(self):
        self.text = "Hello"
        self.sprite = arcade.Sprite("assets/sprites/WhiteTemplate.png")
    def setup(self):
        print(self.text)

    def on_draw(self):
        self.sprite.draw()

    def on_update(self):
        print(self.text)

def launch_redactor():
   # redactor = Redactor(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    print('aaa')
    #redactor.setup()
    #arcade.set_window(redactor)