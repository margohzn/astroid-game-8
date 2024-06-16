import pygame
import random
import math 

pygame.init()

screen_width = 800 
screen_height = 800 
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Hit the astroid game!")


clock = pygame.time.Clock()

# loading images
bg_img = pygame.image.load("images/starbg.png")
alien_img = pygame.image.load("images/alienShip.png")
player_rocket = pygame.image.load("images/spaceRocket.png")
star_img = pygame.image.load("images/star.png")
asteroid50 = pygame.image.load("images/asteroid50.png")
asteroid100 = pygame.image.load("images/asteroid100.png")
asteroid150 = pygame.image.load("images/asteroid150.png")

# loading sound
shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
bangSmall_sound = pygame.mixer.Sound("sound/bangSmall.wav")
bangLarge_sound = pygame.mixer.Sound("sound/bangLarge.wav")

shoot_sound.set_volume(0.25)
bangSmall_sound.set_volume(0.25)
bangLarge_sound.set_volume(0.25)


game_over = False
lives = 5 
score = 0 
rapid_fire = False # cannot press fire button non stop
rf_start = -1
is_sound_on = True 
count =0 
high_score = 0
run = True


player_bullets = []
asteroids = []
stars = []
aliens = []
alien_bullets = [] 

class Player(object):
    def __init__(self):
        self.img = player_rocket
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = screen_width // 2
        self.y = screen_height // 2 
        self.angle = 0 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rotated_rect)

    def turn_left(self):
        self.angle += 5 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def turn_right(self):
        self.angle -= 5 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def move_farward(self):
        self.x += self.cosin * 6
        self.y -= self.sine * 6
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def update_location(self):
        if self.x > screen_width + 50:
            self.x = 0 
        elif self.x < 0 - self.width:
            self.x = screen_width
        elif self.y > screen_height + 50:
            self.y = 0
        elif self.y < -50:
            self.y = screen_height
    


class Bullets(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.width, self.height = 4,4
        self.c = player.cosin
        self.s = player.sine
        self.vx = self.c * 10 
        self.vy = self.c * 10 

    def move(self):
        self.x += self.vx 
        self.y -= self.vy 

    def draw():
        pygame.draw.rect(screen, (255,255,255), [self.x, self.y, self.width, self.height])

    def check_offscreen(self):
        if self.x < -50 or self.x > screen_width or self.y < -50 or self.y > screen_height:
            return True 
        
class Astroids(object):
    def __init__(self, rank):
        self.rank = rank 
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.width = 50 * rank 
        self.height = 50 * rank 
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width // 2:
            self.xdir = 1 
        else:
            self.xdir = -1

        if self.y < screen_height // 2:
            self.ydir = 1 
        else:
            self.ydir = -1

        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)

    
class Star(object):
    def __init__(self):
        self.image = star_img 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height:
            self.ydir = 1 
        else:
            self.ydir = -1 

        self.vx = self.x * random.randrange(1,3)
        self.vy = self.y * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)



class Alien(object):
    def __init__(self):
        self.image = alien_img 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height:
            self.ydir = 1 
        else:
            self.ydir = -1 

        self.vx = self.x * random.randrange(1,3)
        self.vy = self.y * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)


class AlienBullet(object):
    def __init__(self, x,y):
        self.x = x 
        self.y = y 
        self.width = 4
        self.height = 4 
        self.dirx, self.diry = player.x - self.x, player.y - self.y 
        self.dist = math.hypot(self.dirx, self.diry)
        self.dx, self.dy = self.dirx/self.dist, self.diry/self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5 

    def draw(self, screen):
        pygame.draw.rect(screen, "pink", [self.x,self.y,self.width,self.height])


def redraw_game_window():
    screen.blit(bg_img, (0,0))
    font = pygame.font.SysFont("arial", 30)
    lives_text = font.render("Lives: " + str(lives), 1, (255,255,255))
    play_again_text = font.render("Press tab to play again", 1, (255,255,255))
    score_text = font.render("Score: " + str(score), 1, (255,255,255))
    high_score_text = font.render("High Score: " + str(high_score), 1, (255,255,255))

    player.draw(screen)

    for a in asteroids:
        a.draw(screen)

    for b in player_bullets:
        b.draw(screen)

    for s in stars:
        s.draw(screen)

    for i in aliens:
        i.draw(screen)

    for b in alien_bullets:
        b.draw(screen)

    if rapid_fire:
        pygame.draw.rect(screen, (0,0,0), [screen_width // 2 - 51 ,19,102,22])
        pygame.draw.rect(screen, (255,255,255), [screen_width //2 - 50, 20, 100 - 100 *(count-rf_start) / 500, 20])

    if game_over:
        screen.blit(play_again_text, (screen_width//2 - play_again_text.get_width() // 2, screen_height//2 - play_again_text.get_height()//2))

    screen.blit(lives_text, (25,25))
    screen.blit(score_text, (screen_width//2 - score_text.get_width() -25,  25))
    screen.blit(high_score_text, (screen_width - high_score_text.get_width()- 25, 35 + score_text.get_height()))
    pygame.display.update()


player = Player()

while run:
    clock.tick(60)
    count += 1 

    if not game_over:
        if count % 50 == 0:
            r = random.choice([1,1,1,2,2,3])
            asteroids.append(Astroids(r))
        
        if count % 1000 == 0:
            stars.append(Star())
        
        if count % 750 == 0:
            aliens.append(Alien())

        for i,a in enumerate(aliens):
            a.x += a.vx 
            a.y += a.vy
            if a.x > screen_width + 150 or a.x + a.width < -100 or a.y > screen_height + 150 or a.y + a.height < -100:
                aliens.pop(i)
            #creating alien bullets 
            if count % 60 == 0:
                alien_bullets.append(AlienBullet(a.x + a.width // 2, a.y + a.height // 2))
            
            for b in player_bullets:
                if (b.x >= a.x and b.x <= a.x + a.width) or (b.x + b.width >= a.x and b.x + b.width <= a.x + a.width):
                    if (b.y >= a.y and b.y <= a.y + a.height) or (b.y + b.height >= a.y and b.y + b.height <= a.y + a.height):
                        aliens.pop(i)
                        if is_sound_on:
                            bangLarge_sound.play()
                        score += 100
                        break
            
        for i,b in enumerate(alien_bullets):
            b.x += b.xv 
            b.y += b.yv
            if (b.x >= player.x - player.width // 2 and b.x <= player.x + player.width // 2) or (b.x + b.width >= player.x - player.width // 2 and b.x + b.width <= player.x + player.width // 2):
                if (b.y >= player.y - player.height // 2 and b.y <= player.y + player.height // 2) or (b.y + b.height >= player.y - player.height // 2 and b.y + b.height <= player.y + player.height // 2 ):
                    lives -= 1 
                    alien_bullets.pop(i)
                    break
            
        player.update_location()


        for b in player_bullets:
            b.move()
            if b.check_offscreen():
                player_bullets.pop(player_bullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv 
            if (a.x >= player.x - player.width // 2 and a.x <= player.x + player.width // 2) or (a.x + a.width >= player.x - player.width // 2 and a.x + a.width <= player.x + player.width // 2):
                if (a.y >= player.y - player.height // 2 and a.y <= player.y + player.height // 2) or (a.y + a.height >= player.y - player.height // 2 and a.y + a.height <= player.y + player.height // 2 ):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if is_sound_on:
                        bangLarge_sound.play()
                    break

            for b in player_bullets:
                if (a.x >= b.x - b.width // 2 and a.x <= b.x + b.width // 2) or (a.x + a.width >= b.x - b.width // 2 and a.x + a.width <= b.x + b.width // 2):
                    if (a.y >= b.y - b.height // 2 and a.y <= b.y + b.height // 2) or (a.y + a.height >= b.y - b.height // 2 and a.y + a.height <= b.y + b.height // 2 ):
                        if a.rank == 3:
                            if is_sound_on:
                                bangLarge_sound.play()
                            score += 15

                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x 
                            na2.x = a.x 
                            na1.y = a.y
                            na2.y = a.y

                            asteroids.append(na1)
                            asteroids.append(na2)

                        elif a.rank == 2:
                            if is_sound_on:
                                bangLarge_sound.play()
                            score += 10

                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x 
                            na2.x = a.x 
                            na1.y = a.y
                            na2.y = a.y

                            asteroids.append(na1)
                            asteroids.append(na2)

                        else:
                            score += 5
                            if is_sound_on:
                                bangLarge_sound.play()
                        asteroids.pop(asteroids.index(a))
                        player_bullets.pop(player_bullets.index(b))
                        break
        for s in stars:
            s.x += s.vx 
            s.y += s.vy

            if s.x < -100 - s.width or s.x > screen_width + 100 or s.y > screen_height + 100 or s.y < -100 - s.height:
                stars.pop(stars.index(s))
                break

            for b in player_bullets:
                if (b.x >= s.x - s.width // 2 and b.x <= s.x + s.width // 2) or (b.x + b.width >= s.x - s.width // 2 and b.x + b.width <= b.x + b.width // 2):
                    if (b.y >= s.y - s.height // 2 and b.y <= s.y + s.height // 2) or (b.y + b.height >= s.y - s.height // 2 and b.y + b.height <= s.y + s.height // 2 ):
                        rapid_fire = True 
                        rf_start = count 
                        stars.pop(stars.index(s))
                        player_bullets.pop(player_bullets.index(b))
                        break
            
        if lives <= 0:
            game_over = True 
        
        if rf_start != -1:
            if count - rf_start > 500:
                rapid_fire = False
                rf_start = -1
                

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.turn_left()
        if keys[pygame.K_RIGHT]:
            player.turn_right()
        if keys[pygame.K_UP]:
            player.move_farward()
        if keys[pygame.K_SPACE]:
            if rapid_fire:
                player_bullets.append(Bullets())
                if is_sound_on:
                    shoot_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    if not rapid_fire:
                        player_bullets.append(Bullets())
                        if is_sound_on:
                            shoot_sound.play()
            if event.key == pygame.K_m:
                is_sound_on = not is_sound_on
            if event.key == pygame.K_TAB:
                if game_over:
                    game_over = False
                    lives = 3
                    if score > high_score:
                        high_score = score
                    score = 0 
                    asteroids.clear()
                    aliens.clear()
                    alien_bullets.clear()
                    player_bullets.clear()
                    stars.clear()
    redraw_game_window()


pygame.quit()