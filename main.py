import pygame
import sys
from random import random, choice


#from <tvojeMeno> import <tvojeMeno>
from Hrac import Hrac

pygame.init()

Player1 = None #ak je tu None, tak palku ovladas pomocou W, S alebo ↑, ↓. ak chces aby palku ovladal program napis tu <tvojeMeno>("left")
Player2 = Hrac("right")

#hra sa bude simulovat v nastaveniach ake su tu
#ak si chces nieco zmenit, tak daj pozor aby ti vsetko fungovalo aj pre povodne nastavenia.

WIDTH = 1080
HEIGHT = WIDTH //3 * 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 30)
LIME = (102, 156, 92) #Toto je farba pozadia, ak sit o chces zmenit na GREY, tak prepis 158. riadok na win.fill(GREY)

PADDLE_WIDTH, PADDLE_HEIGHT = (WIDTH//32, HEIGHT//5)
BALL_RADIUS = WIDTH//80
VEL_INC = 0.13

FPS = 60
MAX_SCORE = 3

SCORE_FONT = pygame.font.SysFont("comicsans", HEIGHT//20)
WINNER_FONT = pygame.font.SysFont("comicsans", HEIGHT//10)

class Paddle:
    VEL = 5
    
    def __init__(self, x, y, width, height, player = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.color = WHITE
        self.player = player
    
    def reset(self):
        self.y = HEIGHT//2 - PADDLE_HEIGHT//2
    
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height)
        )
        pygame.draw.circle(win, LIME, (self.x + self.width//2, self.y + self.height//2), self.width//5)
        
    def move(self, up = "True"):
        if up and self.y > 0: #dont cross the boundary
            self.y -= self.VEL
        
        if not up and self.y + self.height < HEIGHT:
            self.y += self.VEL

class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        
        self.x_vel = (0.5 + random()/2) * self.MAX_VEL
        self.y_vel = ( self.MAX_VEL**2 - self.x_vel**2 )**0.5
        
        self.x_vel *= choice((-1, 1))
    
    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        
        self.MAX_VEL = 5
        
        self.x_vel = (0.5 + random()/2) * self.MAX_VEL
        self.y_vel = ( self.MAX_VEL**2 - self.x_vel**2 )**0.5
        
        self.x_vel *= choice((-1, 1))
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(win, LIME, (self.x, self.y), self.radius//3)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
def paddle_movement(keys, left_paddle, right_paddle, ball):
    ball_info = (ball.x, ball.y, ball.MAX_VEL, ball.x_vel, ball.y_vel)
    left_paddle_info = (left_paddle.x, left_paddle.y)
    right_paddle_info = (right_paddle.x, right_paddle.y)
    
    if left_paddle.player:
        left_player = left_paddle.player.make_move(ball_info, left_paddle_info, right_paddle_info)
        left_paddle.move(up = left_player)
    else:
        if keys[pygame.K_w]: left_paddle.move(up = True)
        if keys[pygame.K_s]: left_paddle.move(up = False)
    
    if right_paddle.player:
        right_player = right_paddle.player.make_move(ball_info, left_paddle_info, right_paddle_info)
        right_paddle.move(up = right_player)
    else:
        if keys[pygame.K_UP]: right_paddle.move(up = True)
        if keys[pygame.K_DOWN]: right_paddle.move(up = False)

def handle_collisions(ball, left_paddle, right_paddle):
    collided = False
    if (ball.y + ball.radius > HEIGHT and ball.y_vel > 0) or (ball.y - ball.radius < 0 and ball.y_vel < 0):
        ball.y_vel *= -1
        collided = True
    
    if ball.x_vel < 0: #left paddle
        if ball.y - ball.radius <= left_paddle.y + left_paddle.height and ball.y + ball.radius >= left_paddle.y:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                
                ball.MAX_VEL += VEL_INC #increase speed
                
                dx = left_paddle.width//2 + ball.radius #vec of next ball's direction
                dy = ball.y - (left_paddle.y + left_paddle.height//2)
                
                denominator = abs(dx) + abs(dy)
                ball.x_vel = ball.MAX_VEL * dx / denominator
                ball.y_vel = ball.MAX_VEL * dy / denominator
                
                collided = True
                    
    elif ball.x_vel > 0: #right paddle
        if ball.y - ball.radius <= right_paddle.y + right_paddle.height and ball.y + ball.radius >= right_paddle.y:
            if ball.x + ball.radius >= right_paddle.x:
                
                ball.MAX_VEL += VEL_INC
                
                dx = - (right_paddle.width//2 + ball.radius)
                dy = ball.y - (right_paddle.y + right_paddle.height//2)
                
                denominator = abs(dx) + abs(dy)
                ball.x_vel = ball.MAX_VEL * dx / denominator
                ball.y_vel = ball.MAX_VEL * dy / denominator
                
                collided = True
    
    if collided:
        ball.MAX_VEL = round(max(10, ball.MAX_VEL + VEL_INC), 2)

def draw(win, paddles, ball, left_score, right_score):
    win.fill(LIME)
    
    left_paddle, right_paddle = paddles
    if left_paddle.player: left_name = left_paddle.player.name
    else: left_name = "Player 1"
    if right_paddle.player: right_name = right_paddle.player.name
    else: right_name = "Player 2"
    
    left_name_text = SCORE_FONT.render(left_name, 1, WHITE)
    right_name_text = SCORE_FONT.render(right_name, 1, WHITE)
    left_score_text = SCORE_FONT.render(str(left_score), 1, WHITE)
    right_score_text = SCORE_FONT.render(str(right_score), 1, WHITE)
    
    win.blit(
        left_name_text, (WIDTH//4 - left_name_text.get_width()//2, HEIGHT//4 - left_name_text.get_height()//2 - left_score_text.get_height() )
    )
    win.blit(
        right_name_text, (3*WIDTH//4 - right_name_text.get_width()//2, HEIGHT//4 - right_name_text.get_height()//2 - right_score_text.get_height() )
    )
    win.blit(
        left_score_text, (WIDTH//4 - left_score_text.get_width()//2, HEIGHT//2 - left_score_text.get_height()//2)
    )
    win.blit(
        right_score_text, (3*WIDTH//4 - right_score_text.get_width()//2, HEIGHT//2 - right_score_text.get_height()//2)
    )
    
    for paddle in paddles: #updating position of paddles on screen
        paddle.draw(win)
    
    for i in range(10, HEIGHT, HEIGHT//20): #dashed line in the middle
        if i%2:
            continue
        pygame.draw.rect(
            win, WHITE, (WIDTH//2 - 3, i, 6, HEIGHT//40)
        )
    
    ball.draw(win)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(
        PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, Player1
    )
    right_paddle = Paddle(
        WIDTH - PADDLE_WIDTH*2, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, Player2
    )
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    
    left_score, right_score = 0, 0
    
    while run:
        clock.tick(FPS)
        
        draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
        keys = pygame.key.get_pressed() #get map of keys
        paddle_movement(keys, left_paddle, right_paddle, ball)
        
        ball.move()
        handle_collisions(ball, left_paddle, right_paddle)

        if ball.x < 0: #left paddle missed
            right_score += 1
            ball.reset()
            left_paddle.reset()
        
        if ball.x > WIDTH: #right paddle missed
            left_score += 1
            ball.reset()
            right_paddle.reset()

        if MAX_SCORE in (left_score, right_score):
            run = False
            break
    
    WIN.fill(GREY)
    winner = left_paddle if left_score == MAX_SCORE else right_paddle
    if winner.player: winner = winner.player.name
    else: winner = "Player"
        
    while MAX_SCORE in (left_score, right_score):
        clock.tick(FPS)
        
        message = WINNER_FONT.render(f"{winner} has won: {left_score}-{right_score}", 1, WHITE)
        WIN.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - message.get_height()//2))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()