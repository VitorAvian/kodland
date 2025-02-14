import pgzero.game
import pgzrun

# Game parameters
TITLE = "Astronautilas"
WIDTH = 360
HEIGHT = 360
TILE_SIZE = 18

# Game state
STATE = 'menu'

# Game variables
GRAVITY = 1
JUMP_VELOCITY = -12
RESPAWN_POINT = (TILE_SIZE*9, TILE_SIZE*19-5)

# GUI actors
start = Actor('start', center = (WIDTH // 2, HEIGHT // 2 - 20))
exit = Actor('exit', center = (WIDTH // 2, HEIGHT // 2 + 50))
sounds_on = Actor('on', center = (WIDTH // 2-50, HEIGHT // 2+125))
sounds_off = Actor('off', center = (WIDTH // 2+50, HEIGHT // 2+125))

# Sound config
sounds.aplaceicallhome.play(-1)
MUSIC = True;

class Player:
    def __init__(self, x, y):
        self.right_animation = ['playerr1', 'playerr2']
        self.left_animation = ['playerl1', 'playerl2']
        self.actor = Actor('playerr1')
        self.actor.bottomleft = (x, y)
        self.velocity_x = 3
        self.velocity_y = 0
        self.jumping = False

        self.current_frame = 0
        self.animation_timer = 0
        self.running = False
        self.flip = False

    def draw(self):
        self.actor.draw()

    def update(self):

        # Horizontal movement
        self.running = False
        if keyboard.LEFT and self.actor.midleft[0] > 0:
            self.actor.x -= self.velocity_x
            self.flip = True
            self.running = True

        elif keyboard.RIGHT and self.actor.midright[0] < WIDTH:
            self.actor.x += self.velocity_x
            self.flip = False
            self.running = True

        # Applying gravity
        self.velocity_y += GRAVITY
        self.actor.y += self.velocity_y

        # Check collision with platform
        self.jumping = False
        for platform in platforms:
            if self.actor.colliderect(platform.rect) and self.velocity_y > 0:
                self.actor.bottom = platform.rect.top
                self.velocity_y = 0
                self.jumping = True

        # Jumping
        if (keyboard.SPACE or keyboard.UP) and self.jumping:
            self.velocity_y = JUMP_VELOCITY
            if MUSIC:
                sounds.jump.play()

        # Check collision with enemies and respawn
        for enemy in enemies:
            if self.actor.colliderect(enemy.actor):
                if MUSIC:
                    sounds.hurt.play()
                self.respawn()

        # Respawn if falling off the screen
        if self.actor.y > HEIGHT:
            self.respawn()

        # Update animation frames
        self.animation_timer += 1
        if self.animation_timer % 15 == 0:
            self.current_frame = (self.current_frame + 1) % (len(self.right_animation))

        # Choose animation direction
        if self.running:
            if self.flip:
                self.actor.image = self.left_animation[self.current_frame]
            else:
                self.actor.image = self.right_animation[self.current_frame]

    def respawn(self):
        self.actor.bottomleft = RESPAWN_POINT
        self.velocity_y = 0


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def draw(self):
        screen.draw.filled_rect(self.rect, "lightblue")

class Enemy:
    def __init__(self, x, y, velocity_x, range_start, range_end):
        self.animation = ['enemy1', 'enemy2', 'enemy3']
        self.actor = Actor('enemy1')
        self.actor.bottomleft = (x, y)
        self.velocity_x = velocity_x
        self.range_start = range_start
        self.range_end = range_end

        self.current_frame = 0
        self.animation_timer = 0

    def draw(self):
        self.actor.draw()

    def update(self):

        # Horizontal movement
        self.actor.x += self.velocity_x

        # Moving back and forth
        if self.actor.x < self.range_start or self.actor.x > self.range_end:
            self.velocity_x *= -1

        # Update animation frames
        self.animation_timer += 1
        if self.animation_timer % 20 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.animation)
            self.actor.image = self.animation[self.current_frame]
        
player = Player(*RESPAWN_POINT)

platforms = [
    Platform(50, 340, 260, 20),
    Platform(50, 270, 80, 20),
    Platform(240, 270, 80, 20), #enemy
    Platform(140, 200, 80, 20), #enemy
    Platform(50, 130, 80, 20), #enemy
    Platform(240, 130, 80, 20), #enemy
    Platform(140, 60, 80, 20),
]

enemies = [
    Enemy(240, 260, 2, 240, 320),
    Enemy(140, 190, 1, 140, 220),
    Enemy(50, 120, 3, 50, 130),
    Enemy(300, 120, 2, 240, 320),
]

def draw():
    global STATE
    screen.clear()

    if STATE == 'menu':
        draw_menu()

    elif STATE == 'game':
        draw_game()

def update():
    global STATE
    if STATE == 'game':
        player.update()
        for enemy in enemies:
            enemy.update()

def draw_menu():
    screen.fill("lightblue")
    screen.draw.text(
        "Astronautilas", 
        (45, 35), 
        fontname="barriecito", 
        fontsize=50, 
        color = 'black'
        )
    start.draw()
    exit.draw()
    sounds_on.draw()
    sounds_off.draw()

def draw_game():
    screen.fill("darkblue")
    for platform in platforms:
        platform.draw()

    for enemy in enemies:
        enemy.draw()

    player.draw()

def on_mouse_down(button,pos):
    global STATE
    global MUSIC
    if start.collidepoint(pos):
        STATE='game'
    if exit.collidepoint(pos):
        pgzero.game.exit()
    if sounds_off.collidepoint(pos):
        MUSIC = False
        sounds.aplaceicallhome.stop()
    if sounds_on.collidepoint(pos):
        MUSIC = True
        sounds.aplaceicallhome.play(-1)

pgzrun.go()