import pygame
import touch_menu

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 480))

test_slider = touch_menu.Slider("Test", -5, 5, None)

while True:
    delta = clock.tick(60) * 0.001

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    test_slider.draw(screen)
    test_slider.handle_input()

    pygame.display.update()