#Comments in first person by LordZagger
#import needed modules and functions
import pygame                 #duh
import sys                    #for exiting without errors
from random import choice     #for the npc opponent to choose a random move
from random import randrange  #for a random number

#Initialize pygame
pygame.init()

#Screen setup (size, icon, size, caption)
Zlogo = pygame.image.load('Screenshot 2024-11-24 161343.png')
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Z-Legends: Exceedra's Awakening")
pygame.display.set_icon(Zlogo)

# Colors and Fonts (Jin and I defined different shades of red, green, and blue;
#Jin's are in Uppercase, mine are in Lowercase)
white = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DIALOGUE_FONT = pygame.font.Font("animeace2_reg.ttf", 21)
HINT_FONT = pygame.font.Font("animeace2_reg.ttf", 12)
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

# Game States (global variables for transitions and making the game run)
pause = False
scene = "start_menu"  # Start with the menu/title screen
dialogue_index = 0
running = True
Locked1 = False #for locked buttons and/or moves for character 1 (in battles)
Locked2 = False #for locked buttons and/or moves for character 2 (in battles)
battle_ON = False #if a battle is in progress
battle_e1_s2 = False #to see which battle is currently on
battle_e1_s4 = False
battle_e1_s5 = False
battle_e2_s1 = False
Episode1_completed = False #to see which episodes are completed
Episode2_completed = False
Episode3_completed = False
Episode4_completed = False
Game_completed = False
CH1 = '' #for restarting battles, we save the battle function call parameters in variables and call them as global in functions
CH2 = ''
BACKGROUND = ''
ZE_BATTLE = ''
MUSIC = ''

#Music and sounds
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
aProblem = 'A_theme_for_episode_2.wav' #I thought I would use this in episode 2, but I thought this would fit better for the mood at the start of episode 3
#other themes

#background images and character images
dreamspace = pygame.image.load("dreamspace.png")  # Episode 1 Scene 1 background
dreamspace = pygame.transform.scale(dreamspace, (SCREEN_WIDTH, SCREEN_HEIGHT))

school = pygame.image.load("school.png")  # Episode 1 Scene 2 background
school = pygame.transform.scale(school, (SCREEN_WIDTH, SCREEN_HEIGHT))

library = pygame.image.load('Library.png') # Episode 1 Scene 3 background
library = pygame.transform.scale(library, (SCREEN_WIDTH,SCREEN_HEIGHT))

hill = pygame.image.load('hill.png') # Episode 1 Scene 4 background
hill = pygame.transform.scale(hill,(SCREEN_WIDTH,SCREEN_HEIGHT))

house = pygame.image.load('House.png') # Episode 1 Scene 5 background
house = pygame.transform.scale(house,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Character Images: first load them, then scale them
Exceedra1_pic = pygame.image.load("exceedra1.png")  # Main character (Exceedra) sprite episode 1
Exceedra1_pic = pygame.transform.scale(Exceedra1_pic, (700, 700))

Exceedra3_pic = pygame.image.load("exceedra3.png")  # Exceedra sprite episode 3
Exceedra3_pic = pygame.transform.scale(Exceedra3_pic, (700, 700))

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

Nightmare_pic = pygame.image.load('nightmare.png') #Nightmare sprite
Nightmare_pic = pygame.transform.scale(Nightmare_pic,(700,700))

#dialogues for Episode 1 (scenes 1-5)
#scene 1
scene_1_dialogue = [
    "[Exceedra awakes in a dark dreamspace]",
    "Overlord: Welcome, Son. It’s been a while since you last came here.",
    "Exceedra: What do you want?",
    "Overlord: Nothing much. Except to know how my son is doing.",
    "[Exceedra grins angrily.]",
    "Exceedra: Yea right. What do you really want?",
    "Overlord: You do realize you wandered in here on your own, right?",
    "[Exceedra is shocked.]",
    "Exceedra: [mumbling] Wait, what? Why would I come here…",
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
    "Hydranoid: [smiling] You’d be crying right now if you didn’t get 100. [tease] Remember last time?",
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
    "Hydranoid: All right… [Exceedra offers his hand so Hydranoid can get up.]",
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
    "Exceedra: It won’t be like that for long. [heroically] For the sake of the plot, I’m gonna catch up.",
    "Hydranoid: Well at least you have powers. That’s the one thing humans can’t have that you do.",
    "Exceedra: [dark, and taking a dark face] Well… even that has its troubles…",
    "[Hydranoid catches the dark tone and gets curious, but he decides to let it go for later.]",
    "Hydranoid: [taking one last bite] Are we still on for the mission later?",
    "Exceedra: [also done his food, getting up] Aye. We’re gonna rat out the rat and kick him in the butt right to the other side of the galaxy!",
    "[Hydranoid and Exceedra, face to face, smiling at each other.]",
    "Hydranoid: [happy and serious] Well said, Cap! Let’s go kick butt… after Chem.",
    "[They all part ways.]"
]
#Scene 3
scene_3_dialogue = [
    "[Library. Exceedra and his classmates/friends Ken, Grace and Finlay are at a table, working… but actually really just talking.]",
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
#Scene 4
scene_4_dialogue = [
    "[Exceedra and his team are downtown, talking through communicators. Exceedra is close to Parliament Hill, talking to his brother.]", 
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
    "Akobos: Damn! [Rushing at Exceedra] This isn’t over!", 
    "[Exceedra easily dodges and trips Akobos. As Akobos trips, Hydranoid slams his head with the hilt of his sword, right into the ground.]", 
    "[With that, Akobos has been taken down and the brothers rejoice (they happily high five.)]", 
    "Exceedra: That was too easy!", 
    "Hydranoid: [happily] Yeah! [Darker, in thought] Too easy…"
]
#Scene 5
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

#dialogue for Episode 2 (scenes 6-) {TO UPDATE}
#scene 6
scene_6_dialogue = [
    
]

#classes for characters and moves
class Character:
    '''
    This class contains variables related to them for the battle system, such as health, recovery and energy and attack potential stats
    Has variables for the name, stats and moves of a character.
    Health is the amount of HP (aka life/hit points) a character has. it's how they stay alive, until health is reduce to 0, at which point they die
    Recovery is to determine the amount of energy and health a character will recover when using that move
    Energy is the amount of energy a character has to use a move. it's a special stat that helps prevent spamming of a single attack, and so requires players to have a strategy
    Attack potential is a special stat that helps determine which attack lands in a pinch
    battle_pic is the character's png image (image name) for battles, optional argument (though 99.9% of the time it's not None)
    og stands for original, those attributes help reset the characters stats in the reset method
    '''
    def __init__(self, name, health, energy, attack_potential, AttackMove, GuardMove, RecoverMove, battle_pic=None):
        '''
        initialize a character
        '''
        #current stats to keep track off
        self.name = name
        self.health = health
        self.energy = energy
        self.attack_potential = attack_potential
        self.AttackMove = AttackMove
        self.GuardMove = GuardMove
        self.RecoverMove = RecoverMove
        self.battle_pic = battle_pic
        
        #original stats, to reset the character and as references during battles
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
        health and energy
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
        if battle_ON == False:
            if self.battle_pic != None:
                screen.blit(self.battle_pic, (x,y))

        else:

            #character health bar; we keep while health >= 0 because if it falls below that, there might be an error
            #we hopefully manage to avoid the error, and let a later function correct the health value
            if self.health >= 0:
                screen.blit(self.battle_pic, (x,y))
                
                if self == Nightmare:
                    pygame.draw.rect(screen, health_bar_red, (x-180, y+40, 5*self.og_health, 10))
                    pygame.draw.rect(screen, health_bar_green, (x-180, y+40, 50 - (5 * (10 - self.health)), 10))
                else:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+80, 5*self.og_health, 10))
                    pygame.draw.rect(screen, health_bar_green, (x+80, y+80, 50 - (5 * (10 - self.health)), 10))
                #also draw energy bar if playable character
                if self == CH1:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+20, 5*self.og_energy, 10))
                    pygame.draw.rect(screen, BLUE, (x+80, y+20, 50 - (5 * (10 - self.energy)), 10))
                
class Move:
    '''
    This class will serve to define all the moves similarly to how characters will be created.
    Has variables for the name, energy consumption and/or damage caused, protection given and recovery made of the move
    Damage is the amount of damage (health lost by opponent) made by the move
    Specialty is the type of the move (attack, guard or recover) (I'm tired of using Type all the time), is used to identify and name the type of the move
    recovery is how much energy and health are recovered
    energy consumption is the amount of energy needed to use a move
    '''
    def __init__(self, name, damage, specialty, recovery, energy_consumption):
       '''
       initialize a move
       '''
       self.name = name
       self.damage = damage
       self.specialty = specialty
       self.recovery = recovery
       self.energy_consumption = energy_consumption

#moves    
ExceedraMainAttack = Move('Dragon Fist of Fury',30,'ATTACK',0,10)
ExceedraGuard = Move('Tail Block',0,'GUARD',0,3)
ExceedraRecover = Move('Dragon Spirit',0,'RECOVER',15,0)
HydranoidAttack = Move('Sword Slash',10,'ATTACK',0,5) #I know his sprite doesn't have a sword, but canonically... he uses a sword
ClassicGuard = Move('Block',0,'GUARD',0,2)
ClassicRecover = Move('Heal',0,'RECOVER',10,0)
AkobosAttack = Move('Scythe of Demise',25,'ATTACK',0,10) #His sprite has a trident, but canonically he can summon a scythe for battle
AkobosRecover = Move('Demon Blood',0,'RECOVER',15,0)
NightmareAttack = Move('Mental Plague',30,'ATTACK',0,20)
NightmareGuard = Move('Dream Trapped',0,'GUARD',0,10)
NightmareRecover = Move('Dream Eater',0,'RECOVER',20,0)
NullMove = Move('Play Dead',0,None,0,0) #nothing, just for characters who aren't in battles
DestinyAttack = Move('Time Pulse',30,'ATTACK',0,15) #destiny is available for battle in episode 2
DestinyGuard = Move('Time Stop',0,'GUARD',0,5)
DestinyRecover = Move('Centered',0,'RECOVER',10,0)
OverlordAttack = Move('Dark En',50,'ATTACK',0,30) #overlord battle is in episode 2
OverlordGuard = Move('Black Shield',0,'GUARD',0,5)
OverlordRecover = Move('Shadow Bath',0,'RECOVER',25,0)

#characters (NPC opponents are "overloaded" on energy to avoid their moves getting locked, though canonically they have around the same energy as ExceedraMain)
ExceedraMain = Character('Exceedra',100,50,20,ExceedraMainAttack,ExceedraGuard,ExceedraRecover,battle_pic=Exceedra1_pic)
Hydranoid = Character('Hydranoid',70,1000,12,HydranoidAttack,ClassicGuard,ClassicRecover,battle_pic=Hydranoid_pic)
Akobos = Character('Akobos',100,1000,19,AkobosAttack,ClassicGuard,AkobosRecover,battle_pic=Akobos_pic)
Nightmare = Character('Nightmare',150,1000,17,NightmareAttack,NightmareGuard,NightmareRecover,battle_pic=Nightmare_pic)
Destiny = Character('Destiny',80,30,15,DestinyAttack,DestinyGuard,DestinyRecover,battle_pic=Destiny_pic)
Grace = Character('Grace',0,0,0,NullMove,NullMove,NullMove,battle_pic=Grace_pic)
Finlay = Character('Finlay',0,0,0,NullMove,NullMove,NullMove,battle_pic=Finlay_pic)
Ken = Character('Ken',0,0,0,NullMove,NullMove,NullMove,battle_pic=Ken_pic)
Junia = Character('Junia',0,0,0,NullMove,NullMove,NullMove,battle_pic=Junia_pic)
Overlord = Character('Overlord',200,1500,30,OverlordAttack,OverlordGuard,OverlordRecover,battle_pic=Overlord_pic)

#main functions used by the game (the main while loop)
#plays music and sound
def playMusic(sound,Type,Forever=False):
    '''
    function to play sound or music
    '''
    if Type == 'sound':
        da_sound = pygame.mixer.Sound(sound) #da_sound... LOL
        pygame.mixer.Sound.set_volume(da_sound,0.2)
        pygame.mixer.Sound.play(da_sound)
        
    elif Type == 'music':
        pygame.mixer.music.load(sound)
        if Forever == False:
            pygame.mixer.music.play()
        elif Forever == True:
            pygame.mixer.music.play(-1)

#creates text, used for pause and menu screens
def make_text(text,font,size,color,x,y):
    '''function to make texts and rectangles for them
    helper function of make_button or function to display text that doesn't need button
    '''
    the_font = pygame.font.SysFont(font,size)
    the_text = the_font.render(text,True,color)
    TextSurface, TextRectangle = the_text, the_text.get_rect()
    TextRectangle.center = (x,y)
    screen.blit(TextSurface, TextRectangle)

#pause and unpause the game            
def unpause():
    '''unpauses the game'''
    global pause
    pygame.mixer.music.unpause()
    pause = False
    pygame.display.flip()

def pause_the_game():
    '''pauses the game'''
    pygame.mixer.music.pause()
    
    make_text('PAUSE',"comicsansms",100,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    
    while pause:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    unpause()
                elif event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()

#These next 3 functions make the dialogue run smoothly...
#and makes it look nice too! :)   good job Jin!
def draw_text(surface, text, font, x, y, color=black, max_width=SCREEN_WIDTH-40):
    '''render text with wrapping, for dialogues'''
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

def draw_text_box():
    '''draws the text box for dialogues during story scenes'''
    pygame.draw.rect(screen, white, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))  # Bottom box
    pygame.draw.rect(screen, black, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120), 5)  # Border

def draw_hint_text():
    '''draw the hint text (explaining how to move on with the dialogue)'''
    hint_text = "Press Enter to continue, Backspace to go back"
    hint_surface = HINT_FONT.render(hint_text, True, black)
    hint_x = SCREEN_WIDTH - hint_surface.get_width() - 10  # Align to the bottom-right corner
    hint_y = SCREEN_HEIGHT - 20  # Above the bottom of the box
    screen.blit(hint_surface, (hint_x, hint_y))

#ultimately, they make...
def dialogueBox(scene_list):
    '''combines above 3 functions to make the dialogue for story scenes'''
    global dialogue_index, DIALOGUE_FONT, SCREEN_HEIGHT
    draw_text_box()
    if dialogue_index < len(scene_list):
        draw_text(screen, scene_list[dialogue_index], DIALOGUE_FONT, 20, SCREEN_HEIGHT - 110)
    draw_hint_text()

#in-game BUTTONS! (not the ones you button your shirt with)
def make_button(text,font,text_size,text_color,x,y,button_width,button_height,button_color,highlight_color,Type,action):
    '''as per the name, function to make buttons. shows text made with make_text at text_color, 
    button_color is the button's color and whenever the cursor is on the button, 
    its colors turns to highlight_color if the button is associated to a function, 
    the function call is placed at action can_cancel_move is for buttons connected to moves in battles, 
    helps lock or unlock a button to respectively prevent or allow the use of a move, default is false (for menu buttons)
    Type is for me, to see if it's a menu or battle button
    '''
    #all possible things with the button (when clicking)
    global scene, dialogue_index, CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC #lots of global variables to consider
    
    #collision detection with the mouse (unfortunately we gotta redefine the mouse in here too)
    rect = pygame.Rect(x,y,button_width,button_height)
    mouse = pygame.mouse.get_pos()
    current_collision = rect.collidepoint(mouse)
    click = pygame.mouse.get_pressed()
    
    #if the mouse is clicked and on the button
    if click[0] == 1 and current_collision:
        playMusic(press_button_sound,'sound')
        if scene == 'start_menu':
            scene = action
            dialogue_index = 0
            if action == 'scene_1':
                playMusic(Dreamspace_theme,'music',Forever=True)
        elif scene in ['battle_e1_s2','battle_e1_s4','battle_e1_s5','battle_e2_s1']:
            if action == 'quit': #to quit the game after losing a battle
                pygame.quit()
                sys.exit()
            elif action == Battle: #to restart the battle after losing, with the saved parameters
                #reset characters' stats
                CH1 = CH1.reset()
                CH2 = CH2.reset()
                #start the battle
                playMusic(MUSIC,'music',Forever=True)
                action(CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC)
            elif action == None:
                print("Nuh-Uh! Use your own moves (or Recover if that's the situation you're in!)") #aka do nothing; no worries, this won't cause a turn to go by, since the opponent also won't do anything (he only does things when Attack, Guard or Recover)
            elif action in [Attack,Guard,Recover]: #the battle moves
                action(CH1,CH2)

    if current_collision:
        #switch button colour to highlight_color when mouse is on button
        pygame.draw.rect(screen,highlight_color,(x,y,button_width,button_height))
    else:
        #draw button at position x,y and with dimensions button_width and button_height, mormal colour
        pygame.draw.rect(screen,button_color,(x,y,button_width,button_height))
        
    make_text(text,font,text_size,text_color,x+button_width/2,y+button_height/2)
        
#the main menu/title screen
def Menu():
    '''
    makes the menu, which contains the title and buttons that activate scenes and therefore episodes
    of the story
    '''
    #background colour
    screen.fill(black)
    
    #title (game name)
    make_text("Z-Legends: Exceedra's Awakening",'comicsansms',70,white,SCREEN_WIDTH/2,100)
    #buttons for each episode
    make_button('Episode 1','Corbel',35,white,500,210,200,70,red,green,'menu','scene_1')
    if Episode1_completed:
        make_button('Episode 2','Corbel',35,white,500,310,200,70,red,green,'menu','scene_6')
    if Episode2_completed:
        make_button('Episode 3','Corbel',35,white,500,410,200,70,red,green,'menu','scene_11')
    if Episode3_completed:
        make_button('Final Episode','Corbel',35,white,500,510,200,70,red,green,'menu','scene_16_1')
    
#the 5 battle-system functions
#game over (if you lose your battle)
def try_again(character1,character2,background,battle_name,music):
    '''tell the user to try again after losing a battle'''
    #lost the battle sound    
    playMusic(BattleLost,'sound')
    #buttons
    screen.fill(black)
    make_button('Try again?','Corbel',35,white,500,260,200,70,red,green,'battle',Battle)
    make_button('I give up...','Corbel',35,white,500,560,200,70,red,green,'battle','quit')
        
    pygame.display.flip()

#rock-paper-scissors like: rock=attack, paper=guard, scissors=recover
#these functions are what happens when character1 (you!) selects that corresponding move
def Attack(character1,character2):
    '''attack scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.GuardMove: #if opponent guards and you attack, no damage
        character2.losePower(0,character2.GuardMove.energy_consumption)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove: #if opponent recovers and you attack, damage for the opponent
        character2.losePower(character1.AttackMove.damage,0)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        
    elif opponent_move == character2.AttackMove: #if both of you attack
        #prompt for special event to determine which move lands
        start = pygame.time.get_ticks()
        SPACEBAR_count = 0
        while pygame.time.get_ticks() - start < 1000:
            #do the following for 1 seconds (1000 milliseconds):
            #make the user press SPACEBAR as many times as they can to help boost
            #their chances of landing their attack instead of the npc opponent
            make_text('To amp up your power keep pressing SPACEBAR!!!','Corbel',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

            for event in pygame.event.get():  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SPACEBAR_count += 1
            pygame.display.flip()
            
        potential1 = character1.attack_potential + SPACEBAR_count
        potential2 = character2.attack_potential + randrange(1,11)
        if potential1 >= potential2:
            character2.losePower(character1.AttackMove.damage,0)
            character1.losePower(0,character1.AttackMove.energy_consumption)
            print(character1.name,'did ATTACK;',character2.name,'did',opponent_move.specialty,'but',character1.name,'landed damage!') #description of the turn
        else:
            character1.losePower(character2.AttackMove.damage,0)
            character2.losePower(0,character2.AttackMove.energy_consumption)
            print(character1.name,'did ATTACK;',character2.name,'did',opponent_move.specialty,', but',character2.name,'landed damage!') #description of the turn
        

def Guard(character1,character2):
    '''guard scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.AttackMove: #if the opponent attacks and you guard, no damage
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.AttackMove.energy_consumption)
        
    elif opponent_move == character2.GuardMove: #if the opponent guards and you guard, nothing
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.GuardMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove: #if the opponent recovers and you guard, they recover, you nothing
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.Recover(character2.RecoverMove.recovery)
        #if the opponent recovers up to max stats
        if character2.health >= character2.og_health:
            character2.health = character2.og_health
        if character2.energy >= character2.og_energy:
            character2.energy = character2.og_energy 
            
    print(character1.name,'did GUARD;',character2.name,'did',opponent_move.specialty) #description of the turn

    
def Recover(character1,character2):
    '''recover scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.GuardMove: #if the opponent guards and you recover, good for you, they wasted a turn
        character1.Recover(character1.RecoverMove.recovery)
        character2.losePower(0,character2.GuardMove.energy_consumption)
        
    elif opponent_move == character2.RecoverMove: #if both recover, both recover
        character1.Recover(character1.RecoverMove.recovery)
        character2.Recover(character2.RecoverMove.recovery)
        #if the opponent recovers up to max stats
        if character2.health >= character2.og_health:
            character2.health = character2.og_health
        if character2.energy >= character2.og_energy:
            character2.energy = character2.og_energy 
        
    elif opponent_move == character2.AttackMove: #if the opponent attacks and you recover, you take damage
        character1.losePower(character2.AttackMove.damage,0)
        character2.losePower(0,character2.AttackMove.energy_consumption)
    
    #if you recover up to your max stats:
    if character1.health >= character1.og_health:
        character1.health = character1.og_health
    if character1.energy >= character1.og_energy:
        character1.energy = character1.og_energy  
        
    print(character1.name,'did RECOVER;',character2.name,'did',opponent_move.specialty) #description of the turn
        
#run the battle      
def Battle(character1,character2,background,battle_name,music):
    '''function for battles
    next_scene is function call of following scene in story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    battle_name is to keep track of what battle is going on; the battle's corresponding scene has the same name
    '''
    #start the battle    
    global Locked1, Locked2, dialogue_index, battle_ON, battle_e1_s2, battle_e1_s4, battle_e1_s5, battle_e2_s1, CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene
    #save the parameters in the global variables so we can use them in external functions (functions not directly connected to this one) requiring them
    CH1 = character1
    CH2 = character2
    BACKGROUND = background
    ZE_BATTLE = battle_name
    MUSIC = music
    
    #during the battle
    while battle_ON:
        for event in pygame.event.get():
            #pausing and/or exiting
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    pause_the_game()
                if event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
                
            #setup the background and character placements
            screen.blit(background,(0, 0))
            if battle_name == 'battle_e1_s2':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650) #hydranoid
            elif battle_name == 'battle_e1_s4' or battle_name == 'battle_e1_s5':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500) #akobos/nightmare
            elif battle_name == 'battle_e2_s1':
                pass
                    
            #controlling energy and buttons for character 1 (usually Exceedra)
            if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                Locked1 = True
            elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                Locked1 = False
            
            if Locked1 == True:
                make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle',None)
                make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle',None)
                make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
            else:
                make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)    
            
            #controlling energy and buttons for character 2 (NPC Opponent; though it will probably never get to that)
            if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                Locked2 = True
            elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                Locked2 = False
            
            if Locked2 == True:
                character2.movepool = [character2.RecoverMove]
                make_button(character2.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character2.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character2.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character2.movepool = [character2.AttackMove, character2.GuardMove, character2.RecoverMove]
                make_button(character2.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character2.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character2.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
                        
            #losing
            if character1.health <= 0 and character2.health > 0:
                pygame.mixer.music.stop()
                try_again(character1,character2,background,battle_name,music)
            
            #winning
            elif character1.health > 0 and character2.health <= 0:
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                if battle_name == 'battle_e1_s2':
                    battle_ON, battle_e1_s2, scene = False, False, 'scene_2'
                elif battle_name == 'battle_e1_s4':
                    battle_ON, battle_e1_s4, scene = False, False, 'scene_4'
                elif battle_name == 'battle_e1_s5':
                    battle_ON, battle_e1_s5, scene = False, False, 'scene_5'
                dialogue_index += 1
        
        pygame.display.flip()

#credits, when all episodes are beaten
def Credits():
    '''
    the credits!!!
    '''
    global scene, Finished
    while Finished:
        #black background
        screen.fill(black)
        #the end (big)
        make_text('THE END','arialblack',115,white,SCREEN_WIDTH/2,SCREEN_WIDTH/2)
        #names of the creators and collaborators {TO UPDATE}
        
        #to quit the credits and go back to menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Finished = False
                    scene = 'start_menu'
            
        pygame.display.flip()


#main while loop of the game, that takes all the variables and functions
#to make the whole game run
while running:
    #get mouse position, continuously, while playing
    mouse = pygame.mouse.get_pos()
    #if the player quits, or to move along with the dialogue and story,
    #and do story-battle transitions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #exits out of the while running loop and into the exit statements at the end of the code
        if event.type == pygame.KEYDOWN:
            if battle_ON == False:
                if event.key == pygame.K_RETURN: #press return to keep going with the dialogue, also handles story-battle transitions and setting transitions
                    if scene == "scene_1" and dialogue_index < len(scene_1_dialogue):
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 38:
                            pygame.mixer.music.stop()
                            playMusic(ExceedraLonelyTheme1,'music',Forever=True)
                        elif dialogue_index >= len(scene_1_dialogue):
                            pygame.mixer.music.stop()
                            scene = "scene_2"
                            dialogue_index = -1
                            playMusic(Hydranoid_DestinyTheme,'music',Forever=True)
                            
                    elif scene == "scene_2" and dialogue_index != 22:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 22:
                            pygame.mixer.music.stop()
                            battle_ON, battle_e1_s2, scene = True, True, 'battle_e1_s2'  # Trigger battle and get out of dialogue
                            playMusic(BattleTheme1,'music',Forever=True)
                        elif dialogue_index == 33:
                            pygame.mixer.music.stop()
                            playMusic(ExceedraLonelyTheme2,'music',Forever=True)
                        elif dialogue_index >= len(scene_2_dialogue):
                            pygame.mixer.music.stop()
                            ExceedraMain = ExceedraMain.reset()
                            Hydranoid = Hydranoid.reset()
                            scene = "scene_3"
                            dialogue_index = -1
                            playMusic(LibraryTheme,'music',Forever=True)
                            
                    elif scene == "scene_3" and dialogue_index < len(scene_3_dialogue):
                        dialogue_index += 1 
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 16:
                            pygame.mixer.music.stop()
                            playMusic(ExceedraAngryTheme,'music')
                        elif dialogue_index == 25:
                            pygame.mixer.music.stop()
                            playMusic(ExceedraAngryTheme,'music')
                        elif dialogue_index >= len(scene_3_dialogue):
                            pygame.mixer.music.stop()
                            scene = "scene_4"
                            dialogue_index = -1
                            
                    elif scene == "scene_4" and dialogue_index != 18:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 5:
                            pygame.mixer.music.stop()
                            playMusic(AkobosAppears,'music',Forever=True)
                        elif dialogue_index == 18:
                            pygame.mixer.music.stop()
                            battle_ON, battle_e1_s4, scene = True, True, 'battle_e1_s4'  # Trigger battle and get out of dialogue
                            playMusic(AkobosBattle,'music',Forever=True)
                        elif dialogue_index >= len(scene_4_dialogue):
                            pygame.mixer.music.stop()
                            ExceedraMain = ExceedraMain.reset()
                            Akobos = Akobos.reset()
                            scene = "scene_5"
                            dialogue_index = -1
                            
                    elif scene == "scene_5" and dialogue_index != 37:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 32:
                            pygame.mixer.music.stop()
                            playMusic(NightmareAppears,'music',Forever=True)
                        elif dialogue_index == 37:
                            pygame.mixer.music.stop()
                            playMusic(NightmareScream,'sound')
                            battle_ON, battle_e1_s5, scene = True, True, 'battle_e1_s5'  # Trigger battle and get out of dialogue
                            playMusic(NightmareBattle,'music',Forever=True)
                        elif dialogue_index == 41:
                            pygame.mixer.music.stop()
                            playMusic(NightmareDying,'music',Forever=True)
                        elif dialogue_index == 48:
                            pygame.mixer.music.stop()
                            playMusic(NightmareDeath,'sound')
                            ExceedraMain = ExceedraMain.reset()
                            Nightmare = Nightmare.reset()
                        elif dialogue_index >= len(scene_5_dialogue):
                            pygame.mixer.music.stop()
                            Episode1_completed = True
                            scene = "start_menu"
                            dialogue_index = -1
                    
                    elif scene == 'scene_6': #{TO UPDATE}
                        #dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                            
                if event.key == pygame.K_BACKSPACE:  # On Backspace key
                    if dialogue_index > 0:
                        playMusic(press_button_sound,'sound')
                        dialogue_index -= 1  # Go to previous line
                    else:
                        dialogue_index = 0  # Keep at the first line
            #pause or exit during story scenes (these 2 don't work during battles (though they should), which is why we have the whole pygame.event.get() also in the battle function)           
            if event.key == pygame.K_p:
                pause = True
                pause_the_game()
            if event.key == pygame.K_0:
                pygame.quit() #press 0 to quit
                sys.exit()
    
    #the menu screen
    if scene == 'start_menu':
        Menu()
        
    #episode 1, scene 1
    elif scene == 'scene_1':
        screen.blit(dreamspace, (0, 0))
        ExceedraMain.BattlePosition(100, 200)
        Overlord.BattlePosition(700,150)
        dialogueBox(scene_1_dialogue)
        
    #episode 1, scene 2
    elif scene == 'scene_2':
        screen.blit(school, (0, 0))
        ExceedraMain.BattlePosition(100, 200)
        Destiny.BattlePosition(300,200)
        Hydranoid.BattlePosition(400,100)
        dialogueBox(scene_2_dialogue)
    
    #battle in episode 1, scene 2: Exceedra VS Hydranoid
    elif scene == 'battle_e1_s2':
        Battle(ExceedraMain,Hydranoid,school,'battle_e1_s2',BattleTheme1)
            
    #episode 1, scene 3
    elif scene == "scene_3":
        screen.blit(library, (0, 0))
        ExceedraMain.BattlePosition(100, 200)
        Finlay.BattlePosition(200,200)
        Grace.BattlePosition(300,200)
        Ken.BattlePosition(400,200)
        dialogueBox(scene_3_dialogue)
        if dialogue_index >= 22:
            screen.blit(school, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            Hydranoid.BattlePosition(20,100)
            dialogueBox(scene_3_dialogue)
    
    #episode 1, scene 4
    elif scene == "scene_4":
        screen.blit(hill, (0, 0))
        ExceedraMain.BattlePosition(100, 200)
        dialogueBox(scene_4_dialogue)
        if 5 <= dialogue_index < 10:
            screen.blit(hill, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            Akobos.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            dialogueBox(scene_4_dialogue)

        if dialogue_index >= 10 and dialogue_index != 18:
            screen.blit(hill, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            Hydranoid.BattlePosition(20,100)
            Akobos.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            dialogueBox(scene_4_dialogue)
    
    #battle in episode 1, scene 4: Exceedra VS Akobos
    elif scene == 'battle_e1_s4':
        Battle(ExceedraMain,Akobos,hill,'battle_e1_s4',AkobosBattle)
    
    #episode 1, scene 5
    elif scene == "scene_5":
        screen.blit(house, (0, 0))
        ExceedraMain.BattlePosition(100, 200)
        Junia.BattlePosition(500,50)
        dialogueBox(scene_5_dialogue)
        if 24 <= dialogue_index < 31 or dialogue_index >= 48:
            screen.blit(house, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            dialogueBox(scene_5_dialogue)
        elif 31 <= dialogue_index < 36:
            screen.blit(dreamspace, (0, 0))
            ExceedraMain.BattlePosition(0, SCREEN_HEIGHT-500)
            dialogueBox(scene_5_dialogue)
        elif 36 <= dialogue_index < 48 and dialogue_index != 37:
            screen.blit(dreamspace, (0, 0))
            ExceedraMain.BattlePosition(0, SCREEN_HEIGHT-500)
            Nightmare.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            dialogueBox(scene_5_dialogue)
    
    #battle in episode 1, scene 5: Exceedra VS Nightmare
    if scene == 'battle_e1_s5':
        Battle(ExceedraMain,Nightmare,dreamspace,'battle_e1_s5',NightmareBattle)
            
    #episode 2, scene 1 (aka scene 6)
    if scene == 'scene_6':
        screen.fill(BLUE)
        make_text('EPISODE 2 WILL BE READY SOON! :)',"comicsansms",65,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    
    if scene == 'battle_e2_s1': #{TO UPDATE}
        pass
    
    #credits when the game is completed (after Game_completed is made True)
    if scene == 'credits':
        Finished = True
        Credits()
            
    #updates the display whenever needed
    #(WE LOVE U DISPLAY.FLIP(), THANK YOU FOR MAKING TRANSITIONS POSSIBLE!!!, AND FOR SOMEHOW WORKING EVERY TIME U NEED TO
    #EVEN THOUGH YOU'RE ONLY CALLED THIS ONE TIME AT THE END OF THE CODE!)
    pygame.display.flip()
    
#exit the game, happens only when the main loop (while running) is exited
#through the pygame.QUIT event; almost all of the time, game exit is done by pressing 0
pygame.quit()
sys.exit()
