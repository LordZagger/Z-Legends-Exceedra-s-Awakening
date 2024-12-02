#Made by LordZagger and {jin username}

#import modules
import pygame
from random import choice
from random import randrange

#init pygame and pygame.mixer
pygame.init()

#classes
#The real first thing is to define a basic class for every character. Characters can then be created by variables to a class call
class Character:
    '''
    This class contains variables related to them for the battle system, such as health, recovery and energy and attack potential stats
    Has variables for the name, stats and moves of a character.
    Health is the amount of HP (aka life/hit points) a character has. it's how they stay alive, until health is reduce to 0, at which point they die
    Recovery is to determine the amount of energy and health a character will recover when using that move
    Energy is the amount of energy a character has to use a move. it's a special stat that helps prevent spamming of a single attack, and so requires players to have a strategy
    Attack potential is a special stat that helps determine which attack lands in a pinch
    battle_pic is the character's png image (image name) for battles, optional argument
    og stands for original, those variables help reset the characters stats in the reset method
    '''
    def __init__(self, name, health, energy, attack_potential, AttackMove, GuardMove, RecoverMove, battle_pic=None):
        '''
        initialize a character
        '''
        self.name = name
        self.health = health
        self.energy = energy
        self.attack_potential = attack_potential
        self.AttackMove = AttackMove
        self.GuardMove = GuardMove
        self.RecoverMove = RecoverMove
        self.battle_pic = battle_pic
        
        self.og_name = name
        self.og_health = health
        self.og_energy = energy
        self.og_attack_potential = attack_potential
        self.og_AttackMove = AttackMove
        self.og_GuardMove = GuardMove
        self.og_RecoverMove = RecoverMove
        self.og_battle_pic = battle_pic
        
        self.movepool = [AttackMove, GuardMove, RecoverMove]
    
    def reset(self):
        '''reset a character's stats by returning a character of the original stats'''
        return Character(self.og_name,self.og_health,self.og_energy,self.og_attack_potential,self.og_AttackMove,self.og_GuardMove,self.og_RecoverMove,battle_pic=self.og_battle_pic)
    
    def losePower(self,health_amount,energy_amount):
        '''
        during a battle, a character loses health and/or energy after using/taking a move
        '''
        self.health -= health_amount
        self.energy -= energy_amount
    
    def Recover(self,amount):
        '''
        during a battle, when successfully using Recover, a character regains 
        health and energt
        '''
        self.health += 2*amount
        self.energy += amount
    
    def randomMove(self):
        '''
        during a battle, the npc chooses a random move
        '''
        return choice(self.movepool)
    
    def BattlePosition(self,x,y):
        '''
        placing a character and their health bar on top of the background during a battle
        '''
        #place the character
        screen.blit(self.battle_pic, (x,y))
        
        #character health bar; we keep while health > 0 because if it falls below that, there might be an error
        #we hopefully manage to avoid the error, and let a later function correct the health value
        while self.health > 0:
            pygame.draw.rect(screen, health_bar_red, (x, y+20, 50, 10))
            pygame.draw.rect(screen, health_bar_green, (x, y+20, 50 - (5 * (10 - self.health)), 10))
    
    EpisodeOn=False #control episode
    battleOn=False #control battles
    
#same as characters but this time for moves
class Move:
    '''
    This class will serve to define all the moves similarly to how characters will be created.
    Has variables for the name, energy consumption and/or damage caused, protection given and recovery made of the move
    Damage is the amount of damage (health lost by opponent) made by the move
    Protection is whether or not this move protects from damage or not (True or False)
    recovery is how much energy and health are recovered
    energy consumption is the amount of energy needed to use a move
    '''
    def __init__(self, name, damage, protection, recovery, energy_consumption):
       '''
       initialize a move
       '''
       self.name = name
       self.damage = damage
       self.protection = protection
       self.recovery = recovery
       self.energy_consumption = energy_consumption
    
    #special variables that can be used outside this class definition for the application of
    #locking or unlocking moves
    Move_isLocked = True
    Move_isUnlocked = False

#animations functions {TO UPDATE}


#other important helper functions
def playMusic(sound,Type,Forever=False):
    '''
    function to play sound or music
    '''
    if Type == 'sound':
        da_sound = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.set_volume(da_sound,0.2)
        pygame.mixer.Sound.play(da_sound)
        
    elif Type == 'music':
        pygame.mixer.music.load(sound)
        if Forever == False:
            pygame.mixer.music.play()
        elif Forever == True:
            pygame.mixer.music.play(-1)

def stopLoopingMusic():
    '''
    function to stop music on repeat, called eventually when we want to stop the music
    '''
    pygame.mixer.music.stop()

def make_text(text,font,size,color,x,y):
    '''function to make texts and rectangles for them
    helper function of make_button or function to display text that doesn't need button
    '''
    the_font = pygame.font.SysFont(font,size)
    the_text = the_font.render(text,True,color)
    TextSurface, TextRectangle = the_text, the_text.get_rect()
    TextRectangle.center = (x,y)
    screen.blit(TextSurface, TextRectangle)

def make_button(text,font,text_size,text_color,x,y,button_width,button_height,button_color,highlight_color,action=None,can_cancel_move=False):
    '''function to make buttons. shows text made with make_text at text_color, button_color is the button's color
    and whenever the cursor is on the button, its colors turns to highlight_color
    if the button is associated to a function, the function call is placed at action
    can_cancel_move is for buttons connected to moves in battles, helps lock or unlock a button to respectively prevent or allow the use of a move
    '''
    for event in pygame.event.get():
        if can_cancel_move == True:
            #checks if a mouse is clicked and there is an action
            #if Move.Move_isUnlocked is False, the whole condition is False and it skips to the elif
            #if Move.Move_isUnlocked is True, the whole condition is True and the move is possible
            if event.type == pygame.MOUSEBUTTONDOWN and action != None and Move.Move_isUnlocked:
                if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
                    playMusic(press_button_sound,'sound')
                    if action in [Episode1_1(),Episode1_2_1(),Episode1_2_2(),Episode1_3(),Episode1_4_1(),Episode1_4_2(),Episode1_5_1(),Episode1_5_2(),Episode2_1(),Episode3_1(),FinalEpisode_1()]:
                        Character.EpisodeOn = not Character.EpisodeOn
                        action
                    else:
                        action
            #if Move.Move_isLocked is True, the whole condition is True and the move is no longer possible; nothing happens when you click
            #if Move.Move_isLocked is False, at the same time Move.Move_isUnlocked is made True so above runs automatically,
            #but this below statement would be False and would not run, but the code will never skip both ifs because one or the other var is always True
            elif event.type == pygame.MOUSEBUTTONDOWN and action != None and Move.Move_isLocked:
                if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
                    pass
            #if no action, don't do anything
            elif event.type == pygame.MOUSEBUTTONDOWN and action == None:
                if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
                    pass
        elif can_cancel_move == False:
            if event.type == pygame.MOUSEBUTTONDOWN and action != None:
                if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
                    playMusic(press_button_sound,'sound')
                    if action in [Episode1_1(),Episode1_2_1(),Episode1_2_2(),Episode1_3(),Episode1_4_1(),Episode1_4_2(),Episode1_5_1(),Episode1_5_2(),Episode2_1(),Episode3_1(),FinalEpisode_1()]:
                        Character.EpisodeOn = not Character.EpisodeOn
                        action
                    else:
                        action
            #if Move.Move_isLocked is True, the whole condition is True and the move is no longer possible; nothing happens when you click
            #if Move.Move_isLocked is False, at the same time Move.Move_isUnlocked is made True so above runs automatically,
            #but this below statement would be False and would not run, but the code will never skip both ifs because one or the other var is always True
            elif event.type == pygame.MOUSEBUTTONDOWN and action == None:
                if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
                    pass  
                
    if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
        #switch button color to highlight_color
        pygame.draw.rect(screen,highlight_color,(x,y,button_width,button_height))
    
    else:
        #draw button at position x,y and with dimensions button_width and button_height
        pygame.draw.rect(screen,button_color,(x,y,button_width,button_height))
        
    make_text(text,font,text_size,text_color,x+button_width/2,y+button_height/2)
    
#main menu both in game and in python, which will serve to connect all functions through the Episodes functions
def Menu(): 
    '''makes the menu, and serves as the primary hub for the game, 
    as all episodes and the functions needed to run them are connected through this function
    '''
    #background
    screen.fill(black)
    
    #texts and buttons for episodes    
    make_text("Z-Legends: Exceedra's Awakening",'comicsansms',70,white,width/2,100)
    make_button('Episode 1','Corbel',35,white,500,210,200,70,red,green,action=Episode1_1())
    make_button('Episode 2','Corbel',35,white,500,310,200,70,red,green,action=Episode2_1())
    make_button('Episode 3','Corbel',35,white,500,410,200,70,red,green,action=Episode3_1())
    make_button('Final Episode','Corbel',35,white,500,510,200,70,red,green,action=FinalEpisode_1())
    
    pygame.display.update()

#game over (if you lose your battle)
def try_again(character1,character2,background,music):
    '''tell the user to try again after losing a battle'''
    #reset characters' stats
    character1 = character1.reset()
    character2 = character2.reset()
    #lost the battle sound    
    playMusic(BattleLost,'sound')
    #buttons
    screen.fill(black)
    make_button('Try again?','Corbel',35,white,500,260,200,70,red,green,action=Battle(character1,character2,background,music))
    make_button('I give up...','Corbel',35,white,500,560,200,70,red,green,action=pygame.quit())
        
    pygame.display.update()

#battle system, rock-paper-scissors like
#these functions are what happens when character1 (you!) selects that corresponding move
def Attack(character1,character2):
    '''attack scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.GuardMove:
        character2.losePower(0,character2.GuardMove.energy_consumption)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove:
        character2.losePower(character1.AttackMove.damage,0)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        
    elif opponent_move == character2.AttackMove:
        #prompt for special event to determine which move lands
        make_text('To amp up your power keep pressing SPACEBAR!!!','Corbel',40,white,500,360)
        start = pygame.time.get_ticks()
        SPACEBAR_count = 0
        while pygame.time.get_ticks() - start < 5000:
            #do the following for 5 seconds (5000 milliseconds):
            #make the user press SPACEBAR as many times as they can to help boost
            #their chances of landing their attack instead of the npc opponent
            for event in pygame.event.get():  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SPACEBAR_count += 1
            
        potential1 = character1.attack_potential + SPACEBAR_count
        potential2 = character2.attack_potential + randrange(1,11)
        if potential1 >= potential2:
            character2.losePower(character1.AttackMove.damage,0)
            character1.losePower(0,character1.AttackMove.energy_consumption)
        else:
            character1.losePower(character2.AttackMove.damage,0)
            character2.losePower(0,character2.AttackMove.energy_consumption)
    
    #if health becomes negative after taking damage, set health to 0 for the check in the Battle function
    if character1.health < 0:
        character1.health = 0
    if character2.health < 0:
        character2.health = 0

def Guard(character1,character2):
    '''guard scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.AttackMove:
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.AttackMove.energy_consumption)
        
    elif opponent_move == character2.GuardMove:
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.GuardMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove:
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.Recover(character2.RecoverMove.recovery)
    
def Recover(character1,character2):
    '''recover scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.GuardMove:
        character1.Recover(character1.RecoverMove.recovery)
        character2.losePower(0,character2.GuardMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove:
        character1.Recover(character1.RecoverMove.recovery)
        character2.Recover(character2.RecoverMove.recovery)
        
    elif opponent_move == character2.AttackMove:
        character1.losePower(character2.AttackMove.damage,0)
        character2.losePower(0,character2.AttackMove.energy_consumption)

#run the battle        
def Battle(character1, character2, background,music,next_scene):
    '''function for battles
    next_scene is function call of following scene in story
    '''
    #variable to start the battle        
    while Character.battleOn:
        #setup the background and character placements
        screen.blit(background,(0,0))
        character1.BattlePosition(400,500)
        character2.BattlePosition(200,500)
        
        #setup music
        playMusic(music,'music',Forever=True)
    
        #make buttons for the 3 moves of character1 (Exceedra)
        make_button(character1.AttackMove.name,'Corbel',35,white,500,210,200,70,red,pale_red,action=Attack(character1,character2),can_cancel_move=True)
        make_button(character1.GuardMove.name,'Corbel',35,white,500,310,200,70,green,pale_green,action=Guard(character1,character2),can_cancel_move=True)
        make_button(character1.RecoverMove.name,'Corbel',35,white,500,410,200,70,blue,pale_blue,action=Recover(character1,character2))    
        
        #controlling energy
        if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
            Move.MoveisUnlocked = False
            Move.MoveisLocked = True
        elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
            Move.MoveisLocked = False
            Move.MoveisUnlocked = True
            
        #losing
        if character1.health == 0 and character2.health != 0:
            stopLoopingMusic()
            try_again(character1,character2,background,music)
        
        #winning
        elif character1.health != 0 and character2.health == 0:
            stopLoopingMusic()
            playMusic(BattleWon,'sound')
            Character.battleOn = not Character.battleOn
        
        pygame.display.update()
    
    #return to story by playing the next scene
    next_scene

#pause and unpause
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    pygame.display.update()

def pause_the_game():
    '''pauses the game'''
    pygame.mixer.music.pause()
    
    make_text('PAUSE',"comicsansms",100,white,width/2,height/2)
    
    while pause:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    unpause()
                    
        pygame.display.update()

#story
def Episode1_1():
    '''do episode 1, scene 1'''
    #run = not Character.EpisodeOn
    #while run:
     #   screen.fill(white)
      #  playMusic(Dreamspace_theme,'music',Forever=True)
    pass

def Episode1_2_1():
    '''do episode 1, scene 2, before battle'''
    #pygame.update.display()
    pass
    #Character.battleOn = not Character.battleOn
    #Battle(ExceedraMain,Hydranoid,???,BattleTheme1,Episode1_2_2())

def Episode1_2_2():
    '''do episode 1, scene 2, after battle'''
    #pygame.update.display()
    pass    

def Episode1_3():
    '''do episode 1, scene 3'''
    #pygame.update.display()
    pass

def Episode1_4_1():
    '''do episode 1, scene 4,before battle'''
    #pygame.update.display()
    pass
    #Battle(ExceedraMain,Akobos,???,AkobosBattle,Episode1_4_2())


def Episode1_4_2():
    '''do episode 1, scene 4, after battle'''
    #pygame.update.display()
    pass


def Episode1_5_1():
    '''do episode 1, scene 5, before battle'''
    #pygame.update.display()
    pass
    #Battle(ExceedraMain,Nightmare,???,NightmareBattle,Episode1_5_2())


def Episode1_5_2():
    '''do episode 1, scene 5, after battle'''
    #pygame.update.display()

    #story
    
    #when the episode is completed, make Episode1_completed True and return to Menu
    Episode1_completed == True
    if Episode1_completed:
        Menu()

def Episode2_1():
    '''do episode 2'''
    if Episode1_completed == False:
        pass
    else:
        make_text('Episode 2 will come out soon!','Corbel',35,blue,600,600)
        #else will eventually be changed to run episode 2

def Episode3_1():
    '''do episode 3'''
    if Episode2_completed == False:
        pass
    else:
        #the episode
        pass

def FinalEpisode_1():
    '''do episode 4 (final)'''
    if Episode3_completed == False:
        pass
    else:
        #the episode
        pass
        #FinalEpisode_completed = True
        #if Episode1_completed and Episode2_completed and Episode3_completed and FinalEpisode_completed:
            #Game_completed=True
            
def Credits():
    #black baground
    screen.fill(black)
    #the end (big)
    make_text('THE END','arialblack',115,white,width/2,height/2)
    
    #run the credits...
    while Game_completed:
        pygame.update.display()
        
    
#With all functions and classes defined, let's create our characters, colors, sounds, and game progression controllers
#moves
ExceedraMainAttack = Move('Dragon Fist of Fury',30,False,0,10)
ExceedraGuard = Move('Tail Block',0,True,0,3)
ExceedraRecover = Move('Dragon Spirit',0,False,15,0)
HydranoidAttack = Move('Jab',10,False,0,5)
ClassicGuard = Move('Block',0,True,0,2)
HydranoidRecover = Move('Heal',0,False,10,0)
AkobosAttack = Move('Scythe of Demise',25,False,0,10)
AkobosRecover = Move('Demon Blood',0,False,15,0)
NightmareAttack = Move('Mental Plague',20,False,0,5)
NightmareGuard = Move('Dream Trapped',0,True,0,5)
NightmareRecover = Move('Dream Eater',0,False,20,0)
NullMove = Move('NullMove',0,False,0,0) #nothing, just for characters who aren't in battles
DestinyAttack = Move('Time Pulse',30,False,0,15)
DestinyGuard = Move('Time Stop',0,True,0,5)
DestinyRecover = Move('Centered',0,False,10,0)

#characters {TO UPDATE WITH PICS}
ExceedraMain = Character('Exceedra',100,50,20,ExceedraMainAttack,ExceedraGuard,ExceedraRecover)
Hydranoid = Character('Hydranoid',100,1000,15,HydranoidAttack,ClassicGuard,HydranoidRecover)
Akobos = Character('Akobos',100,1000,19,AkobosAttack,ClassicGuard,AkobosRecover)
Nightmare = Character('Nightmare',150,1000,17,NightmareAttack,NightmareGuard,NightmareRecover)
Destiny = Character('Destiny',80,30,12,DestinyAttack,DestinyGuard,DestinyRecover)
Grace = Character('Grace',0,0,0,NullMove,NullMove,NullMove)
Finlay = Character('Finlay',0,0,0,NullMove,NullMove,NullMove)
Ken = Character('Ken',0,0,0,NullMove,NullMove,NullMove)
Pilon = Character('Ken',0,0,0,NullMove,NullMove,NullMove)
Denis = Character('Denis',0,0,0,NullMove,NullMove,NullMove)
Junia = Character('Junia',0,0,0,NullMove,NullMove,NullMove)
Ross = Character('Ross',0,0,0,NullMove,NullMove,NullMove)
#Abby=... (in episode 2)

#sounds and music
press_button_sound = 'pokemon-a-button.wav'
Dreamspace_theme = 'Dreamspace_Dark.wav'
ExceedraLonelyTheme1 = 'Exceedras_Defiance.wav'
Hydranoid_DestinyTheme = ''
BattleTheme1 = ''
BattleWon = ''
BattleLost = ''
ExceedraLonelyTheme2 = ''
LibraryTheme = ''
ExceedraAngryTheme = 'Exceedra_Angry.wav'
AkobosAppears = 'Akoboss_Theme.wav'
AkobosBattle = ''
NightmareAppears = 'Nightmare_Theme.wav'
NightmareScream = 'NightmareScream.wav'
NightmareBattle = ''
NightmareDeath = 'Nightmare_HeartbeatDying.wav'
NightmareScream = 'NightmareScream.wav'

#variables for game progression
Episode1_completed = False
Episode2_completed = False
Episode3_completed = False
FinalEpisode_completed = False
Game_completed = False
pause = False

#colors (RGB)
white = (255,255,255)  
grey = (150,150,150)  
black = (0,0,0)
red = (181,42,42)
pale_red = (247,84,82)
blue = (42,46,181)
pale_blue = (3,202,252)
green = (42,181,42)
pale_green = (140,252,3)
health_bar_red = (255,0,0)
health_bar_green = (0,128,0)

#images and backgrounds
Zlogo = pygame.image.load('Screenshot 2024-11-24 161343.png')

#screen
res = (1200,720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Z-Legends: Exceedra's Awakening") 
pygame.display.set_icon(Zlogo)
width = screen.get_width()    
height = screen.get_height()

#now that all necessary variables and functions have been defined,
#run the main functions of the game; treat functions like substitutions of bits of code
while True:
    for event in pygame.event.get():  
        
        mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:  
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = True
                pause_the_game()
                
            elif event.key == pygame.K_0:
                pygame.quit()
        
    Menu()
    
    if Game_completed:
        Credits()
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Z-Legends: Exceedra's Awakening")

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TITLE_FONT = pygame.font.Font("animeace2_reg.ttf", 30)  # Title font size
DIALOGUE_FONT = pygame.font.Font("animeace2_reg.ttf", 21)  # Dialogue font size
HINT_FONT = pygame.font.Font("animeace2_reg.ttf", 12)  # Hint font size

# Background Images
background_title = pygame.image.load("title_background.png")  # Title screen background
background_title = pygame.transform.scale(background_title, (SCREEN_WIDTH, SCREEN_HEIGHT))

dreamspace = pygame.image.load("dreamspace.png")  # Scene 1 background
dreamspace = pygame.transform.scale(dreamspace, (SCREEN_WIDTH, SCREEN_HEIGHT))

school = pygame.image.load("school.png")  # Scene 2 background
school = pygame.transform.scale(school, (SCREEN_WIDTH, SCREEN_HEIGHT))

battle_background = pygame.image.load("battle_background.png")  # Battle scene background
battle_background = pygame.transform.scale(battle_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Character Images
main_character = pygame.image.load("main_character.png")  # Main character sprite
main_character = pygame.transform.scale(main_character, (150, 150))

enemy = pygame.image.load("enemy.png")  # Enemy sprite
enemy = pygame.transform.scale(enemy, (150, 150))

# Game State
scene = "start_menu"  # Start with the start menu
dialogue_index = 0
running = True
battle_mode = False

# Battle Stats
player_hp = 100
player_energy = 100
enemy_hp = 100

# Dialogue for Scene 1
scene_1_dialogue = [
    "[Exceedra awakes in a dark dreamspace]",
    "Overlord: Welcome, Son. It’s been a while since you last came here.",
    "Exceedra: What do you want?",
    "Overlord: Nothing much. Except to know how my son is doing.",
    "[Exceedra grins angrily.]",
    "Exceedra: Yea right. What do you really want?",
    "Overlord: You do realize you wandered in here on your own, right?",
    "[Exceedra is shocked.]",
    "Exceedra: Wait, what? Why would I come here…",
    "Overlord: [worried] Look. I’ve been watching you. Your life on Earth is becoming more and more miserable.",
    "Overlord: It’s sad to watch. You’re getting nothing back out of the good you’re doing.",
    "Overlord: If you’d only obey my instructions, you wouldn’t have so many problems.",
    "Overlord: I’m positive that if you start killing people, you should get closer to what you want.",
    "Exceedra: [firmly] Killing is not the path forward.",
    "Overlord: [grandiose] THEN WHAT IS, OH GREAT DRAGON PRINCE? [Grips Exceedra.]",
    "Overlord: The path forward is the one you make yourself. There is no other path.",
    "Overlord: Only you can make the path that will get you to what you want.",
    "Overlord: Do you seriously believe you can stay the way you are and one day you will get what you want? Naive little boy!",
    "[Overlord ungrips and continues.]",
    "Overlord: You can’t trust humans. They will always disappoint you.",
    "Overlord: They will always be better than you. They’ll always have what you want.",
    "Overlord: They can’t understand you, Exceedra. They’re just humans.",
    "Overlord: They aren’t Gods. They can’t give you what you want.",
    "Exceedra: [angrily] So?",
    "Overlord: [foreboding] Just kill them. You don’t need things that don’t help you.",
    "Overlord: Listen, kiddoboy, if you don’t believe, then just pick a number. Any number.",
    "Overlord: [foreboding] No matter the number you pick… the humans will betray you.",
    "Overlord: The path forward is the path you will have to make yourself. So choose.",
    "Overlord: Let go of your childish human hope or take the reins of your existence on Earth and kill the humans so you can finally establish your empire.",
    "[Overlord looks as if to the future, disappointed and worried.]",
    "Overlord: It’s only a matter of time now before there is nothing left to fight for.",
    "Exceedra: [worried] What do you mean?",
    "Overlord: [ignoring, looking directly at Exceedra] Just kill the humans and take what you want. You won’t regret it.",
    "[Exceedra prepares to leave.]",
    "Overlord: You can take 1 million more steps on the path you’re walking on and still not get where you want to go.",
    "[Exceedra stops.]",
    "Overlord: You can blame God as much as you want, but you’re the one making the path forward.",
    "Overlord: You’re the one who needs to change. You need to listen to me!",
    "Exceedra: [interrupting, screaming] NO! THE PATH FORWARD IS THE ONE I WILL MAKE MYSELF, BUT IT’S NOT MY FAULT GOD ISN’T GIVING ME WHAT IS RIGHTFULLY MINE.",
    "Exceedra: I WILL RULE THIS PLANET AND TAKE WHAT IS RIGHTFULLY MINE. I just… [struggling to continue.]",
    "[Exceedra walks away. Before leaving, looks back.]",
    "Exceedra: I’ll figure it out. I have to. For the sake of the plot."
]

# Dialogue for Scene 2
scene_2_dialogue = [
    "[Exceedra goes to school and greets his friends. It's lunchtime; he meets Hydranoid and Destiny.]",
    "Exceedra: [happily] Hey!",
    "Destiny: Hi Captain! How’s it going?",
    "Exceedra: [grinning] Ace positively amazing! [Shows his math test] Rightfully got another 100.",
    "Hydranoid: Congratulations, Captain. As usual, you get what you want.",
    "Exceedra: [pissed, frowning at his twin] And what’s that supposed to mean?",
    "Hydranoid: [smiling] You’d be crying right now if you didn’t get 100. tease Remember last time?",
    "Exceedra: [dark, takes a step towards Hydranoid] Don’t push it.",
    "Destiny: [gets in between them] Cap, that’s enough!",
    "Hydranoid: [calmly, to Exceedra] Now now, chill. You know I’m in no mood to make you angry.",
    "[They go sit down and start eating.]",
    "Hydranoid: [curious tone] Though, I wonder how you’re going to react if you don’t get 100 on Chem. You better not throw a tantrum like last time.",
    "Exceedra: [leans in and Hydranoid and pulls out his tails, very pissed] Are you calling me an idiot?",
    "Hydranoid: [still calmly] Nope. I just don’t want you to embarrass yourself.",
    "Hydranoid: Wouldn’t bring you closer to what you’re looking for, you know what I mean? [Looks Exceedra in the eye, challenging.]",
    "Exceedra: [grinning darkly] You’re right, Hydranoid. No need for a spanking. [Sits down and resumes eating.]",
    "Hydranoid: [eating, until he realises something. In a pointing-out tone] Though, I’m pretty sure Den probably got 100.",
    "[Exceedra, completely pissed, gets up, pulls out his tails.]",
    "Exceedra: [angry as f*] WHERE ARE YOU GETTING AT, LITTLE BROTHER?",
    "Hydranoid: [unaware] Huh?",
    "Destiny: Uh oh…",
    "[Exceedra, fully pissed, triggers a battle.]",
    "[BATTLE]",
    "[Hydranoid is defeated. Stands up, scratching his head, smiling.]",
    "Hydranoid: You really are strong, Captain. No wonder you’re the Lagoon.",
    "Exceedra: Don’t piss me off like that again, little brother.",
    "[Hydranoid: All right… Exz offers his hand so Hyde can get up. Image of the two strongly together.]",
    "Hydranoid: [noticing] Is something up?",
    "Exceedra: [surprised by his brother noticing something’s up with him] Hein! No I’m good.",
    "Destiny: [sad] It’s just that… these past few days, you’ve seemed… more distant.",
    "Exceedra: Distant? Nah. I’m Ace Positive. [Poses, grinning.]",
    "Hydranoid: [direct] You sure not having a girlfriend doesn’t bother you?",
    "Destiny: [slaps her hand on her brother’s head] Hydranoid!",
    "Exceedra: [sad] No, Destiny, it’s all right… Truth be told, [puts his hand to his heart and grips it] it does hurt.",
    "Exceedra: But the path forward is the one we make together. That’s more than enough for me.",
    "Hydranoid: Did you hear back anything from the job you applied to?",
    "Exceedra: Huuuuuuuuuuuuuuuuuuuuuuuuh…",
    "Hydranoid: Oh my. Nothing!",
    "[Exceedra nods in shame.]",
    "Hydranoid: Nothing to be ashamed of, big brother. Life on Earth always makes no sense from what I’ve seen.",
    "Hydranoid: You don’t have a girlfriend, you have no job, you have no G2, and you can’t get 100.",
    "Hydranoid: Meanwhile… [stares at the other side of the atrium, where their group of IB friends are happily chatting.]",
    "Exceedra: It won’t be like that for long. heroically For the sake of the plot, I’m gonna catch up.",
    "Hydranoid: Well at least you have powers. That’s the one thing humans can’t have that you do.",
    "Exceedra: [dark, and taking a dark face] Well… even that has its troubles…",
    "[Hydranoid catches the dark tone and gets curious, but he decides to let it go for later.]",
    "Hydranoid: [taking one last bite] Are we still on for the mission later?",
    "Exceedra: also done his food, getting up Aye. We’re gonna rat out the rat and kick him in the butt right to the other side of the galaxy!",
    "[Hydranoid and Exceedra, face to face, smiling at each other.]",
    "Hydranoid: [happy and serious] Well said, Cap! Let’s go kick butt… after Chem.",
    "[They all part ways.]"
]

# Render text with wrapping
def draw_text(surface, text, font, x, y, color=BLACK, max_width=SCREEN_WIDTH-40):
    words = text.split(' ')
    lines = []
    current_line = ""

    # Wrap text
    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    y_offset = y
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y_offset))
        y_offset += font.get_height()

# Draw text box
def draw_text_box():
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))  # Bottom box
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120), 5)  # Border

# Draw hint text
def draw_hint_text():
    hint_text = "Press Enter to continue, Backspace to go back"
    hint_surface = HINT_FONT.render(hint_text, True, BLACK)
    hint_x = SCREEN_WIDTH - hint_surface.get_width() - 10  # Align to the bottom-right corner
    hint_y = SCREEN_HEIGHT - 20  # Above the bottom of the box
    screen.blit(hint_surface, (hint_x, hint_y))

# Show battle screen
def battle_screen():
    global player_hp, player_energy, enemy_hp

    screen.blit(battle_background, (0, 0))  # Battle background
    screen.blit(main_character, (100, SCREEN_HEIGHT - 300))  # Main character position
    screen.blit(enemy, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300))  # Enemy position

    # Draw stats
    draw_text(screen, f"HP: {player_hp}", DIALOGUE_FONT, 20, 20, RED)
    draw_text(screen, f"Energy: {player_energy}", DIALOGUE_FONT, 20, 50, BLUE)
    draw_text(screen, f"Enemy HP: {enemy_hp}", DIALOGUE_FONT, SCREEN_WIDTH - 200, 20, RED)

    # Draw action buttons
    button_width, button_height = 150, 50
    button_spacing = 20
    button_y = SCREEN_HEIGHT - 100

    attack_rect = pygame.Rect(50, button_y, button_width, button_height)
    guard_rect = pygame.Rect(50 + button_width + button_spacing, button_y, button_width, button_height)
    recovery_rect = pygame.Rect(50 + 2 * (button_width + button_spacing), button_y, button_width, button_height)

    pygame.draw.rect(screen, RED, attack_rect)
    pygame.draw.rect(screen, GREEN, guard_rect)
    pygame.draw.rect(screen, BLUE, recovery_rect)

    draw_text(screen, "Attack", DIALOGUE_FONT, attack_rect.x + 25, attack_rect.y + 10, WHITE)
    draw_text(screen, "Guard", DIALOGUE_FONT, guard_rect.x + 30, guard_rect.y + 10, WHITE)
    draw_text(screen, "Recover", DIALOGUE_FONT, recovery_rect.x + 20, recovery_rect.y + 10, WHITE)

    return attack_rect, guard_rect, recovery_rect

# Show title screen
def show_start_menu():
    screen.blit(background_title, (0, 0))  # Title background
    draw_text(screen, "Z-Legends: Exceedra's Awakening", TITLE_FONT, 90, 200, BLACK)  # Title
    draw_text(screen, "Press Enter to Start", DIALOGUE_FONT, 235, 300, BLACK)  # Prompt
    pygame.display.flip()

# Main Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not battle_mode:
                if event.key == pygame.K_RETURN:  # On Enter key
                    if scene == "start_menu":
                        scene = "scene_1"
                        dialogue_index = 0
                    elif scene == "scene_1" and dialogue_index < len(scene_1_dialogue):
                        dialogue_index += 1
                        if dialogue_index >= len(scene_1_dialogue):
                            scene = "scene_2"
                            dialogue_index = 0
                    elif scene == "scene_2" and dialogue_index < len(scene_2_dialogue):
                        dialogue_index += 1
                        if dialogue_index >= len(scene_2_dialogue):
                            battle_mode = True  # Trigger battle
                    elif scene == "scene_2" and battle_mode:
                        # Handle battle mechanics
                        pass
                elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                    if dialogue_index > 0:
                        dialogue_index -= 1  # Go to previous line
                    else:
                        dialogue_index = 0  # Keep at the first line
        elif event.type == pygame.MOUSEBUTTONDOWN and battle_mode:
            mouse_pos = event.pos
            attack_rect, guard_rect, recovery_rect = battle_screen()
            if attack_rect.collidepoint(mouse_pos):
                enemy_hp -= 20  # Attack action
            elif guard_rect.collidepoint(mouse_pos):
                # Guard action logic
                pass
            elif recovery_rect.collidepoint(mouse_pos):
                player_hp = min(100, player_hp + 20)  # Recovery action

    if battle_mode:
        battle_screen()
    elif scene == "start_menu":
        show_start_menu()
    elif scene == "scene_1":
        screen.blit(dreamspace, (0, 0))
        draw_text_box()
        if dialogue_index < len(scene_1_dialogue):
            draw_text(screen, scene_1_dialogue[dialogue_index], DIALOGUE_FONT, 20, SCREEN_HEIGHT - 110)
        draw_hint_text()  # Display hint
    elif scene == "scene_2":
        screen.blit(school, (0, 0))
        draw_text_box()
        if dialogue_index < len(scene_2_dialogue):
            draw_text(screen, scene_2_dialogue[dialogue_index], DIALOGUE_FONT, 20, SCREEN_HEIGHT - 110)
        draw_hint_text()  # Display hint

    pygame.display.flip()

pygame.quit()
sys.exit()
