# Module For Pong Game Assets and Objects
import pygame

# Paddle Class
class Paddle:

    """Pong Paddle

    Default class for all pong
    paddle records and physics!
    """

    width = 16
    height = 48
    speed = 10

    def __init__(self, x_pos, y_pos):
        self.bounds = pygame.Rect(0, 0, self.width, self.height)
        self.bounds.center = (x_pos, y_pos)
    
    def move(self, y_off):
        self.bounds.move_ip(0, y_off * self.speed)


# Ball Class
class Ball:

    def __init__(self, x_pos, y_pos):
        self.radius = 8
        self.bounds = pygame.Rect(0, 0, self.radius, self.radius)
        self.bounds.center = (x_pos, y_pos)
        self.velocity = pygame.Vector2(0, 0)
    
    def update(self, mod=1.0):
        self.bounds.move_ip(self.velocity.xy * mod)

    def deflect(self, angle):
        self.velocity.from_polar((self.velocity.magnitude(), angle))

    def reflect(self, p_x=True, p_y=True):
        if p_x: self.velocity.x *= -1
        if p_y: self.velocity.y *= -1

# AI Paddle Class
class PaddleAI (Paddle):
    
    def update(self, ball:Ball):

        # Find Direction of Ball
        if ball.bounds.centery > self.bounds.centery:
            self.move(1)

        if ball.bounds.centery < self.bounds.centery:
            self.move(-1)

# Specific Angle Deflection:
# Comparts each paddle into separate hit boxes.
# Each hitbox has a different angle of deflection.
def specific_angle_deflect(paddle:Paddle, ball:Ball) -> int:

    parts = 3
    collisions = 0
    sum_angle = 0
    avg_angle = 90
    left_angles = [315, 360, 45]
    right_angles = [225, 180, 135]

    paddle_comps = []

    def compart(parts):
        
        y = paddle.bounds.y
        x = paddle.bounds.x
        w = paddle.width
        h = paddle.height / parts

        for i in range(parts):
            paddle_comps.append(pygame.Rect(x, y + i*h, w, w))
        
        print(paddle_comps)

    compart(parts)

    print(type(paddle))
    if type(paddle) == PaddleAI:
        print('AI PADDLE ALERT!!!!')

        for i in range(parts):

            if ball.bounds.colliderect(paddle_comps[i]):
                sum_angle += right_angles[i]
                collisions += 1
                print('COL! ANGLE:', right_angles[i])

        avg_angle = sum_angle / collisions

        print('SUM ANGLE:', sum_angle)
        print('COLLISIONS:', collisions)
        print('AVG ANGLE:', avg_angle)

    
    if type(paddle) == Paddle:
        print('OG PADDLE ALERT!!!!')
        
        for i in range(parts):

            if ball.bounds.colliderect(paddle_comps[i]):
                sum_angle += left_angles[i]
                collisions += 1
                print('COL! ANGLE:', left_angles[i])

        avg_angle = sum_angle / collisions

        print('SUM ANGLE:', sum_angle)
        print('COLLISIONS:', collisions)
        print('AVG ANGLE:', avg_angle)

    return avg_angle
            