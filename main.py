import pygame
import random

# Initialize Pygame
pygame.init()

# Variables for screen and game elements
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 20
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 8
BRICK_COLS = 13
BRICK_SPACING = 4
BRICK_OFFSET_TOP = 50
BALL_SPEED = 1
PADDLE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Create the paddle
paddle_width = PADDLE_WIDTH
paddle_height = PADDLE_HEIGHT
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - paddle_height
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

# Create the ball
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED

# Create the bricks with different colors
bricks = []
colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN, MAGENTA, GRAY, WHITE]
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * (BRICK_WIDTH + BRICK_SPACING)
        brick_y = row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_OFFSET_TOP
        color = random.choice(colors)
        brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append((brick_rect, color))

# Game variables
score = 0
lives = 10
current_level = 1

# Game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += PADDLE_SPEED

        # Move the ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        if ball.colliderect(paddle) and ball_speed_y > 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with bricks
        for brick, color in bricks[:]:  # Iterate over a copy of the bricks list to allow removal
            if ball.colliderect(brick):
                bricks.remove((brick, color))
                ball_speed_y = -ball_speed_y
                score += 1

        # Game over condition
        if ball.top >= SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset the ball position
                ball.x = SCREEN_WIDTH // 2
                ball.y = SCREEN_HEIGHT // 2
                ball_speed_x = BALL_SPEED * random.choice((1, -1))
                ball_speed_y = BALL_SPEED

        # Check for level completion (all bricks destroyed)
        if not bricks:
            current_level += 1
            # Load the next level or end the game if there are no more levels

        # Clear the screen
        screen.fill(WHITE)

        # Draw bricks
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

        # Draw paddle
        pygame.draw.rect(screen, RED, paddle)

        # Draw the ball
        pygame.draw.circle(screen, RED, (ball.x + BALL_RADIUS, ball.y + BALL_RADIUS), BALL_RADIUS)

        # Draw score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, GREEN)
        lives_text = font.render(f"Lives: {lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()




