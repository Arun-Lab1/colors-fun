import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.metrics import sp
from kivy.core.window import Window

# Fixes the black flashing background during screen transitions
Window.clearcolor = (0.12, 0.12, 0.15, 1)


def create_styled_button(text, bg_color=(0.2, 0.6, 1, 1), font_size='20sp'):
    btn = Button(
        text=text,
        font_size=font_size,
        background_normal='',        # Removes default Kivy gray image texture
        background_color=(0, 0, 0, 0),  # Makes button base transparent
        color=(1, 1, 1, 1),          # White text
        bold=True
    )

    # Draw rounded background
    with btn.canvas.before:
        btn.bg_color_inst = Color(*bg_color)
        btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[18])

    # Keep background position updated when window moves or resizes
    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    btn.bind(pos=update_rect, size=update_rect)
    return btn


class BaseScreen(Screen):
    """Base screen class that sets a consistent dark theme background."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.12, 0.12, 0.15, 1)  # Dark slate background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class StartScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=25)
        
        self.title_label = Label(text="Colors Fun",font_name="LuckiestGuy-Regular.ttf", font_size='52sp', bold=True)

        
        
        play_button = create_styled_button("Play", bg_color=(0.1, 0.7, 0.4, 1), font_size='24sp')
        play_button.bind(on_press=self.go_to_game)
        
        layout.add_widget(self.title_label)
        layout.add_widget(play_button)
        self.add_widget(layout)


        self.start_title_animation()



    def start_title_animation(self):
        # Cycle through high-contrast vibrant colors
        color_anim = Animation(color=(1, 0.3, 0.3, 1), duration=1.2) + \
                   Animation(color=(0.3, 0.8, 1, 1), duration=1.2) + \
                   Animation(color=(1, 0.8, 0.2, 1), duration=1.2) + \
                   Animation(color=(0.4, 0.9, 0.4, 1), duration=1.2)
    
        color_anim.repeat = True
        color_anim.start(self.title_label)


    def go_to_game(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'mode'

    


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.correct_sound = SoundLoader.load('correct-answer.mp3')
        self.wrong_sound = SoundLoader.load('wrong-answer.mp3')

        self.score = 0

        # Mode timer limits
        self.mode_settings = {
            20: (50, 20),
            30: (60, 30),
            40: (70, 40),
            50: (80, 50)
        }
        self.current_max_time = 35  # Default time limit
        self.target_score = 20

        self.all_colors = {
            # --- BASE VIBRANT COLORS (20 Mode) ---
            "Red": (0.95, 0.1, 0.1, 1),
            "Green": (0.1, 0.75, 0.2, 1),
            "Blue": (0.05, 0.35, 0.95, 1),
            "Yellow": (1, 0.9, 0, 1),             # Pure Sun Yellow
            "Orange": (1, 0.45, 0, 1),            # Deep Flame Orange
            "Purple": (0.55, 0.1, 0.85, 1),        # Vivid Purple
            "Pink": (1, 0.4, 0.7, 1),
            "Brown": (0.45, 0.2, 0.05, 1),        # Rich Dark Wood Brown
            "Black": (0.08, 0.08, 0.08, 1),       # Soft Charcoal Black
            "White": (0.98, 0.98, 0.98, 1),
            "Gray": (0.5, 0.5, 0.5, 1),
            "Cyan": (0, 0.85, 0.95, 1),
            "Magenta": (0.95, 0, 0.85, 1),
            "Lime": (0.5, 1, 0, 1),               # Bright Neon Lime
            "Maroon": (0.45, 0, 0.1, 1),          # Dark Crimson Wine
            "Navy": (0.02, 0.08, 0.35, 1),        # Very Dark Deep Blue
            "Olive": (0.4, 0.45, 0.05, 1),        # Deep Muted Olive
            "Teal": (0, 0.45, 0.45, 1),
            "Gold": (0.9, 0.68, 0.05, 1),         # Rich Metallic Amber (Distinct from Yellow)
            "Coral": (1, 0.35, 0.25, 1),

            # --- MEDIUM EXPANSION (30 Mode) ---
            "Turquoise": (0.15, 0.8, 0.7, 1),
            "Indigo": (0.2, 0, 0.6, 1),
            "Violet": (0.8, 0.35, 0.95, 1),
            "Salmon": (0.95, 0.45, 0.4, 1),
            "Sky Blue": (0.4, 0.75, 1, 1),
            "Khaki": (0.75, 0.7, 0.4, 1),
            "Plum": (0.55, 0.2, 0.55, 1),
            "Crimson": (0.8, 0.05, 0.2, 1),
            "Orchid": (0.8, 0.3, 0.75, 1),
            "Lavender": (0.75, 0.7, 0.95, 1),

            # --- HARD EXPANSION (40 Mode) ---
            "Mint": (0.35, 0.95, 0.65, 1),
            "Peach": (1, 0.7, 0.55, 1),           # Warm Soft Peach
            "Tan": (0.7, 0.5, 0.35, 1),           # Medium Leather Tan
            "Beige": (0.95, 0.92, 0.75, 1),       # Very Light Warm Cream
            "Forest Green": (0.05, 0.4, 0.15, 1),
            "Sea Green": (0.2, 0.65, 0.4, 1),
            "Dark Green": (0, 0.25, 0.05, 1),
            "Royal Blue": (0.2, 0.3, 0.85, 1),
            "Steel Blue": (0.25, 0.45, 0.6, 1),
            "Chocolate": (0.35, 0.15, 0.05, 1),

            # --- EXPERT EXPANSION (50 Mode) ---
            "Sienna": (0.6, 0.25, 0.1, 1),
            "Deep Pink": (0.95, 0.05, 0.45, 1),
            "Hot Pink": (1, 0.2, 0.65, 1),
            "Tomato": (0.9, 0.25, 0.15, 1),
            "Wheat": (0.88, 0.78, 0.55, 1),       # Warm Light Grain
            "Aquamarine": (0.3, 0.95, 0.85, 1),
            "Chartreuse": (0.7, 0.9, 0.05, 1),    # Yellow-Green Leaf
            "Slate Gray": (0.35, 0.4, 0.45, 1),
            "Dark Blue": (0, 0.1, 0.45, 1),
            "Dark Red": (0.35, 0, 0, 1)


        }

        self.colors = self.all_colors  # Default set

        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=10)

        back_btn = create_styled_button("Menu", bg_color=(0.3, 0.3, 0.3, 1), font_size='14sp')
        back_btn.size_hint_x = 0.32
        back_btn.bind(on_press=self.go_to_mode)
        header.add_widget(back_btn)

        self.time_left = self.current_max_time
        self.timer_event = None
        self.timer_label = Label(text=str(self.time_left), font_size='28sp', bold=True, size_hint_x=0.36, halign='center', valign='middle')
        self.timer_label.bind(size=self.timer_label.setter('text_size'))
        header.add_widget(self.timer_label)

        self.warning_anim = None

        self.score_label = Label(text=f"Score: {self.score}/{self.target_score}", font_size='18sp', size_hint_x=0.32, halign='center', valign='middle')
        self.score_label.bind(size=self.score_label.setter('text_size'))
        header.add_widget(self.score_label)

        layout.add_widget(header)

        self.target_label = Label(text="Target Color", font_size='32sp', bold=True, size_hint_y=0.2)
        layout.add_widget(self.target_label)

        self.grid = GridLayout(cols=2, spacing=12)
        layout.add_widget(self.grid)

        self.add_widget(layout)
        self.generate_round()

    def animate_low_time(self):
        if self.warning_anim:
            return
        
        self.warning_anim = Animation(color= (1, 0.2, 0.2, 1), font_size=sp(38), duration=0.3) + \
                            Animation(color= (1, 1, 1, 1), font_size=sp(28), duration=0.3)

        self.warning_anim.repeat = True
        self.warning_anim.start(self.timer_label)

    def stop_low_time_warning(self):
        if self.warning_anim:
            self.warning_anim.cancel(self.timer_label)
            self.warning_anim = None

        self.timer_label.color = (1, 1, 1, 1)
        self.timer_label.font_size = '28sp'

    def generate_round(self):
        self.grid.clear_widgets()
        options = random.sample(list(self.colors.keys()), 4)
        self.target_color = random.choice(options)
        self.target_label.text = self.target_color

        for color_name in options:
            btn = Button(
                text="",
                background_normal='',
                background_color=(0, 0, 0, 0)
            )
            btn.color_name = color_name
            btn.color_rgba = self.colors[color_name]
            
            # Draw rounded color tile + subtle border
            with btn.canvas.before:
                Color(*btn.color_rgba)
                btn.bg_shape = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[12])
                Color(1, 1, 1, 0.4)
                btn.border_shape = Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, 12), width=1.5)

            btn.bind(pos=self._update_tile, size=self._update_tile)
            btn.bind(on_press=self.check_answer)
            btn.disabled = False
            self.grid.add_widget(btn)

    def _update_tile(self, instance, value):
        instance.bg_shape.pos = instance.pos
        instance.bg_shape.size = instance.size
        instance.border_shape.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 12)

    def check_answer(self, instance):

        pop_effect = Animation(size_hint_x=1.08, size_hint_y=1.08, duration=0.08) + \
                     Animation(size_hint_x=1.0, size_hint_y=1.0, duration=0.08)

        # Trigger it on the button that was pressed (instance)
        pop_effect.start(instance)
        
        for btn in self.grid.children:
            btn.disabled = True

        if instance.color_name == self.target_color:
            self.score += 1
            self.target_label.text = "Correct"
            if self.correct_sound:
                self.correct_sound.play()
        else:
            self.score = max(0, self.score - 1)
            self.target_label.text = "Try Again"
            if self.wrong_sound:
                self.wrong_sound.play()

        self.score_label.text = f"Score: {self.score}/{self.target_score}"

        if self.score >= self.target_score:
            if self.timer_event:
                self.timer_event.cancel()
            self.stop_low_time_warning()
            self.score = 0
            self.manager.current = 'win'
        else:
            Clock.schedule_once(self.next_round_callback, 1)

    def next_round_callback(self, dt):
        self.generate_round()

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = str(self.time_left)


        if self.time_left <= 5 and self.time_left > 0:
            self.animate_low_time()
        elif self.time_left > 5:
            self.stop_low_time_warning()


        if self.time_left <= 0:
            if self.timer_event:
                self.timer_event.cancel()

            self.stop_low_time_warning()
            game_over_screen = self.manager.get_screen('game_over')
            game_over_screen.score_label.text = f"You answered: {self.score}/{self.target_score} correctly"
            self.manager.current = 'game_over'

    def on_enter(self, *args):
        self.stop_low_time_warning()
        self.score = 0
        self.score_label.text = f"Score: {self.score}/{self.target_score}"
        self.time_left = self.current_max_time
        self.timer_label.text = str(self.time_left)
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self, *args):
        if self.timer_event:
            self.timer_event.cancel()

    def set_mode(self, count):
        color_items = list(self.all_colors.items())[:count]
        self.colors = dict(color_items)
        if count in self.mode_settings:
            self.current_max_time, self.target_score = self.mode_settings[count]

    def go_to_mode(self, instance):
        if self.timer_event:
            self.timer_event.cancel()

        self.stop_low_time_warning()
        self.manager.transition.direction = 'right'
        self.manager.current = 'mode'


class WinScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)

        win_label = Label(text="You Win", font_size='36sp', bold=True, color=(0.2, 0.9, 0.4, 1))
        layout.add_widget(win_label)

        replay_button = create_styled_button("Play Again", bg_color=(0.2, 0.6, 1, 1), font_size='22sp')
        replay_button.bind(on_press=self.play_again)
        layout.add_widget(replay_button)

        change_mode_button = create_styled_button("Change Mode", bg_color=(0.5, 0.3, 0.8, 1), font_size='22sp')
        change_mode_button.bind(on_press=self.go_to_mode)
        layout.add_widget(change_mode_button)

        self.add_widget(layout)

    def go_to_mode(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'mode'

    def play_again(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.score = 0
        game_screen.score_label.text = f"Score: 0/{game_screen.target_score}"
        game_screen.generate_round()
        self.manager.current = 'game'


class GameOverScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)

        game_over_label = Label(text="Game Over", font_size='36sp', bold=True, color=(1, 0.3, 0.3, 1))
        layout.add_widget(game_over_label)

        self.score_label = Label(text="Final Score: 0/0", font_size='22sp', color=(1, 1, 1, 1))
        layout.add_widget(self.score_label)

        try_again_button = create_styled_button("Try Again", bg_color=(0.9, 0.3, 0.3, 1), font_size='22sp')
        try_again_button.bind(on_press=self.try_again)
        layout.add_widget(try_again_button)

        change_mode_button = create_styled_button("Change Mode", bg_color=(0.4, 0.4, 0.4, 1), font_size='22sp')
        change_mode_button.bind(on_press=self.go_to_mode)
        layout.add_widget(change_mode_button)

        self.add_widget(layout)

    def try_again(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.score = 0
        game_screen.score_label.text = "Score: 0"
        game_screen.generate_round()
        self.manager.current = 'game'

    def go_to_mode(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'mode'


class ModeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        title_label = Label(text='Choose Difficulty', font_size='28sp', bold=True)
        layout.add_widget(title_label)

        modes = [
            ('Basic (20 Colors)', 20, (0.2, 0.6, 1, 1)),
            ('Advanced (30 Colors)', 30, (0.95, 0.6, 0.1, 1)),
            ('Expert (40 Colors)', 40, (0.85, 0.25, 0.4, 1)),
            ('Master (50 Colors)', 50, (0.6, 0.2, 0.8, 1)),
        ]

        for text, count, color in modes:
            btn = create_styled_button(text, bg_color=color)
            btn.bind(on_press=lambda inst, c=count: self.select_mode(c))
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_mode(self, count):
        game_screen = self.manager.get_screen('game')
        game_screen.set_mode(count)
        game_screen.score = 0
        game_screen.score_label.text = 'Score: 0'
        game_screen.generate_round()

        self.manager.transition.direction = 'left'
        self.manager.current = 'game'


class ColorGameApp(App):
    def build(self):
        self.icon = 'icon.png'
        sm = ScreenManager()
        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(ModeScreen(name='mode'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(WinScreen(name='win'))
        sm.add_widget(GameOverScreen(name='game_over'))
        return sm


if __name__ == '__main__':
    ColorGameApp().run()


#create by Arun