from kivy.app import App
from kivymd.theming import ThemeManager
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen

class MyApp(App):
    theme_cls = ThemeManager()
    def build(self):
        self.title = "My App"

        # Create the navigation drawer
        nav_drawer = MDNavigationDrawer()

        # Create the list items for the navigation drawer
        menu_items = [
            OneLineListItem(text="Home"),
            OneLineListItem(text="Settings"),
            OneLineListItem(text="About")
        ]

        # Add the list items to the navigation drawer
        for item in menu_items:
            nav_drawer.add_widget(item)

        # Create the screen manager and add screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(SettingsScreen(name="settings"))
        screen_manager.add_widget(AboutScreen(name="about"))

        # Create the navigation layout and add the screen manager and navigation drawer
        nav_layout = MDNavigationLayout()
        nav_layout.add_widget(screen_manager)
        nav_layout.add_widget(nav_drawer)

        return nav_layout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Home"

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Settings"

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "About"

if __name__ == '__main__':
    MyApp().run()