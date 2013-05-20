from os.path import dirname, abspath
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label



class Stream(Widget):

	def __init__(self, **kwargs):
		super(Stream, self).__init__(**kwargs)
		
		story = "And then she was there. Across the salad bar."
		self.loadstory(story)


	def loadstory(self, story):
		letters = []
		currentx, num = 0, 0
		for currentletter in story:
			
			#First, let's make a Label with the current letter:
			label = Label(text=currentletter, x=currentx, font_name=dirname(abspath(__file__))+'/data/edunline.ttf')
			
			#Then add it to a list:
			letters.append(label)
			
			#Then also add it to the parent Stream widget:
			self.add_widget(label)
			
			#Next we have to update the texture--because otherwise it won't be updated until the next frame. We can't wait that long:
			letters[num].texture_update()
			
			#Using texture_size here only works with fixed width fonts--and the spacing for spaces is a hack:
			if currentletter == " ":
				currentx = currentx + 10
			else:
				currentx = currentx + letters[num].texture_size[0]

			num+=1

	def move(self):
		self.pos_x =- 1



class GuiltyGame(Widget):
	stream = ObjectProperty()
	
	def update(self, dt):
		self.stream.move()



class GuiltyApp(App):

	def build(self):
		game = GuiltyGame()
		Clock.schedule_interval(game.update, 1.0/60.0)
		#stream = Stream()
		#stream.loadstory()
		#game.add_widget(stream)
		return game



if __name__ == '__main__':
	GuiltyApp().run()