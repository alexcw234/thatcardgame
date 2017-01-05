import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label

from UI.u_card import U_Card


class ThatcardgameApp(App):

    def build(self):
        return U_Card()


if __name__ == '__main__':
    ThatcardgameApp().run()
