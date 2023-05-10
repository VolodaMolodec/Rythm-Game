from Settings import SCREEN_HEIGHT, SCREEN_WIDTH, LINES_X, DOWN_BORDER, NOTES_SPEED, RENDER_UPDATE
import arcade

class SimpleNote:
    def __init__(self, line):
        self.line = line
        self.type = "Simple"
        self.sprite = arcade.Sprite("assets/sprites/Note.png")
        self.sprite.center_x = LINES_X[self.line]
        self.sprite.center_y = SCREEN_HEIGHT

    def update(self):
        self.sprite.center_y -= NOTES_SPEED
        if self.sprite.center_y <= DOWN_BORDER:
            return 1
        return 0

    def draw(self):
        self.sprite.draw()

    def get_height(self):
        return self.sprite.center_y

class LongNote:
    def __init__(self, line, duration):
        self.line = line
        self.type = "Long"
        h = NOTES_SPEED * duration / RENDER_UPDATE
        
        self.l = arcade.Sprite("assets/sprites/ProgressBarElement.png")
        self.l.center_y = SCREEN_HEIGHT + h/2
        self.l.center_x = LINES_X[line]
        self.l.height = h
        

        self.startNote = arcade.Sprite("assets/sprites/Note.png")
        self.startNote.center_y = SCREEN_HEIGHT
        self.startNote.center_x = LINES_X[line]

        self.endNote = arcade.Sprite("assets/sprites/Note.png")
        self.endNote.center_y = SCREEN_HEIGHT + h
        self.endNote.center_x = LINES_X[line]

    def update(self):
        self.l.center_y -= NOTES_SPEED
        if self.startNote != None:
            self.startNote.center_y -= NOTES_SPEED
        self.endNote.center_y -= NOTES_SPEED

    def draw(self):
        self.l.draw()
        if self.startNote != None:
            self.startNote.draw()
        self.endNote.draw()

    def get_height(self, note = None):
        if note == "Up":
            return self.endNote.center_y
        else:
            return self.startNote.center_y




