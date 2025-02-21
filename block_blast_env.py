import time
import pygame 
import random
import ai 

class Block:
    def __init__(self,state:bool,pos:tuple,board_size,screen_size=(500,500)):
        margin = 90
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
        self.block_chossen = 0
        self.board = {}
        self.screen_size = (500,500)
        self.screen = pygame.display.set_mode(self.screen_size)
        #self.screen = pygame.display.set_mode((1000,1000))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial",30) 
        self.score = 0
        self.blocks = ["xoxoxoxo","xxxx","xxxoxxxoxxx","xxxoxxx","xoxoxxx","xoxoxx"]
        self.current_blocks = []
        self.block_count = 3
        for x in range(self.size): 
            for y in range(self.size):
                choice = random.choice([False]) 
                self.board[(x,y)] = Block(choice,(x,y),self.size,self.screen_size)

        pygame.init()

    def get_rows_and_colums_to_clear(self):
        rows_to_clear = [row for row in range(self.size) if sum(self.board[(row, block)].state for block in range(self.size)) >= self.size]
        cols_to_clear = [col for col in range(self.size) if sum(self.board[(block, col)].state for block in range(self.size)) >= self.size]

        return rows_to_clear,cols_to_clear,len(rows_to_clear) * self.size + len(cols_to_clear) * self.size

    def clear_rows_and_columns(self,rows,cols):
        # Clear rows
        for row in rows:
            for block in range(self.size):
                self.board[(row, block)].set(False)

        # Clear columns
        for col in cols:
            for block in range(self.size):
                self.board[(block, col)].set(False)

    def give_blocks(self):
        self.current_blocks = [random.choice(self.blocks) for _ in range(self.block_count)]
        
    def draw(self):
            self.screen.fill("black")
            score_text = self.font.render(f"Score: {self.score}", False, (255,255,255))

            self.screen.blit(score_text,(20,0))
            
            for block in self.board:
                block = self.board[block]
                self.screen.blit(block.image,block.rect)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {str(self.clock.get_fps())}")

    def check_blocks_eh(self,block:str,pos):
        # split into lines and check collison
        lines = block.split("o")

        x = 0
        y = 0
        pos_to_replace = []
        for line in lines:
            x = 0
            for xl in line:
                new_x = pos[0] + x
                new_y = pos[1] + y

                # Check if the calculated position is within board bounds
                if (new_x,new_y) in self.board:
                    if self.board[(new_x,new_y)].state == True:
                        print("at least 1 spot is full")
                        return
                else:
                    print(f"Position out of bounds: ({new_x}, {new_y})")
                    return

                pos_to_replace.append((new_x,new_y))
                x+=1
            y+=1

        for posa in pos_to_replace:
            self.board[posa].set(True)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                good_sprite = [self.board[block] for block in self.board if self.board[block].rect.collidepoint(pos)] 

                keys = pygame.key.get_mods()
                lshift_held = keys & pygame.KMOD_LSHIFT
                for a in good_sprite:
                    if lshift_held:
                        a.set(not a.state)
                        continue
                    self.check_blocks_eh(self.current_blocks[self.block_chossen], a.pos)
                    self.current_blocks.pop(self.block_chossen)
    def reset(self):  
        self.current_blocks.clear()
        self.score = 0
        for pos, block in self.board.items():
            if block.state:  # Only reset filled blocks
                block.set(False)
        
    def is_valid_move(self, block, pos):
        lines = block.split("o")
        x, y = pos

        for line_index, line in enumerate(lines):
            for char_index, char in enumerate(line):
                check_x = x + char_index
                check_y = y + line_index

                if check_x < 0 or check_x >= self.size or check_y < 0 or check_y >= self.size:
                    return False

                # Check if position is already filled
                if (check_x, check_y) in self.board and self.board[(check_x, check_y)].state:
                    return False
        return True
    def run(self,mode="human"):
        while self.running:
            if len(self.current_blocks) <= 0:
                self.give_blocks()

            rows,cols,score = self.get_rows_and_colums_to_clear()
            self.clear_rows_and_columns(rows,cols)
            self.score += score
            if mode == "human":
                self.draw() 
                self.events()
            if mode == "ai":
                self.draw() 
                ai.ai_play(self)
                time.sleep(0.5)
            
            move_found = False  
            empty_spots = [pos for pos in self.board if not self.board[pos].state]

            for piece in self.current_blocks:
                for pos in empty_spots:  
                    if self.is_valid_move(piece, pos):
                        move_found = True
                        break
                if move_found:
                    break  

            if not move_found:
                print(f"Game Over! Final Score: {self.score}")
                pygame.time.delay(1000)  # Small delay before resetting
                self.reset()
        self.clock.tick(60) 

        pygame.quit()
