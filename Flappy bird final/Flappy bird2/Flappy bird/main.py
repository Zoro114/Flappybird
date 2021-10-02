import pygame,random,sys
from pygame.constants import *
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)

def create_pipe():
    random_pipe_height=random.choice(pipe_heights)
    bottom_pipe=pipe_surface.get_rect(midtop=(300,random_pipe_height))
    top_pipe=pipe_surface.get_rect(midtop=(300,random_pipe_height-450))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=1
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=460:
            window.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            window.blit(flip_pipe,pipe)
    return pipes

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            maingame_sound.stop()
            return False
        
    if bird_rect.top<=-100 or bird_rect.bottom>=512:
        maingame_sound.stop()
        return False
        
    return True

def rotate_bird(Bird):
    new_bird=pygame.transform.rotozoom(Bird,bird_movement*-10,1)
    return new_bird

def bird_animation():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(50,bird_rect.centery))
    return new_bird,new_bird_rect

def background():
    if score<=30:
        window.blit(background_day,(0,0))
    else:
        window.blit(background_night,(0,0))

def display_score(game_state):
    if game_state=="carry_on":
        
        score_surface=game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surface.get_rect(center=(144,50))
        window.blit(score_surface,score_rect)
    
    elif game_state=="game_over":

        score_surface=game_font.render("SCORE : "+str(int(score)),True,(0,255,0))
        score_rect=score_surface.get_rect(center=(144,30))
        window.blit(score_surface,score_rect)

        game_over_screen()
    
        high_score_surface=game_font.render("HIGH SCORE : "+str(int(High_score)),True,(255,0,0))
        high_score_rect=high_score_surface.get_rect(center=(144,380))
        window.blit(high_score_surface,high_score_rect)

def main_screen():

    window.blit(message,(50,50))
def game_over_screen():
    window.blit(game_over,(50,200))

def get_high_score():

    high_score=0
    high_score_file = open("high_score.txt", "r")
    high_score = int(float(high_score_file.read()))
    high_score_file.close()
    return high_score

def save_high_score(new_high_score):
    high_score_file = open("high_score.txt", "w")
    high_score_file.write(str(int(new_high_score)))
    high_score_file.close()

window =pygame.display.set_mode((288,512))
caption=pygame.display.set_caption("Flappy bird CP project")

logo=pygame.image.load("favicon.ico")
pygame.display.set_icon(logo)
clock=pygame.time.Clock()
game_font=pygame.font.Font(None,40)

background_day=pygame.image.load("background-day.png").convert()
background_night=pygame.image.load("background-night.png").convert()
message=pygame.image.load("message.png").convert()
game_over=pygame.image.load("gameover.png").convert_alpha()
base = pygame.image.load("base.png").convert()
base_x=0

bird_downflap=pygame.image.load("bluebird-downflap.png").convert_alpha()
bird_midflap=pygame.image.load("bluebird-midflap.png").convert_alpha()
bird_upflap=pygame.image.load("bluebird-upflap.png").convert_alpha()
bird_frames=[bird_upflap,bird_midflap,bird_downflap]
bird_index=0
bird=bird_frames[bird_index]
bird_rect=bird.get_rect(center=(50,200))
bird_movement=0
BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,100)

pipe_surface=pygame.image.load("pipe-green.png").convert()
pipe_list=[]
pipe_heights=[180,250,350]
SPAWN_PIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE,1400)

gravity=0.05
game_active=False
score=0
High_score=0
fps=190
clock=pygame.time.Clock()

maingame_sound=pygame.mixer.Sound("Super Mario Bros. medley.ogg")
gameover_sound=pygame.mixer.Sound("smb_gameover.wav")
collision_sound=pygame.mixer.Sound("hit.ogg")
jump_sound=pygame.mixer.Sound("smb_jump-small.wav")
while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP and game_active:
                bird_movement=0
                bird_movement-=2
                jump_sound.play()

            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,200)
                bird_movement=0
                score=0
                maingame_sound.play()
                gameover_sound.stop()
    
        if event.type==SPAWN_PIPE:
            pipe_list.extend(create_pipe())
        
        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,bird_rect=bird_animation()

    High_score=get_high_score()
    background()    
# Base movement            
    base_x=base_x-1
    if base_x<=-288:
        base_x=0

    game_active=check_collision(pipe_list)
    if game_active:
            
    # pipe movement
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # bird movement
        rotated_bird=rotate_bird(bird)
        bird_movement+=gravity
        bird_rect.centery+=bird_movement

        window.blit(rotated_bird,bird_rect)
        score+=0.01
        maingame_sound.play(-1)

    
        display_score("carry_on")
        if score>High_score:
            save_high_score(score)
                 
    else:
        display_score("game_over")
        gameover_sound.play()

    window.blit(base,(base_x ,400))
    window.blit(base,(base_x +288,400))


    pygame.display.update()
    

pygame.quit()
