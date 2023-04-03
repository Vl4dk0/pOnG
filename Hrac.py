from random import randint
#0, 0 je lavy horny roh

'''
takto sa v programe simuluje smer po odraze lopticky od palky

dx = paddle.width//2 + ball.radius #vec of next ball's direction
dy = ball.y - (paddle.y + paddle.height//2)

denominator = abs(dx) + abs(dy)
ball.x_vel = ball.MAX_VEL * dx / denominator
ball.y_vel = ball.MAX_VEL * dy / denominator
'''

WIDTH = 1080
HEIGHT = 1080 //3 * 2
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = (WIDTH//32, HEIGHT//5)
BALL_RADIUS = WIDTH//80
PADDLE_VEL = 5

VEL_INC = 0.13

class Hrac:
    def __init__(self, side):
        self.name = "Hrac" #toto si vyber sam
        self.side = side #"left" alebo "right", strana na ktorej si
        
        #tu mozes pridat nejake svoje premene
        self.x = None
        self.y = None
        
        self.opp_x = None
        self.opp_y = None
            
        self.current_target = HEIGHT - PADDLE_HEIGHT//2
        self.next_target = PADDLE_HEIGHT//2

    #sem si mozes pridat nejake svoje funkcie

    def get_target(self):
        self.current_target, self.next_target = self.next_target, self.current_target

    #hlavna funkcia
    def make_move(self, ball_info, left_paddle_info, right_paddle_info):
        ball_x, ball_y, ball_max_vel, x_vel, y_vel = ball_info #x, y su suradnice stredu. 
                                                               #x_vel, y_vel su vektory rychlosti v danych smeroch
        left_x, left_y = left_paddle_info #x, y su lave horne rohy paliek
        right_x, right_y = right_paddle_info
        
        #toto je len ukazka, kod nizsie sluzi len na pochopenie returnovania.
        
        if self.side == "left":
            self.x, self.y = left_x + PADDLE_WIDTH//2, left_y + PADDLE_HEIGHT//2
            self.opp_x, self.opp_y = right_x + PADDLE_WIDTH//2, right_y + PADDLE_HEIGHT//2
            
        else:
            self.x, self.y = right_x + PADDLE_WIDTH//2, right_y + PADDLE_HEIGHT//2
            self.opp_x, self.opp_y = left_x + PADDLE_WIDTH//2, left_y + PADDLE_HEIGHT//2
            
                
        #return 0 -> pohyb dole
        if self.y < self.current_target: 
            if self.y + PADDLE_HEIGHT//2 > self.current_target: 
                self.get_target()
            return 0
        
        #return 1 -> pohyb hore
        else: 
            if self.y - PADDLE_HEIGHT//2 < self.current_target: 
                self.get_target()
                
            return 1
    