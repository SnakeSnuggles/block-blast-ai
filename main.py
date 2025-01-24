import time
import pygame 
import random

'''
GOALS: 
    GET MOUSE DETECTION TO WORK 
    BE ABLE TO CHANGE THE DIFFERENT GRID PLACES
    MAYBE GET LINE CLEARS

'''

class Block:
    def __init__(self,state:bool,pos:tuple,size:int=50,):
        self.size_image = (size,size)
        self.pos = pos
        self.state = state
        self.set(self.state)
        self.image = pygame.transform.scale(self.image,self.size_image)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos[0]*50+20,self.pos[1]*50+40)

    def toggle(self):
       ... 
    def set(self,new_state:bool):
        self.image = pygame.image.load("empty_block.png" if new_state == False else "filled_block.png")
        self.image = pygame.transform.scale(self.image,self.size_image)
        self.state = new_state

class Block_Blast:
    def __init__(self):
        self.size = 8 
        self.board:list[Block] = []
        self.board_state = [[False for x in range(self.size)] for y in range(self.size)]
        self.screen = pygame.display.set_mode((500, 500))
        #self.screen = pygame.display.set_mode((1000,1000))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial",30) 
        self.score = 0
        for x in range(self.size): 
            for y in range(self.size):
                choice = random.choice([True,False]) 
                self.board.append(Block(choice,(x,y))) 

        pygame.init()

    def draw(self):
            self.screen.fill("black")

            
            score_text = self.font.render(f"Score: {self.score}", False, (255,255,255))

            self.screen.blit(score_text,(20,0))
            
            for block in self.board:
                self.screen.blit(block.image,block.rect)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {str(self.clock.get_fps())}")
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    good_sprite:list[Block] = [block for block in self.board if block.rect.collidepoint(pos)]

                    for a in good_sprite:
                        a.set(not a.state)

            self.draw() 
            self.clock.tick(100)  

        pygame.quit()


game = Block_Blast()

game.run()
