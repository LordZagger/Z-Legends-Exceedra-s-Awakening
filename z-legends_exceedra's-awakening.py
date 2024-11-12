#this file is for copy-pasting purposes ;)

#first we import pygame
import pygame

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

def Title_Menu():
    '''
    This function is to make the title and menu screens of the game.
    '''
    pass
    
#next, we make variables for every character using the Character class
Exceedra = Character('Exceedra',100,30,50,30)
Hydranoid = Character('Hydranoid',100,30,50,30)
Akobos = Character('Akobos',100,30,50,30)
Nightmare = Character('Nightmare',100,30,50,30)


#finally, run the game with battles, dialogue, backgrounds and animations in a while True loop
i = 2 #this is just temporary, the loop will eventually be changed to a while True loop, right now we limit the number of iterations so we don't have to deal with infinite loops
while i > 0:
    print(None)
    i -= 1
