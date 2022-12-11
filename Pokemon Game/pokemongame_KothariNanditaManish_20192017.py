import pygame
import random
from os import path

WIDTH = 794
HEIGHT = 600
FPS = 60

#define colors

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# set up assets (art and sound)

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
pokemon_folder = path.join(img_folder,"pokemons")
snd_folder = path.join(game_folder,'snd')

#initialize pygame and create window
pygame.init()

#if you want sound
pygame.mixer.init()

#creating the screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup!")

clock = pygame.time.Clock()

font_name = pygame.font.match_font('Times New Roman')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shieldbar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_begin_screen():
    screen.blit(background,background_rect)
    draw_text(screen, "POKÉMON", 60, WIDTH/2, HEIGHT/3, WHITE)
    draw_text(screen, "Use Arrow Keys to move & Spacebar release pokéballs", 25, WIDTH/2, HEIGHT/3 + 70, WHITE)
    draw_text(screen, "Press any key to begin", 20, WIDTH/2, HEIGHT - 50, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_go_screen():
    screen.blit(background,background_rect)
    draw_text(screen, "YOU ARE DEAD", 60, WIDTH/2, HEIGHT/3, RED)
    #draw_text(screen, "Arrow Keys move, Space to fire", 25, WIDTH/2,HEIGHT - 100)
    draw_text(screen, "Press any key to begin again", 30, WIDTH/2, HEIGHT - 50, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

#graphic assets
player_img = pygame.image.load(path.join(img_folder, "ash.png")).convert_alpha()
pokeball_img = pygame.image.load(path.join(img_folder, "pokeball.png")).convert_alpha()
pokemon_images = []

for i in range(1,152):
    pokemon = pygame.image.load(path.join(pokemon_folder, str(i) + ' Background Removed.png')).convert_alpha()
    pokemon_images.append(pokemon)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['sm'].append(img_sm)


#Load game sounds
throw_sound = pygame.mixer.Sound(path.join(snd_folder, 'throw.ogg'))
capture_sound = pygame.mixer.Sound(path.join(snd_folder, "pikachu.ogg"))
dead_sound = pygame.mixer.Sound(path.join(snd_folder, "dead.ogg"))
ouch_sound = pygame.mixer.Sound(path.join(snd_folder, "Ouch.ogg"))

#make a player class that has the attributes and functions of the player sprite
class Player(pygame.sprite.Sprite):
    #sprite for the player

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #every sprite needs to have
        self.image = pygame.transform.scale(player_img, (100,100))
        #self.image.set_colorkey(BLACK) 
        #every object has a rectangle and it helps to give cordinates to the objects
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()



    def update(self):
        #evertime the gameloop repeats and does the update section,
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        
        #constraining the sprite inside the walls of the window
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            throw_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #every sprite needs to have
        self.image_orig = random.choice(pokemon_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width +10, self.rect.height + 10))
        #self.image = pygame.transform.scale((random.choice(pokemon_images)),(60,60))
        #removing background color
        #every object has a rectangle and it helps to give cordinates to the objects
        
        self.radius = int(self.rect.width *0.85/2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,4)
        self.speedx = random.randrange(-1,2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #if it goes below the screen, it will be randomly placed on top again
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,4)
            self.speedx = random.randrange(-1,2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #every sprite needs to have
        self.image = pygame.transform.scale(pokeball_img, (35,35))
        self.radius = 17
        #removing background color
        #every object has a rectangle and it helps to give cordinates to the objects
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5
    
    def update(self):
        self.rect.y += self.speedy
       
       #kill it if it moves of the screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#making a group of sprites to make the code more efficient
#we will put all the sprites in this group
all_sprites = pygame.sprite.Group()
player = Player()

#create a seperate group of mobs
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#add the sprite to the allsprites group

#Load all game graphics
background = pygame.image.load(path.join(img_folder, "pokemonworld.png")).convert()
background_rect = background.get_rect()
pygame.mixer.music.load(path.join(snd_folder, "bgm.ogg"))
pygame.mixer.music.set_volume (0.5)
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()

all_sprites.add(player)

for i in range(8):
    newmob()

score = 0

#Game loop
game_begin = True
game_over = False
running = True

while running:
    if game_begin:
        show_begin_screen()
        game_begin = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        
        score = 0

    #keep running at the right speed
    clock.tick(FPS)

    # Process input/events -> can go in aat any time of the process
    for event in pygame.event.get():
        #check closing for window
        if event.type == pygame.QUIT:
            running = False
        

    # update --> tell it what to do with the sprites - where to move, etc.
    all_sprites.update()

    #false or true helps you decided whether to remove that sprite or not
    #false = does not delete
  
    #check to see if a bullet kits a mob
    mob_hits = pygame.sprite.groupcollide(mobs,bullets, True, True, pygame.sprite.collide_circle)
    #True means if its True, they will be deleted

    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs, True, pygame.sprite.collide_circle) 


    for hit in mob_hits:
        capture_sound.play()
        score += 25 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

        if score >= 100:
            m.speedy = random.randrange(5,8)
            
        if score >= 300:
            m.speedy = random.randrange(8,10)
        


    #if the player gets hit by a mob, the game ends
    for hit in hits:
        ouch_sound.play()
        player.shield -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        
        if player.shield <= 0:
            dead_sound.play()
            death_expl = Explosion(player.rect.center, 'lg')
            all_sprites.add(death_expl)
            player.kill()
            #draw_text(screen, "YOU GOT EATEN BY A POKEMON", 50, WIDTH/2, HEIGHT/2)
            
    #if the player dies and the explosion has finished playing
    if not player.alive() and not death_expl.alive():   
        show_go_screen()
        game_over = True
        all_sprites = pygame.sprite.Group()
        player = Player()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        
        score = 0
        
    
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_text(screen, str(score), 35, WIDTH - 30, 20, WHITE)

    draw_shieldbar(screen,5,5,player.shield)
    #flip the imaginary back side to show to the viewer
    #always flip AFTER drawing everything
    pygame.display.flip() 

pygame.quit()