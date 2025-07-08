import pygame

# Game Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 20
PADDLE_SPEED = 500
BALL_RADIUS = 10
BLOCK_WIDTH = 95
BLOCK_HEIGHT = 25
BLOCK_ROWS = 6
BLOCK_COLS = 12
BLOCK_SPACING = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_COLOR = (27, 35, 46)
BALL_COLOR = (220, 50, 50)
BACKGROUND_COLOR = (180, 210, 210)
BLOCK_COLORS = [(224, 89, 89), (101, 153, 212), (113, 219, 124), (230, 184, 99)]

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PADDLE_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 400
        self.velocity = pygame.Vector2(0.2*self.speed, self.speed)

    def update(self, dt):
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        if self.rect.left <= 0:
            self.velocity.x *= -1
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.velocity.x *= -1
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.velocity.y *= -1
            self.rect.top = 0

    def bounce_paddle(self, paddle_rect):
        self.velocity.y = -abs(self.velocity.y)
        hit_pos = (self.rect.centerx - paddle_rect.centerx) / (paddle_rect.width / 2)
        self.velocity.x = hit_pos * self.speed

        if self.rect.bottom > paddle_rect.top:
            self.rect.bottom = paddle_rect.top

    def bounce_block(self, block):
        overlap_x = (self.rect.width / 2 + block.rect.width / 2) - abs(self.rect.centerx - block.rect.centerx)
        overlap_y = (self.rect.height / 2 + block.rect.height / 2) - abs(self.rect.centery - block.rect.centery)

        if overlap_x < overlap_y:
            self.velocity.x *= -1
            if self.rect.centerx > block.rect.centerx:
                self.rect.left = block.rect.right
            else:
                self.rect.right = block.rect.left
        else:
            self.velocity.y *= -1
            if self.rect.centery > block.rect.centery:
                self.rect.top = block.rect.bottom
            else:
                self.rect.bottom = block.rect.top

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

def create_background(screen):
    background = pygame.Surface(screen.get_size())
    background.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 50)
    text = font.render("I love you <3", True, BLACK)
    textpos = text.get_rect(centerx=screen.get_width() / 2, y=SCREEN_HEIGHT - 600)
    background.blit(text, textpos)
    return background

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block Breaker")
    clock = pygame.time.Clock()

    background = create_background(screen)

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    paddle = Paddle(SCREEN_WIDTH / 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2)
    ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    all_sprites.add(paddle, ball)

    for row in range(BLOCK_ROWS):
        for col in range(1,BLOCK_COLS):
            x = col * (BLOCK_WIDTH + BLOCK_SPACING) + BLOCK_SPACING
            y = row * (BLOCK_HEIGHT + BLOCK_SPACING) + BLOCK_SPACING + 50
            block = Block(x, y, BLOCK_COLORS[(row + col) % len(BLOCK_COLORS)])
            all_sprites.add(block)
            blocks.add(block)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60) / 1000.0

        all_sprites.update(dt)

        if pygame.sprite.collide_rect(ball, paddle):
            ball.bounce_paddle(paddle.rect)

        collided_blocks = pygame.sprite.spritecollide(ball, blocks, True)
        if collided_blocks:
            ball.bounce_block(collided_blocks[0])

        if ball.rect.bottom >= SCREEN_HEIGHT:
            ball.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            ball.velocity = pygame.Vector2(0, -ball.speed)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()