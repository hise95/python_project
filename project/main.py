from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty,NumericProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from random import shuffle, choice, randint
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.base import stopTouchApp
from kivy.uix.popup import Popup

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        app.save_prog

class GameScreen(Screen):
    points = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        popup = Popup(title='Title window',
                      content=Label(text='text Popup'))
        popup.open()
        
    def on_enter(self, *args):
        self.ids.planet.new_planet()
        return super().on_enter(*args)

class Planet(Image):
    is_anim = False
    hp = None
    planet = None
    planet_index = 0
    points = 0
    mult = 1

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_anim:

            self.parent.parent.parent.points += (1*self.mult)
            self.points += (1*self.mult)
            self.hp -= 1

            if self.hp <=0:
                self.break_planet()
                app.storage.put('progress', planet=self.planet)
            else:
                x = self.x
                y = self.y
                size = self.size.copy()   
                anim = Animation(
                    size=(size[0]*1.2, size[1]*1.2), d=.1, t='out_back') + Animation(size=(size[0], size[1]), d=.1)
                x = x
                y = y - 5
                anim &= Animation(x=x, y=y, d=.05) + Animation(x=x, y=y, d=.1)
            anim.start(self)
            self.is_anim = True
            anim.on_complete = lambda *arg: setattr(self, "is_animation", False)

        return super().on_touch_down(touch)
    
    def new_planet(self):

       Planet.planet = self.planet = app.LEVELS[randint(0, len(app.LEVELS)-1)]
       self.source = app.PLANETS[self.planet]['source']
       self.hp = app.PLANETS[self.planet]['hp']
       size_copy = self.size.copy()
       self.size = app.PLANETS[self.planet]['size']
       self.center = self.parent.center
       anim = Animation(opacity=1, d=0.3)
       anim &= Animation(
           size=(self.size[0]/1.5, self.size[1]/1.5), d=.2, t='out_back')
       anim &= Animation(center=self.parent.center, d=.3)
       anim.start(self)
       anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)
       self.size = size_copy  # Використовуйте size_copy, щоб зберегти попередні розміри


    def break_planet(self):
        self.is_anim = True
        anim = Animation(size=(self.size[0]*2, self.size[1]*2), d=.2)
        anim &= Animation(center=self.parent.center, d=.2)
        anim &= Animation(opacity=0, d=.3)

        anim.start(self)
        anim.on_complete = Clock.schedule_once(self.new_planet, .5)


class MainApp(App):
    storage = None
    LEVELS = ['LVL1', 'LVL2', 'LVL3', 'LVL4', 'LVL5', 'LVL6', 'LVL7']

    PLANETS = {
        'LVL1': {"source": 'assets/img/.png', 'hp': 10, "size": ("200dp", "200dp")},
        'LVL2': {"source": 'assets/img/.png', 'hp': 20, "size": ("200dp", "200dp")},
        'LVL3': {"source": 'assets/img/.png', 'hp': 30, "size": ("200dp", "200dp")},
        'LVL4': {"source": 'assets/img/.png', 'hp': 40, "size": ("200dp", "200dp")},
        'LVL5': {"source": 'assets/img/.png', 'hp': 50, "size": ("200dp", "200dp")},
        'LVL6': {"source": 'assets/img/.png', 'hp': 60, "size": ("200dp", "200dp")},
        'LVL7': {"source": 'assets/img/.png', 'hp': 80, "size": ("200dp", "200dp")}
}

    def save_prog(self):
        print(Planet.planet)
        app.storage.put('progress', planet=Planet.planet,
                        hp=Planet.hp,
                        planet_index=Planet.planet_index,
                        mult=Planet.mult,
                        points=Planet.points)
        
    def build(self):
        global storage
        self.storage = JsonStore(self.user_data_dir+"storage.json")
        storage = self.storage
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

    def load_prog(self):
        return self.storage.get("progress")


if platform != 'android':
    Window.size = (400, 800)
    Window.left = 1050
    Window.top = 100
    
app = MainApp()
app.run()
    