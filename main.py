from os.path import dirname, abspath
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

class Letter(Label):
	def __init__(self, **kwargs):
		super(Letter, self).__init__(**kwargs)



class Stream(RelativeLayout):

	def __init__(self, **kwargs):
		super(Stream, self).__init__(**kwargs)
		
		story = "And then she was there. Across the salad bar."
		self.loadstory(story)

	def loadstory(self, story):
		self.letters = []
		currentx, num = 0, 0
		for currentletter in story:
			
			#First let's make a Label with the current letter, in a list of Label instances.
			self.letters.append(Letter(text=currentletter, x=self.center_x + currentx, y=self.center_y, font_name=dirname(abspath(__file__))+'/data/edunline.ttf'))
			
			#Then add it to the parent Stream widget:
			self.add_widget(self.letters[num])

			#This is a bit of a hack for spaces.
			if currentletter == " ":
				currentx += self.letters[num]._label.get_extents("a")[0] #Spaces don't actually register as anything when in a label, so here I'm using "a" to get a width.
			else:
				currentx += self.letters[num]._label.get_extents(currentletter)[0]

			num+=1
		self.storyLength = num

	def move(self):
		self.x += 1
		num = 0
		for x in self.letters:
			self.letters[num].angle += 1
			#print self.letters[num].angle
			num += 1



class GuiltyGame(Widget):
	#stream = ObjectProperty()
	
	def update(self, dt):
		#self.stream.x += 1
		#print self.stream.x
		self.stream.move()



class GuiltyApp(App):

	def build(self):
		game = GuiltyGame()
		Clock.schedule_interval(game.update, 1.0/60.0)
		return game



if __name__ == '__main__':
	GuiltyApp().run()