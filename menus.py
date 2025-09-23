import wheel_menu

class MainMenu(wheel_menu.Menu):
    def __init__(self, quit_func):
        items = [
            wheel_menu.MenuItem("Item 1", lambda: print("Item 1 clicked!")),
            wheel_menu.MenuItem("Item 2", lambda: print("Item 2 clicked!")),
            wheel_menu.MenuItem("Item 3", lambda: print("Item 3 clicked!")),
            wheel_menu.MenuItem("Exit", quit_func),
            wheel_menu.Menu("Sub Menu", lambda: print("Sub Menu clicked!"), [
                wheel_menu.MenuItem("Sub Item 1", lambda: print("Sub Item 1 clicked!")),
                wheel_menu.MenuItem("Sub Item 2", lambda: print("Sub Item 2 clicked!"))
            ])
        ]
        super().__init__("Main Menu", None, items)
        self.text_width = 0
        self.width = 0

    def draw(self, surface, pos: tuple, delta: float):
        # Only draw sub items.
        self.propagate_draw(surface, pos, delta)