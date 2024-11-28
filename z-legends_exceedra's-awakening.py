#first we import pygame
import pygame
import time

#The real first thing is to define a basic class for every character. Characters can then be created by variables to a class call
class Character:
    '''
    This class contains variables related to him for the battle system, such as health, recovery and energy and attack potential stats
    Has variables for the name and stats of the character.
    Health is the amount of HP (aka hit points) a character has... it's how they stay alive, until health is reduce to 0, at which point they die'
    Recovery is to determine the amount of energy and health a character will recover when using that move
    Energy is the amount of energy a character has to use a move. it's a special stat that helps prevent spamming of a single attack, and so requires players to have a strategy
    Attack potential is a special stat for certain characters. It's used when calculating damage, and acts as a critical-hit ratio (basically, this stat helps give damage moves a chance to do more damage than usual)
    '''
    def __init__(self, name, health, recovery, energy, attack_potential):
        self.name = name
        self.health = health
        self.recovery = recovery
        self.energy = energy
        self.attack_potential = attack_potential
    
class Move:
    '''
    This class will serve to define all the moves similarly to how characters will be created.
    Has variables for the name, energy consumption and/or damage caused, protection given and recovery made of the move
    Damage is the amount of damage (health lost by opponent) made by the move
    Protection is...
    '''
    def __init__(self, name, damage, protection, recovery, energy_consumption):
        self.name = name
        self.damage = damage
        self.protection = protection
        self.recovery = recovery
        self.energy_consumption = energy_consumption
    

#next, we make functions. the first function would be for the battle system, and uses the classes defined above
def battle_system():
    '''
    This function makes the battle system work.
    '''
    pass

def make_text(text, font):
    '''functio to make texts and rectangles for them'''
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def make_button():
    '''buttons'''
    pass

def pause_the_game():
    pygame.mixer.music.pause()
    largePause = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = make_texts("Paused", largePause)
    TextRect.center = ((width/2),(height/2))
    screen.blit(TextSurf, TextRect)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    
#finally, run the game with battles, dialogue, backgrounds and animations in a while True loop
if __name__ == '__main__':
    pygame.init()  
    
    #initialize characters using the Characters class
    Exceedra = Character('Exceedra',100,30,50,30)
    Hydranoid = Character('Hydranoid',100,30,50,30)
    Akobos = Character('Akobos',100,30,50,30)
    Nightmare = Character('Nightmare',100,30,50,30)
    
    #sounds and music
    press_button_sound = pygame.mixer.Sound('pokemon-a-button.wav')
    Dreamspace_theme = 'Dreamspace_Dark.wav'
    ExceedraLonelyTheme1 = 'Exceedras_Defiance.wav'
    Hydranoid_DestinyTheme = ''
    BattleTheme1 = ''
    ExceedraLonelyTheme2 = ''
    Library_ClassroomTheme = ''
    ExceedraAngryTheme = ''
    AkobosAppears = ''
    AkobosBattleTheme = ''
    NightmareAppears = ''
    NightmareBattleTheme = ''
    
    #initialize text and menu screen with buttons
    res = (720,720)  
    screen = pygame.display.set_mode(res)  
    pygame.display.set_caption('Z-Legends: Exceedra\'s Awakening')
    color = (255,255,255)  
    color_light = (170,170,170)  
    color_dark = (0,0,0)  
    width = screen.get_width()    
    height = screen.get_height()  
    smallfont = pygame.font.SysFont('Corbel',35)  
    text1 = smallfont.render('Episode 1' , True , color)  
    text2 = smallfont.render('Episode 2' , True , color)
    text3 = smallfont.render('Episode 3' , True , color)
    text4 = smallfont.render('Episode 4' , True , color)
    
    #backgrounds and images

    while True:  
        
        for event in pygame.event.get():  
              
            if event.type == pygame.QUIT:  
                pygame.quit()  
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    pause_the_game()
            # stores the (x,y) coordinates into  
            # the variable as a tuple  
            mouse = pygame.mouse.get_pos()   
            
            #checks if a mouse is clicked  
            if event.type == pygame.MOUSEBUTTONDOWN:  
                  
                #if the mouse is clicked on the  
                # button the game is terminated  
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
                    pygame.quit()  
                      
        # fills the screen with a color  
        screen.fill((60,25,60))  
          
        # if mouse is hovered on a button it  
        # changes to lighter shade  
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
            pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])  
              
        else:  
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])  
          
        # superimposing the text onto our button  
        screen.blit(text1 , (width/2+50,height/2))  
          
        # updates the frames of the game  
        pygame.display.update()
        
        #runs the rest of the game
        
        #pygame.mixer.music.load(Dreamspace_theme)
        #pygame.mixer.music.play(-1)
