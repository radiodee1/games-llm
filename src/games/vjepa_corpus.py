
import sys
import pygame

# 1. Start Pygame
pygame.init()

# 2. Set screen size (width, height)
screen = pygame.display.set_mode((320, 420))
pygame.display.set_caption("Show Image and Wait for Key")

# 3. Load the image (replace 'example.png' with your file)
try:
    image = pygame.image.load("./pic/figure_0.png")
except pygame.error:
    # Fallback plain surface if no image file exists
    image = pygame.Surface((320, 420))
    image.fill((200, 50, 50))

# 4. Draw image to screen once
screen.fill((255, 255, 255))  # White background
screen.blit(image, (0, 0))  # Position x, y
pygame.display.flip()

# 5. Wait for a single key press or quit event
waiting = True
while waiting:
    event = pygame.event.wait()  # Pauses CPU until an event happens
    if event.type == pygame.QUIT:
        waiting = False
    elif event.type == pygame.KEYDOWN:
        key_name = pygame.key.name(event.key)
        print(key_name)
        waiting = False  # Exit loop on any key press

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

pygame.quit()
sys.exit()
