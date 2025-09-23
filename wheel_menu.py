import pygame

MENU_COLOR_HIGHLIGHTED = (255, 255, 255)
MENU_COLOR_FOCUSED = (0, 0, 0)
MENU_COLOR_NOT_FOCUSED = (100, 100, 100)
MENU_COLOR_SELECTED = (33, 103, 255)
MENU_Y_POS = 300 # Half of the screen height
MENU_ITEM_SPACING = 5
TEXT_SIZE = 20
MARGIN_Y = 5

font = pygame.font.Font("data/Open_Sans/static/OpenSans-Bold.ttf", size=TEXT_SIZE)

MENU_ITEM_HEIGHT = font.size("Example")[1]

ANIMATION_SPEED = 20.0

def animate_value(delta: float, current, target, speed):
    distance = target - current

    return current + distance * speed * delta

class MenuItem:
    def __init__(self, display_name: str, callback: callable):
        self.parent_menu = None
        self.display_name = display_name
        self.rendered_name_black = font.render(self.display_name.encode(), True, (0, 0, 0))
        self.rendered_name_white = font.render(self.display_name.encode(), True, (255, 255, 255))
        (self.text_width, self.text_height) = self.rendered_name_black.get_size()
        self.height = self.text_height + 2 * MARGIN_Y
        self.width = self.text_width + self.height
        self.callback = callback
        self.selected = False
        self.last_confirmed = False
        self.focused = False
    
    def draw(self, surface, pos: tuple, delta: float):
        color = None
        text_white = True

        if self.selected:
            color = MENU_COLOR_SELECTED
            text_white = False
        elif self.last_confirmed:
            color = MENU_COLOR_HIGHLIGHTED
            text_white = False
        elif self.parent_menu.focused:
            color = MENU_COLOR_FOCUSED
        else:
            color = MENU_COLOR_NOT_FOCUSED
        
        rect_pos = (pos[0] + self.height / 2, pos[1])

        pygame.draw.ellipse(surface, color, ((pos, (self.height, self.height))))
        pygame.draw.ellipse(surface, color, ((pos[0] + self.text_width, pos[1]), (self.height, self.height)))
        pygame.draw.rect(surface, color, (rect_pos, (self.text_width, self.height)))

        text_pos = (pos[0] + self.height / 2, pos[1] + MARGIN_Y)

        if text_white:
            surface.blit(self.rendered_name_white, text_pos)
        else:
            surface.blit(self.rendered_name_black, text_pos)
    
    def handle_ok(self):
        if self.parent_menu:
            for menu_item in self.parent_menu.menu_items:
                menu_item.last_confirmed = False

        self.last_confirmed = True

        if self.callback:
            self.callback()
    
    def handle_back(self):
        pass

    def handle_up(self):
        pass

    def handle_down(self):
        pass


class Menu(MenuItem):
    def __init__(self, display_name: str, callback: callable, menu_items: list):
        super().__init__(display_name, callback)
        self.menu_items = menu_items
        self.menu_width = 0

        for menu_item in self.menu_items:
            menu_item.parent_menu = self
            self.menu_width = max(self.menu_width, menu_item.width)

        if len(self.menu_items) > 0:
            self.menu_items[0].selected = True

        self.expanded = False
        self.selected_sub_item_index = 0

        # Animation
        self.animated_index = 0.0
        self.animated_offset = 0.0
    
    def draw(self, surface, pos: tuple, delta: float):
        super().draw(surface, pos, delta)
        self.propagate_draw(surface, pos, delta)

    def propagate_draw(self, surface, pos: tuple, delta: float):
        if self.expanded:
            offset = 0
            if self.parent_menu:
                offset = self.parent_menu.menu_width
            
            self.animated_index = animate_value(delta, self.animated_index, self.selected_sub_item_index, ANIMATION_SPEED)
            self.animated_offset = animate_value(delta, self.animated_offset, offset, ANIMATION_SPEED)

            i = 0
            for menu_item in self.menu_items:
                menu_item.draw(surface, (pos[0] + self.animated_offset + MENU_ITEM_SPACING, pos[1] + (i - self.animated_index) * (self.height + MENU_ITEM_SPACING)), delta)
                i += 1
        else:
            self.animated_offset = -100.0
    
    def handle_down(self):
        selected_sub_item = self.menu_items[self.selected_sub_item_index]
        
        if self.focused:
            if self.selected_sub_item_index < len(self.menu_items) - 1:
                selected_sub_item.selected = False
                self.selected_sub_item_index += 1
                selected_sub_item = self.menu_items[self.selected_sub_item_index]
                selected_sub_item.selected = True
        elif self.expanded:
            selected_sub_item.handle_down()
    
    def handle_up(self):
        selected_sub_item = self.menu_items[self.selected_sub_item_index]

        if self.focused:
            if self.selected_sub_item_index > 0:
                selected_sub_item.selected = False
                self.selected_sub_item_index -= 1
                selected_sub_item = self.menu_items[self.selected_sub_item_index]
                selected_sub_item.selected = True

        elif self.expanded:
            selected_sub_item.handle_up()
    
    def handle_ok(self):
        if self.expanded:
            selected_sub_item = self.menu_items[self.selected_sub_item_index]
            selected_sub_item.handle_ok()
        elif not self.focused:
            super().handle_ok()
            self.expanded = True
            self.focused = True
            if self.parent_menu:
                self.parent_menu.focused = False
    
    def handle_back(self):
        if self.focused:
            self.focused = False
            self.expanded = False
            if self.parent_menu:
                self.parent_menu.focused = True
        elif self.expanded:
            selected_sub_item = self.menu_items[self.selected_sub_item_index]
            selected_sub_item.handle_back()