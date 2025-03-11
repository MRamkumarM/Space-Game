import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
# Screen dimensions
wn_width, wn_height = 1000, 700
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption("Shooting Game")

# Define the Enemy class
class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

# Function to create a new enemy
def create_enemy():
    x = random.randint(0, wn_width - 20)  # Random x position within screen bounds
    y = 0  # Start at the top of the screen
    width, height = 20, 20  # Size of the enemy
    speed = random.randint(1, 3)  # Random speed
    return Enemy(x, y, width, height, speed)

# Load player image
img = pygame.image.load("E:/py/python/sample_python_projects/s.png")
img = pygame.transform.scale(img, (50, 75))  # Resize the image
player = img.get_rect(center=(500, 650))  # Position the player

# img1 = pygame.image.load("E:\py\python\sample_python_projects\OIP.jpg")
# img1 = pygame.transform.scale(img1,(1000,700))

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
            print("Game Over!")  # You can add game-over logic here
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
                print("Enemy Hit!")  # You can add scoring logic here
                break  # Break to avoid checking the same bullet against other enemies

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate

# Quit Pygame
pygame.quit()
