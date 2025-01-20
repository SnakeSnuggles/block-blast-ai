import time
import pygame 
import random


# env = block_blast_env()
# 
# model = PPO("MlpPolicy", env, verbose=1)
# 
# model.learn(total_timesteps=10000)
# 
# obs, _ = env.reset()
# 
# for _ in range(20):
#     action, _ = model.predict(obs, deterministic=True)  # Predict optimal action
#     obs, reward, done, _, _ = env.step(action)
#     env.render()
#     if done:
#         break
# 
# env.close()


'''
GOALS: 
    create a window with a grid (8x8)
'''

pygame.init()




'''
GOALS: 
    GET MOUSE DETECTION TO WORK 
    BE ABLE TO CHANGE THE DIFFERENT GRID PLACES
    MAYBE GET LINE CLEARS

'''
class Block:
    def __init__(self,image_path:str,pos:tuple):
        size_image = (50,50)
        self.image = pygame.image.load(image_path)
        self.pos = pos
        self.image = pygame.transform.scale(self.image,size_image)

        self.image_rect = self.image.get_rect()
   
    def change_state(self):
        ...

    def move(self,x,y):
        self.image_rect.move(x,y)


class Block_Blast:
    def __init__(self):
        self.size = 8
        self.board = [[random.choice([True,False]) for x in range(self.size)] for y in range(self.size)] 
        self.screen = pygame.display.set_mode((450, 510))
        #self.screen = pygame.display.set_mode((1000,1000))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial",30) 
        self.score = 0

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER YOUR GAME HERE
            # box = pygame.Rect(20,20,50,50)
            # pygame.draw.rect(self.screen, "black", box)
            
            score_text = self.font.render(f"Score: {self.score}", False, (255,255,255))

            self.screen.blit(score_text,(20,0))
            

            blocks_ = []
            for x in range(self.size):
                for y in range(self.size):
                    block = Block("error_block.png",(x,y)) 
                    if self.board[x][y] == False:
                        block = Block("empty_block.png",(x,y))
                    elif self.board[x][y] == True:
                        block = Block("filled_block.png",(x,y))

                    blocks_.append(block)
                    self.screen.blit(block.image,block.image_rect.move(x*50+20,y*50+55))
            



            # flip() the display to put your work on screen
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {str(self.clock.get_fps())}")
            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


game = Block_Blast()

game.run()
