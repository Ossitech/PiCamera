import pygame
import pygame_gui

class Gui:
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

    def setup(self):
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='Menu',
            manager=self.ui_manager,
            command=self.toggle_menu
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 10 - 50, 10), (50, 40)),
            text='Exit',
            manager=self.ui_manager,
            command=exit
        )
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((60, 60), (self.screen_width - 120, self.screen_height - 120)),
            manager=self.ui_manager,
            visible=False
        )

        self.lel = pygame_gui.elements.UIProgressBar(
            relative_rect=pygame.Rect((100, 100), (100, 100)),
            manager=self.ui_manager
        )

        self.a = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 200), (50, 40)),
            text="Test",
            manager=self.ui_manager,
            container=self.menu_panel
        )
    
    def toggle_menu(self):
        if self.menu_panel.visible:
            # self.menu_panel.visible = False
            self.menu_panel.visible = False
            self.menu_button.set_text("Menu")
        else:
            self.menu_panel.visible = True
            self.menu_button.set_text("Close")
        
        self.lel.visible = self.menu_panel.visible
        self.a.visible = self.menu_panel.visible
    
    def process_events(self, pygame_events):
        self.ui_manager.process_events(pygame_events)
    
    def update(self, delta: float):
        self.ui_manager.update(delta)
    
    def draw(self, surface: pygame.Surface):
        self.ui_manager.draw_ui(surface)