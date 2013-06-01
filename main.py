#!/usr/bin/env python2.7
import string
from os.path import dirname, abspath, join
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.text import Label as CoreLabel
from kivy.metrics import sp


class Letter(Widget):
    angular = NumericProperty(0)
    texture = ObjectProperty()
    texture_size = ListProperty([0, 0])


class Word(RelativeLayout):

    stream = ObjectProperty()

    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)

        self.text = kwargs.get('text')
        self.letters = []
        spacing_x = 0
        letternumber = 0

        for eachletter in self.text:
            texture = self.stream.tex_letters[eachletter]

            # First let's make a Letter widget with the current letter, in a
            # list of Letter instances.
            letter = Letter(texture=texture, x=spacing_x, y=self.y,
                    texture_size=texture.size)
            self.letters.append(letter)

            # Then add it to the parent Word widget:
            self.add_widget(letter)

            # Next we need to increment spacing_x to be ready to properly place
            # the next letter without overlapping.
            if eachletter == ' ':
                eachletter = 'a'
            spacing_x += self.stream.tex_letters[eachletter].width

            letternumber += 1

        # This is the easiest way I know to get the width, in x, of my Word
        # class. Maybe kivy provides another way?
        # NOT NEEDED NOW
        self.length_x = spacing_x

    #def explode(self):
                #num = 0
        #for x in self.children:
        #    self.letters[num].angular += 120*dt #dt is current framerate. 
        #    num += 1



class Stream(RelativeLayout):

    def __init__(self, **kwargs):
        super(Stream, self).__init__(**kwargs)
        # texture associated to each letter
        self.tex_letters = {}
        # currently displayed word
        self.displayed_words = {}
        self.font_name = join(dirname(__file__), 'data', 'edunline.ttf')
        self.loadstory()


    def loadstory(self):
        with open(join(dirname(__file__), 'data', 'story.txt'), 'r') as fd:
            story = fd.read().split('|')

        self.words = words = []
        cue_Rachel = []
        cue_tears = []
        spacing_x = 0
        wordnumber = 0

        # first, prebuilt all the characters texture.
        # one optimization would be, at the end, to put all the letter into a
        # big atlas = one texture used
        letters = ''
        for eachword in story:
            if eachword[:1] == '^':
                continue
            letters += eachword
        letters = list(set(letters))

        for letter in letters:
            clabel = CoreLabel(text=letter, font_size=sp(40),
                    font_name=self.font_name)
            clabel.refresh()
            self.tex_letters[letter] = clabel.texture

        for eachword in story:
            if eachword == "^n":
                spacing_x += 50 #I really need the width of 27 spaces. Might have to create a sample Word just to do this.
            elif eachword == "^r":
                cue_Rachel.append(len(words))
            elif eachword == "^t":
                cue_tears.append(len(words))
            else:
                paragraph_width = self.get_paragraph_width(eachword)
                words.append({
                    'text': eachword,
                    'width': paragraph_width,
                    'offset_x': spacing_x})
                spacing_x += paragraph_width
                wordnumber += 1

    def get_paragraph_width(self, text):
        width = 0
        for letter in text:
            if letter == ' ':
                letter = 'a'
            width += self.tex_letters[letter].width
        return width

    def move(self, dt):
        self.x -= 60 * dt

        # calculate which word should be displayed on the screen
        # we should display word that collide in the screen
        left = -self.x
        right = left + self.width
        matches = []
        for index, p in enumerate(self.words):
            pleft = p['offset_x']
            pright = pleft + p['width']

            if pleft < right and pright > left:
                matches += [index]

        # matches contain the index of each word we need to display
        # create and add the non-existing word
        for index in matches:

            # index already displayed ? don't recreate
            if index in self.displayed_words:
                continue

            # new index = new word. create and add the widget
            data = self.words[index]
            word = Word(text=data['text'],
                    stream=self,
                    x=data['offset_x'])
            self.add_widget(word)
            self.displayed_words[index] = word

        # remove the non-displayed-word anymore
        for index in list(self.displayed_words.keys()):
            if index not in matches:
                word = self.displayed_words[index]
                self.remove_widget(word)
                del self.displayed_words[index]


class GuiltyGame(FloatLayout):

    def update(self, dt):
        self.stream.move(dt)



class GuiltyApp(App):

    def build(self):
        game = GuiltyGame()
        Clock.schedule_interval(game.update, 1 / 60.)
        return game



if __name__ == '__main__':
    GuiltyApp().run()
