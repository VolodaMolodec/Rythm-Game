import arcade
import math
#import Settings

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rythm game"

MUSIC_VOLUME = 1

LIST_OF_SOUNDTRACKS = [
    "Demo"
    ]

CIRCLES_HEIGHT = 110
DOWN_BORDER = CIRCLES_HEIGHT - 120

NOTES_SPEED = 10

LINES_X = [125,235,345,455,565,675]

RENDER_UPDATE = 0.017

PROGRESS_BARS_UPDATE = 50


class ProgressBar:
    def __init__(self, time):
        self.cons = 100
        self.widthIncreaseIteration = int(time / RENDER_UPDATE / self.cons  / 2)
        self.iterations = 0
        self.sprite = arcade.Sprite("assets/sprites/ProgressBarElement.png")
        self.sprite.width = 0.1
        self.sprite.center_x = 0
        self.sprite.center_y = 0
        self.scale = SCREEN_WIDTH / self.cons
     
    def update(self):
        self.iterations += 1
        self.sprite.width = (self.iterations // self.widthIncreaseIteration + 0.1) * self.scale
        #print(self.sprite.height)
        


class TempSprite:
    def __init__(self, name, pos_x, pos_y, time):
        self.sprite = arcade.Sprite("assets/sprites/" + name + ".png")
        self.sprite.center_x = pos_x
        self.sprite.center_y = pos_y
        self.time = time


    def update(self, delta_time):
        self.time -= delta_time
        if(self.time <= 0.0):
            return 1
        else:
            return 0




class Soundtrack:
    def __init__(self,name):
        self.name = name

        self.Background = arcade.Sprite("assets/music/" + name + "/Background.png")
        self.Background.center_x = 400
        self.Background.center_y = 300

        self.Music = arcade.load_sound("assets/music/" + name + "/Music.mp3")

        self.time = self.Music.get_length()
        
        self.playingTime = 0

        self.notes = []

        self.musicState = "None"


    def update(self, time):
        self.playingTime += time
        if self.musicState == "inGame":
            returningNotes = []
            while True:
               if len(self.notes) != 0:
                   temp = self.notes[0].get_if_ready(self.playingTime)
                   if temp != 0:
                       returningNotes.append(temp)
                       self.notes.pop(0)
                   else:
                       return returningNotes
               else:
                   return returningNotes


    def load_to_game(self):
        self.notes.clear()
        with open('assets/music/' + self.name + '/Notes.txt') as f:
            cons_time = RENDER_UPDATE * (SCREEN_HEIGHT - CIRCLES_HEIGHT) / NOTES_SPEED #Time then note reach center of circle
            while True:                
                temp = f.readline()
                temp = temp.split()
                if len(temp) != 3:
                    return
                
                time = float(temp[0]) - cons_time
                typ = temp[1]
                line = int(temp[2])
                if time == '' or typ == '' or line == '':
                    break
                temp = Note(time,typ,line)
                self.notes.append(temp)
                    



class Note:
    def __init__(self, time, typ, line):
        self.time = time
        self.type = typ
        self.line = line


    def get_if_ready(self, time):
        if self.time <= time:
            sprite = arcade.Sprite("assets/sprites/" + self.type + ".png")
            return [self.line, self.type, sprite]
        else:
            return 0



        

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.loadedSprites = None
        self.tempSprites = []
        self.currentSoundtrack = None
        self.player = None
        self.gameState = "Loading"
        self.soundtracks = None

        self.timer = False
        self.timerCount = 0

        self.tempSprite = None

        self.linesNotes = []
        for i in range(6):
            self.linesNotes.append(arcade.SpriteList())

        self.score = None
        self.combo = None

        self.progressBar = None


    def loadGameTitle(self):
        if self.currentSoundtrack != None:
            self.player.volume *= 0.6
        if len(self.tempSprites) != 0:
            self.tempSprites.clear()
        self.gameState = "MainTitle"
        self.loadedSprites = arcade.SpriteList()
        Background = arcade.Sprite("assets/sprites/TitleScreen.png")
        Background.center_x = 400
        Background.center_y = 300
        self.loadedSprites.append(Background)

        title = arcade.Sprite("assets/sprites/TitleName.png")
        title.center_x = 400
        title.center_y = 500
        self.loadedSprites.append(title)

        demoButton = arcade.Sprite("assets/sprites/DemoButton.png")
        demoButton.center_x = 400
        demoButton.center_y = 300
        self.loadedSprites.append(demoButton)


    def playSoundtrack(self, name):
        self.gameState = "Playing"
        self.score = 0
        self.combo = 0
        self.timer = True
        self.timerCount = 2

        for sound in self.soundtracks:
            if sound.name == name:
                self.currentSoundtrack = sound
                break
        self.currentSoundtrack.playingTime = 0
        self.currentSoundtrack.load_to_game()
        self.progressBar = ProgressBar(self.currentSoundtrack.time)

        self.loadedSprites.clear()
        self.loadedSprites.append(self.currentSoundtrack.Background)

        circles = arcade.Sprite("assets/sprites/Circles.png")
        circles.center_x = 400
        circles.center_y = 110
        self.loadedSprites.append(circles)

        

    def loadSoundtracks(self):
        self.soundtracks = []
        for name in LIST_OF_SOUNDTRACKS:
            self.soundtracks.append(Soundtrack(name))

    

    def setup(self):
        self.gameState = "Loading"
        pass


    def on_draw(self):
        arcade.start_render()

        self.loadedSprites.draw()
        if self.gameState == "Playing":
            for i in self.tempSprites:
                i.sprite.draw()
            for line in self.linesNotes:
                if len(line) != 0:
                 line.draw()
            arcade.draw_text("Score: " + str(self.score),SCREEN_WIDTH / 16, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)
            if self.combo >= 3:
                 arcade.draw_text("Combo: " + str(self.combo),SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)

            if self.progressBar != None:
                self.progressBar.sprite.draw()
             
        arcade.finish_render()


    def on_update(self, delta_time):
        if self.timer == True:
            self.timerCount -= delta_time
            if(self.timerCount <= 0):
                self.timer = False
                self.player = arcade.play_sound(self.currentSoundtrack.Music,MUSIC_VOLUME)
                self.currentSoundtrack.musicState = "inGame"

        elif self.gameState == "Playing":
            notes = self.currentSoundtrack.update(delta_time)
            i = 0
            while i < len(self.tempSprites):
                result = self.tempSprites[i].update(delta_time)
                if result == 1:
                    self.tempSprites[i].sprite.remove_from_sprite_lists()
                    self.tempSprites.pop(i)
                    i -= 1
                i+=1
            for i in self.linesNotes:
                j = 0
                while j < len(i):
                    i[j].center_y -= NOTES_SPEED
                    if i[j].center_y <= DOWN_BORDER:
                        self.getScore("Bad")
                        i.pop(j)
                    j+=1
            if len(notes) != 0:
                i = 0
                while i < len(notes):
                    sprite = notes[i][2]
                    sprite.center_x = LINES_X[notes[i][0] - 1]
                    sprite.center_y = SCREEN_HEIGHT
                    self.linesNotes[notes[i][0] - 1].append(sprite)
                        
                    i += 1
            self.progressBar.update()
            

                

        elif self.gameState == "Loading":
            self.loadGameTitle()
            self.loadSoundtracks()
            self.currentSoundtrack = arcade.load_sound("assets/MainTheme.mp3")
            self.player = arcade.play_sound(self.currentSoundtrack, MUSIC_VOLUME * 0.6)
            self.gameState = "MainTitle"
            self.tempSprites = []

        pass


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.gameState == "MainTitle":
            if (x >= 250 and x <= 650) and (y >= 260 and y <= 340):
                sound = arcade.Sound("assets/tecnical_sounds/ButtonClick.wav")
                sound.play(MUSIC_VOLUME)
                if self.currentSoundtrack != None:
                    self.player.pause()
                self.playSoundtrack("Demo")
        return super().on_mouse_press(x, y, button, modifiers)
              

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            if self.gameState == "Playing":
                if self.timer != False:
                    self.timer = False
                    self.timerCount = 0
                self.currentSoundtrack.musicStatus = "None"
                for i in self.linesNotes:
                    i.clear()
                self.loadGameTitle()
            else:
                quit()
        elif key == arcade.key.Z:
            self.circle_press(0)
        elif key == arcade.key.X:
            self.circle_press(1)
        elif key == arcade.key.C:
            self.circle_press(2)
        elif key == arcade.key.B:
            self.circle_press(3)
        elif key == arcade.key.N:
            self.circle_press(4)
        elif key == arcade.key.M:
            self.circle_press(5)

        return super().on_key_press(key, modifiers)
    

    def circle_press(self, id):
        if len(self.linesNotes[id]) != 0:
                delta = math.fabs(self.linesNotes[id][0].center_y - CIRCLES_HEIGHT)
                if delta <= 100:
                    if delta <= 25:
                        self.getScore("Ideal")
                    elif delta <= 75:
                        self.getScore("Good")
                    else:
                        self.getScore("Bad")
                        
                    self.linesNotes[id].pop(0)
                elif delta <= 200:
                    self.getScore("Bad")


    def getScore(self, _type):
        modif = 1
        if self.score >= 60:
            modif = 2
        if _type == "Ideal":
            self.tempSprites.append(TempSprite("Ideal",100,500, 2))
            self.score += 10 * modif
            self.combo += 1
        elif _type == "Good":
            self.tempSprites.append(TempSprite("Good",100,500, 2))
            self.score += 5 * modif
            self.combo += 1
        else:
            self.tempSprites.append(TempSprite("Bad",100,500, 2))
            self.combo = 0
            
    

def main():
    game = Game(SCREEN_WIDTH,SCREEN_HEIGHT,"Rythm Game")

    arcade.start_render()
    load = arcade.Sprite("assets/sprites/Loading.png")
    load.center_x = SCREEN_WIDTH / 2
    load.center_y = SCREEN_HEIGHT / 2
    load.draw()

    
    game.setup()
    
    del load
    arcade.finish_render()
    arcade.run()
    
    

if __name__ == "__main__":
    main()

