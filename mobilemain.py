from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

import math

class PlatonGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_pos = [200, 1000]
        self.enemy_pos = [800, 420]
        self.heal_pos = [2000, 450]
        self.round_heal_pos = [2200, 450]
        self.hay_pos = [1000, 500]
        self.enemyHP = 100
        self.playerHP = 100
        self.HayHP = 100
        self.attack_cooldown = 0
        self.attack_enemy_cooldown = 0
        self.attack_hay_cooldown = 0
        self.hay_cooldown = 0
        self.cursor_setting = -1
        self.coins = 0
        self.kills = 0
        self.roundHP = 0

        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.bg_image = Image(source='data/images/bg.png')
        self.layout.add_widget(self.bg_image)

        self.player_image = Image(source='data/images/player.png', size=(95, 90))
        self.bg_image.add_widget(self.player_image)

        self.sword_image = Image(source='data/images/knife.png', size=(60, 50))
        self.player_image.add_widget(self.sword_image)

        self.hay_image = Image(source='data/images/hay.png', size=(60, 50))
        self.bg_image.add_widget(self.hay_image)

        self.enemy_image = Image(source='data/images/enemy_stand.png', size=(95, 90))
        self.bg_image.add_widget(self.enemy_image)

        self.cursor_image_black = Image(source='data/images/cursor_black.png', size=(40, 40))
        self.cursor_image_white = Image(source='data/images/cursor_white.png', size=(40, 40))
        self.cursor_image_green = Image(source='data/images/cursor_green.png', size=(40, 40))
        self.cursor = self.cursor_image_white
        self.bg_image.add_widget(self.cursor)

        self.player_hp_label = Label(text='Numbis HP: 100')
        self.layout.add_widget(self.player_hp_label)

        self.enemy_hp_label = Label(text='Prixie HP: 100')
        self.layout.add_widget(self.enemy_hp_label)

        self.round_hp_label = Label(text='Rounds: 0')
        self.layout.add_widget(self.round_hp_label)

        self.kills_label = Label(text='Kills / Coins: 0')
        self.layout.add_widget(self.kills_label)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        self.attack_cooldown -= dt * 1000
        self.attack_enemy_cooldown -= dt * 1000
        self.attack_hay_cooldown -= dt * 1000
        self.hay_cooldown -= dt * 1000

        self.cursor.pos = self.player_pos
        self.player_image.pos = self.player_pos
        self.sword_image.pos = (self.player_pos[0] + 61, self.player_pos[1] + 30)
        self.enemy_image.pos = self.enemy_pos
        self.hay_image.pos = self.hay_pos

        self.player_hp_label.text = f'Numbis HP: {self.playerHP}'
        self.enemy_hp_label.text = f'Prixie HP: {self.enemyHP}'
        self.round_hp_label.text = f'Rounds: {self.roundHP}'
        self.kills_label.text = f'Kills / Coins: {self.kills}'

        self.attack_player()
        self.attack_enemy()
        self.attack_hay()

        if self.HayHP <= 0:
            self.hay_pos = [-1000, -1000]
            self.hay_cooldown = 10000

        if self.hay_cooldown <= 0:
            self.hay_pos = [1000, 500]

    def attack_player(self):
        if self.distance_between_points(self.player_pos, self.enemy_pos) <= 100 and self.attack_cooldown <= 0:
            self.playerHP -= 7
            self.attack_cooldown = 2000

    def attack_enemy(self):
        if self.distance_between_points(self.player_pos, self.enemy_pos) <= 100 and self.attack_enemy_cooldown <= 0:
            self.enemyHP -= 15
            self.attack_enemy_cooldown = 1500

    def attack_hay(self):
        if self.distance_between_points(self.player_pos, self.hay_pos) <= 100 and self.attack_hay_cooldown <= 0:
            self.HayHP -= 15
            self.attack_hay_cooldown = 2000

    def distance_between_points(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

class PlatonApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlatonGame(name='game'))
        return sm

if __name__ == '__main__':
    PlatonApp().run()
