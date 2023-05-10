from sqlite3 import DateFromTicks
import arcade
import math
import random
from datetime import datetime
from Redactor import launch_redactor, Redactor
from Player import Player
from Scene import Scene, ProgressBar
from Settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, LIST_OF_SOUNDTRACKS



random.seed(datetime.now().timestamp())

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.gameState = None
        self.scene = Scene()
        self.player = Player()
        

    def setup(self):
        self.gameState = "Loading"

    def on_update(self, delta_time):
        if self.gameState == "Loading":
            self.load()
        elif self.gameState == "Playing":
            has_ended = self.player.update(delta_time)
            if has_ended:
                self.gameState = "Results"
                self.scene.change("Results")
            self.scene.update()
            if self.player.timer == None:
                self.scene.add_notes(self.player.get_avaible_notes())
            
    def on_draw(self):
        self.scene.draw()

    def load(self):
        self.scene.change("Loading")
        self.scene.draw()
        self.player.load_soundtracks()
        self.scene.change("MainMenu")
        self.player.play("MainTheme")
        self.gameState = "MainMenu"

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.gameState == "MainMenu":
            if (x >= 250 and x <= 650) and (y >= 260 and y <= 340):
                self.gameState = "SelectLevel 0"
                self.scene.change("SelectLevel", 0)
                sound = arcade.Sound("assets/tecnical_sounds/ButtonClick.wav")
                sound.play()
            elif (x >= SCREEN_WIDTH / 2 - 150 and x <= SCREEN_WIDTH / 2 + 150) and (y >= SCREEN_HEIGHT / 2 - 190 and y <= SCREEN_HEIGHT / 2 + 190):
                self.gameState = "Redactor"
                self.player.stop()
                redactor = Redactor(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
                #arcade.set_window(redactor)
                #launch_redactor()
                
        elif self.gameState.startswith("SelectLevel"):
            number = None
            temp = self.gameState.split()
            page_id = int(temp[1])
            if (x >= 350 and x <= 450) and (y >= 530 and y <= 595) and page_id > 0:
                self.scene.change("SelectLevel", page_id - 1)
                self.gameState = "SelectLevel " + str(page_id - 1)
            if (x >= 350 and x <= 450) and (y >= 5 and y <= 80) and page_id * 4 < len(LIST_OF_SOUNDTRACKS):
                self.scene.change("SelectLevel", page_id + 1)
                self.gameState = "SelectLevel " + str(page_id + 1)
            for i in range(4):
                if (x >= 50 and x <= 750) and (y >= SCREEN_HEIGHT - 63 - (i + 1) * 100 - i * 20 and y <= SCREEN_HEIGHT + 63 - (i + 1) * 100 - i * 25):
                    number = i
                    break
            if number != None:
                number += page_id * 4
                self.startGame(LIST_OF_SOUNDTRACKS[number])

                
    def startGame(self,name):
        sound = arcade.Sound("assets/tecnical_sounds/ButtonClick.wav")
        sound.play()
        self.player.load_to_game(name, 3)
        self.scene.change(self.player.name)
        self.scene.progressBar = ProgressBar(self.player.len)
        self.gameState = "Playing"


    def on_key_press(self, key: int, modifiers: int):
        if self.gameState == "Playing":
            if key == arcade.key.Z:
                self.scene.circle_press(0)
            elif key == arcade.key.X:
                self.scene.circle_press(1)
            elif key == arcade.key.C:
                self.scene.circle_press(2)
            elif key == arcade.key.B:
                self.scene.circle_press(3)
            elif key == arcade.key.N:
                self.scene.circle_press(4)
            elif key == arcade.key.M:
                self.scene.circle_press(5)
            elif key == arcade.key.ESCAPE:
                self.scene.change("MainMenu")
                self.player.play("MainTheme")
                self.gameState = "MainMenu"
        elif self.gameState.startswith("SelectLevel"):
            if key == arcade.key.ESCAPE:
                self.scene.change("MainMenu")
                self.gameState = "MainMenu"
        elif self.gameState == "MainMenu":
            if key == arcade.key.ESCAPE:
                quit()
        elif self.gameState == "Results":
            if key == arcade.key.ESCAPE:
                self.gameState = "MainMenu"
                self.scene.change("MainMenu")
                self.player.play("MainTheme")

        return super().on_key_press(key, modifiers)

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.Z:
            self.scene.circle_release(0)
        elif key == arcade.key.X:
            self.scene.circle_release(1)
        elif key == arcade.key.C:
            self.scene.circle_release(2)
        elif key == arcade.key.B:
            self.scene.circle_release(3)
        elif key == arcade.key.N:
            self.scene.circle_release(4)
        elif key == arcade.key.M:
            self.scene.circle_release(5)
        return super().on_key_release(key, modifiers)

    


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
       
