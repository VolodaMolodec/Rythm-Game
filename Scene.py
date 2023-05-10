import arcade
from Notes import SimpleNote, LongNote
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH, RENDER_UPDATE, DOWN_BORDER, CIRCLES_HEIGHT, LINES_X, LIST_OF_SOUNDTRACKS


class GameScore:
    def __init__(self):
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
        elif result == "Long":
            self.score += 1 * self.mult
        else:
            self.combo = 0

    def draw(self):
        if self.score != None:
            arcade.draw_text("Score: " + str(self.score),SCREEN_WIDTH / 16, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)
            if self.combo >= 3:
                arcade.draw_text("Combo: " + str(self.combo),SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)

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

    def draw(self):
        self.sprite.draw()

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
        self.lines = [[],[],[],[],[],[]]
        self.linePressed = [0,0,0,0,0,0]
        self.score = GameScore()
        self.tempSprites = []


    def add(self,note): #Adding note to line
        self.lines[note.line].append(note)

    def update(self):
        i = 0
        while i < len(self.tempSprites):    #There we updating ticks of temporal sprites and, if needed, deleting those that ended
            hasEnded = self.tempSprites[i].update()
            if hasEnded:
                self.tempSprites.pop(i)
                i-=1
            i += 1

        for i in range(6):
            l = len(self.lines[i])
            if l == 0:
                continue
            j = 0
            while j < l:
                self.lines[i][j].update()
                if type(self.lines[i][j]) == SimpleNote:
                    if self.lines[i][j].get_height() <= DOWN_BORDER:
                        self.get_result("Bad", i)
                        self.pop(i)
                        j-=1
                        l-=1

                else:
                    if self.lines[i][j].get_height("Up") <= CIRCLES_HEIGHT:
                        self.pop(i)
                        j-=1
                        l-=1
                    elif self.lines[i][j].get_height("Down") <= DOWN_BORDER and self.linePressed[i] == 0:
                        self.get_result("Bad", i)
                    elif self.linePressed[i] == 1:
                        self.score.add_result("Long")
                j+=1

    def draw(self): #Drawing lines
        self.score.draw()
        for line in self.lines:
            for note in line:
                note.draw()

        for sprite in self.tempSprites:
            sprite.draw()

    def get_result(self, result, line = None):
        self.score.add_result(result)
        if line != None:
            self.tempSprites.append(TempSprite(result, LINES_X[line], CIRCLES_HEIGHT))

    def pop(self,id):   #Function that delete first note in line with id matches argument
        if len(self.lines[id]) != 0:
            self.lines[id].pop(0)

    def get_element(self, id):
        l = len(self.lines[id])
        if l == 0:
            return None
        else:
            return self.lines[id][0]

    def line_press(self, id):
        self.linePressed[id] = 1
        element = self.get_element(id)
        if element != None:
            self.get_result(self.calc_result(id), id)

    def line_release(self, id):
        self.linePressed[id] = 0
        if len(self.lines[id]) != 0 and type(self.lines[id][0]) == LongNote:
            self.get_result("Bad", id)

    def calc_result(self, id):
        delta = abs(self.lines[id][0].get_height() - CIRCLES_HEIGHT)
        if delta < 200:
            if delta < 25:
                score = "Ideal"
            elif delta < 100:
                score = "Good"
            else:
                score = "Bad"
            if type(self.lines[id][0]) == SimpleNote:
                self.pop(id)
            return score
        else:
            return "Bad"





class Scene:    #There all visual parts are placed
    def __init__(self):
        self.loadedSprites = None
        self.lines = None    #Defining lines
        self.tempSprites = []   #Defining list of temporal sprites
        self.progressBar = None
        self.texts = None

    def change(self, new_scene, par = None):    #Changing scene to new with new_scene name. Par - additional parametr for some purposes
        self.loadedSprites = arcade.SpriteList()
        self.texts = []
        
        if new_scene == "Loading":  #Loading scene
            load = arcade.Sprite("assets/sprites/Loading.png")
            load.center_x = SCREEN_WIDTH / 2
            load.center_y = SCREEN_HEIGHT / 2
            self.loadedSprites.append(load)

        elif new_scene == "MainMenu":   #Main Menu scene
            self.lines = None
            self.progressBar = None
            background = arcade.Sprite("assets/sprites/TitleScreen.png", 1,0,0,SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
            title = arcade.Sprite("assets/sprites/TitleName.png", 1,0,0,0,0,SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
            demoButton = arcade.Sprite("assets/sprites/DemoButton.png", 1,0,0,0,0,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            redactor = arcade.Sprite("assets/sprites/WhiteTemplate.png", 1, 0, 0, 300, 80, SCREEN_WIDTH/2, SCREEN_HEIGHT / 2 - 150)
            redactorText = arcade.Text("Redactor", SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 150, arcade.color.BLACK, 16, 2)
            self.loadedSprites.append(background)
            self.loadedSprites.append(title)
            self.loadedSprites.append(demoButton)
            self.loadedSprites.append(redactor)
            self.texts.append(redactorText)

        elif new_scene == "SelectLevel":    #Select Level scene
            background = arcade.Sprite("assets/sprites/TitleScreen.png", 1,0,0,0,0,SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
            self.loadedSprites.append(background)
            if par != 0:
                up = arcade.Sprite("assets/sprites/Up.png",1,0,0,0,0,SCREEN_WIDTH/2, SCREEN_HEIGHT - 40)
                self.loadedSprites.append(up)
            i = 0
            while par * 4 + i < len(LIST_OF_SOUNDTRACKS) and i < 4:
                icon = arcade.Sprite("assets/music/" + LIST_OF_SOUNDTRACKS[par * 4 + i] + "/Background.png", 0.2,0,0,0,0,SCREEN_WIDTH / 4,SCREEN_HEIGHT - 100 * (i + 1) - 25 * i)
                template = arcade.Sprite("assets/sprites/WhiteTemplate.png", 0.95, 0,0,0,0,SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100 * (i + 1) - 25 * i)
                text = arcade.Text(LIST_OF_SOUNDTRACKS[par * 4 + i], SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100 * (i + 1) - 25 * i, arcade.color.BLACK, 16, 2)
                self.loadedSprites.append(template)
                self.loadedSprites.append(icon)
                self.texts.append(text)
                i += 1
            if i + par * 4 < len(LIST_OF_SOUNDTRACKS):
                down = arcade.Sprite("assets/sprites/Down.png",1,0,0,0,0,SCREEN_WIDTH / 2, 40)
                self.loadedSprites.append(down)

        elif new_scene == "Redactor":
            background = arcade.Sprite("assets/sprites/BlackTemplate.png", 1, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.loadedSprites.append(background)

        elif new_scene == "Results":
            self.score = None
            self.progressBar = None
            background = arcade.Sprite("assets/sprites/TitleScreen.png", 1, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            score = arcade.Text(str(self.lines.score.score), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK)
            
            self.loadedSprites.append(background)
            self.texts.append(score)

        else:   #Game scene
            background = arcade.Sprite("assets/music/" + new_scene + "/Background.png", 1,0,0,0,0,SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
            circles = arcade.Sprite("assets/sprites/Circles.png", 1, 0, 0, 0, 0, SCREEN_WIDTH / 2, 110)
            self.lines = Lines()
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
            if self.lines:
                self.lines.draw()
            for sprite in self.tempSprites:
                sprite.draw()
            if self.progressBar:
                self.progressBar.draw()
            
            for text in self.texts:
                text.draw()
            arcade.finish_render()
        

    def update(self):   #Updating scene parts
        self.lines.update()
        
        if self.progressBar:
            self.progressBar.update()


    def circle_press(self, id): #If circle has been pressed, this function called with id of the circle as argument
        self.lines.line_press(id)

    def circle_release(self,id):
        self.lines.line_release(id)




