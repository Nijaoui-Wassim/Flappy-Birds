#space invader (ship and bullets)
import math
import random
import pygame
from pygame import mixer

#initializing pygame
pygame.init()

#change number of pipes
num_of_pipes = 100
#change player speed
step = 1.9*2
speed_pipe = 1.9*2
another_pipe = False
collision_p = False
# score 
score_value = 0
font = pygame.font.Font("assets//Sportive-Regular.ttf", 32)
font2 = pygame.font.Font("assets//font2.otf", 100)

#font size
TextX = 10
TextY = 10

#creating game window
screen_w = 800
screen_h = 600
screen = pygame.display.set_mode((screen_w,screen_h))


#change title
pygame.display.set_caption("Flappy Bird")

#change icon
icon = pygame.image.load("assets//bird_fly.png") #define icon

pygame.display.set_icon(icon)             #set the icon


#rocket icon from Flaticon by Freepik
#add player
bird_fly = pygame.image.load("assets//bird_fly.png") #define player
bird_rest = pygame.image.load("assets//bird_rest.png") #define player


pipe_h = 642
pipe_w = 67

#Load background image
bg = pygame.image.load("assets//background.jpg")
#Load background music
mixer.music.load("assets//bck_music.mp3")
mixer.music.play(-1)



PlayerX = 50
PlayerY = screen_h/2 + 15
dead_or_alive = "alive"

#Load bullet image
bulletIMG = pygame.image.load("assets//bullet_24.png")

jump_state = "ready"
bullet_sound = mixer.Sound("assets//laser1.wav")
death_sound = mixer.Sound("assets//die.wav")

#ready means bullet is invisible
#fire means bullets are firing

#add pipes

up_pipe = pygame.image.load("assets//upper.png") #define up pipe image
low_pipe = pygame.image.load("assets//lower.png") #define low pipe image

pipe_states = []
pipe_X = []
pipe_Y =[]
pipe_X_change = []
pipe_Y_change = []

for i in range(num_of_pipes):
    if i == 0 :
        pipe_states.append("show")
        pipe_X.append(screen_w)
        pipe_Y.append(random.randint(40,150))
        pipe_X_change.append(0.3)
        pipe_Y_change.append(random.randint(-50,50))
    else:
        pipe_states.append("hide")
        pipe_X.append(-100)
        pipe_Y.append(0)
        pipe_X_change.append(0)
        pipe_Y_change.append(0)

stepY = 0.5*2


def game_over(x,y):
    screen.fill((255,255,255,0.5)) #change background color - RGB
    game_o = font2.render("GAME OVER",True, (0, 0, 0))
    screen.blit(game_o, (x, y))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def fire_jump():
    global jump_state, PlayerY,PlayerX
    jump_state = "jump"
    screen.blit(bird_rest, (PlayerX, PlayerY))
    PlayerY-= 14


def player(x,y,s):
    if s == 0:
        screen.blit(bird_rest,(x,y))
    if s == 1:
        screen.blit(bird_fly,(x,y))

def pipes(Img, x,y):
    screen.blit(Img,(x,y))
    
def isCollision(x_e, y_e, x_b, y_b):
    distance = math.sqrt(math.pow(x_e-x_b,2) + math.pow(y_e-y_b,2))
    #distance = y_b - y_e
    if distance < 5:
        return True
    else:
        return False
#closing window - add quit event
running = True

while running:
    
    #screen.fill((255,155,10)) #change background color - RGB
    #INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))
    
    for event in pygame.event.get():      #get all user events
        try:
            if event.type == pygame.QUIT:     # pressing the close button = Pygame.Quit
                running = False               #quit the window
                pygame.display.quit()
                pygame.quit()
                break
            #get keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if jump_state == "ready":
                        fire_jump()
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_SPACE):
                    jump_state = "ready"
                    PlayerY += 0.0002*4
                    
        except Exception as e:
            print(e)
        
    #anything that you want to stay inside thescreen need to be inside the while loop
 
    try:  
        PlayerY += stepY
        
        #keep the bird inside the screen
        if (PlayerY >= screen_h-70):   #bottom side
            PlayerY = screen_h-70 
        if (PlayerY <= 10):            #up side
            PlayerY = 10
            
        #show player
        if dead_or_alive == "alive":
            player(PlayerX,PlayerY, 1) #call it after fill because order matters
        else:
            game_over((screen_w/2)-120, (screen_h/2)-40)
        
        #collision
        
        for i in range(num_of_pipes):   
            
            if pipe_X[i] <= 2*screen_w/3 :
                pipe_X[i] -= pipe_X_change[i]
                another_pipe = True

            else:
                pipe_X[i] -= pipe_X_change[i]
            if another_pipe:
                try:
                    another_pipe = False 
                    pipe_states[i+1] = "show"
                    pipe_X[i+1] = screen_w
                    pipe_Y[i+1] = random.randint(40,150)
                    pipe_X_change[i+1] = 0.3
                    pipe_Y_change[i+1] = random.randint(-50,50)
                except:
                    pass
                
            if pipe_states[i] == 'show':
                pipes(up_pipe, pipe_X[i],pipe_Y_change[i]-pipe_h/2-100)
                pipes(low_pipe, pipe_X[i],screen_w-pipe_h/2+pipe_Y_change[i]-100)

            temp_h = pipe_h+pipe_Y_change[i]-120-64-64
#             pygame.draw.rect(screen, [255, 0, 0], [pipe_X[i], temp_h , 64, -170], 0)
            
            rect_player = pygame.Rect(50,PlayerY,64,64) #player
            temp_hh=temp_h-170
            rect_pipe_up   = pygame.Rect(pipe_X[i],  0, 64, temp_hh+20) 
            rect_pipe_down = pygame.Rect(pipe_X[i], temp_h-20 , 64, screen_h-temp_h)  
            
#             pygame.draw.rect(screen, [255, 0, 0], rect_player, 0)
#             pygame.draw.rect(screen, [0, 255, 0], rect_pipe_up, 0)
#             pygame.draw.rect(screen, [0, 255, 0], rect_pipe_down, 0)

            collideTest2 = rect_player.colliderect(rect_pipe_down)        
            collideTest1 = rect_player.colliderect(rect_pipe_up)
                
            if (collideTest1 >0 or collideTest2 >0):
                collision_p = True
            if collision_p:
                death_sound.play()
                dead_or_alive = "dead"
                PlayerX = 50
                PlayerY = 480               
                for j in range(num_of_pipes):   
                    pipe_states[j] = 'hide'              
        #making bullet ready for firing again
        #bullet movement
        if jump_state == "jump" :
            bullet_sound.play()
            fire_jump()
        else:
            PlayerY += 0.0002*4           

        score_value += 1        
        #show scare
        show_score(TextX, TextY)
        pygame.display.update()   #to update screen
    except Exception as e:
        print(e)
