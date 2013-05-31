#!/usr/bin/env python2.7
import string
from os.path import dirname, abspath
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout



class Letter(Label):
    angle = NumericProperty()

    def __init__(self, **kwargs):
        super(Letter, self).__init__(**kwargs)



class Word(RelativeLayout):

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
        
        self.text = text
        self.letters = []
        spacing_x = 0
        letternumber = 0

        for eachletter in self.text:
            #First let's make a Letter widget with the current letter, in a list of Letter instances.
            self.letters.append(Letter(text=eachletter, font_size='40sp', x=self.x + spacing_x, y=self.y, font_name=dirname(abspath(__file__))+'/data/edunline.ttf'))
            #Then add it to the parent Word widget:
            self.add_widget(self.letters[letternumber])
            #Next we need to increment spacing_x to be ready to properly place the next letter without overlapping.
            if eachletter == " ":
                spacing_x += self.letters[letternumber]._label.get_extents("a")[0] #Since spaces currently don't return any width, we use the width of the letter "a".
            else:
                spacing_x += self.letters[letternumber]._label.get_extents(eachletter)[0]
            
            letternumber += 1
        
        self.length_x = spacing_x #This is the easiest way I know to get the width, in x, of my Word class. Maybe kivy provides another way?



class Stream(RelativeLayout):

    def __init__(self, **kwargs):
        super(Stream, self).__init__(**kwargs)
        self.loadstory()


    def loadstory(self):
        story = "And then she was there. Across the salad bar."
        #storyfile = open(dirname(abspath(__file__))+"/data/story.txt", "r")
        #story = storyfile.read().split("|")
        #storyfile.close()

        paragraph = []
        cue_Rachel = []
        cue_tears = []
        spacing_x = 0
        wordnumber = 0
        
        for eachword in story:
            if eachword == "^n":
                spacing_x += 50 #I really need the width of 27 spaces. Might have to create a sample Word just to do this.
            elif eachword == "^r":
                cue_Rachel.append(len(paragraph))
            elif eachword == "^t":
                cue_tears.append(len(paragraph))
            else:
                paragraph.append(Word(text=eachword, x=spacing_x, y=self.y)) #Filling the list with instances of Word.
            spacing_x += paragraph[wordnumber].length_x

        wordnumber += 1


    def move(self, dt):
        self.x += 1
        num = 0
        for x in self.children:
            self.letters[num].angular += 120*dt #dt is current framerate. 
            num += 1



class GuiltyGame(Widget):
    
    def update(self, dt):
        self.stream.move(dt)



class GuiltyApp(App):

    def build(self):
        game = GuiltyGame()
        #Clock.schedule_interval(game.update, 1.0/60.0)
        return game



if __name__ == '__main__':
    GuiltyApp().run()