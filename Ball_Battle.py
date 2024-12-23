import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Clamp player's position to stay within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

# Computer class
class Computer(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.score = 0

    def update(self, balls):
        nearest_ball = None
        min_distance = float('inf')

        for ball in balls:
            dx = ball.rect.centerx - self.rect.centerx
            dy = ball.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                min_distance = distance
                nearest_ball = ball

        if nearest_ball:
            dx = nearest_ball.rect.centerx - self.rect.centerx
            dy = nearest_ball.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
            self.rect.clamp_ip(screen.get_rect())

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed_y *= -1

# Create player
player = Player(RED, 100, 100)

# Create computer
computer = Computer(BLUE, 700, 500)

# Create balls
balls = pygame.sprite.Group()
for _ in range(20):
    ball = Ball(BLACK, random.randint(0, screen_width), random.randint(0, screen_height), 10)
    balls.add(ball)

# Button class
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(None, 36)
            text = font.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

# Create start/stop button
button = Button(WHITE, screen_width // 2 - 50, 500, 100, 50, 'Start')

# Main loop
running = False
clock = pygame.time.Clock()
winner = None

while not running:
    screen.fill(WHITE)

    # Display game name
    game_name_text = font.render("Ball Battle", True, BLACK)
    screen.blit(game_name_text, ((screen_width - game_name_text.get_width()) // 2, 200))

    button.draw(screen, BLACK)
    pygame.display.flip()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_over(pos):
                running = True

# Game loop
while not winner:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            winner = "Computer"
            break

    screen.fill(WHITE)

    # Update player
    player.update()

    # Update computer
    computer.update(balls)

    # Update balls
    balls.update()

    # Check for collisions between players and balls
    player_collisions = pygame.sprite.spritecollide(player, balls, True)
    if player_collisions:
        player.score += len(player_collisions)

    computer_collisions = pygame.sprite.spritecollide(computer, balls, True)
    if computer_collisions:
        computer.score += len(computer_collisions)

    # Check for win condition
    if player.score >= 10:
        winner = "You"
    elif computer.score >= 10:
        winner = "Computer"

    # Draw player, computer, and balls
    screen.blit(player.image, player.rect)
    screen.blit(computer.image, computer.rect)
    balls.draw(screen)

    # Render and display scores
    player_score_text = font.render(f"Player Score: {player.score}", True, BLACK)
    computer_score_text = font.render(f"Computer Score: {computer.score}", True, BLACK)
    screen.blit(player_score_text, (10, 10))
    screen.blit(computer_score_text, (screen_width - computer_score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

# Display the winner
if winner:
    winner_text = font.render(f"{winner} wins!", True, BLACK)
    screen.blit(winner_text, ((screen_width - winner_text.get_width()) // 2, (screen_height - winner_text.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Pause for 2 seconds before quitting

pygame.quit()
