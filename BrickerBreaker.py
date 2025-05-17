import pygame
# pygame setup



def createBackground(screen,midx,midy):
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((170, 238, 187))
            font = pygame.font.Font(None, 64)
            text = font.render("You best break those blocks!", True, (10, 10, 10))
            textpos = text.get_rect(centerx=midx, y=3.5*midy/2)
            background.blit(text, textpos)
            screen.blit(background, (0, 0))  # This line makes it actually appear


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.verticalControl = False

    def updatePos(self, w, h):
        self.x += w
        self.y += h
        self.pos = pygame.Vector2(self.x, self.y)


class Paddle(Player):
    def __init__(self,x,y,w,h):
        super().__init__(x,y)
        self.Rect = pygame.Rect(x, y, w, h)
        self.w = w
        self.h = h

    def updateRect(self):
        self.Rect.topleft = (self.x, self.y)


    def controls(self, player, paddleSpeed,dt):
            
        keys = pygame.key.get_pressed()
        if player.verticalControl == True:
            if keys[pygame.K_w]:
                self.updatePos(0 , -paddleSpeed * dt)
                self.updateRect()
            if keys[pygame.K_s]:
                self.updatePos(0 , paddleSpeed * dt)
                self.updateRect()

        if keys[pygame.K_a]:
            self.updatePos( -paddleSpeed * dt, 0)
            self.updateRect()
        if keys[pygame.K_d]:
            self.updatePos( paddleSpeed * dt, 0)
            self.updateRect()

    


class Block():
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Rect = pygame.Rect(x,y,w,h)
        self.hit = False


class Ball:
    def __init__(self, x, y, r, vx, vy, color="red"):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx  # horizontal velocity
        self.vy = vy # vertical velocity
        self.top = self.y + r
        self.bottom = self. y - r
        self.left = self.x - r
        self.right = self.x + r


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def get_pos(self):
        return (self.x, self.y)

    def update_bounds(self):
        self.top = self.y + self.r
        self.bottom = self.y - self.r
        self.left = self.x - self.r
        self.right = self.x + self.r

    def update_pos(self):
        self.x +=  self.vx
        self.y +=  self.vy


    def Collision(self,obj):
        # Simple reversal of vertical direction
        self.vy *= -1

        # adjusts ball.y to prevent sticking
        #ball.y = obj.y - ball.r
        
        self.update_bounds()

    def paddleCollision(self, obj):
        
        # Simple reversal of vertical direction
        if (obj.x + obj.w) < self.x or obj.x > self.x:
            self.vx *= -1 
        else: 
            self.vy *= -1

        
        
        # #Makes the collision less boring
        hit_pos = (self.x - obj.x) / obj.w  
        self.vx = (hit_pos - 0.5) * 10  

        # adjusts ball.y to prevent sticking
        self.y = obj.y - self.r
        self.update_bounds()





def main():
            



    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    screenw = screen.get_width()
    screenh = screen.get_height()
    midx = screenw / 2
    midy = screenh / 2
    tolerance = 10



    player = Player(midx, (3*midy) // 2)
    paddleOne = Paddle(player.x, player.y, 150, 20)
    ball = Ball(midx,midy,5,0.1,-3, "red")

    blocks = []

    rows = 6
    columns = 12

    for i in range(1,columns):
        for j in range(rows,2*rows):
            blocks.append(Block(100*i, 30*j, 95,15))


    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        createBackground(screen,midx,midy)

        pygame.draw.rect(screen, "red", paddleOne.Rect)
        ball.draw(screen)
        
        colours = ["red","orange","blue","purple","green"]
        for i in blocks:
            index = blocks.index(i)
            pygame.draw.rect(screen,colours[index%len(colours)],i.Rect)

        #Paddle collision logic

        ball_rect = pygame.Rect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2)

        if ball_rect.colliderect(paddleOne.Rect):
            ball.paddleCollision(paddleOne.Rect)

        for i in range(len(blocks)):
            if ball_rect.colliderect(blocks[i].Rect):
                blocks[i].hit = True
                ball.Collision(blocks[i].Rect)

        for i in blocks:
            if i.hit == True:
                blocks.remove(i)
 
        ball.update_pos()
        ball.update_bounds()

        # wall collision logic
        if ball.bottom >  screenh or ball.top < 0:
            ball.vy = -ball.vy

        if ball.right > screenw or ball.left < 0:
            ball.vx = -ball.vx

        if ball.bottom >  screenh:
            main()
            

        #Controls logic
        paddleSpeed = 350
        paddleOne.controls(player,paddleSpeed,dt)

        # flip() the display 
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        fps = 60
        dt = clock.tick(fps) / 1000

    pygame.quit()


main()