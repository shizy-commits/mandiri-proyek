import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon & Star Adventure Deluxe")
clock = pygame.time.Clock()

BACKGROUND = (245, 235, 255)
TEXT = (60, 40, 80)
PURPLE = (120, 60, 200)
GREEN = (40, 180, 80)
RED = (180, 50, 100)
GRAY = (120, 120, 120)

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = 5

    def move(self, dx, dy, walls):
        self.rect.x += dx

        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= dx

        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.y -= dy

        self.rect.clamp_ip(screen.get_rect())

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

LEVELS = [
{
"luna":(80,600),
"nova":(870,600),
"moons":[(180,500),(250,180),(450,350)],
"stars":[(800,500),(700,220),(550,150)],
"walls":[pygame.Rect(300,150,30,400), pygame.Rect(650,150,30,400)]
},
{
"luna":(80,600),
"nova":(870,600),
"moons":[(180,100),(300,500),(350,300)],
"stars":[(820,100),(700,500),(650,200)],
"walls":[pygame.Rect(200,250,600,30), pygame.Rect(450,100,30,400)]
},
{
"luna":(80,600),
"nova":(870,600),
"moons":[(120,120),(450,500),(350,250)],
"stars":[(820,120),(650,520),(700,250)],
"walls":[pygame.Rect(250,150,30,400), pygame.Rect(500,100,30,500), pygame.Rect(750,150,30,400)]
}
]

def remove_items_inside_walls(items, walls):

    safe_items = []

    for x, y in items:

        rect = pygame.Rect(x, y, 30, 30)

        valid = True

        for wall in walls:
            if rect.colliderect(wall):
                valid = False
                break

        if valid:
            safe_items.append((x, y))

    return safe_items

class Game:
    def __init__(self):
        self.state = "menu"
        self.level = 0
        self.score = 0

    def load_level(self, index):
        data = LEVELS[index]

        self.luna = Player(
            *data["luna"],
            (220,180,255)
        )

        self.nova = Player(
            *data["nova"],
            (255,220,180)
        )

        self.walls = data["walls"]

        safe_moons = remove_items_inside_walls(
            data["moons"],
            self.walls
        )

        safe_stars = remove_items_inside_walls(
            data["stars"],
            self.walls
        )

        self.moons = [
            pygame.Rect(x, y, 30, 30)
            for x, y in safe_moons
        ]

        self.stars = [
            pygame.Rect(x, y, 30, 30)
            for x, y in safe_stars
        ]

        self.door = pygame.Rect(
            450,
            40,
            100,
            120
        )

        self.door_open = False
        self.win = False

        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.state != "game":
            return

        keys = pygame.key.get_pressed()

        luna_dx = (keys[pygame.K_d]-keys[pygame.K_a])*self.luna.speed
        luna_dy = (keys[pygame.K_s]-keys[pygame.K_w])*self.luna.speed

        nova_dx = (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*self.nova.speed
        nova_dy = (keys[pygame.K_DOWN]-keys[pygame.K_UP])*self.nova.speed

        self.luna.move(luna_dx,luna_dy,self.walls)
        self.nova.move(nova_dx,nova_dy,self.walls)

        for moon in self.moons[:]:
            if self.luna.rect.colliderect(moon):
                self.moons.remove(moon)
                self.score += 10

        for star in self.stars[:]:
            if self.nova.rect.colliderect(star):
                self.stars.remove(star)
                self.score += 10

        if not self.moons and not self.stars:
            self.door_open = True

        if self.door_open:
            if self.luna.rect.colliderect(self.door) and self.nova.rect.colliderect(self.door):
                self.win = True
                self.state = "win"

    def draw(self):
        screen.fill(BACKGROUND)

        if self.state == "menu":
            title = big_font.render("Moon & Star Adventure", True, PURPLE)
            screen.blit(title, title.get_rect(center=(WIDTH//2,220)))

            txt = font.render("Press SPACE to Start", True, TEXT)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2,350)))
            return

        if self.state in ["game","win"]:
            seconds = (pygame.time.get_ticks()-self.start_time)//1000

            pygame.draw.rect(screen, GREEN if self.door_open else PURPLE, self.door)

            for wall in self.walls:
                pygame.draw.rect(screen, GRAY, wall)

            angle = pygame.time.get_ticks()/5

            for moon in self.moons:
                surf = pygame.Surface((30,30), pygame.SRCALPHA)
                pygame.draw.circle(surf,(200,150,255),(15,15),15)
                rot = pygame.transform.rotate(surf, angle)
                screen.blit(rot, rot.get_rect(center=moon.center))

            for star in self.stars:
                surf = pygame.Surface((30,30), pygame.SRCALPHA)
                pygame.draw.circle(surf,(255,220,0),(15,15),15)
                rot = pygame.transform.rotate(surf, -angle)
                screen.blit(rot, rot.get_rect(center=star.center))

            self.luna.draw(screen)
            self.nova.draw(screen)

            screen.blit(font.render(f"Level: {self.level+1}",True,TEXT),(20,20))
            screen.blit(font.render(f"Score: {self.score}",True,TEXT),(20,60))
            screen.blit(font.render(f"Time: {seconds}s",True,TEXT),(20,100))

            msg = "Collect all items!" if not self.door_open else "Door Open! Enter Together!"
            screen.blit(font.render(msg,True,RED if not self.door_open else GREEN),(350,180))

        if self.state == "win":
            overlay = pygame.Surface((WIDTH,HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((255,255,255))
            screen.blit(overlay,(0,0))

            win = big_font.render("LEVEL COMPLETE!",True,PURPLE)
            screen.blit(win, win.get_rect(center=(WIDTH//2,280)))

            if self.level < len(LEVELS)-1:
                txt = font.render("Press N for Next Level",True,TEXT)
            else:
                txt = font.render("All Levels Complete! Press R",True,TEXT)

            screen.blit(txt, txt.get_rect(center=(WIDTH//2,380)))

game = Game()

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game.state == "menu" and event.key == pygame.K_SPACE:
                print("START")
                game.level = 0
                game.score = 0
                game.load_level(0)
                game.state = "game"
                
            elif game.state == "win":
                if event.key == pygame.K_n and game.level < len(LEVELS)-1:
                    game.level += 1
                    game.load_level(game.level)
                    game.state = "game"

                if event.key == pygame.K_r:
                    game.level = 0
                    game.score = 0
                    game.load_level(0)
                    game.state = "game"
                
                if event.key == pygame.K_ESCAPE:
                    game.state = "menu"

    game.update()
    game.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()

