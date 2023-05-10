import arcade
from Notes import SimpleNote, LongNote
from Settings import LIST_OF_SOUNDTRACKS, TITLE_SCREEN_SOUND, RENDER_UPDATE, SCREEN_HEIGHT, CIRCLES_HEIGHT, NOTES_SPEED
import random

class NoteData: #Note data class
    def __init__(self, time, line, duration = None):    #Note has it's time when it spawns, it's type and line where the note should be spawned
        self.time = time
        if duration != None:
            self.type = "Long"
            self.duration = duration
        else:
            self.type = "Simple"
        self.line = line

    def get_if_ready(self, time):   #Checking if the note is reandy. If ready, returns line, where the note should be spawned, and sprite of the note
        if self.time <= time:
            if self.type == "Simple":
                return SimpleNote(self.line)
            else:
                return LongNote(self.line, self.duration)
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
        self.notesData = []

    def load_soundtracks(self):
        self.soundtracks = []
        for name in LIST_OF_SOUNDTRACKS:
            self.soundtracks.append(Soundtrack(name))

    def play(self, name):
        if name == "MainTheme":
            if self.currentSoundtrack != None:
                self.currentSoundtrack.volume = 0.6
            else:
                sound = None
                if TITLE_SCREEN_SOUND == "Random":
                    _id = random.randint(0, len(LIST_OF_SOUNDTRACKS) - 1)
                    soundName = LIST_OF_SOUNDTRACKS[_id]
                    for soundtrack in LIST_OF_SOUNDTRACKS:
                        if soundtrack == soundName:
                            sound = arcade.Sound("assets/music/" + soundName + "/Music.mp3")
                            break
                else:
                   sound = arcade.Sound("assets/music/MainTheme/Music.mp3")
                self.currentSoundtrack = sound.play()
        else:
            if self.currentSoundtrack != None:
                self.currentSoundtrack.pause()
                self.currentSoundtrack = None
        
            for sound in self.soundtracks:
                if name == sound.name:
                    self.currentSoundtrack = sound
                    break

            self.currentSoundtrack = self.currentSoundtrack.sound.play()

    def stop(self):
        if self.currentSoundtrack != None:
            self.currentSoundtrack.pause()

    def load_to_game(self, name, timer = None):
        if self.currentSoundtrack != None:
            self.currentSoundtrack.pause()
            self.currentSoundtrack = None
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

        self.notesData = []
        with open('assets/music/' + self.name + '/Notes.txt') as f:
            cons_time = RENDER_UPDATE * (SCREEN_HEIGHT - CIRCLES_HEIGHT) / NOTES_SPEED #Time then note reach center of circle
            while True:                
                temp = f.readline()
                temp = temp.split()
                if len(temp) > 4 or len(temp) < 3:
                    return
                
                time = float(temp[0]) - cons_time
                typ = temp[1]
                line = int(temp[2])
                duration = None
                if typ == "Long":
                    duration = float(temp[3])
                self.notesData.append(NoteData(time, line, duration))

    def get_avaible_notes(self):
        returningNotes = []
        while True:
            if len(self.notesData) != 0:
                temp = self.notesData[0].get_if_ready(self.playingTime)
                if temp != 0:
                    returningNotes.append(temp)
                    self.notesData.pop(0)
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

            if self.playingTime >= self.len:
                self.currentSoundtrack = None
                return 1







