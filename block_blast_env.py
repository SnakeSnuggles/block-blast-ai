import time
import pygame 
import random

'''
GOALS: 
    get blocks working
'''

class Block:
    def __init__(self,state:bool,pos:tuple,board_size,screen_size=(500,500)):
        margin = 50
        available_width = screen_size[0] - 2 * margin
        available_height = screen_size[1] - 2 * margin
        block_width = available_width / board_size
        block_height = available_height / board_size

        self.size_image = (block_width, block_height)
        self.pos = pos
        self.state = state

        # Set the block's image and scale it to the calculated size
        self.set(self.state)
        self.image = pygame.transform.scale(self.image, self.size_image)

        # Position the block, including margins
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            self.pos[0] * block_width + margin,
            self.pos[1] * block_height + margin
        )

    def toggle(self):
       ... 
    def set(self,new_state:bool):
        self.image = pygame.image.load("assets/empty_block.png" if new_state == False else "assets/filled_block.png")
        self.image = pygame.transform.scale(self.image,self.size_image)
        self.state = new_state

class Block_Blast:
    def __init__(self,size):
        self.size = size
        self.board = {}
        self.screen_size = (500,500)
        self.screen = pygame.display.set_mode(self.screen_size)
        #self.screen = pygame.display.set_mode((1000,1000))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial",30) 
        self.score = 0
        for x in range(self.size): 
            for y in range(self.size):
                choice = random.choice([True,False]) 
                self.board[(x,y)] = Block(choice,(x,y),self.size,self.screen_size)

        pygame.init()

    def clear_rows_and_columns(self):
        # Track rows and columns with >= 8 "on" blocks
        rows_to_clear = [row for row in range(self.size) if sum(self.board[(row, block)].state for block in range(self.size)) >= self.size]
        cols_to_clear = [col for col in range(self.size) if sum(self.board[(block, col)].state for block in range(self.size)) >= self.size]

        # Clear rows
        for row in rows_to_clear:
            for block in range(self.size):
                self.board[(row, block)].set(False)

        # Clear columns
        for col in cols_to_clear:
            for block in range(self.size):
                self.board[(block, col)].set(False)

    def draw(self):
            self.screen.fill("black")
            
            score_text = self.font.render(f"Score: {self.score}", False, (255,255,255))

            self.screen.blit(score_text,(20,0))
            
            for block in self.board:
                block = self.board[block]
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

                    good_sprite = [self.board[block] for block in self.board if self.board[block].rect.collidepoint(pos)] 
                    for a in good_sprite:
                        a.set(not a.state)

            self.clear_rows_and_columns()
            self.draw() 
            self.clock.tick(100)  

        pygame.quit()
