import pygame
import random
import math


def get_angle_by_catan(a, b):
    if b == 0:
        if a > 0:
            angle = 90
        else:
            angle = -90
    else:
        angle = math.atan(a / b) / math.pi * 180
        if b < 0:
            angle += 180
    return angle


class Game():
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 60

    BLACK = (0, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shoot!")

    bg_surf = pygame.image.load('images/bg.png').convert_alpha()
    bg_surf = pygame.transform.scale(bg_surf, (WIDTH, HEIGHT))

    ui_surf = pygame.image.load('images/buttonBlue.png').convert_alpha()
    ui_rect = ui_surf.get_rect()

    clock = pygame.time.Clock()

    speed_shoot = 2

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    players = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    enumy_bullets = pygame.sprite.Group()

    pygame.time.set_timer(pygame.USEREVENT, 5000)
    TIME_TO_DMG = pygame.USEREVENT + 1

    TIME_TO_BOSS = pygame.USEREVENT + 2
    pygame.time.set_timer(TIME_TO_BOSS, 5000, loops=1)

    TIME_TO_SHOOT = pygame.USEREVENT + 3

    TIME_TO_EXTRA_BULLET = pygame.USEREVENT + 4

    boost_damage = ['boost_damage', 'images/powerupBlue_bolt.png']
    extra_bullets = ['extra_bullets', 'images/powerupBlue_star.png']
    boost_Templates = [boost_damage, extra_bullets]

    def start_init(self):
        global player, score, text, font, textpos

        player = Player()
        my_game.all_sprites.add(player)
        my_game.players.add(player)

        score = 0
        font = pygame.font.Font(None, 32)
        text = font.render("Набрано очков: " + str(score), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=my_game.WIDTH-120, bottom=42)


class Speed():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_rotate_speed(angle, absolute_speed):
        s = Speed(0, 10)
        s.x = math.cos(math.radians(angle + 180)) * absolute_speed
        s.y = math.sin(math.radians(angle + 180)) * absolute_speed
        return s


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'images/playerShip1_blue.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.original_image = pygame.image.load(
            'images/playerShip1_blue.png').convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (50, 50))
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = my_game.WIDTH / 2
        self.rect.bottom = my_game.HEIGHT - 30
        self.speed = Speed(0, 0)
        self.demage = 1
        self.posx = self.rect.x - self.original_image.get_size()[0]
        self.posy = self.rect.y - self.original_image.get_size()[1]
        self.shoot_interval = 20
        self.current_shootframe = 0
        self.triple = False

    def update(self):
        self.angle = get_angle_by_catan(
            self.posx - mouse_pos[0],
            self.posy - mouse_pos[1])
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.posx, self.posy))

        self.speed = Speed(0, 0)

        keystate = pygame.key.get_pressed()
        mousekeystate = pygame.mouse.get_pressed()
        if mousekeystate[0]:
            self.current_shootframe += 1 * my_game.speed_shoot
            if self.current_shootframe >= self.shoot_interval:
                player.shoot()
                self.current_shootframe = 0
        vector = [0, 0]
        if keystate[pygame.K_a]:
            vector[1] += 1
        if keystate[pygame.K_d]:
            vector[1] -= 1
        if keystate[pygame.K_w]:
            vector[0] += 1
        if keystate[pygame.K_s]:
            vector[0] -= 1
        if vector != [0, 0]:
            speed_angle = get_angle_by_catan(*vector)
            self.speed = Speed.get_rotate_speed(speed_angle, 10)

        self.posx += self.speed.x
        self.posy += self.speed.y

        if self.posx > my_game.WIDTH:
            self.posx = my_game.WIDTH
        if self.posx < 0:
            self.posx = 0
        if self.posy > my_game.HEIGHT:
            self.posy = my_game.HEIGHT
        if self.posy < 0:
            self.posy = 0

    def shoot(self):
        bullet = Ally_bullet(self.posx, self.posy, Speed.get_rotate_speed(
            self.angle, 10))
        my_game.all_sprites.add(bullet)
        my_game.bullets.add(bullet)
        if self.triple:
            bullet = Ally_bullet(self.posx,
                            self.posy,
                            Speed.get_rotate_speed(self.angle - 15, 10))
            my_game.all_sprites.add(bullet)
            my_game.bullets.add(bullet)
            bullet = Ally_bullet(self.posx,
                            self.posy,
                            Speed.get_rotate_speed(self.angle + 15, 10))
            my_game.all_sprites.add(bullet)
            my_game.bullets.add(bullet)


class Power_up(pygame.sprite.Sprite):
    def __init__(self, name, path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, my_game.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 5)
        self.speedx = random.randrange(-3, 3)
        self.name = name

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > my_game.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > my_game.WIDTH + 20:
            self.rect.x = random.randrange(0, my_game.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 5)
        if self.rect.bottom > my_game.HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, size, life, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(my_game.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = speed.x
        self.speedy = speed.y
        self.life = life
        my_game.all_sprites.add(self)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Mob(Enemy):
    def __init__(self, list_path_life):
        Enemy.__init__(
            self,
            list_path_life[0],
            (50, 50),
            list_path_life[1],
            Speed(random.randrange(-3, 3), random.randrange(1, 8)))
        my_game.mobs.add(self)

    def update(self):
        super().update()
        if self.rect.top > my_game.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > my_game.WIDTH + 20:
            self.rect.x = random.randrange(my_game.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 5)


class Heavy_mob(Mob):
    def __init__(self):
        Mob.__init__(self, ['images/enemyBlack4.png', 3])


class Medium_mob(Mob):
    def __init__(self):
        Mob.__init__(self, ['images/enemyBlack2.png', 2])


class Light_mob(Mob):
    def __init__(self):
        Mob.__init__(self, ['images/enemyBlack5.png', 1])


class Boss(Enemy):
    def __init__(self):
        Enemy.__init__(
            self,
            'images/ufoYellow.png',
            (150, 150),
            100,
            Speed(random.randrange(1, 3), 0))
        self.rect.y = 15
        my_game.bosses.add(self)

    def update(self):
        super().update()
        if self.rect.left < -25 or self.rect.right > my_game.WIDTH + 25:
            self.speedx *= -1

    def shoot(self):
        enumy_bullet = Enemy_bullet(self.rect.centerx, self.rect.top, Speed(10, 10))
        my_game.all_sprites.add(enumy_bullet)
        my_game.enumy_bullets.add(enumy_bullet)
        enumy_bullet = Enemy_bullet(
            self.rect.centerx - 30, self.rect.top, Speed(10, 10))
        my_game.all_sprites.add(enumy_bullet)
        my_game.enumy_bullets.add(enumy_bullet)
        enumy_bullet = Enemy_bullet(
            self.rect.centerx + 30, self.rect.top, Speed(10, 10))
        my_game.all_sprites.add(enumy_bullet)
        my_game.enumy_bullets.add(enumy_bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, path, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed.x
        self.speedx = speed.y

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.bottom > my_game.HEIGHT:
            self.kill()


class Ally_bullet(Bullet):
    def __init__(self, x, y, speed):
        Bullet.__init__(self, 'images/laserRed02.png', x, y, speed)


class Enemy_bullet(Bullet):
    def __init__(self, x, y, speed):
        Bullet.__init__(self, 'images/laserGreen04.png', x, y, speed)
        dx = x - player.rect.x
        dy = y - player.rect.y
        self.speedx = speed.y * (dx/dy)
        self.speedy = speed.y


my_game = Game()
my_game.start_init()

for i in range(3):
    Heavy_mob()
    Light_mob()
    Medium_mob()


mouse_pos = (0, 0)
game = True

while game:
    if score >= 1000:
        game = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.USEREVENT:
            random_power_up = random.choice(my_game.boost_Templates)
            power_up = Power_up(random_power_up[0], random_power_up[1])
            my_game.power_ups.add(power_up)
            my_game.all_sprites.add(power_up)
        if event.type == my_game.TIME_TO_DMG:
            player.demage -= 5
            print('Усиление "Допонительный урон" отменено')
        if event.type == my_game.TIME_TO_EXTRA_BULLET:
            player.triple = False
            print('Усиление "Дополнительные пули" отменено')
        if event.type == my_game.TIME_TO_BOSS:
            boss = Boss()
            pygame.time.set_timer(my_game.TIME_TO_SHOOT, 500)
        if event.type == my_game.TIME_TO_SHOOT:
            boss.shoot()

    my_game.clock.tick(my_game.FPS)
    my_game.all_sprites.update()

    hits = pygame.sprite.groupcollide(
        my_game.mobs,
        my_game.bullets,
        False,
        True)
    for mob in hits:
        mob.life -= player.demage
        if mob.life <= 0:
            mob.kill()
            score += 1
            text = font.render("score: " + str(score), 1, (10, 10, 10))
            random.choice([Heavy_mob, Medium_mob, Light_mob])()

    hits = pygame.sprite.groupcollide(
        my_game.bosses,
        my_game.bullets,
        False,
        True)
    for enemy in hits:
        print(f'У боса осталось {enemy.life} здоровья')
        enemy.life -= player.demage
        if enemy.life <= 0:
            enemy.kill()
            score += 1000
            text = font.render("score: " + str(score), 1, (10, 10, 10))
            my_game.TIME_TO_SHOOT = False

    hits = pygame.sprite.groupcollide(
        my_game.power_ups,
        my_game.players,
        True,
        False)
    if hits:
        for power_up in hits:
            if power_up.name == 'boost_damage':
                player.demage += 5
                pygame.time.set_timer(my_game.TIME_TO_DMG, 5000, loops=1)
                print('Усиление сработало')
            elif power_up.name == 'extra_bullets':
                pygame.time.set_timer(my_game.TIME_TO_EXTRA_BULLET, 5000, loops=1)
                player.triple = True

    hits = pygame.sprite.spritecollide(player, my_game.mobs, False)
    if hits:
        break

    hits = pygame.sprite.spritecollide(player, my_game.enumy_bullets, False)
    if hits:
        break

    my_game.screen.fill(my_game.BLACK)
    my_game.screen.blit(my_game.bg_surf, (0, 0))
    my_game.all_sprites.draw(my_game.screen)
    my_game.screen.blit(my_game.ui_surf, (my_game.WIDTH-230, 10))
    my_game.screen.blit(text, textpos)
    pygame.display.flip()

pygame.quit()