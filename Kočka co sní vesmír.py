import pygame

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Corrected pygame.draw.rect() usage
    pygame.draw.rect(screen, WHITE, (100, 100, 200, 150))  # Example rect: (surface, color, rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()