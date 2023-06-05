import pygame
import random
from sys import exit
import  csv

score=0
pygame.init()
window_width = 800
window_height = 800
icon = pygame.image.load("assets/icon.ico")


window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Acceleration Racer")
pygame.display.set_icon(icon)

#functions
def load_high_score():
    try:
        with open('score.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                return int(row[0])
    except FileNotFoundError:
        return 0

def save_high_score(high_score):
    scores = []
    try:
        with open('score.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                scores.append(int(row[0]))
    except FileNotFoundError:
        pass

    scores.append(high_score)

    with open('score.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(max(scores))])

high_score = load_high_score()
menuu=pygame.image.load("assets/menu.png")
menu=pygame.transform.scale(menuu, (800,800))
gamemusic=pygame.mixer.Sound("assets/game.mp3")


def game(score):
    global high_score
    #car vars

    
    cx = 400
    cy = 800-300
    clock = pygame.time.Clock()

    carimg=pygame.image.load('assets/car.png')
    car1=pygame.transform.scale(carimg,(200,250))
    car= pygame.transform.flip(car1, False, True) # to upside down the car cuz it was upside down for some reason 🤷‍♂️
    carspeed=3
    # barriers
    barrierh =200
    barrierx = random.randint(0,600)
    barriery =-500 #how far it is at start
    barriers = 3 # speed
    barrierw=105 #width
    barrier2=pygame.image.load('assets/barrier.png')
    barrier=pygame.transform.scale(barrier2,(barrierw,barrierh))
    

    background=pygame.image.load("assets/background.png")
    bg=pygame.transform.scale(background, (800,800))
    running = True
    clock = pygame.time.Clock()

    righttrigger=False
    lefttrigger=False
    while running:
        gamemusic.play()
        if lefttrigger:
            cx-=carspeed
        elif righttrigger:
            cx+=carspeed       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    lefttrigger=True
                if event.key==pygame.K_RIGHT:
                    righttrigger=True
                if event.key==pygame.K_ESCAPE:
                    running=False
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    lefttrigger=False
                if event.key==pygame.K_RIGHT:
                    righttrigger=False
                
        current_fps = clock.get_fps()

   
        barriery += barriers

        
        if cx - 20 < barrierx + barrierw and cx +180 > barrierx and cy < barriery + barrierh and cy + 250 > barriery:
            running=False
            exit()
        elif cx>535: cx=534
        elif cx<71: cx=72

        
        if barriery > 800:
                score+=1
                carspeed+=0.5
                barriers+=1
                barrierx = random.randint(135,450)
                barriery = -barrierh

        #all the drawing and blitting and window stuff
        window.fill((67, 97, 238))
        window.blit(bg,(0,0))
        window.blit(car,(cx,cy))
        window.blit(barrier,(barrierx,barriery))
        window.blit((pygame.font.SysFont("Arial",25)).render("X:"+str(cx),True,(255,236,255)),(0,0))
        window.blit((pygame.font.SysFont("Arial",25)).render("Fps:"+str(int(current_fps)),True,(255,236,255)),(60,0))
        window.blit((pygame.font.SysFont("Arial",25)).render("Current score:"+str(score),True,(255,255,255)),(0,40))
        window.blit((pygame.font.SysFont("Arial",25)).render("Current High score:"+str(high_score),True,(255,255,255)),(0,90))

        pygame.draw.rect(window, (202, 100, 23), pygame.Rect(barrierx, barriery, barrierw , barrierh), 2)
        pygame.draw.rect(window, (202, 100, 23), pygame.Rect(cx,cy,200,250), 2)
        clock.tick(90)

        if high_score < score:
            high_score = score
        save_high_score(high_score)

        pygame.display.update()
    running=False


#back to main thing
running = True
menusong=pygame.mixer.Sound("assets/menu.mp3")
clock = pygame.time.Clock()
print("Thank you for playing one of my first 20 games made.I hope you have a good time playing")
while running:
    window.fill((255, 255, 255))
    menusong.play()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                menusong.stop()
                game(score)
    window.blit(menu, (0, 0))
    window.blit((pygame.font.SysFont("Arial",75)).render(f'{high_score}',True,(250,250,250)),(600,250))
    pygame.display.update()
pygame.quit()