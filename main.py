from re import S
import pygame  # docs found here: https://www.pygame.org/docs/
from random import randint, choice
import time

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE
)

from brainflow.data_filter import (
    DataFilter,
    FilterTypes,
    AggOperations,
    WindowFunctions,
    DetrendOperations,
)
import numpy as np
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from Board import Board


# GLOBAL VARIABLES
WIDTH = 768
HEIGHT= 640
ORDERS = ['fries', 'fish']
PLAYER_SPEED = 16
CUSTOMER_SPEED = 5

BOARD_ID = 22  # muse 2 id
BOARD = Board(board_id=BOARD_ID)
SAMPLING_RATE = BOARD.get_sampling_rate(BOARD_ID)

BUFFER_LENGTH = 1
num_points = SAMPLING_RATE * BUFFER_LENGTH

ALPHA_LEVELS = []
THETABETA_RATIOS = []


# USER DEFINED FUNCTIONS
def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    
    # create a game object
    game = Game()
    
    # start the main game loop by calling the play method on the game object
    game.run()
    
    # quit pygame and clean up the pygame window
    pygame.quit()

def average(list):
    return sum(list)/len(list)
  
  
# USER-DEFINED CLASSES
class Game:
    def __init__(self):
        # create the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface = pygame.display.get_surface()
        self.bg_color = pygame.Color('white')
        self.max_frames = 150
        self.frame_counter = 0
        self.FPS = 60
        self.close_clicked = False
        self.continue_game = True
        self.started = False
        self.round_started = False
        
        # create Clock object
        self.game_Clock = pygame.time.Clock()
        
        # customize the pygame window
        pygame.display.set_caption('calm the food down')
        window_icon = pygame.image.load('assets/icon.png')
        pygame.display.set_icon(window_icon)

        # create Wall objects
        self.wall1 = Wall(0 ,128 , 384, 128, 'brown', self.surface)
        self.wall2 = Wall(256, 256, 128, 128, 'brown', self.surface)
        self.wall3 = Wall(512, 128, 256, 128, 'brown', self.surface)
        self.wall4 = Wall(512, 384, 128, 256, 'brown', self.surface)
        self.wall5 = Wall(0, 512, 384, 128, 'brown', self.surface)
        self.wall6 = Wall(384,128, 128, 128, 'brown', self.surface)
        
        self.walls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.walls.add([self.wall1, self.wall2, self.wall3, self.wall4, self.wall5,self.wall6])
        self.all_sprites.add([self.wall1, self.wall2, self.wall3, self.wall4, self.wall5,self.wall6])

        # player properties
        player_width = 72
        player_height = 72
        food_height=64
        food_weight =64
        self.player_speed = 15
        self.holding= None
        self.score_counter=0

        # create Player object
        self.player = Player(player_height,player_width,self)
        self.all_sprites.add(self.player)

        # create Food object
        self.food = Food(food_height,food_weight,self.surface,self.player)
        
        # ingredients
        self.potato_surf = pygame.Surface((64, 64))
        self.potato_surf.fill('orange')
        self.potato_rect = self.potato_surf.get_rect(center = (self.wall4.rect.center[0], self.wall4.rect.center[1] - 1/4*(self.wall4.rect.height)))

        self.fish_surf = pygame.Surface((64, 64))
        self.fish_surf.fill('cyan')
        self.fish_rect = self.fish_surf.get_rect(center = (self.wall4.rect.center[0], self.wall4.rect.center[1] + 1/4*(self.wall4.rect.height)))

        # stove
        self.stove_surf = pygame.Surface((128, 128))
        self.stove_surf.fill('gray')
        self.stove_rect = self.stove_surf.get_rect(center = self.wall1.rect.center)

        # checkout
        self.checkout_surf = pygame.Surface((128, 128))
        self.checkout_surf.fill('green')
        self.checkout_rect = self.stove_surf.get_rect(topright=self.wall3.rect.topright)
        
        # customers
        self.customer_surf = pygame.Surface((128, 128))
        self.customer_rect = self.customer_surf.get_rect(topright=(0,0))
        self.customer_rect_list = []
        self.customer_order_list = []
        self.customers = Customers(self.screen, self.customer_surf)

        # calibration timer
        self.calibrating = False
        self.calibration_timer = 0

        # customer timer
        self.customer_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.customer_timer, 1000)

        # BCI
        self.calibrated_data = []
        self.baseline = None
        self.stress_threshold_index = 0.9
        self.stress_threshold = None

    def run(self):    
        while not self.close_clicked:  # until player clicks close box
            self.data = self.record_muse_data()
            self.handle_events()
            if not self.started:
                self.display_main_menu()
            elif self.calibrating:
                self.baseline = self.calibrate()
            if self.round_started:
                self.stress_threshold = self.baseline * self.stress_threshold_index

                if self.continue_game:
                    self.draw()
                    self.update()
                else:
                    self.display_game_over()
            self.game_Clock.tick(self.FPS)  # set FPS ceiling to self.FPS

    def display_game_over(self):
        self.screen.fill('beige')

        gameover_font = pygame.font.Font('assets/title_font.ttf', 64)
        gameover_text_surf = gameover_font.render('you lose! you were too stressed', True, 'black')
        gameover_text_rect = gameover_text_surf.get_rect(center=(WIDTH/2, HEIGHT/4))
        self.surface.blit(gameover_text_surf, gameover_text_rect)

        button_text_font = pygame.font.Font('assets/title_font.ttf', 64)
        button_text_surf = button_text_font.render('play again', True, 'black')
        button_text_rect = button_text_surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.surface.blit(button_text_surf, button_text_rect)
        button_border_rect = pygame.Rect(0, 0, button_text_rect.width + 32, button_text_rect.height + 32)
        button_border_rect.center = button_text_rect.center
        pygame.draw.rect(self.surface, 'black', button_border_rect, 8)

        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_press[0] and pygame.Rect.collidepoint(button_border_rect, mouse_pos):
            self.__init__()
            time.sleep(1)

        pygame.display.update()

    def calibrate(self):
        self.surface.fill('beige')

        calibrate_text = 'calibrating'
        if self.calibration_timer >= 4:
            self.calibrating = False
            self.round_started = True

            return average(self.calibrated_data)
        elif self.calibration_timer >= 3:
            calibrate_text += '...'
        elif self.calibration_timer >= 2:
            calibrate_text += '..'
        elif self.calibration_timer >= 1:
            calibrate_text += '.'
        self.calibration_timer += 1/self.FPS

        calibrate_font = pygame.font.Font('assets/title_font.ttf', 64)
        calibrate_text_surf = calibrate_font.render(calibrate_text, True, 'black')
        calibrate_text_rect = calibrate_text_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.surface.blit(calibrate_text_surf, calibrate_text_rect)

        self.calibrated_data.append(self.data)

        pygame.display.flip()

    def display_muse_data(self, data, x=None, y=None):
        data_text_font = pygame.font.Font('assets/game_font.ttf', 32)
        data_text_surf = data_text_font.render('theta/beta ratio: ' + str(round(data, 2)), True, 'black')
        if not (x and y):
            x, y = 0 + data_text_surf.get_width()/2, self.scores_rect.top - data_text_surf.get_height()/2
        data_text_rect = data_text_surf.get_rect(center=(x, y))
        self.surface.blit(data_text_surf, data_text_rect)

        return data_text_rect

    def record_muse_data(self):
        # BCI
        data = BOARD.get_data_quantity(num_points)
        alpha_session = []
        theta_session = []
        beta_session = []

        alpha_index = 2
        theta_index = 1
        beta_index = 3

        exg_channels = BOARD.get_exg_channels()

        for i in exg_channels:
            channel = data[i, :]
            fftData = np.fft.fft(channel)
            freq = np.fft.fftfreq(len(channel))*250

            # Remove unnecessary negative reflection
            fftData = fftData[1:int(len(fftData)/2)]
            freq = freq[1:int(len(freq)/2)]

            # Recall FFT is a complex function
            fftData = np.sqrt(fftData.real**2 + fftData.imag**2)

            # Band binding
            bandTotals = [0,0,0,0,0]
            bandCounts = [0,0,0,0,0]

            for point in range(len(freq)):
                if(freq[point] < 4):
                    bandTotals[0] += fftData[point]
                    bandCounts[0] += 1
                elif(freq[point] < 8):
                    bandTotals[1] += fftData[point]
                    bandCounts[1] += 1
                elif(freq[point] < 12):
                    bandTotals[2] += fftData[point]
                    bandCounts[2] += 1
                elif(freq[point] < 30):
                    bandTotals[3] += fftData[point]
                    bandCounts[3] += 1
                elif(freq[point] < 100):
                    bandTotals[4] += fftData[point]
                    bandCounts[4] += 1

            # Save the average of all points 
            bands = list(np.array(bandTotals)/np.array(bandCounts))
            alpha_bands = bands[alpha_index]
            theta_bands = bands[theta_index]
            beta_bands = bands[beta_index]

            alpha_session.append(alpha_bands)
            theta_session.append(theta_bands)
            beta_session.append(beta_bands)
        ALPHA_LEVELS.append(average(alpha_session))
        THETABETA_RATIOS.append(sum(theta_session)/sum(beta_session))

        return average(THETABETA_RATIOS)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if self.round_started and event.type == self.customer_timer:
                self.customer_rect_list.append(self.customer_surf.get_rect(topleft=(randint(-256, -128), 0)))
                self.customer_order_list.append(choice(ORDERS))
                pygame.time.set_timer(self.customer_timer, randint(3000, 7000))  # randomize customer timer

    def check_holding(self,pressed_keys):
        # determine if pressed keys
        points=[]
        point1= (self.player.rect.center[0],self.player.rect.center[1]+100)
        points.append(point1)
        point2= (self.player.rect.center[0]+100,self.player.rect.center[1])
        points.append(point2)
        point3= (self.player.rect.center[0],self.player.rect.center[1]-100)
        points.append(point3)
        point4= (self.player.rect.center[0]-100,self.player.rect.center[1])
        points.append(point4)
        for x in points:
            if pygame.Rect.collidepoint(self.fish_rect,x):
                if pressed_keys[K_SPACE]:
                    self.food.surf.fill("cyan")
                    self.holding="raw_fish"
                    
            elif pygame.Rect.collidepoint(self.stove_rect,x):
                if pressed_keys[K_SPACE]:
                    if self.holding=="raw_fish" or self.holding=="potato":
                        if self.holding == "raw_fish":
                            self.food.surf.fill("blue")
                            self.holding="fish"
                        elif self.holding == "potato":
                            self.food.surf.fill("yellow")
                            self.holding="fries"
                        
            elif pygame.Rect.collidepoint(self.potato_rect,x):
                if pressed_keys[K_SPACE]:
                    self.food.surf.fill("orange")
                    self.holding="potato"
            
            if pygame.Rect.collidepoint(self.checkout_rect,x):
                if pressed_keys[K_SPACE]:
                    if self.holding=="fish" or self.holding=="fries":
                        if self.holding == self.customer_order_list[0]:
                            self.customers.customer_complete(self.customer_rect_list,self.customer_order_list)
                            self.food.surf.fill("black")
                            self.score_counter += 1
                            self.holding = None

    def draw(self):
        # Draw all game objects.
        self.surface.fill(self.bg_color)  # clear the display surface first
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
            
        self.screen.blit(self.potato_surf, self.potato_rect)
        self.screen.blit(self.fish_surf, self.fish_rect)
        self.screen.blit(self.stove_surf, self.stove_rect)
        self.screen.blit(self.checkout_surf, self.checkout_rect)
        
        self.customers.draw(self.customer_rect_list, self.customer_order_list)
        
        self.scores_rect = self.draw_scores()
        self.food.draw()

        self.muse_data_rect = self.display_muse_data(self.data)
        self.display_stress_threshold()

        pygame.display.flip()  # updates the display

    def display_stress_threshold(self):
        text_font = pygame.font.Font('assets/game_font.ttf', 32)
        text_surf = text_font.render('stay above ' + str(round(self.stress_threshold, 2)), True, 'black')
        text_rect = text_surf.get_rect(bottomleft = self.muse_data_rect.topleft)
        self.screen.blit(text_surf, text_rect)

    def draw_scores(self):
        score_string = 'score: ' + str(self.score_counter)
        fg_color = pygame.Color('black')
        font = pygame.font.Font('assets/game_font.ttf', 32)
        text_box = font.render(score_string, True, fg_color)
        text_rect = text_box.get_rect(bottomleft=(0,HEIGHT))
        self.surface.blit(text_box, text_rect)

        return text_rect

    def update(self):
        # Update the game objects for the next frame.
        pressed_keys = pygame.key.get_pressed()
        self.check_holding(pressed_keys)
        self.player.move(pressed_keys)

        # customers
        self.customers.customer_movement(self.customer_rect_list)
        self.customers.handle_customer_collisions(self.customer_rect_list)

        # win condition
        if self.data < self.stress_threshold:
            self.continue_game = False

    def display_main_menu(self):
        self.surface.fill('beige')

        title_font = pygame.font.Font('assets/title_font.ttf', 96)
        title_surf = title_font.render('calm the food down!', True, 'black')
        title_rect = title_surf.get_rect(center=(WIDTH/2, HEIGHT/4))
        self.surface.blit(title_surf, title_rect)

        button_text_font = pygame.font.Font('assets/title_font.ttf', 64)
        button_text_surf = button_text_font.render('start', True, 'black')
        button_text_rect = button_text_surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.surface.blit(button_text_surf, button_text_rect)
        button_border_rect = pygame.Rect(0, 0, button_text_rect.width + 32, button_text_rect.height + 32)
        button_border_rect.center = button_text_rect.center
        pygame.draw.rect(self.surface, 'black', button_border_rect, 8)

        self.display_muse_data(self.data, WIDTH/2, 3*HEIGHT/4)

        censor_rect = pygame.Rect(0, 0, 104, 12)
        censor_rect.center = (title_rect.center[0]+47, title_rect.center[1]+10)
        pygame.draw.rect(self.surface, 'black', censor_rect)

        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_press[0] and pygame.Rect.collidepoint(button_border_rect, mouse_pos):
            self.started = True
            self.calibrating = True

        pygame.display.flip()
        

class Wall(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, height, color, surface):
        super(Wall,self).__init__()
        
        self.surf = pygame.Surface((width,height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(topleft = (x,y))
        self.color = pygame.Color(color)
        

class Player(pygame.sprite.Sprite):
    def __init__(self, height, width, parent):
        super(Player,self).__init__()
        
        self.surf = pygame.Surface((width,height))
        self.rect = self.surf.get_rect(topleft=(15,270))
        self.color = pygame.Color('black')
        self.surf.fill(self.color)
        self.parent = parent

    def move(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -PLAYER_SPEED)
            
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, PLAYER_SPEED)

        if pygame.sprite.spritecollideany(self,self.parent.walls):
            hits = pygame.sprite.spritecollide(self,self.parent.walls,False)
            for hit in hits:
                move_up = hit.rect.top - self.rect.bottom
                move_down = hit.rect.bottom-self.rect.top
                if abs(move_up) < abs(move_down):
                    self.rect.move_ip(0,move_up)
                else:
                    self.rect.move_ip(0,move_down)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)

        if pygame.sprite.spritecollideany(self,self.parent.walls):
            hits=pygame.sprite.spritecollide(self,self.parent.walls,False)
            for hit in hits:
                move_r = hit.rect.right-self.rect.left
                move_l = hit.rect.left-self.rect.right
                if abs(move_r) < abs(move_l):
                    self.rect.move_ip(move_r,0)
                else:
                    self.rect.move_ip(move_l,0)

        if self.rect.left <= 0:
            self.rect.move_ip(-self.rect.left,0)
        elif self.rect.right >= WIDTH:
            self.rect.move_ip(-(self.rect.right-WIDTH),0)
        if self.rect.top <= 0:
            self.rect.move_ip(0,-self.rect.top)
        elif self.rect.bottom >= HEIGHT:
            self.rect.move_ip(0,-(self.rect.bottom-HEIGHT))
            
            
class Customers:
    def __init__(self, screen, customer_surf):
        self.screen = screen
        self.customer_surf = customer_surf
    
    def customer_movement(self, customer_list):
        for customer_rect in customer_list:
            customer_rect.x += CUSTOMER_SPEED

    def handle_customer_collisions(self, customer_list):
        for i in range(len(customer_list)):
            if i == 0:
                if customer_list[i].right >= WIDTH: 
                    customer_list[i].right = WIDTH
            else:
                if customer_list[i].right >= customer_list[i-1].left:
                    customer_list[i].right = customer_list[i-1].left

    def customer_complete(self, customer_list, order_list):
        customer_list.pop(0)
        order_list.pop(0)

    def draw(self, customer_list, order_list):
        for i in range(len(customer_list)):
            self.screen.blit(self.customer_surf, customer_list[i])
            order_text = pygame.font.Font('assets/game_font.ttf', 32)
            order_surf = order_text.render(order_list[i], True, 'white')
            order_rect = order_surf.get_rect(center=customer_list[i].center)
            self.screen.blit(order_surf, order_rect)

class Food(pygame.sprite.Sprite):
    def __init__(self, height, width, surface,player):
        super(Food,self).__init__()
        self.surf=pygame.Surface((width,height))
        self.surface=surface
        self.player=player
        self.rect=self.surf.get_rect(center=self.player.rect.center) 
        self.color = pygame.Color('black')
        self.surf.fill(self.color)

    def draw(self):
        self.rect.center=self.player.rect.center
        self.surface.blit(self.surf,self.rect)

main()