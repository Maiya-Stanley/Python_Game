import pygame
import random
from pygame import mixer
import os
import json
import sys
from random import choice
from pygame.locals import *
import csv

mixer.init()
pygame.init()

mixer.music.load('background.wav')
mixer.music.play(-1)


flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags, 16)
screen_rect = screen.get_rect()

background =pygame.image.load(os.path.join('white_background.png')).convert_alpha()
spaceshipimg=pygame.image.load(os.path.join('spaceship.png')).convert_alpha()

alienimg=pygame.image.load(os.path.join('alien1.png')).convert_alpha()

bulletimg=pygame.image.load(os.path.join('bullet2.png')).convert_alpha()

json_list = """{
                "1":
                [
                    {
                    "ID":1,
                    "Question":"Question 1: How many people work for Santander UK?",
                    "Answer":"23500",
                    "Options":["3100","7200","13000","23500","25400"]
                    },

                    {
                    "ID":2,
                   "Question":"Question 2: Where did Santander originate?",
                    "Answer":"Spain",
                    "Options":["Greece","Spain","United States","France","Germany"]
                    },
                    
                    {
                    "ID":3,
                    "Question":"Question 3: How many active customers does Santander UK have?",
                    "Answer":"14 million",
                    "Options":["3 million","5 million","8 million","11 million","14 million"]
                    },

                    {
                    "ID":4,
                    "Question":"Question 4: When was Santander UK founded?",
                    "Answer":"2010",
                    "Options":["2010","2004","2009","1995","2014"]
                    },

                    {
                    "ID":5,
                    "Question":"Question 5: Who is the CEO of Santander UK?",
                    "Answer":"Mike Regnier",
                    "Options":["Mike Regnier","Reena Varu","Danielle Bodimeade","Enrique Alvarez","Ana Botin"]
                    }
                    ],

                    
                    "2":
                    [
                    {
                    "ID":1,
                    "Question":"Question 1: How many branches does Santander UK have?",
                    "Answer":"449",
                    "Options":["271","107","348","449","512"]
                    },

                    {
                    "ID":2,
                    "Question":"Question 2: What is the new Santander UK headquarters called?",
                    "Answer":"Unity Place",
                    "Options":["Unity Place","Santander Tower","Prosper Point","Santander House","The Centre"]
                   },

                    {
                    "ID":3,
                    "Question":"Question 3: How many countries is Santander in?",
                    "Answer":"25",
                    "Options":["16","7","29","25","32"]
                    },

                    {
                    "ID":4,
                    "Question":"Question 4: Who has not been an ambassador for Santander UK?",
                    "Answer":"Andy Murray",
                    "Options":["Ant & Dec","Jessica Ennis","Jenson Button","Andy Murray","Rory McIlroy"]
                    },

                    {
                    "ID":5,
                    "Question":"Question 5: What F1 team does Santander Group sponsor?",
                    "Answer":"Ferrari",
                    "Options":["Red Bull Racing","Aston Martin","Ferrari","Williams Racing","Mercedes"]
                    }
                ],
                "3":
                [
                    {
                    "ID":1,
                    "Question":"Question 1: Where is Santander UK's new Headquarters located?",
                    "Answer":"Milton Keynes",
                    "Options":["Milton Keynes","London","Birmingham","Luton","Liverpool"]
                    },
                
                    {
                    "ID":2,
                    "Question":"Question 2:How many ATMs does Santander have across the US?",
                    "Answer":"2000",
                    "Options":["300","800","1200","2000","2400"]
                    },

                    {
                    "ID":3,
                    "Question":"Question 3: What is Santander UK's newest banking product called?",
                    "Answer":"Edge",
                    "Options":["Curve","Edge","Brink","Verge","Twist"]
                    },

                    {
                    "ID":4,
                    "Question":"Question 4: What is not a specialism on the DTS Apprenticeship Scheme?",
                    "Answer":"Project Management",
                    "Options":["Data Analytics","Cyber Security","Network Engineering","Software Engineering","Project Management"]
                    },

                    {
                    "ID":5,
                    "Question":"Question 5: What is the percentage of women employees across Santander globally?",
                    "Answer":"54%",
                    "Options":["22%","54%","33%","62%","47%"]
                    }
                    ]
            }"""


questions = json.loads(json_list)

answerlist = []
bulletlist = []
alienlist = []
target_surf_list = []
target_rect_list = []
destroylist = []
gameround = 0
newround = True
score=0
spaceship_loc = screen_rect.midbottom
spaceshipX=int(spaceship_loc[0])
spaceshipY=int(spaceship_loc[1]-150)
bulletX=(spaceshipX)
bulletY=(spaceshipY)
rand_int = random.randint(1,3)
rand_question = str(rand_int)

changeX=0
running=True
pygame.mouse.set_visible(False)
game_over = False
bullet_removed_answer = False
exit_game = False
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

font=pygame.font.Font(os.path.join('arcade.regular.ttf'),32)
instruction_font = pygame.font.Font(os.path.join('arcade.regular.ttf'),24)
gameover_font=pygame.font.Font(os.path.join('arcade.regular.ttf'),60)


black = (0,0,0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255,0,0)


#with open('engagement.csv', "r") as f:
 #   row = []
  #  row.append(f.readline())
   # games_played = int(row[0])

#f.close()
    
    


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.x = x
        self.y = bulletY

        self.image = bulletimg

        screen.blit(self.image, (x, bulletY))
            


    def update(self):

        self.y = self.y - 2
        
        screen.blit(self.image, (self.x, self.y))

    def getY(self):
        return self.y

    def checkCollisions(self):
        
        global score
        global gameround
        global newround
        global destroylist

        self.rect = pygame.Rect(self.x, self.y, 27, 53)

        for answer in answerlist:
            if self.rect.colliderect(answer.getRect()):
                if answer.isCorrect():
                    newround = True
                    gameround += 1
                    score += 50
                    answerlist.clear()
                else:
                    answerlist.remove(answer)
                    score -= 10

                destroylist.append(self)
                

        for alien in alienlist:
            if self.rect.colliderect(alien.getRect()):
                score += 25
                alienlist.remove(alien)
                destroylist.append(self)
  

    
       
class Answer(pygame.sprite.Sprite):
    def __init__(self, x, y, text, correct):
        super().__init__()

        self.x = x
        self.y = y
        self.correct = correct
        self.image_answer = font.render(text, True, red)

        self.width = self.image_answer.get_width()
        self.height = self.image_answer.get_height()
        
        screen.blit(self.image_answer, (self.x, self.y))

        self.speed = round(random.uniform(0.2,1), 3)
                       
    def update(self):
        self.x += self.speed
        if self.x <= 0:
            self.speed = round(random.uniform(0.2,1), 3)
            self.y += 30
        if self.x >= (screen_rect.right-75):
            self.speed = round(random.uniform(-0.2,-1), 3)
            self.y += 30

        
        screen.blit(self.image_answer, (self.x, self.y))

    def getY(self):
        return self.y

    def isCorrect(self):
        return self.correct

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)



def generate_answers(gameround):
    if gameround <= 4:
        for answer_option in questions[rand_question][gameround]["Options"]:
            bulletlist.clear()
            if answer_option == questions[rand_question][gameround]["Answer"]:
                answerlist.append(Answer(random.randint(1,(screen_rect.right-200)), random.randint(50,150), answer_option, True))
            else:
                answerlist.append(Answer(random.randint(1,(screen_rect.right-200)), random.randint(50,150), answer_option, False))
    else:
        end()


       
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.image_alien = alienimg
        screen.blit(self.image_alien, (x, y))
        self.width = self.image_alien.get_width()
        self.height = self.image_alien.get_height()

        self.speed = round(random.uniform(0.5,1.5), 3)
                       
    def update(self):
        self.x += self.speed
        if self.x <= 0:
            self.speed = round(random.uniform(0.5,1.5), 3)
            self.y += 50
        if self.x >= (screen_rect.right-75):
            self.speed = round(random.uniform(-0.5,-1.5), 3)
            self.y += 50

        
        screen.blit(self.image_alien, (self.x, self.y))

    def getY(self):
        return self.y


    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def generate_aliens():
    i = 1
    if len(alienlist) < 4:
        while i < 3:
            x_int = int(random.randint(1,(screen_rect.right-200)))
            y_int = random.randint(50,200)
            alienlist.append(Alien(x_int, y_int))
            i += 1
       


def score_text():
    img=font.render(f'Score: {score}', True, red)
    screen.blit(img,(10,10))


def gameover():
    global score, gameround, newround, game_over, rand_question, rand_int
    #games_played

    hold = True

    while hold == True:

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    hold = False
                    gameround = 0
                    newround = True
                    game_over = False
                    bulletlist.clear()
                    alienlist.clear()
                    answerlist.clear()
                    score=0
                    rand_int_orig = rand_int
                    rand_int = choice([i for i in range(1,3) if i not in [rand_int_orig]])
                    rand_question = str(rand_int)
                    #with open("engagement.csv", 'w') as f:
                        #writer = csv.writer(f)
                        #total = str(games_played)
                        #writer.writerow([games_played])
                    start()
                    gameloop()
                    bulletlist.clear()


        background=pygame.image.load(os.path.join('black_background.png')).convert_alpha()
        screen.blit(background,(0,0))
        
        img_gameover = gameover_font.render('GAME OVER', True, red)
        screen.blit(img_gameover, img_gameover.get_rect(center=screen_rect.center))

        final_score=font.render(f'Final Score: {score}', True, white)
        screen_x = (final_score.get_rect(center=screen_rect.center)[0])
        screen_y = int(screen.get_height()/3)
        screen.blit(final_score, (screen_x, screen_y))

        img_play = font.render('PRESS ENTER TO RESTART', True, white)
        midbottom = img_play.get_rect(midbottom=screen_rect.midbottom)
        screen.blit(img_play, (midbottom[0], (midbottom[1]-100), midbottom[2], midbottom[3]))

        
        pygame.display.update()
        


def end():

    global score, gameround, newround, rand_question, rand_int
    #games_played

    hold = True

    while hold == True:

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    hold = False
                    gameround = 0
                    newround = True
                    bulletlist.clear()
                    alienlist.clear()
                    answerlist.clear()
                    score=0
                    rand_int_orig = rand_int
                    rand_int = choice([i for i in range(1,3) if i not in [rand_int_orig]])
                    rand_question = str(rand_int)
                   # with open("engagement.csv", 'w') as f:
                    #    writer = csv.writer(f)
                        #total = str(games_played)
                     #   writer.writerow([games_played])
                    start()
                    gameloop()
                    bulletlist.clear()
                   
        
        background=pygame.image.load(os.path.join('black_background.png')).convert_alpha()
        screen.blit(background,(0,0))
        
        img_gameover = gameover_font.render('THE END', True, green)
        screen.blit(img_gameover, img_gameover.get_rect(center=screen_rect.center))

        final_score=font.render(f'Final Score: {score}', True, white)
        screen_x = (final_score.get_rect(center=screen_rect.center)[0])
        screen_y = int(screen.get_height()/3)
        screen.blit(final_score, (screen_x, screen_y))

        img_play = font.render('PRESS ENTER TO RESTART', True, white)
        midbottom = img_play.get_rect(midbottom=screen_rect.midbottom)
        screen.blit(img_play, (midbottom[0], (midbottom[1]-100), midbottom[2], midbottom[3]))

        pygame.display.update()

        



def start():

    hold = True

    while hold == True:

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    hold = False
            
        background_start=pygame.image.load(os.path.join('black_background.png')).convert_alpha()
        screen.blit(background_start,(0,0))
                
        img_start = font.render('THE SANTANDER QUIZ', True, white)
        midtop = img_start.get_rect(midtop=screen_rect.midtop)
        screen.blit(img_start, (midtop[0], (midtop[1]+100), midtop[2], midtop[3]))

        instruction1 = "- Use the Left and Right Arrow Keys to move your spaceship and spacebar to shoot."
        instruction2 = "- Shoot the correct answer to the question."
        instruction3 = "- 50 points for the correct answer. Minus 10 points for the wrong answer."
        instruction4 = "- Each alien shot will add 25 points to your score."
        instruction5 = "- If an alien or an answer reach the bottom of the screen, you will lose the game."
        formatted_instruction1 = instruction_font.render(instruction1, True, white)
        formatted_instruction2 = instruction_font.render(instruction2, True, white)
        formatted_instruction3 = instruction_font.render(instruction3, True, white)
        formatted_instruction4 = instruction_font.render(instruction4, True, white)
        formatted_instruction5 = instruction_font.render(instruction5, True, white)
        midleft = formatted_instruction1.get_rect(midleft=screen_rect.midleft)
        screen.blit(formatted_instruction5, ((midleft[0]+150), (midleft[1]+100), midleft[2], midleft[3]))
        screen.blit(formatted_instruction4, ((midleft[0]+150), (midleft[1]+50), midleft[2], midleft[3]))
        screen.blit(formatted_instruction3, ((midleft[0])+150, (midleft[1]+0), midleft[2], midleft[3]))
        screen.blit(formatted_instruction2, ((midleft[0])+150, (midleft[1]-50), midleft[2], midleft[3]))
        screen.blit(formatted_instruction1, ((midleft[0])+150, (midleft[1]-100), midleft[2], midleft[3]))

        img_play = font.render('PRESS ENTER TO PLAY', True, white)
        midbottom = img_play.get_rect(midbottom=screen_rect.midbottom)
        screen.blit(img_play, (midbottom[0], (midbottom[1]-100), midbottom[2], midbottom[3]))

        pygame.display.update()

def gameloop():

    global spaceshipX, spaceshipY, changeX, changeY, newround, game_over, rand_question
    #games_played

    #games_played += 1
    running=True

    while running == True:
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.type==pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running=False
                    exit_game = True
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_LEFT]:
                    changeX=-3
                if keys[pygame.K_RIGHT]:
                    changeX=3
                if keys[pygame.K_SPACE]:
                    if len(bulletlist) < 5:
                        bulletSound=mixer.Sound('laser.wav')
                        bulletSound.play()
                        bulletlist.append(Bullet(spaceshipX+29))

            if event.type==pygame.KEYUP:
                changeX=0
        spaceshipX+=changeX  
        if spaceshipX<=0:
            spaceshipX=0
        elif spaceshipX>=(screen_rect.right-75):
            spaceshipX=(screen_rect.right-75)
      
        for answer in answerlist:
            if answer.getY() > (screen_rect.bottom-150):
                game_over = True
                gameover()
                break
            answer.update()


        for alien in alienlist:
            if alien.getY() > (screen_rect.bottom-150):
                game_over = True
                gameover()
                break
            alien.update()
            

        for bullet in bulletlist:
            bullet.update()
            bullet.checkCollisions()

            if bullet.getY() < 0:
                destroylist.append(bullet)
   

        if newround == True:
            generate_answers(gameround)
            generate_aliens()
            newround = False

        if gameround <= 4 and game_over == False:
            image_question = font.render(questions[rand_question][gameround]["Question"], True, red)
            screen.blit(image_question, image_question.get_rect(midbottom=screen_rect.midbottom))
            screen.blit(spaceshipimg, (spaceshipX, spaceshipY))
            score_text()
            pygame.display.update()

            
        for bullet in destroylist:
            if bullet in bulletlist:
                bulletlist.remove(bullet)

        destroylist.clear()

if exit_game == True:
    pygame.display.quit()
    pygame.quit()
    sys.exit()
else:
    start()
    gameloop()
