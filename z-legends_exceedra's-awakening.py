#Made by LordZagger and Jin4843, November-December 2024, made public dec 3,2024

#import modules
import pygame
from random import choice
from random import randrange

#init pygame and pygame.mixer
pygame.init()
pygame.mixer.init()

#sounds and music
press_button_sound = 'pokemon-a-button.wav'
Dreamspace_theme = 'Dreamspace_Dark.wav'
ExceedraLonelyTheme1 = 'Exceedras_Defiance.wav'
Hydranoid_DestinyTheme = 'Library_Theme.wav'
BattleTheme1 = 'Nightmare_Battle.wav'
BattleWon = 'Battle_Won_Sound.wav'
BattleLost = 'Battle_Lost_Sound.wav'
ExceedraLonelyTheme2 = 'Exceedra_Sad.wav'
LibraryTheme = 'Library_Theme.wav'
ExceedraAngryTheme = 'Exceedra_Angry.wav'
AkobosAppears = 'Akoboss_Theme.wav'
AkobosBattle = 'Nightmare_Battle.wav'
NightmareAppears = 'Nightmare_Theme.wav'
NightmareScream = 'NightmareScream.wav'
NightmareBattle = 'Nightmare_Battle.wav'
NightmareDying = 'Nightmare_HeartbeatDying.wav'
NightmareDeath = 'NightmareDeath.wav'
NightmareScream = 'NightmareScream.wav'

#variables for game progression
pause = False
dialogue_index = 0
running = True
scene = "start_menu"  # Start with the start menu

#colors (RGB)
white = (255,255,255)  
grey = (150,150,150)  
black = (0,0,0)
red = (181,42,42)
pale_red = (247,84,82)
blue = (42,46,181)
green = (42,181,42)
pale_green = (140,252,3)
health_bar_red = (255,0,0)
health_bar_green = (0,128,0)
yellow = (241,245,5)
pale_yellow = (158,161,8)

#screen icon
Zlogo = pygame.image.load('Screenshot 2024-11-24 161343.png')

#screen
res = (1200,720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Z-Legends: Exceedra's Awakening") 
pygame.display.set_icon(Zlogo)
width = screen.get_width()    
height = screen.get_height()

#backgrounds and fonts
DIALOGUE_FONT = pygame.font.Font("animeace2_reg.ttf", 21)  # Dialogue font size
HINT_FONT = pygame.font.Font("animeace2_reg.ttf", 12)  # Hint font size
dreamspace = pygame.image.load("dreamspace.png")  # Scene 1.1 background
dreamspace = pygame.transform.scale(dreamspace, (width, height))

school = pygame.image.load("school.png")  # Scene 1.2 background
school = pygame.transform.scale(school, (width, height))

library = pygame.image.load('Library.png') #Scene 1.3 background
library = pygame.transform.scale(library, (width,height))

hill = pygame.image.load('hill.png') #Scene 1.4 background
hill = pygame.transform.scale(hill,(width,height))

house = pygame.image.load('House.png') #Scene 1.5 background
house = pygame.transform.scale(house,(width,height))

#Character Images
Exceedra1_pic = pygame.image.load("exceedra1.png")  # Main character sprite
Exceedra1_pic = pygame.transform.scale(Exceedra1_pic, (700, 700))

Hydranoid_pic = pygame.image.load("hydranoid.png")  # Hydranoid sprite
Hydranoid_pic = pygame.transform.scale(Hydranoid_pic, (700, 700))

Overlord_pic = pygame.image.load("overlord.png")  # Ovelord sprite
Overlord_pic = pygame.transform.scale(Overlord_pic, (700, 700))

Destiny_pic = pygame.image.load("destiny.png")  # Destiny sprite
Destiny_pic = pygame.transform.scale(Destiny_pic, (700, 700))

Akobos_pic = pygame.image.load("akobos.png")  # Akobos sprite
Akobos_pic = pygame.transform.scale(Akobos_pic, (700, 700))

Grace_pic = pygame.image.load("grace.png")  # Grace sprite
Grace_pic = pygame.transform.scale(Grace_pic, (700, 700))

Ken_pic = pygame.image.load("ken.png")  # Ken sprite
Ken_pic = pygame.transform.scale(Ken_pic, (700, 700))

Finlay_pic = pygame.image.load("finlay.png")  # Finlay sprite
Finlay_pic = pygame.transform.scale(Finlay_pic, (700, 700))

Junia_pic = pygame.image.load("junia.png")  # Junia sprite
Junia_pic = pygame.transform.scale(Junia_pic, (700, 700))

Nightmare_pic = pygame.image.load('nightmare.png') #Nightmare Pic
Nightmare_pic = pygame.transform.scale(Nightmare_pic,(700,700))

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
        placing a character and their health bar (if during a battle) on top of the background
        mainly used for positioning during battles, but this method's existence is also convenient for scenes
        '''
        #place the character
        if self.battle_pic != None:
            screen.blit(self.battle_pic, (x,y))
        else:
            pass #do nothing if there is no pic
        
        #character health bar; we keep while health > 0 because if it falls below that, there might be an error
        #we hopefully manage to avoid the error, and let a later function correct the health value
        while self.health > 0 and Character.battleOn:
            pygame.draw.rect(screen, health_bar_red, (x, y+20, 50, 10))
            pygame.draw.rect(screen, health_bar_green, (x, y+20, 50 - (5 * (10 - self.health)), 10))
    
    EpisodeOn=False #control episode
    battleOn=False #control battles
    character1=''
    character2=''
    background=''
    music=''
    next_scene=''
    Episode1_completed = False
    Episode2_completed = False
    Episode3_completed = False
    FinalEpisode_completed = False
    Game_completed = False
    
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

#regular text (not in dialogue)
def make_text(text,font,size,color,x,y):
    '''function to make texts and rectangles for them
    helper function of make_button or function to display text that doesn't need button
    '''
    the_font = pygame.font.SysFont(font,size)
    the_text = the_font.render(text,True,color)
    TextSurface, TextRectangle = the_text, the_text.get_rect()
    TextRectangle.center = (x,y)
    screen.blit(TextSurface, TextRectangle)

#dialogue text
def draw_text(surface, text, font, x, y, color=black, max_width=width-40):
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
    pygame.draw.rect(screen, white, (0, height - 120, width, 120))  # Bottom box
    pygame.draw.rect(screen, black, (0, height - 120, width, 120), 5)  # Border

# Draw hint text
def draw_hint_text():
    hint_text = "Press Enter to continue, Backspace to go back"
    hint_surface = HINT_FONT.render(hint_text, True, black)
    hint_x = width - hint_surface.get_width() - 10  # Align to the bottom-right corner
    hint_y = height - 20  # Above the bottom of the box
    screen.blit(hint_surface, (hint_x, hint_y))

def make_button(text,font,text_size,text_color,x,y,button_width,button_height,button_color,highlight_color,action=None,can_cancel_move=False,events=None):
    '''function to make buttons. shows text made with make_text at text_color, button_color is the button's color
    and whenever the cursor is on the button, its colors turns to highlight_color
    if the button is associated to a function, the function call is placed at action
    can_cancel_move is for buttons connected to moves in battles, helps lock or unlock a button to respectively prevent or allow the use of a move, default is false (for menu buttons)
    '''
    global scene, dialogue_index    
    if events == None:
        events = []
        
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if can_cancel_move == True and Character.battleOn:
                #checks if a mouse is clicked and there is an action
                #if Move.Move_isUnlocked is False, the whole condition is False and it skips to the elif
                #if Move.Move_isUnlocked is True, the whole condition is True and the move is possible
                if action != None and Move.Move_isUnlocked:
                    if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height and (event.button == 1 or event.button == 2):
                        if action in [Battle,Attack,Guard,Move]:
                            action(Character.character1,Character.character2,Character.background,Character.music,Character.next_scene)
                            pygame.display.flip()
                        else:
                            action()
                            pygame.display.flip()
                #if Move.Move_isLocked is True, the whole condition is True and the move is no longer possible; nothing happens when you click
                #if Move.Move_isLocked is False, at the same time Move.Move_isUnlocked is made True so above runs automatically,
                #but this below statement would be False and would not run, but the code will never skip both ifs because one or the other var is always True
                elif action != None and Move.Move_isLocked:
                    if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height and (event.button == 1 or event.button == 2):
                        pass
                #if no action, don't do anything
            elif can_cancel_move == False:
                if action != None:
                    if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height and (event.button == 1 or event.button == 2):
                        playMusic(press_button_sound,'sound')
                        if action==Episode1_1:
                            if scene == "start_menu":
                                scene = "scene_1"
                                dialogue_index = 0                            
                                Character.EpisodeOn = True
                                action()
                        elif action in [Battle,Attack,Guard,Move]:
                            action(Character.character1,Character.character2,Character.background,Character.music,Character.next_scene)
                            pygame.display.flip()
                        elif action == Episode2_1_1:
                            if scene == 'start_menu':
                                scene = 'scene_6.1'
                                dialogue_index = 0
                                Character.EpisodeOn = not Character.EpisodeOn
                                action()
                                pygame.display.flip()
                        else:
                            action()
                            pygame.display.flip()
                 
    if x <= mouse[0] <= x+button_width and y <= mouse[1] <= y+button_height:
        #switch button color to highlight_color
        pygame.draw.rect(screen,highlight_color,(x,y,button_width,button_height))
    
    else:
        #draw button at position x,y and with dimensions button_width and button_height
        pygame.draw.rect(screen,button_color,(x,y,button_width,button_height))
        
    make_text(text,font,text_size,text_color,x+button_width/2,y+button_height/2)
    
#main menu both in game and in python, which will serve to connect all functions through the Episodes functions
def Menu(events): 
    '''makes the menu, and serves as the primary hub for the game, 
    as all episodes and the functions needed to run them are connected through this function
    '''
    #background
    screen.fill(black)
    
    #texts and buttons for episodes    
    make_text("Z-Legends: Exceedra's Awakening",'comicsansms',70,white,width/2,100)
    make_button('Episode 1','Corbel',35,white,500,210,200,70,red,green,action=Episode1_1,events=events)
    make_button('Episode 2','Corbel',35,white,500,310,200,70,red,green,action=Episode2_1_1,events=events)
    make_button('Episode 3','Corbel',35,white,500,410,200,70,red,green,action=Episode3_1,events=events)
    make_button('Final Episode','Corbel',35,white,500,510,200,70,red,green,action=FinalEpisode_1,events=events)
    
    pygame.display.flip()

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
    make_button('Try again?','Corbel',35,white,500,260,200,70,red,green,action=Battle)
    make_button('I give up...','Corbel',35,white,500,560,200,70,red,green,action=pygame.quit)
        
    pygame.display.flip()

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
def Battle(character1,character2,background,music,next_scene):
    '''function for battles
    next_scene is function call of following scene in story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    '''
    #start the battle        
    while Character.battleOn and (not Character.EpisodeOn):
        #setup the background and character placements
        screen.blit(background,(0,0))
        character1.BattlePosition(100,height-300)
        character2.BattlePosition(width-250,height-300)
        
        #setup music
        playMusic(music,'music',Forever=True)
    
        #make buttons for the 3 moves of character1 (Exceedra)
        make_button(character1.AttackMove.name,'Corbel',35,white,500,210,200,70,red,pale_red,action=Attack,can_cancel_move=True)
        make_button(character1.GuardMove.name,'Corbel',35,white,500,310,200,70,green,pale_green,action=Guard,can_cancel_move=True)
        make_button(character1.RecoverMove.name,'Corbel',35,white,500,410,200,70,yellow,pale_yellow,action=Recover)    
        
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
            Character.EpisodeOn = not Character.EpisodeOn
        
        pygame.display.flip()
    
    #return to story by playing the next scene
    next_scene()

#pause and unpause
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    pygame.display.flip()

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
                    
        pygame.display.flip()

#dialogue for episode 1 scene 1
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

# Dialogue for episode 1 Scene 2
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

scene_3_dialogue = [
    "[Library. Exceedra and his classmates/friends Ken, Grace and Finlay are at a table, working… but actually really just talking.",
    "Finlay: [screwed] Bro, Politique is actually bad. I haven’t started the video and it’s due Friday.",
    "Exceedra: [reprimanding] Bro, Finlay, what is wrong with you! Get started already! [Banging on the table] LOCK IN!",
    "Ken: [mocking] That’s what you get for choosing Politics.",
    "Exceedra: Nah! It’s not that bad. Unless you wait until the last minute to do everything… [glares at Finlay while saying that last part]",
    "Finlay: [defensive] Bro, I’m busy. We got Calc, and Chem, and Politics…",
    "Grace: [firm] Finlay, it’s on you.",
    "[Finlay grumbles in defeat. Exceedra sighs (of happiness, looking at his friends)].",
    "Exceedra: You know, when I first came here in Grade 9, I was planning to be completely antisocial. Making it through the next four years on my own, with no friends.",
    "Exceedra: [shakes his head no] But then all of you had to happen. [smiles] You know, if it wasn’t for all of you, I don’t know what I would turn into [grumble] literally.",
    "Exceedra: I’m really glad I met you guys.",
    "Finlay: Us too, Captain.",
    "[Cap realises something.]",
    "Exceedra: Manion! I gotta check if the novel I’m looking for is back, be right back.", 
    "[Cap gets up and goes to the book shelf, he finds his book, looks in it, but Cap being Cap, is also looking around.]",
    "[He spots Finlay leaning forward to whisper something to Grace and Ken, and hears Finlay say his name and something about him.]",
    "[Exceedra is outraged but decides not to show it, as he is as curious as he is furious about his friends talking behind his back.]", 
    "[He puts the book back and goes back to his seat.]",
    "Exceedra: [seating down] What I really want is to see my Chem test. I wanna see my sweet 100… [smiling too much and face contorsioned from wanting 100]", 
    "Finlay: Bro, obviously you got 100.",
    "Exceedra: [GLARES at him] You know how Pilon can be…",
    "[They head to class. Later on, in the hallway...]", 
    "Exceedra: [wide eyed, screaming] WHAAAAAAAAT! 95? WHAT DID I DO WRONG?",
    "[Checks through the test to try and find his mistake. Meanwhile, he overhears:]",
    "Denis: 100! As usual.",
    "[Exceedra is in shock. All of their friends crowds up around Den (Denis) to see his copy. Exceedra is jealous that Denis gets all that attention and curls up his fist.]", 
    "[Hydranoid comes next to Exceedra.]", 
    "Hydranoid: Damn. [looking at the crowd, which includes a special girl] This is what you were afraid of, wasn’t it?",
    "[Exceedra, in a dark mood, does not respond, as he watches the girl happily chat with Denis about his test result.]",
    "Hydranoid: [chill] Don’t be so gloomy Cap. You’re getting 100 next time, no matter what.", 
    "Exceedra: [still dark] Yea. No matter what."
]

scene_4_dialogue = [
    "Exceedra and his team are downtown, talking through communicators. Exceedra is close to Parliament Hill, talking to his brother.", 
    "Exceedra: I’ve got a bad feeling about this…",
    "Hydranoid: [excited] Nah! He’s bound to show up. Our trap is way too enticing.",
    "Exceedra: [big grin] Oh yea…",
    "[Akobos appears alone out of a portal. You can see he has a sinister look on his face, but it immediately turns into a very pissed face, as he screams:]", 
    "Akobos: LAGOON!",
    "[Akobos has just noticed that a big poster is hanging on the Parliament clock that reads: AKOBOS SUCKS! in big black characters.]", 
    "Akobos: You’re done for Exceedra! Where are you?",
    "[Exceedra jumps out of the shadows and attacks Akobos, who easily parries and dodges away.]", 
    "Exceedra: Do you like our welcome gift?",
    "[Hydranoid pops up.]",
    "Hydranoid: [smiling] We made it specifically for you!", 
    "Akobos: [mad] You think this is funny, punies! [Draws out his red blades] I’m gonna kill both of you right here and now!", 
    "[The twins get side by side and do their battle speech].", 
    "Hydranoid: You can try…", 
    "Exceedra: But we’ll take you down, no matter what it takes! For the sake of plot…", 
    "Hydranoid: And for all our sakes…", 
    "Exceedra & Hydranoid: [pointing to Akobos in challenge] PREPARE FOR BATTLE!", 
    "[BATTLE]",
    "Akobos: Damn! Rushing at Exceedra This isn’t over!", 
    "[Exceedra easily dodges and trips Akobos. As Akobos trips, Hydranoid slams his head with the hilt of his sword, right into the ground.]", 
    "[With that, Akobos has been taken down and the brothers rejoice (they happily high five.)]", 
    "Exceedra: That was too easy!", 
    "Hydranoid: [happily] Yeah! [Darker, in thought] Too easy…"
]

scene_5_dialogue = [
    "[Late at night, at Exceedra's home. Exceedra’s mother is waiting for him at a table. Exceedra is tired from his mission and just wants to eat dinner.]",
    "Exceedra: What is it?", 
    "Junia (mom): How was your day?", 
    "Exceedra: [annoyed, going for the fridge] Why the hell are you asking?", 
    "Junia: How are you progressing with the AIF?", 
    "[Exceedra stops, clearly pissed.]", 
    "Exceedra: [in a murderous mood] I’ve been busy.", 
    "Junia: Oh right. So you’re going to leave this to the last minute, as usual?", 
    "Exceedra: That’s not what I said…", 
    "Junia: Have you looked at those links I sent you for scholarships?", 
    "Exceedra: [annoyed, reprimanding tone] Do I have to repeat myself? I’ve been busy!",
    "Junia: Oh, so you just don’t care about your future?", 
    "Exceedra: [glaring at her] Don’t you dare imply that. I will get to those things... when I have time.", 
    "Junia: Oh, but you have plenty of time to be running around defeating demons and spending time with Hydranoid and Destiny.",
    "Junia: [Gets closer to him] Jeremy, stop wasting your time and get your priorities straight.",
    "Junia: University is expensive and you know how little money we have to send you to Waterloo.",
    "Junia: The best thing you can do for yourself is to apply for those scholarships before the deadline, otherwise you’re never going to get anywhere.", 
    "Exceedra: [straight in her eyes] Don’t you think I know that?!", 
    "Junia: What are you screaming at me for?",
    "Exceedra: I’m not screaming!", 
    "Junia: With that kind of attitude, you’re showing that you're immature and not ready to go to university.", 
    "Junia: I can write to the University to tell that you aren’t fit for their program and keep you here, you know that?", 
    "[Exceedra terribly wants to kill her, but he has to stay there and take it.]", 
    "Junia: Anyway, your future’s on you. [Deadly tone] In this house, we don’t wait until the last minute to do things. [leaves to go upstairs]", 
    "[Exceedra is pissed at her, badly wants to kill her, but can’t. You can see the emotional struggle on his face.]", 
    "Exceedra: [thinking] Damn, so much for asking about her revenue info for the Queens bursaries… Talking to her now is pointless, especially since the due date is tomorrow…",
    "Exceedra: Looks like I’ll have to figure something out on my own; as usual I can’t count on anyone…", 
    "[Exceedra eats dinner, then goes to his room to do homework, then does his nightly routine, then goes to bed. In bed,]", 
    "Exceedra: (thinking) You know, sleep is the only way for me to escape this miserable existence on Earth.", 
    "Exceedra: Tch. I just don’t have the power to change things, not the way I am now. I need to become a god if I’m gonna get what I want.", 
    "Exceedra: [sighs] I just wanna go home… [while sulking, falls asleep]", 
    "[He reenters the Dreamspace where he was first talking to the Overlord. This time, no one is around.]", 
    "Nightmare: [far off, cackles sinisterly] Look what the baby dragon brought in. More food!", 
    "[Exceedra turns around, ready for a battle.]", 
    "Exceedra: [weary] Who is this?", 
    "[Nightmare cackles again.]", 
    "Nightmare: [appears before Exceedra] You don’t know? We’re your worst NIGHTMARE!",
    "[BATTLE]",
    "[Throughout the battle, Nightmare has been taunting Exceedra by engulfing him in nightmares where his friends start ignoring him, and the girl he has a crush on doesn't like him back at all.]", 
    "[The darkest part is that Hydranoid and Destiny aren't around to help him.]",
    "[Now...]",
    "Nightmare: [laughing as he is disintegrating] See, baby dragon! See how you had to fight alone? There isn’t anyone who can help you. [Laughs heartily] Your father has a point.",
    "Exceedra: [angry as f*, staring at Nightmare disintegrating, battle-angry face] Don’t tell me? Dad sent you?",
    "Nightmare: [rauque cackle, since he’s disintegrating] You can’t count on anyone to help you. At this point, the only thing you can do is just stand around and take all of it!", 
    "Nightmare: [Laughing crazily] Kill, Exceedra, KILL!",
    "Exceedra: grrrrrrr",
    "Nightmare: There isn’t anyone who can move forward with you. The only path forward for you… is one you can only walk on… on your own!", 
    "Nightmare: [Mocking and laughing in his final moments] DON’T YOU GET IT? YOU WILL NEVER BE HAPPY! YOU WILL ALWAYS BE ALONE!",
    "[Nightmare disintegrates completely. Exceedra wakes up in the real world, shocked awake.]",
    "[It’s 1 AM, pitch black, and Exceedra is sitting on his bed, head and hands on his knees, clearly shocked and sad (as in about to cry), reeling from the battle he’s just had.]"
]

#let's create our characters, colors, sounds, and game progression controllers with variables
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
DestinyAttack = Move('Time Pulse',30,False,0,15) #destiny is available for battle in episode 2
DestinyGuard = Move('Time Stop',0,True,0,5)
DestinyRecover = Move('Centered',0,False,10,0)
OverlordAttack = Move('Dark En',40,False,0,10)
OverlordGuard = Move('Black Shield',0,True,0,2)
OverlordRecover = Move('Darkness',0,False,25,0)

#characters
ExceedraMain = Character('Exceedra',100,50,20,ExceedraMainAttack,ExceedraGuard,ExceedraRecover,battle_pic=Exceedra1_pic)
Hydranoid = Character('Hydranoid',100,1000,15,HydranoidAttack,ClassicGuard,HydranoidRecover,battle_pic=Hydranoid_pic)
Akobos = Character('Akobos',100,1000,19,AkobosAttack,ClassicGuard,AkobosRecover,battle_pic=Akobos_pic)
Nightmare = Character('Nightmare',150,1000,17,NightmareAttack,NightmareGuard,NightmareRecover,battle_pic=Nightmare_pic)
Destiny = Character('Destiny',80,30,12,DestinyAttack,DestinyGuard,DestinyRecover,battle_pic=Destiny_pic)
Grace = Character('Grace',0,0,0,NullMove,NullMove,NullMove,battle_pic=Grace_pic)
Finlay = Character('Finlay',0,0,0,NullMove,NullMove,NullMove,battle_pic=Finlay_pic)
Ken = Character('Ken',0,0,0,NullMove,NullMove,NullMove,battle_pic=Ken_pic)
Junia = Character('Junia',0,0,0,NullMove,NullMove,NullMove,battle_pic=Junia_pic)
Overlord = Character('Overlord',200,1500,30,OverlordAttack,OverlordGuard,OverlordRecover,battle_pic=Overlord_pic)
#Ross = Character('Ross',0,0,0,NullMove,NullMove,NullMove) (dad)
#Abby = ... (in episode 2)

#story functions
def Episode1_1():
    '''do episode 1, scene 1
    function parameters are for character placements, and especially if a battle is triggered at the end of a scene (not for 1 though; for 2_1, 4_1, 5_1)
    '''
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_1':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_1" and dialogue_index < len(scene_1_dialogue):
                            dialogue_index += 1
                            if dialogue_index == 39:
                                stopLoopingMusic()
                                playMusic(ExceedraLonelyTheme1,'music',Forever=True)
                            if dialogue_index >= len(scene_1_dialogue): #go to next scene
                                stopLoopingMusic()
                                scene = "scene_2.1"
                                dialogue_index = 0
                                Episode1_2_1()
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        screen.blit(dreamspace, (0, 0))
        ExceedraMain.BattlePosition(100, 500)
        Overlord.BattlePosition(900,500)
        playMusic(Dreamspace_theme,'music',Forever=True)
        draw_text_box()
        if dialogue_index < len(scene_1_dialogue):
            draw_text(screen, scene_1_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
        draw_hint_text()  # Display hint
        
def Episode1_2_1():
    '''do episode 1, scene 2, before battle'''
    Character.character1 = ExceedraMain
    Character.character2 = Hydranoid
    Character.background = school
    Character.music = BattleTheme1
    Character.next_scene = Episode1_2_2
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_2.1':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_2.1" and dialogue_index < 22:
                            dialogue_index += 1
                        elif scene == 'scene_2.1' and dialogue_index == 22:
                            dialogue_index = 22
                            stopLoopingMusic()
                            Character.battleOn = not Character.battleOn  # Trigger battle
                            scene = 'scene_2.2'
                            Battle(Character.character1,Character.character2,Character.background,Character.music,Character.next_scene)
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_2.1":
            stopLoopingMusic()
            screen.blit(school, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Destiny.BattlePosition(600,500)
            Hydranoid.BattlePosition(900,500)
            playMusic(Hydranoid_DestinyTheme,'music',Forever=True)
            draw_text_box()
            if dialogue_index < 22:
                draw_text(screen, scene_2_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_2_2():
    '''do episode 1, scene 2, after battle'''
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_2.2':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_2.2" and dialogue_index < len(scene_2_dialogue):
                            dialogue_index += 1
                            if dialogue_index >= len(scene_2_dialogue):
                                stopLoopingMusic()
                                scene = "scene_3"
                                dialogue_index = 0
                                Episode1_3()
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_2.2":
            stopLoopingMusic()
            screen.blit(school, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Destiny.BattlePosition(600,500)
            Hydranoid.BattlePosition(900,500)
            playMusic(ExceedraLonelyTheme2,'music',Forever=True)
            draw_text_box()
            if dialogue_index < len(scene_2_dialogue):
                draw_text(screen, scene_2_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_3():
    '''do episode 1, scene 3'''
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_3':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_3" and dialogue_index < len(scene_3_dialogue):
                            dialogue_index += 1
                            if dialogue_index == 16:
                                stopLoopingMusic()
                                playMusic(ExceedraAngryTheme,'music')
                            if dialogue_index == 25:
                                pygame.mixer.music.stop()
                                playMusic(ExceedraAngryTheme,'music')
                            if dialogue_index >= len(scene_3_dialogue):
                                pygame.mixer.music.stop()
                                scene = "scene_4.1"
                                dialogue_index = 0
                                Episode1_4_1()
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_3":
            stopLoopingMusic()
            screen.blit(library, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Finlay.BattlePosition(300,500)
            Ken.BattlePosition(500,500)
            Grace.BattlePosition(700,500)
            playMusic(LibraryTheme,'music',Forever=True)
            draw_text_box()
            if dialogue_index < len(scene_3_dialogue):
                draw_text(screen, scene_3_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_4_1():
    '''do episode 1, scene 4,before battle'''
    Character.character1 = ExceedraMain
    Character.character2 = Akobos
    Character.background = hill
    Character.music = AkobosBattle
    Character.next_scene = Episode1_4_2
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_4.1':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_4.1" and dialogue_index < 18:
                            dialogue_index += 1
                            if dialogue_index == 4:
                                playMusic(AkobosAppears,'music',Forever=True)
                        elif scene == 'scene_4.1' and dialogue_index == 18:
                            dialogue_index = 18
                            stopLoopingMusic()
                            Character.battleOn = not Character.battleOn  # Trigger battle
                            scene = 'scene_4.2'
                            Battle(Character.character1,Character.character2,Character.background,Character.music,Character.next_scene)
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_4.1":
            stopLoopingMusic()
            screen.blit(hill, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Hydranoid.BattlePosition(300,500)
            Akobos.BattlePosition(900,500)
            draw_text_box()
            if dialogue_index < 18:
                draw_text(screen, scene_4_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_4_2():
    '''do episode 1, scene 4, after battle'''
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_4.2':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_4.2" and dialogue_index < len(scene_4_dialogue):
                            dialogue_index += 1
                            if dialogue_index >= len(scene_4_dialogue):
                                scene = "scene_5.1"
                                dialogue_index = 0
                                Episode1_5_1()
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_4.2":
            stopLoopingMusic()
            screen.blit(hill, (0, 0))
            draw_text_box()
            if dialogue_index < len(scene_4_dialogue):
                draw_text(screen, scene_4_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_5_1():
    '''do episode 1, scene 5, before battle'''
    Character.character1 = ExceedraMain
    Character.character2 = Nightmare
    Character.background = dreamspace
    Character.music = NightmareBattle
    Character.next_scene = Episode1_5_2
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_5.1':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_5.1" and dialogue_index < 37:
                            dialogue_index += 1
                        elif scene == 'scene_5.1' and dialogue_index == 34:
                            stopLoopingMusic()
                            screen.blit(dreamspace,(0,0))
                            playMusic(NightmareAppears,'music',Forever=True)
                            Nightmare.BattlePosition(900,100)
                        elif scene == 'scene_5.1' and dialogue_index == 37:
                            stopLoopingMusic()
                            playMusic(NightmareScream,'sound')
                            dialogue_index = 37
                            Character.battleOn = not Character.battleOn  # Trigger battle
                            scene = 'scene_5.2'
                            Battle(Character.character1,Character.character2,Character.background,Character.music,Character.next_scene)
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_5.1":
            stopLoopingMusic()
            screen.blit(house, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Junia.BattlePosition(900,500)
            draw_text_box()
            if dialogue_index < 37:
                draw_text(screen, scene_5_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode1_5_2():
    '''do episode 1, scene 5, after battle; once this scene is completed, go back to menu to move on to episode 2'''
    global dialogue_index, scene
    while Character.EpisodeOn and scene == 'scene_5.2':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not Character.battleOn:
                    if event.key == pygame.K_RETURN:
                        if scene == "scene_5.2" and dialogue_index < len(scene_5_dialogue):
                            dialogue_index += 1
                            if dialogue_index == 41:
                                playMusic(NightmareDying,'music',Forever=True)
                            if dialogue_index == 48:
                                stopLoopingMusic()
                                playMusic(NightmareDeath,'sound')
                            if dialogue_index >= len(scene_5_dialogue):
                                stopLoopingMusic()
                                dialogue_index = 0                   
                                #when the episode is completed, make Episode1_completed True and return to Menu
                                Character.Episode1_completed == True
                                if Character.Episode1_completed:
                                    scene = 'start_menu'
                                    Character.EpisodeOn = not Character.EpisodeOn
                                    Menu()
                    elif event.key == pygame.K_BACKSPACE:  # On Backspace key
                        if dialogue_index > 0:
                            dialogue_index -= 1  # Go to previous line
                        else:
                            dialogue_index = 0  # Keep at the first line
                
        if scene == "scene_5.2":
            stopLoopingMusic()
            screen.blit(dreamspace, (0, 0))
            ExceedraMain.BattlePosition(100, 500)
            Nightmare.BattlePosition(900,500)
            draw_text_box()
            if dialogue_index < len(scene_5_dialogue):
                draw_text(screen, scene_5_dialogue[dialogue_index], DIALOGUE_FONT, 20, height - 110)
            draw_hint_text()  # Display hint

def Episode2_1_1():
    '''do episode 2'''
    global dialogue_index, scene
    if Character.Episode1_completed == False: #until episode 1 completed, do nothing if called
        pass
    else:
        if Character.Episode1_completed == True and scene == 'scene_6.1': #when episode 1 completed and ep2 selected from menu
            make_text('Episode 2 will come out soon!','Corbel',35,blue,600,600)
            stopLoopingMusic()
            #eventually more code will be added to run episode 2

def Episode3_1():
    '''do episode 3'''
    global dialogue_index, scene
    if Character.Episode2_completed == False:
        pass
    else:
        #the episode
        pass

def FinalEpisode_1():
    '''do episode 4 (final)'''
    global dialogue_index, scene
    if Character.Episode3_completed == False:
        pass
    else:
        #the episode
        pass
        Character.FinalEpisode_completed = True
        if Character.Episode1_completed and Character.Episode2_completed and Character.Episode3_completed and Character.FinalEpisode_completed:
            Character.Game_completed=True
            
def Credits():
    while Character.Game_completed:
        #black background
        screen.fill(black)
        #the end (big)
        make_text('THE END','arialblack',115,white,width/2,height/2)
        
        pygame.display.flip()
        
#now that all necessary variables and functions have been defined,
#run the main functions of the game; treat functions like substitutions of bits of code
while running:
    mouse = pygame.mouse.get_pos() #mouse position
    events = pygame.event.get()
    for event in events:
        
        if event.type == pygame.QUIT:  
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = True
                pause_the_game()
                
            elif event.key == pygame.K_0:
                running = False

    if scene == 'start_menu' and Character.EpisodeOn == False: 
        Menu(events)
    
    if scene == 'scene_1':
        Episode1_1()
    
    if Character.Game_completed: 
        Credits()
    
    pygame.display.flip()
    
pygame.quit()
