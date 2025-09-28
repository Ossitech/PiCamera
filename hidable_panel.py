import pygame
import pygame_gui

HIDE_OFFSET = 1000

# This class serves as a workaround for the
# "visible" property of pygame_gui.elements.UIPanel,
# which currently does not work as expected.
# Instead of using the visible property,
# elements are simply moved out of view by an offset (HIDE_OFFSET).
class HidablePanel:
    def __init__(self, rect: pygame.Rect, ui_manager: pygame_gui.UIManager):
        self.ui_manager = ui_manager
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=rect,
            manager=ui_manager
        )
    
    def hide(self):
        if self.is_visible():
            # hide by moving out of view.
            self.panel.set_relative_position((
                self.panel.relative_rect.x,
                self.panel.relative_rect.y - HIDE_OFFSET
            ))
    
    def show(self):
        if not self.is_visible():
            # show by moving into view.
            self.panel.set_relative_position((
                self.panel.relative_rect.x,
                self.panel.relative_rect.y + HIDE_OFFSET
            ))
    
    def is_visible(self):
        return self.panel.relative_rect.y > 0