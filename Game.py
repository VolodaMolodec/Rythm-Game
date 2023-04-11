import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rythm game"

MUSIC_VOLUME = 1

LIST_OF_SOUNDTRACKS = [
    "Demo",
    "MainTheme"
    ]

CIRCLES_HEIGHT = 110
DOWN_BORDER = CIRCLES_HEIGHT - 120

NOTES_SPEED = 10

LINES_X = [125,235,345,455,565,675]

RENDER_UPDATE = 0.017

PROGRESS_BARS_UPDATE = 50

class TempSprite:   #Class of temporal sprites that will show on the screen for some ticks
    def __init__(self, name, pos_x, pos_y):
        self.sprite = arcade.Sprite("assets/sprites/" + name + ".png")  #Sprite for remporal sprite
        self.sprite.center_x = pos_x
        self.sprite.center_y = pos_y
        self.ticks = 50 #How long it will show


    def update(self):   #Updating ticks of temporal sprite
        self.ticks -= 1
        if(self.ticks <= 0):    #If ticks is 0 then temporal sprite should be deleted. Deleting realized in other function, so return 1 if ticks is over
            return 1
        else:
            return 0

    def draw(self): #Drawing sprite
        self.sprite.draw()

class Lines:    #Class of lines where notes will be placed
    def __init__(self):
        self.lines = []
        for i in range(6):  #We need 6 lines
            self.lines.append(arcade.SpriteList())
        self.speed = NOTES_SPEED    #Speed of notes

    def add(self,note): #note contains [line_number, sprite]
        sprite = note[1]    #Creating sprite for note and place it in line
        sprite.center_y = SCREEN_HEIGHT
        sprite.center_x = LINES_X[note[0] - 1]
        self.lines[note[0] - 1].append(sprite)

    def update(self):   #Updating notes in lines and checking if some note passed down bordew
        missedLines = []
        for i in range(6):
            l = len(self.lines[i])
            if l == 0:
                continue
            
            for j in range(l):
                self.lines[i][j].center_y -= self.speed
                if self.lines[i][j].center_y <= DOWN_BORDER:    #If note passed down border then add line's id to missedLines and deleting note
                    missedLines.append(i)
                    self.pop(i)
                    j -= 1

        return missedLines

    def draw(self): #Drawing lines
        for line in self.lines:
            line.draw()

    def get_line_element(self, id):
        if len(self.lines[id]) == 0:
            return None
        else:
            return self.lines[id][0]

    def pop(self,id):   #Function that delete first note in line with id matches argument
        if len(self.lines[id]) != 0:
            self.lines[id].pop(0)

class Scene:    #There all visual parts are placed
    def __init__(self):
        self.loadedSprites = None
        self.lines = Lines()    #Defining lines
        self.score = GameScore() #Defining score (ik it is wrong from architecture perspective, but it makes everething easiear)
        self.tempSprites = []   #Defining list of temporal sprites

    def change(self, new_scene):    #Changing scene to new with new_scene name
        self.loadedSprites = arcade.SpriteList()
        if new_scene == "Loading":  #Loading scene
            load = arcade.Sprite("assets/sprites/Loading.png")
            load.center_x = SCREEN_WIDTH / 2
            load.center_y = SCREEN_HEIGHT / 2
            self.loadedSprites.append(load)
        elif new_scene == "MainMenu":   #Main Menu scene
            background = arcade.Sprite("assets/sprites/TitleScreen.png", 1,0,0,0,0,SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
            title = arcade.Sprite("assets/sprites/TitleName.png", 1,0,0,0,0,SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
            demoButton = arcade.Sprite("assets/sprites/DemoButton.png", 1,0,0,0,0,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.loadedSprites.append(background)
            self.loadedSprites.append(title)
            self.loadedSprites.append(demoButton)
        else:   #Game scene
            background = arcade.Sprite("assets/music/" + new_scene + "/Background.png", 1,0,0,0,0,SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
            circles = arcade.Sprite("assets/sprites/Circles.png", 1, 0, 0, 0, 0, SCREEN_WIDTH / 2, 110)
            self.score.setup()
            self.loadedSprites.append(background)
            self.loadedSprites.append(circles)
        if len(self.tempSprites) != 0:  #Everytime we change scene we should clear temporal sprites list
            self.tempSprites.clear()
            

    def add_notes(self,notes_list): #Adding notes to lines
        if len(notes_list) != 0:
            for note in notes_list:
                self.lines.add(note)

    def draw(self): #Drawing scene
        if self.loadedSprites != None:
            arcade.start_render()
            self.loadedSprites.draw()
            self.lines.draw()
            self.score.draw()
            for sprite in self.tempSprites:
                sprite.draw()
            arcade.finish_render()
        

    def update(self):   #Updating scene parts
        missedLines = self.lines.update()
        for line in missedLines:    #If we have missed notes on some of the lines then ids of these lines will be placed in missedLines list. For each missed line we create "Bad" temp sprite
            self.score.add_result("Bad")
            self.tempSprites.append(TempSprite("Bad", LINES_X[line], CIRCLES_HEIGHT))
        i = 0
        while i < len(self.tempSprites):    #There we updating ticks of temporal sprites and, if needed, deleting those that ended
            hasEnded = self.tempSprites[i].update()
            if hasEnded:
                self.tempSprites.pop(i)
                i-=1
            i += 1


    def circle_press(self, id): #If circle has been pressed, this function called with id of the circle as argument
        element = self.lines.get_line_element(id)   #Getting note from line with id of the pressed circle
        if element == None: #If there are no notes, then nothing happen
            return None
        else:
            delta = math.fabs(element.center_y - CIRCLES_HEIGHT)    #If there are note then calculating delta as difference between note's y and circle's y 
            if delta <= 100:    #Depending on the delta we will get specific score
                self.lines.pop(id)
                if delta <= 25:
                    self.score.add_result("Ideal")
                    self.tempSprites.append(TempSprite("Ideal", LINES_X[id], CIRCLES_HEIGHT))
                elif delta <= 75:
                    self.score.add_result("Good")
                    self.tempSprites.append(TempSprite("Good", LINES_X[id], CIRCLES_HEIGHT))
                else:
                    self.score.add_result("Bad") 
                    self.tempSprites.append(TempSprite("Bad", LINES_X[id], CIRCLES_HEIGHT))
            elif delta <= 200: #If note too far, we don't even delete the note
                self.score.add_result("Bad")
                self.tempSprites.append(TempSprite("Bad", LINES_X[id], CIRCLES_HEIGHT))

                
                



class Note: #Note data class
    def __init__(self, time, typ, line):    #Note has it's time when it spawns, it's type and line where the note should be spawned
        self.time = time
        self.type = typ
        self.line = line

    def get_if_ready(self, time):   #Checking if the note is reandy. If ready, returns line, where the note should be spawned, and sprite of the note
        if self.time <= time:
            sprite = arcade.Sprite("assets/sprites/" + self.type + ".png")
            return [self.line, sprite]
        else:
            return 0



class Soundtrack:   #Simple class for soundtrack data
    def __init__(self,name):
        self.name = name
        self.sound = arcade.Sound("assets/music/" + name + "/Music.mp3")

class Player:
    def __init__(self):
        self.currentSoundtrack = None
        self.name = None
        self.playingTime = None
        self.len = None
        self.state = None
        self.soundtracks = None
        self.timer = None
        self.notes = []

    def load_soundtracks(self):
        self.soundtracks = []
        for name in LIST_OF_SOUNDTRACKS:
            self.soundtracks.append(Soundtrack(name))

    def play(self, name):
        if self.currentSoundtrack != None:
            self.currentSoundtrack.pause()
        for sound in self.soundtracks:
            if name == sound.name:
                self.currentSoundtrack = sound
                break

        self.currentSoundtrack = self.currentSoundtrack.sound.play()

    def load_to_game(self, name, timer = None):
        if self.currentSoundtrack != None:
            self.currentSoundtrack.pause()
        for sound in self.soundtracks:
            if name == sound.name:
                self.currentSoundtrack = sound
                break

        self.state = "inGame"
        self.playingTime = 0
        self.timer = timer
        self.name = self.currentSoundtrack.name
        self.len = self.currentSoundtrack.sound.get_length()
        self.currentSoundtrack = self.currentSoundtrack.sound.play()
        if timer != None:
            self.currentSoundtrack.pause()

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

    def get_avaible_notes(self):
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

    def update(self, delta_time):
        if self.state == "inGame":
            self.playingTime += delta_time
            if self.timer != None and self.playingTime >= self.timer:
                self.timer = None
                self.playingTime = 0
                self.currentSoundtrack.play()

    
class GameScore:
    def __init__(self):
        self.score = None
        self.combo = None
        self.mult = None

    def setup(self):
        self.score = 0
        self.combo = 0
        self.mult = 1

    def add_result(self, result):
        if result == None:
            return
        elif result == "Ideal":
            self.score += 10 * self.mult
            self.combo += 1
        elif result == "Good":
            self.score += 5 * self.mult
            self.combo += 1
        else:
            self.combo = 0

    def draw(self):
        if self.score != None:
            arcade.draw_text("Score: " + str(self.score),SCREEN_WIDTH / 16, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)
            if self.combo >= 3:
                arcade.draw_text("Combo: " + str(self.combo),SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)

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
            self.player.update(delta_time)
            self.scene.update()
            if self.player.timer == None:
                self.scene.add_notes(self.player.get_avaible_notes())
            
    def on_draw(self):
        self.scene.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.gameState == "MainMenu":
            if (x >= 250 and x <= 650) and (y >= 260 and y <= 340):
                self.startGame("Demo")
                
    def startGame(self,name):
        sound = arcade.Sound("assets/tecnical_sounds/ButtonClick.wav")
        sound.play()
        self.player.load_to_game(name, 3)
        self.scene.change(self.player.name)
        self.gameState = "Playing"

    def load(self):
        self.scene.change("Loading")
        self.scene.draw()
        self.player.load_soundtracks()
        self.scene.change("MainMenu")
        self.player.play("MainTheme")
        self.gameState = "MainMenu"

    def on_key_press(self, key: int, modifiers: int):
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

        return super().on_key_press(key, modifiers)

    


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
       
