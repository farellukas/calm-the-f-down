import pygame  # docs found here: https://www.pygame.org/docs/
from random import randint, choice

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE
)


# GLOBAL VARIABLES
WIDTH = 768
HEIGHT= 640
ORDERS = ['fries', 'fish']
PLAYER_SPEED = 16
CUSTOMER_SPEED = 5


def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    
    # create a game object
    game = Game()
    
    # start the main game loop by calling the play method on the game object
    game.run()
    
    # quit pygame and clean up the pygame window
    pygame.quit()
  
  
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
        self.started = True
        
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
        self.food=Food(food_height,food_weight,self.surface,self.player)
        
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

        # customer timer
        self.customer_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.customer_timer, 1000)

    def run(self):    
        while not self.close_clicked:  # until player clicks close box
            if not self.started:
                self.display_main_menu()
            else:
                self.draw()
                if self.continue_game:
                    self.update()
                    # self.decide_continue()
            self.game_Clock.tick(self.FPS)  # set FPS ceiling to self.FPS

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == self.customer_timer:
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
                    self.holding="fish"
                    
            elif pygame.Rect.collidepoint(self.stove_rect,x):
                if pressed_keys[K_SPACE]:
                    if self.holding=="fish" or self.holding=="potato":
                        if self.holding == "fish":
                            self.food.surf.fill("blue")
                            self.holding="cooked_fish"
                        elif self.holding == "potato":
                            self.food.surf.fill("yellow")
                            self.holding="fries"
                        
            elif pygame.Rect.collidepoint(self.potato_rect,x):
                if pressed_keys[K_SPACE]:
                    self.food.surf.fill("orange")
                    self.holding="potato"
            
            if pygame.Rect.collidepoint(self.checkout_rect,x):
                if pressed_keys[K_SPACE]:
                    if self.holding=="cooked_fish" or self.holding=="fries":
                        if self.holding == self.customer_order_list[0]:
                            self.customers.customer_complete(self.customers_rect_list,self.customer_order_list)
                            self.food.surf.fill("black")
                            self.score_counter+=1
                            self.holding=None

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
        
        self.draw_scores()
        pressed_keys=pygame.key.get_pressed()
        self.food.draw(pressed_keys)
        pygame.display.flip()  # updates the display

    def draw_scores(self):
        score_string = str(self.score_counter)
        font_size = 50
        fg_color = pygame.Color('black')
        font = pygame.font.SysFont('', font_size)
        text_box = font.render(score_string, True, fg_color)
        text_rect= text_box.get_rect(bottomleft=(0,HEIGHT))
        self.surface.blit(text_box, text_rect)

    def update(self):
        # Update the game objects for the next frame.
        pressed_keys = pygame.key.get_pressed()
        self.check_holding(pressed_keys)
        self.player.move(pressed_keys)

        # customers
        completed = False
        self.customers.customer_movement(self.customer_rect_list)
        self.customers.handle_customer_collisions(self.customer_rect_list)
        if self.customer_order_list and completed == self.customer_order_list[0]:
            self.customers.customer_complete(self.customer_rect_list, self.customer_order_list)

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

        censor_rect = pygame.Rect(0, 0, 104, 12)
        censor_rect.center = (title_rect.center[0]+47, title_rect.center[1]+10)
        pygame.draw.rect(self.surface, 'black', censor_rect)

        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_press[0] and pygame.Rect.collidepoint(button_border_rect, mouse_pos):
            self.started = True

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

    def draw(self, pressed_keys):
        self.rect.center=self.player.rect.center
        #self.direction(pressed_keys)
        self.surface.blit(self.surf,self.rect)

main()