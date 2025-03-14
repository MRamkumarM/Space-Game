import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Screen dimensions
wn_width, wn_height = 1000, 700
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption("Shooting Game")

# Load player image
img = pygame.image.load("E:/py/python/sample_python_projects/s.png")
img = pygame.transform.scale(img, (50, 75))  # Resize the image
player = img.get_rect(center=(500, 650))  # Position the player

# Load enemy image
img1 = pygame.image.load("E:/py/python/sample_python_projects/OIP.jpg")
img1 = pygame.transform.scale(img1, (20, 20))  # Resize enemy image

# Load game over image
game_over_img = pygame.image.load("E:/py/python/sample_python_projects/game_over.jpg")
game_over_img = pygame.transform.scale(game_over_img, (300, 150))

def show_game_over():
    wn.fill((0, 0, 0))  # Clear the screen
    wn.blit(game_over_img, (wn_width // 2 - 150, wn_height // 2 - 75))  # Display game over image
    pygame.display.flip()
    pygame.time.delay(2000)  # Pause for 2 seconds before quitting

# Define the Enemy class
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(img1, self.rect.topleft)

# Function to create a new enemy
def create_enemy():
    x = random.randint(0, wn_width - 20)  # Random x position within screen bounds
    y = 0  # Start at the top of the screen
    speed = random.randint(1, 3)  # Random speed
    return Enemy(x, y, speed)

# Game variables
speed = 5  # Player movement speed
bullets = []  # List to store bullets
bullet_speed = 10  # Bullet movement speed
enemys = [create_enemy() for _ in range(15)]  # Create 15 enemies

# Main game loop
run = True
clock = pygame.time.Clock()

while run:
    wn.fill((0, 0, 0))  # Clear the screen

    # Render the score text
    text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    wn.blit(text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:  # Use keyboard to shoot
            if event.key == K_SPACE:
                bullet = pygame.Rect(player.centerx - 2, player.top, 5, 10)  # Create a bullet at the player's position
                bullets.append(bullet)

    # Player movement (left and right)
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.left > 0:
        player.x -= speed
    if keys[K_RIGHT] and player.right < wn_width:
        player.x += speed

    # Draw the player
    wn.blit(img, player)

    # Update and draw each enemy
    for enemy in enemys[:]:
        enemy.move()
        enemy.draw(wn)

        # Check if the enemy has moved off the screen
        if enemy.rect.y > wn_height:
            enemys.remove(enemy)
            enemys.append(create_enemy())

        # Check for collision between player and enemy
        if player.colliderect(enemy.rect):
            show_game_over()
            run = False  # End the game

    # Update and draw each bullet
    for bullet in bullets[:]:  # Iterate over a copy to avoid removing issues
        pygame.draw.rect(wn, (255, 255, 255), bullet)  # Draw the bullet
        bullet.y -= bullet_speed  # Move the bullet upward

        # Remove bullets that go off the screen
        if bullet.bottom < 0:
            bullets.remove(bullet)
            continue  # Skip checking collision if bullet is already removed

        # Check for collision between bullet and enemy
        for enemy in enemys[:]:
            if bullet.colliderect(enemy.rect):
                if bullet in bullets:  # Ensure the bullet exists before removing
                    bullets.remove(bullet)
                enemys.remove(enemy)
                enemys.append(create_enemy())  # Replace the destroyed enemy
                score += 1  # Increase score
                break  # Break to avoid checking the same bullet against other enemies

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate

# Quit Pygame
pygame.quit()

