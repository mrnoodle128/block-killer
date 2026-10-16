import pygame, sys, random

pygame.init()

screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("block killer")
clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.surface = pygame.Surface((width, height))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()

    def draw(self):
        screen.blit(self.surface, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)


class Block(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed = 30

    def update(self, player, dt):
        super().update()
        self.y += self.speed * dt

        if self.rect.colliderect(player.rect):
            pygame.quit()
            sys.exit()

class Player(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.speed = 50

    def update(self, dt):
        super().update()

        if self.moving_left:
            self.x -= self.speed * dt
        if self.moving_right:
            self.x += self.speed * dt

        if self.moving_down:
            self.y += self.speed * dt
        if self.moving_up:
            self.y -= self.speed * dt 


player = Player(100, 180, 10, 10)
starter_block = Block(0, 0, 100, 20)

blocks = [starter_block]

dt = 0

global_speed = 30

while True:
    screen.fill((128, 255, 100))

    if starter_block.y >= 100:
        next_block = Block(random.randint(0, 200), 0, 100, 20)

        global_speed += 1
        next_block.speed = global_speed
        
        blocks.append(next_block)
        starter_block = next_block

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            elif event.key == pygame.K_RIGHT:
                player.moving_right = True

            if event.key == pygame.K_UP:
                player.moving_up = True
            elif event.key == pygame.K_DOWN:
                player.moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            elif event.key == pygame.K_RIGHT:
                player.moving_right = False

            if event.key == pygame.K_UP:
                player.moving_up = False
            elif event.key == pygame.K_DOWN:
                player.moving_down = False
            
    dt = clock.tick(60) / 1000
    
    player.update(dt)
    for block in blocks:
        block.update(player, dt)
   
    pygame.display.update()