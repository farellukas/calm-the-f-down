import pygame  # docs found here: https://www.pygame.org/docs/
#from settings import *
#from sys import exit
#from level import Level
# initialize the pygame
WIDTH = 768
HEIGHT= 640
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

# game parameters
def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('A template for graphical games with two moving dots')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.run()
    # quit pygame and clean up the pygame window
    pygame.quit()
    


class Game:
    def __init__(self,surface):
    # create the screen
        
       
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.max_frames = 150
        self.frame_counter = 0
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        # customize the pygame window
        pygame.display.set_caption('calm the food down')
        #window_icon = pygame.image.load('calm-the-f-down/assets/icon.png')
        #pygame.display.set_icon(window_icon)

        # create Clock object
        self.clock = pygame.time.Clock()
        #self.level=Level()
        #self.wall1 = wall(0, 512, 256, 128, 'blue', self.surface)
        self.walls = pygame.sprite.Group()
        self.wall2 = wall(0 ,128 , 384, 128, 'brown', self.surface)
        self.wall3 = wall(256, 256, 128, 128, 'brown', self.surface)
        self.wall4 = wall(512, 128, 256, 128, 'brown', self.surface)
        self.wall5 = wall(512, 384, 128, 256, 'brown', self.surface)
        self.wall6 = wall(0, 512, 384, 128, 'brown', self.surface)
        self.wall7 = wall(384,128, 128, 128, 'brown', self.surface)
        self.walls.add([self.wall2, self.wall3, self.wall4, self.wall5, self.wall6,self.wall7])
        self.all_sprite=pygame.sprite.Group()
        self.all_sprite.add([self.wall2, self.wall3, self.wall4, self.wall5, self.wall6,self.wall7])
        #self.wall = wall(30, 50, 128, 128, 'white', self.surface)
        size=self.surface.get_size()
        #player properties
        player_width =72
        player_height=72
        x1 = size[0]/6 - player_width/2
        y = size[1]/2 - player_height/2
        self.player_speed=7

        self.player=Player(player_height,player_width,x1,y,self.surface,self)
        self.all_sprite.add(self.player)

    def run(self):    
         while not self.close_clicked:  # until player clicks close box
            # play frame
            while not self.close_clicked:
                self.handle_events()
                self.draw()
                if self.continue_game:
                    self.update()
                    self.decide_continue()
                self.game_Clock.tick(self.FPS)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type ==pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)
 

    def handle_key_down(self, event):
        if event.key == pygame.K_w:
            self.player.set_velocity_y(self.player.get_velocity_y()-self.player_speed)
        elif event.key == pygame.K_s:
            self.player.set_velocity_y(self.player.get_velocity_y()+self.player_speed)
        if event.key == pygame.K_a:
            self.player.set_velocity_x(self.player.get_velocity_x()-self.player_speed)
        elif event.key == pygame.K_d:
            self.player.set_velocity_x(self.player.get_velocity_x()+self.player_speed)

    def handle_key_up(self,event):
        if event.key == pygame.K_w:
            self.player.set_velocity_y(self.player.get_velocity_y()+self.player_speed)
        elif event.key == pygame.K_s:
            self.player.set_velocity_y(self.player.get_velocity_y()-self.player_speed)
        if event.key == pygame.K_a:
            self.player.set_velocity_x(self.player.get_velocity_x()+self.player_speed)
        elif event.key == pygame.K_d:
            self.player.set_velocity_x(self.player.get_velocity_x()-self.player_speed)

    
    # def collision(self):
    #     if self.wall2.rect.bottom > self.player.get_top():
    #         self.player.top = self.wall2.rect.bottom
    #     #if self.wall3.rect
        


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        #self.wall1.draw()
        # self.wall2.draw()
        # self.wall3.draw()
        # self.wall4.draw()
        # self.wall5.draw()
        # self.wall6.draw()
        # self.player.draw()
        # self.big_dot.draw()
        for entity in self.all_sprite:
            self.screen.blit(entity.surf,entity.rect)
        
        pygame.display.flip()
        #pygame.display.update()

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to updatel
        pressed_keys=pygame.key.get_pressed()
        self.player.move(pressed_keys)
        #self.collision()

        # self.big_dot.move()
        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.frame_counter > self.max_frames:
            self.continue_game = True

class wall(pygame.sprite.Sprite):
    def __init__ (self, x,y,width, height, color,surface):
        super(wall,self).__init__()
        self.surf=pygame.Surface((width,height))
        self.surf.fill(color)
        self.rect=self.surf.get_rect(center=(x,y))
        self.rect=pygame.Rect(x,y,width, height)
        self.color = pygame.Color(color)
        
        #self.surface = surface
    
    # def draw(self):
    #     pygame.draw.rect(self.surface, self.color, self.rect)

    # def collide(self):
    #     self.rect.collidepoint()

class Player(pygame.sprite.Sprite):
    def __init__(self, height, width, left, top, surface, parent):
        super(Player,self).__init__()
        self.surf=pygame.Surface((width,height))
        self.rect=self.surf.get_rect(topleft=(15,270))
        #self.rect=pygame.Rect(x,y,width, height)
        self.color = pygame.Color('white')
        self.surf.fill(self.color)
        # self.height = height
        # self.width = width
        # self.left = left
        # self.top = top
        self.velocity_x = 25
        self.velocity_y = 25
        self.parent=parent
        # self.surface = surface
        
    
    def get_velocity_x(self):
    # a getter method used to return the paddle's velocity
    # - self is the Paddle to get the velocity value from
        return self.velocity_x

    def get_velocity_y(self):
    # a getter method used to return the paddle's velocity
    # - self is the Paddle to get the velocity value from
        return self.velocity_y

    def set_velocity_x(self, velocity):
    # a setter method used to alter the paddle's velocity
    # - self is the Paddle to set the velocity
    # - velocity is the int velocity the paddle will be set to
        self.velocity_x = velocity 
    
    def set_velocity_y(self,velocity):
        self.velocity_y=velocity

    def get_top(self):
        return self.top
    
    def get_left(self):
        return self.left

    def move(self,pressed_keys):
    # Change the location of the Paddle by adding the corresponding speed values to the y coordinate of its top edge
    # - self is the Paddle
        # size = self.surface.get_size()
        # if self.top >= 0 and self.top <= size[1] - self.height:
        #     self.top = self.top + self.velocity_y
        # if self.top < 0:
        #     self.top = 0
        # if self.top >= size[1] - self.height:
        #     self.top = size[1] - self.height
        # if self.left >= 0 and self.left <= size[0] - self.width:
        #     self.left = self.left + self.velocity_x
        # if self.left < 0:
        #     self.left = 0
        # if self.left >= size[0] - self.width:
        #     self.left = size[0] - self.width
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-self.velocity_y)
            
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,self.velocity_y)

        if pygame.sprite.spritecollideany(self,self.parent.walls):
            
            hits=pygame.sprite.spritecollide(self,self.parent.walls,False)
            for hit in hits:
                move_up=hit.rect.top-self.rect.bottom
                move_down=hit.rect.bottom-self.rect.top
                if abs(move_up) <abs(move_down):
                    self.rect.move_ip(0,move_up)
                else:
                    self.rect.move_ip(0,move_down)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.velocity_x,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.velocity_x,0)

        if pygame.sprite.spritecollideany(self,self.parent.walls):
            
            hits=pygame.sprite.spritecollide(self,self.parent.walls,False)
            for hit in hits:
                move_r=hit.rect.right-self.rect.left
                move_l=hit.rect.left-self.rect.right
                if abs(move_r) <abs(move_l):
                    self.rect.move_ip(move_r,0)
                else:
                    self.rect.move_ip(move_l,0)

        if self.rect.left <0:
            self.rect.move_ip(-self.rect.left,0)
        elif self.rect.right > WIDTH:
            self.rect.move_ip(-(self.rect.right-WIDTH),0)
        if self.rect.top<=0:
            self.rect.move_ip(0,-self.rect.top)
        elif self.rect.bottom >= HEIGHT:
            self.rect.move_ip(0,-(self.rect.bottom-HEIGHT))
    

    def draw(self):
    # Draw the Paddle on the surface
    # - self is the Paddle
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(self.surface, self.color, self.rect)

#class food(pygame.sprite.Sprite):
main()