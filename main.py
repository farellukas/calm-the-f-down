import pygame  # docs found here: https://www.pygame.org/docs/
#from settings import *
#from sys import exit
#from level import Level
# initialize the pygame


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
        
        WIDTH = 768
        HEIGHT= 640
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
        window_icon = pygame.image.load('calm-the-f-down/assets/icon.png')
        pygame.display.set_icon(window_icon)

        # create Clock object
        self.clock = pygame.time.Clock()
        #self.level=Level()
        self.wall1 = wall(0, 512, 256, 128, 'brown', self.surface)
        self.wall2 = wall(0 ,128 , 384, 128, 'brown', self.surface)
        self.wall3 = wall(256, 256, 128, 128, 'brown', self.surface)
        self.wall4 = wall(512, 128, 256, 128, 'brown', self.surface)
        self.wall5 = wall(512, 384, 128, 256, 'brown', self.surface)
        self.wall6 = wall(0, 512, 384, 128, 'brown', self.surface)
        #self.wall = wall(30, 50, 128, 128, 'white', self.surface)

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
    
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.wall1.draw()
        self.wall2.draw()
        self.wall3.draw()
        self.wall4.draw()
        self.wall5.draw()
        self.wall6.draw()
        # self.big_dot.draw()
        pygame.display.update()

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to updatel
        

        # self.big_dot.move()
        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.frame_counter > self.max_frames:
            self.continue_game = True

class wall:
    def __init__ (self, x,y,width, height, color,surface):
        self.rect=pygame.Rect(x,y,width, height)
        self.color = pygame.Color(color)
        self.surface = surface
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def collide(self):
        self.rect.collidepoint()

main()