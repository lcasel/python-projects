import random
import pygame
import asset

# Initialize Pygame or Shutdown
pygame.init()
assert pygame.get_init()

# Game Constants
GAME_NAME = 'PONG'
GAME_VERSION = '1.0.0'
GAME_FPS = 60
GAME_FONT = pygame.font.SysFont('Terminal', 128)
# STATES ARE: 'EXITING': 0, 'RUNNING': 1, 'PAUSED': 2

class Game:

    def __init__(self, p_window_size, p_fps=GAME_FPS):

        self.GAME_window_size = p_window_size
        self.GAME_state = 0
        self.GAME_score = [0, 0]
        self.GAME_fps = p_fps

    def init(self):
        
        # GAME Window
        self.GAME_window = pygame.display.set_mode(self.GAME_window_size)
        pygame.display.set_caption(GAME_NAME + ' - ' + GAME_VERSION)

        # GAME Background
        self.GAME_background = pygame.Surface(self.GAME_window.get_size())
        self.GAME_background.fill((127, 127, 127))
        self.GAME_window.blit(self.GAME_background, (0, 0))

        # GAME Pause Screen
        self.GAME_pause_rect = pygame.Rect((0, 0), self.GAME_window_size)
        self.GAME_pause_screen = pygame.Surface(self.GAME_window_size, pygame.SRCALPHA)
        pygame.draw.rect(self.GAME_pause_screen, (0, 0, 0, 127), self.GAME_pause_rect)

        temp_pause_text = GAME_FONT.render('PAUSED', True, 'white')
        self.GAME_pause_screen.blit(temp_pause_text, temp_pause_text.get_rect(center=(320, 240)))

        # GAME Scoreboard
        self.GAME_scoreboard_1 = pygame.Surface((0, 0))
        self.GAME_scoreboard_2 = pygame.Surface((0, 0))

        # GAME Assets
        self.GAME_paddle_1 = asset.Paddle(40, 240)
        self.GAME_paddle_2 = asset.PaddleAI(600, 240)
        self.GAME_ball = asset.Ball(320, 240)
        self.GAME_ball.velocity.xy = (random.choice([-8, 8]), 0)

        if self.GAME_state == 0:
            self.GAME_state = 1

    def update(self):

        speed_mod = 1.0
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.GAME_paddle_1.move(-1)

        if keys[pygame.K_DOWN]:
            self.GAME_paddle_1.move(1)

        if keys[pygame.K_SPACE]:
            speed_mod = 0.5

        if self.GAME_ball.bounds.colliderect(self.GAME_paddle_1.bounds):
            self.GAME_ball.deflect(asset.specific_angle_deflect(self.GAME_paddle_1, self.GAME_ball))
            if keys[pygame.K_s]:
                self.GAME_ball.velocity *= 1.1

        if self.GAME_ball.bounds.colliderect(self.GAME_paddle_2.bounds):
            self.GAME_ball.deflect(asset.specific_angle_deflect(self.GAME_paddle_2, self.GAME_ball))

        # Score Rules
        if self.GAME_score[0] == 3:
            print('GAME OVER')
            self.GAME_state = 0


        # Score Collision
        if self.GAME_ball.bounds.x <= 0:
            self.GAME_score[0] += 1

        if self.GAME_ball.bounds.x + self.GAME_ball.bounds.w >= self.GAME_window_size[0]:
            self.GAME_score[1] += 1

        # Ball Collision
        col_x = (self.GAME_ball.bounds.x + self.GAME_ball.bounds.w >= self.GAME_window_size[0]) or (self.GAME_ball.bounds.x <= 0)
        col_y = (self.GAME_ball.bounds.y + self.GAME_ball.bounds.h >= self.GAME_window_size[1]) or (self.GAME_ball.bounds.y <= 0)
        if col_x:
            self.GAME_ball.reflect(True, False)
        if col_y:
            self.GAME_ball.reflect(False, True)

        self.GAME_ball.update(speed_mod)
        self.GAME_paddle_2.update(self.GAME_ball)

    def run(self):

        # Initialize
        self.init()

        t_Gsb_rect1 = self.GAME_scoreboard_1.get_rect(center=(160, 60))
        t_Gsb_rect2 = self.GAME_scoreboard_2.get_rect(center=(480, 60))

        # Time
        self.GAME_clock = pygame.time.Clock()
        
        # Game Loop
        while (self.GAME_state == 1 or self.GAME_state == 2):

            # Cycle through events
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.GAME_state == 1:
                            self.GAME_state = 2
                        elif self.GAME_state == 2:
                            self.GAME_state = 1

                if event.type == pygame.QUIT:
                    self.GAME_state = 0

            # RENDER CLEAR
            self.GAME_window.blit(self.GAME_background, t_Gsb_rect1, t_Gsb_rect1)
            self.GAME_window.blit(self.GAME_background, t_Gsb_rect2, t_Gsb_rect2)
            self.GAME_window.blit(self.GAME_background, self.GAME_paddle_1.bounds, self.GAME_paddle_1.bounds)
            self.GAME_window.blit(self.GAME_background, self.GAME_paddle_2.bounds, self.GAME_paddle_2.bounds)
            self.GAME_window.blit(self.GAME_background, self.GAME_ball.bounds, self.GAME_ball.bounds)
            self.GAME_window.blit(self.GAME_background, self.GAME_pause_rect, self.GAME_pause_rect)

            # UPDATE
            if self.GAME_state != 2:
                self.update()
            
            # RENDER UPDATE
            self.GAME_scoreboard_1 = GAME_FONT.render(str(self.GAME_score[0]), True, 'lightblue')
            t_Gsb_rect1 = self.GAME_scoreboard_1.get_rect(center=(160, 60))

            self.GAME_scoreboard_2 = GAME_FONT.render(str(self.GAME_score[1]), True, 'lightblue')
            t_Gsb_rect2 = self.GAME_scoreboard_2.get_rect(center=(480, 60))

            self.GAME_window.blit(self.GAME_scoreboard_1, t_Gsb_rect1)
            self.GAME_window.blit(self.GAME_scoreboard_2, t_Gsb_rect2)

            draw_net(self.GAME_window, self.GAME_window_size)

            pygame.draw.rect(self.GAME_window, 'red', self.GAME_paddle_1.bounds)
            pygame.draw.rect(self.GAME_window, 'blue', self.GAME_paddle_2.bounds)
            self.GAME_ball.bounds = pygame.draw.circle(self.GAME_window, 'green', self.GAME_ball.bounds.center, self.GAME_ball.radius)

            if self.GAME_state == 2:
                self.GAME_window.blit(self.GAME_pause_screen, self.GAME_pause_rect)

            pygame.display.update()
            
            self.GAME_clock.tick(60)


def draw_net(surface, size, color='white'):

    divide = 20
    part = size[1]/divide
    w = 16
    h = 48
    w *= (8 / divide)
    h *= (8 / divide)

    for i in range(divide + 1):

        cy_pos = part * i
        cx_pos = size[0]/2

        t_rect = pygame.Rect(0, 0, w, h)
        t_rect.center = (cx_pos, cy_pos)
        pygame.draw.rect(surface, color, t_rect)
