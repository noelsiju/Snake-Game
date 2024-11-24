import pygame,sys,random
from pygame.math import Vector2
state = "level1"

#class for the snake
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        #drawing the head
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        #drawing the tail
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
    #updates the head and tail
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                            screen.blit(self.body_br,block_rect)
        #Adding graphics of the head of the snake
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down
        #Adding graphics of the tail of the snake
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        global state
        state = 'level1'
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

#class for the fruit
class FRUIT:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    #Randomising the position of the fruit
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)
        while(self.check_obstacle_under_the_fruit()):
            self.x = random.randint(0,cell_number - 1)
            self.y = random.randint(0,cell_number - 1)
            self.pos = Vector2(self.x,self.y)

    def get_full_obstacle_positions(self,obs_x,obs_y):
        return [Vector2(obs_x,obs_y),Vector2(obs_x+1,obs_y),Vector2(obs_x,obs_y+1),Vector2(obs_x+1,obs_y+1)]

    def check_obstacle_under_the_fruit(self):
        for obstacle in self.obstacles:
            if self.pos in self.get_full_obstacle_positions(obstacle.get_pos().x, obstacle.get_pos().y): return True
        return False

#class of the obstacle
class OBSTACLE:
    def __init__(self,size):
        self.size = size
        self.randomize()
    #drawing the obstacle
    def draw_obstacle(self):
        global state
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        if self.size == 'l':
            screen.blit(big_obstacle,obstacle_rect)
        else:
            screen.blit(obstacle,obstacle_rect)
    def get_pos(self):
        return self.pos
    #Randomising the postion of the obstacle
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.obstacles = [OBSTACLE('s'),OBSTACLE('s'),OBSTACLE('s'),OBSTACLE('s')]
        self.big_obstacles = [OBSTACLE('l'),OBSTACLE('l'),OBSTACLE('l'),OBSTACLE('l')]
        self.fruit = FRUIT(self.obstacles)

    def update(self):
        global state
        if(len(self.snake.body) -3 == 1 and state== 'level1'):
            state = 'level2'
        elif(len(self.snake.body) -3 == 2 and state== 'level2'):
            state = 'level3'
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
       

    def draw_elements(self, shade_color):
        self.draw_grid(shade_color)
        self.fruit.draw_fruit()
        if state=='level2':
            for obstacle in self.obstacles:
                obstacle.draw_obstacle()
        elif state=='level3':
            for obstacle in self.obstacles:
                obstacle.draw_obstacle()
            for obstacle in self.big_obstacles:
                obstacle.draw_obstacle()

        self.snake.draw_snake()
        self.draw_score()
    #checking collision 
    def check_collision(self):
        global state
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        if state=='level2':
            for obstacle in self.obstacles:
                if self.snake.body[0] in self.get_full_obstacle_positions(obstacle.get_pos().x, obstacle.get_pos().y): self.game_over()


        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def get_full_obstacle_positions(self,obs_x,obs_y):
        return [Vector2(obs_x,obs_y),Vector2(obs_x+1,obs_y),Vector2(obs_x,obs_y+1),Vector2(obs_x+1,obs_y+1)]


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
       
    def game_over(self):
        self.snake.reset()

    def draw_grid(self,colors):
        grass_color = (colors[0],colors[1],colors[2])
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)        

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(40,80,10))
        score_x = int(cell_size * cell_number - 50)
        score_y = int(cell_size * cell_number - 750)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

 #class for levels in the game
class GameState():
    #Controls of the snake
    def game_control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE:
                main_game.update()


        screen.fill((64,36,40))
        main_game.draw_elements([167,209,61])
        pygame.display.update()

    #features of level 1
    def level1(self):
        self.game_control()
        screen.fill((175,215,70))
        main_game.draw_elements([167,209,61])
        pygame.display.update()

    #features of level 2
    def level2(self):
        self.game_control()
        screen.fill((196, 164, 132))
        main_game.draw_elements([255, 248, 220])
        pygame.display.update()

       

    #features of level 3
    def level3(self):
        self.game_control()
        screen.fill((0, 255, 255))
        main_game.draw_elements([255, 255, 255])
        pygame.display.update()


    def state_manager(self):
        if state == 'intro':
            self.intro()
        elif state == 'level1':
            self.level1()
        elif state == 'level2':
            self.level2()
        elif state == 'level3':
            self.level3()



pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
obstacle = pygame.image.load('Graphics/obstacle.png').convert_alpha()
big_obstacle = pygame.transform.scale(pygame.image.load('Graphics/obstacle.png').convert_alpha(), (100,100))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
game_state = GameState()
ready_text = pygame.image.load

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
main_game = MAIN()

       

while True:
    game_state.state_manager()
    clock.tick(60)