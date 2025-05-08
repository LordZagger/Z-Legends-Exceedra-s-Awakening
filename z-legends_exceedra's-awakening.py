#Comments in first person by LordZagger
#import needed modules and functions
import pygame                 #duh
import sys                    #to get sys.exit for exiting the game without errors
import inspect                #for the retrieve_name function so we can use it in the find function
from random import choice     #for the npc opponent to choose a random move, see randomMove method in Character class
from random import randrange  #for a random number, see Attack function

#Initialize pygame
pygame.init()

#Screen setup (size, icon, caption)
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
            #{TO UPDATE};#battle_e#,_s# is in the story; in boss rush, b1-3 episode 1, 4-7 episode 2, 8-11 episode 3. 12-15 final episode; in custom, the battle scene is 0
list_of_battle_scenes = ['battle_e1_s2','battle_e1_s4','battle_e1_s5','battle_e2_s1','battle_e2_s2','battle_e2_s4','battle_e2_s6','battle_e3_s4','battle_e3_s6','battle_e3_s7_1','battle_e3_s7_2','battle_e3_s7_3','battle_e4_s3','battle_e4_s4','battle_e4_s6_1','battle_e4_s6_2','battle_e4_s6_3','battle_e4_s6_4','battle_e4_s7_1',
                         'battle_e4_s7_2','b1','b2','b3','b4','b5','b6','b7','b8','b9','b10.1','b10.2','b10.3','b11','b12','b13.1','b13.2','b13.3','b13.4','b14.1','b14.2','0a','0b','0c']
#create a dictionary associating battles to their scene to avoid billions of elifs in the Battle function
battle_scenes_to_story_scenes = {'battle_e1_s2': 'scene_2', 'battle_e1_s4': 'scene_4', 'battle_e1_s5': 'scene_5','battle_e2_s1': 'scene_6','battle_e2_s2': 'scene_7',
                                 'battle_e2_s4': 'scene_9', 'battle_e2_s6': 'scene_11', 'battle_e3_s4': 'scene_15', 'battle_e3_s6': 'scene_17',
                                 'battle_e3_s7_3': 'scene_18', 'battle_e4_s3': 'scene_21','battle_e4_s4': 'scene_22', 'battle_e4_s6_4': 'scene_24','battle_e4_s7_2': 'scene_25'}
dialogue_index = 0
picking = False #custom battle picking screens (battle type, characters, background, music respectively)
choosing = False
deciding = False
selecting = False
designing = False
b1v1 = False #see which type of battle for the custom battle
b2v1 = False
b3v1 = False
Locked1 = False #for locked buttons and moves for character 1 (in battles)
Locked2 = False
Locked3 = False
Locked4 = False
battle_ON = False #if a battle is in progress
Episode1_completed = False #to see which episodes are completed
Episode2_completed = False
Episode3_completed = False
Game_completed = False
#for restarting battles, we save the battle function call parameters in variables and call them as global in functions
#for now, they're empty strings
CH1 = '' 
CH2 = ''
CH3 = ''
CH4 = ''
BACKGROUND = ''
BACKGROUND2  = ''
ZE_BATTLE = ''
MUSIC = ''
score = 0 #for boss rush score (how many bosses you managed to beat); will be displayed on screen
max_score = False #see if the player got the max score on Battle Rush

#Music and sounds
#introduced in episode 1 {TO UPDATE}
press_button_sound = 'pokemon-a-button.wav'
Dreamspace_theme = 'Dreamspace_Dark.wav'
ExceedraLonelyTheme1 = 'Exceedras_Defiance.wav'
BattleTheme1 = 'Battle_Theme_1.wav'
BattleWon = 'Battle_Won_Sound.wav'
BattleLost = 'Battle_Lost_Sound.wav'
ExceedraLonelyTheme2 = 'Exceedra_Sad.wav'
LibraryTheme = 'Library_Theme.wav'
ExceedraAngryTheme = 'Exceedra_Angry.wav'
DowntownTheme = 'Downtown_Theme.wav'
AkobosAppears = 'Akoboss_Theme.wav'
AkobosBattle = 'Akobos_Battle.wav'
NightmareAppears = 'Nightmare_Theme.wav'
NightmareScream = 'NightmareScream.wav'
NightmareBattle = 'Nightmare_Battle.wav'
NightmareDying = 'Nightmare_HeartbeatDying.wav'
NightmareDeath = 'NightmareDeath.wav'
NightmareScream = 'NightmareScream.wav'

#introduced in episode 2 {TO UPDATE}
aProblem = 'A_theme_for_episode_2.wav'
HunterTheme = ''
LagoonTheme = ''
Mourning = 'Mourning.wav'
OverlordTheme = ''
OverlordBattle = ''
DarkExceedraTheme = ''
LaboratoryTheme = ''
DarkExceedraBattle = ''

#introduced in episode 3 {TO UPDATE}
ZaggerPalaceTheme = ''
BrainstormingTheme = ''
Exceedras_world_of_iceTheme = ''
Exceedra_and_Kyra = ''
Exceedra_VS_Destiny = ''
OverlordSoulBattle = ''
OroborusTerminaBattle = ''

#introduced in final episode {TO UPDATE}
AITheme = ''
DreamWorldUnderAttack = ''
MonsterBattle = ''
AIBattle1 = ''
AIBattle2 = ''
GoodbyeTheme = ''
aPromise = ''
CreditsTheme = ''

#background images {TO UPDATE}
dreamspace = pygame.image.load("dreamspace.png")  # Episode 1 Scene 1 background, recurring location where Exceedra's soul travels when he dreams
dreamspace = pygame.transform.scale(dreamspace, (SCREEN_WIDTH, SCREEN_HEIGHT))

school = pygame.image.load("school.png")  # Episode 1 Scene 2 background, recurring as a High Point Secondary School corridor
school = pygame.transform.scale(school, (SCREEN_WIDTH, SCREEN_HEIGHT))

library = pygame.image.load('Library.png') # Episode 1 Scene 3 background, the High Point Secondary School library
library = pygame.transform.scale(library, (SCREEN_WIDTH,SCREEN_HEIGHT))

hill = pygame.image.load('hill.png') # Episode 1 Scene 4 background, Parliament Hill in Ottawa
hill = pygame.transform.scale(hill,(SCREEN_WIDTH,SCREEN_HEIGHT))

house = pygame.image.load('House.png') # Episode 1 Scene 5 background, recurring as Exceedra's house
house = pygame.transform.scale(house,(SCREEN_WIDTH,SCREEN_HEIGHT))

grass_plain = pygame.image.load('title_background.png') # Dream world grass plain
grass_plain = pygame.transform.scale(grass_plain,(SCREEN_WIDTH,SCREEN_HEIGHT))

#School roof
roof = pygame.image.load('title_background.png')
roof = pygame.transform.scale(roof,(SCREEN_WIDTH,SCREEN_HEIGHT))

#School exterior
school_outside = pygame.image.load('title_background.png')
school_outside = pygame.transform.scale(school_outside,(SCREEN_WIDTH,SCREEN_HEIGHT))

#warehouse
warehouse = pygame.image.load('title_background.png')
warehouse = pygame.transform.scale(warehouse,(SCREEN_WIDTH,SCREEN_HEIGHT))

#prison
prison = pygame.image.load('title_background.png')
prison = pygame.transform.scale(prison,(SCREEN_WIDTH,SCREEN_HEIGHT))

#laboratory
laboratory = pygame.image.load('title_background.png')
laboratory = pygame.transform.scale(laboratory,(SCREEN_WIDTH,SCREEN_HEIGHT))

#The In-Between
in_between = pygame.image.load('title_background.png')
in_between = pygame.transform.scale(in_between,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Dream World Zagger palace
zagger_palace = pygame.image.load('title_background.png')
zagger_palace = pygame.transform.scale(zagger_palace,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Dream World Fire Plain
fire_plain = pygame.image.load('title_background.png')
fire_plain = pygame.transform.scale(fire_plain,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Dream World Ice Plain
exceedras_world_of_ice = pygame.image.load('title_background.png')
exceedras_world_of_ice = pygame.transform.scale(exceedras_world_of_ice,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Dream world grass plain with portal to real world
grass_plain2 = pygame.image.load('title_background.png')
grass_plain2 = pygame.transform.scale(grass_plain2,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Exceedra's 2nd house
house2 = pygame.image.load('title_background.png')
house2 = pygame.transform.scale(house2,(SCREEN_WIDTH,SCREEN_HEIGHT))

#Character images: first load them, then scale them {TO UPDATE}
Exceedra1_pic = pygame.image.load("exceedra1.png")  # Main character (Exceedra) sprite episode 1
Exceedra1_pic = pygame.transform.scale(Exceedra1_pic, (700, 700))

Exceedra4_pic = pygame.image.load("exceedra3.png")  # Exceedra sprite final episode (ExceedraMain2 sprite)
Exceedra4_pic = pygame.transform.scale(Exceedra4_pic, (700, 700))

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

Abby_pic = pygame.image.load('nightmare.png') #Abby sprite
Abby_pic = pygame.transform.scale(Abby_pic,(700,700))

OroborusTermina_pic = pygame.image.load('nightmare.png') #Oroborus Termina sprite
OroborusTermina_pic = pygame.transform.scale(OroborusTermina_pic,(700,700))

OverlordSoul_pic = pygame.image.load('nightmare.png') #Overlord Soul sprite
OverlordSoul_pic = pygame.transform.scale(OverlordSoul_pic,(700,700))

DarkExceedra_pic = pygame.image.load('nightmare.png') #Dark Exceedra (2) sprite
DarkExceedra_pic = pygame.transform.scale(DarkExceedra_pic,(700,700))

Kyra_pic = pygame.image.load('nightmare.png') #Kyra sprite
Kyra_pic = pygame.transform.scale(Kyra_pic,(700,700))

Hunter_pic = pygame.image.load('nightmare.png') #The Hunter sprite
Hunter_pic = pygame.transform.scale(Hunter_pic,(700,700))

Sophie_pic = pygame.image.load('nightmare.png') #Sophie sprite
Sophie_pic = pygame.transform.scale(Sophie_pic,(700,700))

Denis_pic = pygame.image.load('nightmare.png') #Denis sprite
Denis_pic = pygame.transform.scale(Denis_pic,(700,700))

AI_pic = pygame.image.load('nightmare.png') #AI sprite
AI_pic = pygame.transform.scale(AI_pic,(700,700))

AI_2_pic = pygame.image.load('nightmare.png') #AI (Phase 2) sprite
AI_2_pic = pygame.transform.scale(AI_2_pic,(700,700))

Monster1_pic = pygame.image.load('nightmare.png') #Monster1 sprite
Monster1_pic = pygame.transform.scale(Monster1_pic,(700,700))

Monster2_pic = pygame.image.load('nightmare.png') #Monster2 sprite
Monster2_pic = pygame.transform.scale(Monster2_pic,(700,700))

#dialogues for Episode 1 (scenes 1-5)
#episode 1, scene 1: intro to Exceedra and the Overlord, their connection, and the Overlord's philosophy
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
    "Overlord: I’m certain that if you start killing people, you should get closer to what you want.",
    "Exceedra: [firmly] Killing is not the path forward.",
    "Overlord: [grandiose] THEN WHAT IS, OH GREAT HERO? [Grips Exceedra.]",
    "Overlord: The path forward is the one you make yourself. There is no other path.",
    "Overlord: Only you can make the path that will get you to what you want.",
    "Overlord: Do you seriously believe you can stay the way you are and one day you will get what you want? Naive little boy!",
    "[Overlord ungrips and continues.]",
    "Overlord: You can’t trust humans. They will always disappoint you. They’ll always have what you want.",
    "Overlord: They can’t understand you, Exceedra. They’re just humans.",
    "Overlord: They aren’t gods. They can’t give you what you want.",
    "Exceedra: [angrily] So?",
    "Overlord: [foreboding] Just kill them. You don’t need things that don’t help you.",
    "Overlord: Listen, kiddoboy, if you don’t believe me, then just pick a number. Any number. It's that thing you like doing, right?",
    "Overlord: [foreboding] No matter the number you pick… the humans will betray you.",
    "Overlord: The path forward is the path you will have to make yourself. So choose. Pain for the rest of your life...",
    "Overlord: Or let go of your childish hope, take the reins of your existence on Earth and kill the humans so you can finally establish your empire.",
    "[Overlord looks as if to the future, disappointed and worried.]",
    "Overlord: My dear baby dragon... It’s only a matter of time now before there is nothing left to fight for.",
    "Exceedra: [worried] What do you mean?",
    "Overlord: [ignoring, looking directly at Exceedra] Just kill the humans and take what you want. You won’t regret it.",
    "[Exceedra prepares to leave.]",
    "Overlord: [yelling after his son] You can take 1 million more steps on the path you’re walking on and still not get to where you want to go!",
    "[Exceedra stops.]",
    "Overlord: You can blame God as much as you want, but you’re the one advancing on this path.",
    "Overlord: You’re the one who needs to change! You need to listen!",
    "Exceedra: [interrupting, screaming] NO! THE PATH FORWARD IS THE ONE I WILL MAKE MYSELF, BUT IT’S NOT MY FAULT GOD ISN’T GIVING ME WHAT IS RIGHTFULLY MINE!",
    "Exceedra: I WILL BECOME AN UNRIVALED LEGEND AND TAKE WHAT IS RIGHTFULLY MINE. I just… [struggling to continue.]",
    "[Exceedra walks away. Before leaving, looks back.]",
    "Exceedra: I’ll figure it out. I have to. For the sake of the plot."
]

#Episode 1, Scene 2: Intro to Hydranoid and Destiny, Hydranoid's and Exceedra bond, and hint to Exceedra's depression
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
    "[Hydranoid is defeated. Starts to stand up, scratching his head, smiling.]",
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
#Episode 1, Scene 3: Intro to some of Exceedra's friends, and things in school not going the way he wants
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
#Episode 1, Scene 4: Exceedra and Hydranoid taking down a vilain... who better than Akobos?
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
#Episode 1, Scene 5: Exceedra's home life... and nightmares (literally)
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
    "Exceedra: [thinking] You know, sleep is the only way for me to escape this miserable existence on Earth.", 
    "Exceedra: Tch. I just don’t have the power to change things, not the way I am now. I need to become a god if I’m gonna get what I want.", 
    "Exceedra: [sighs] I just wanna go home… [while sulking, falls asleep]", 
    "[He reenters the Dreamspace where he was first talking to the Overlord. This time, no one is around.]", 
    "Nightmare: [far off, cackles sinisterly in a deep, distorted voice] Look what the baby dragon brought in: more food!", 
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

#classes for characters and moves
class Character:
    '''
    This class is for creating the characters in the story
    contains attributes related to them for the battle system, such as health, recovery and energy and attack potential stats
    Also has attributes for the name and moves of a character.
    Health is the amount of HP (aka life/hit points) a character has. it's how they stay alive, until health is reduce to 0, at which point they die
    Energy is the amount of energy a character has to use a move. it's a special stat that helps prevent spamming of a single attack, and so requires players to have somewhat of a strategy
    Attack potential is a special stat that helps determine which attack lands in a pinch (see Attack function)
    battle_pic is the character's png image (image name) for battles
    og stands for original, those attributes help reset the characters stats in the reset method
    '''
    def __init__(self, name, health, energy, attack_potential, AttackMove, GuardMove, RecoverMove, battle_pic):
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
        #original stats, to reset the character in below method and as references during battles
        self.og_health = health
        self.og_energy = energy
        #put the 3 moves in a list for use in the randomMove method below
        self.movepool = [AttackMove, GuardMove, RecoverMove]
        
    def reset(self):
        '''reset a character's stats by making their current health and energy stats equal to the original stats'''
        self.health = self.og_health
        self.energy = self.og_energy
    
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
        self.health += 2 * amount
        self.energy += amount
    
    def randomMove(self):
        '''
        during a battle, the npc chooses a random move from their movepool every turn
        '''
        return choice(self.movepool)
    
    def clone(self):
        '''
        creates a copy of the character so that in custom battles, you don't end up with a "mirror fight issue"
        '''
        return Character(self.name,self.og_health,self.og_energy,self.attack_potential,self.AttackMove,self.GuardMove,self.RecoverMove,self.battle_pic)
    
    def BattlePosition(self,x,y):
        '''
        placing a character, their energy bar and their health bar (if during a battle) on top of the background
        mainly used for positioning during battles, but this method's existence is also convenient for dialogue scenes
        '''
        #place the character
        if battle_ON == False:
            if self.battle_pic != None:
                if self.battle_pic == Junia_pic and scene in ['choose2','0a','0b','0c']:
                    screen.blit(self.battle_pic, (x-200,50))
                elif self.battle_pic == Ken_pic and scene in ['choose2','0a','0b','0c']:
                    screen.blit(self.battle_pic, (x-140,y))
                elif self.battle_pic == Grace_pic and scene in ['choose2','0a','0b','0c']:
                    screen.blit(self.battle_pic, (x-200,y-100))
                else:
                    screen.blit(self.battle_pic, (x,y))

        else:
            #if the character hasn't yet been defeated
            if self.health > 0:
                #place character
                if self.battle_pic != None:
                    if self.battle_pic == Junia_pic and scene in ['choose2','0a','0b','0c']:
                        screen.blit(self.battle_pic, (x-200,50))
                    elif self.battle_pic == Ken_pic and scene in ['choose2','0a','0b','0c']:
                        screen.blit(self.battle_pic, (x-200,y))
                    elif self.battle_pic == Grace_pic and scene in ['choose2','0a','0b','0c']:
                        screen.blit(self.battle_pic, (x-200,y-100))
                    else:
                        screen.blit(self.battle_pic, (x,y))
                #health bar
                if self == Nightmare or self == NightmareC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+40, 500, 10))
                    pygame.draw.rect(screen, health_bar_green, (x+80, y+40, self.health/self.og_health*500, 10))
                elif self == Hydranoid or self == HydranoidC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+230, 500, 10))
                    pygame.draw.rect(screen, health_bar_green, (x+80, y+230, self.health/self.og_health*500, 10))
                elif self == Overlord or self == OverlordC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+110, 500, 10))
                    pygame.draw.rect(screen, health_bar_green, (x+80, y+110, self.health/self.og_health*500, 10))
                else:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+80, 500, 10))
                    pygame.draw.rect(screen, health_bar_green, (x+80, y+80, self.health/self.og_health*500, 10))
                
                #also draw energy bar if playable character
                if self == CH1 and CH1 == HydranoidC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+160, 500, 10))
                    pygame.draw.rect(screen, BLUE, (x+80, y+160, self.energy/self.og_energy*500, 10))
                elif self == CH1 and CH1 == OverlordC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+50, 500, 10))
                    pygame.draw.rect(screen, BLUE, (x+80, y+50, self.energy/self.og_energy*500, 10))
                elif self == CH1 and CH1 != HydranoidC and CH1 != OverlordC:
                    pygame.draw.rect(screen, health_bar_red, (x+80, y+20, 500, 10))
                    pygame.draw.rect(screen, BLUE, (x+80, y+20, self.energy/self.og_energy*500, 10))
                
class Move:
    '''
    This class will serve to define all the moves similarly to how characters will be created.
    __init__ has attributes for the name, type, energy consumption and/or damage caused and recovery made of the move
    Damage is the amount of damage (health lost by opponent) made by the move (for Attack Moves)
    Specialty is the type of the move (attack, guard or recover) (I'm tired of using Type all the time), is mainly used to keep track of and print the type of the move
    recovery is how much energy and health are recovered (for Recover moves)
    energy consumption is the amount of energy needed to use a move (aka lost when move is used)
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
AkobosAttack = Move('Trident of Demise',25,'ATTACK',0,10)
AkobosRecover = Move('Demon Blood',0,'RECOVER',15,0)
NightmareAttack = Move('Mental Plague',30,'ATTACK',0,20)
NightmareGuard = Move('Dream Trapped',0,'GUARD',0,10)
NightmareRecover = Move('Dream Eater',0,'RECOVER',20,0)
NullMove = Move('Play Dead',0,None,0,0) #nothing, just for characters who aren't in battles
DestinyAttack = Move('Time Pulse',30,'ATTACK',0,15) #destiny is available for battle in episode 2
DestinyGuard = Move('Time Stop',0,'GUARD',0,5)
DestinyRecover = Move('Centered',0,'RECOVER',10,0)
OverlordAttack = Move('Dark En',50,'ATTACK',0,30) #overlord 1rst battle is in episode 2
OverlordAttack2 = Move('Dark Missile',30,'ATTACK',0,10) #overlord 2nd and 3rd phases are in episode 3
OverlordGuard = Move('Black Shield',0,'GUARD',0,5)
OverlordGuard2 = Move('Spike Shield',0,'GUARD',0,5)
OverlordRecover = Move('Shadow Bath',0,'RECOVER',25,0)
ExceedraDarkAttack1 = Move('Dark Lightning',40,'ATTACK',0,15) #angry exceedra who uses his dark powers (episode 2)
ExceedraDarkAttack2 = Move("Dark Blast",50,'ATTACK',0,20) #exceedra manipulated by overlord
ExceedraDarkRecover = Move('Spirit of Vengeance',0,'RECOVER',20,0)
KyraAttack = Move('Surprise Attack',40,'ATTACK',0,15)
KyraGuard = Move('Teleport',0,'GUARD',0,5)
KyraRecover = Move('Psychopower',0,'RECOVER',25,0)
HunterAttack = Move('Lightsaber Barrage',30,'ATTACK',0,10)
HunterGuard = Move('Energy Shield',0,'GUARD',0,2)
HunterRecover = Move("Hunter's Way",0,'RECOVER',20,0)
ExceedraMainAttack2 = Move('Galaxy Barrage',50,'ATTACK',0,25)
ExceedraGuard2 = Move('Focus Block',0,'GUARD',0,7)
ExceedraRecover2 = Move("Warrior's Resolve",0,'RECOVER',20,0)
ClassicAttack = Move("Jab-Cross",10,'ATTACK',0,4)
AbbyRecover = Move('Power of Love',0,'RECOVER',50,0)
AiAttack = Move('Distorsion Break',50,'ATTACK',0,25)
AiAttack2 = Move('Cyber Barrage',55,'ATTACK',0,30)
AiGuard = Move('Firewall',0,'GUARD',0,5)
AiRecover = Move('Self Repair',0,'RECOVER',40,0)
Monster2Attack = Move('Blaze Blitz',40,'ATTACK',0,15)
Monster2Guard = Move('Flame Armor',0,'GUARD',0,5)
MonsterRecover = Move('Beast Mode',0,'RECOVER',30,0)
Monster1Attack = Move('Subzero Spear',45,'ATTACK',0,15)
Monster1Guard = Move('Ice Armor',0,'GUARD',0,5)

#characters (some NPC opponents are "overloaded" on energy to avoid their moves getting locked. Some "overloaded" NPCs are meant to be harder versions of their canon selves to make story battles more accurate.)
ExceedraMain = Character('Exceedra',100,50,20,ExceedraMainAttack,ExceedraGuard,ExceedraRecover,Exceedra1_pic)
Hydranoid = Character('Hydranoid',70,1000,15,HydranoidAttack,ClassicGuard,ClassicRecover,Hydranoid_pic)
Akobos = Character('Akobos',100,1000,19,AkobosAttack,ClassicGuard,AkobosRecover,Akobos_pic)
Nightmare = Character('Nightmare',150,1000,17,NightmareAttack,NightmareGuard,NightmareRecover,Nightmare_pic)
Destiny = Character('Destiny',80,40,15,DestinyAttack,DestinyGuard,DestinyRecover,Destiny_pic)
Grace = Character('Grace',0,0,0,NullMove,NullMove,NullMove,Grace_pic)
Finlay = Character('Finlay',0,0,0,NullMove,NullMove,NullMove,Finlay_pic)
Ken = Character('Ken',0,0,0,NullMove,NullMove,NullMove,Ken_pic)
Junia = Character('Junia',0,0,0,NullMove,NullMove,NullMove,Junia_pic)
Overlord = Character('Overlord',200,1500,30,OverlordAttack,OverlordGuard,OverlordRecover,Overlord_pic) #phase 1
OverlordSoul = Character('Overlord Soul',200,1500,30,OverlordAttack2,OverlordGuard2,OverlordRecover,OverlordSoul_pic) #phase 2
OroborusTermina = Character('Oroborus Termina',200,1500,35,ExceedraDarkAttack2,ExceedraGuard,OverlordRecover,OroborusTermina_pic) #phase 3
ExceedraDark1 = Character('Dark Exceedra',150,75,25,ExceedraDarkAttack1,ExceedraGuard,ExceedraDarkRecover,Exceedra1_pic) #just mad
ExceedraDark2 = Character('Dark Exceedra',175,80,29,ExceedraDarkAttack2,ExceedraGuard,ExceedraDarkRecover,DarkExceedra_pic) #controlled by the Overlord
Kyra = Character('Kyra',150,75,28,KyraAttack,KyraGuard,KyraRecover,Kyra_pic) #companion character in Episodes 3/4, None pic for now
NullPerson = Character('',1,1,1,NullMove,NullMove,NullMove,None) #nobody... blank area for character select in custom battle
Hunter = Character('The Hunter',100,1000,16,HunterAttack,HunterGuard,HunterRecover,Hunter_pic)
ExceedraMain2 = Character('Exceedra',175,80,35,ExceedraMainAttack2,ExceedraGuard2,ExceedraRecover2,Exceedra4_pic) #exceedra after realising the Overlord's manipulation
Abby = Character('Abby',60,40,13,ClassicAttack,ClassicGuard,AbbyRecover,Abby_pic)
Sophie = Character('Sophie',0,0,0,NullMove,NullMove,NullMove,Sophie_pic)
Denis = Character('Denis',0,0,0,NullMove,NullMove,NullMove,Denis_pic)
AI = Character('AI',200,2000,37,AiAttack,AiGuard,AiRecover,AI_pic)
AI_2 = Character('AI',200,2000,38,AiAttack2,AiGuard,AiRecover,AI_2_pic)
Monster1 = Character('Ice Monster',175,100,31,Monster1Attack,Monster1Guard,MonsterRecover,Monster1_pic)
Monster2 = Character('Fire Monster',175,100,31,Monster2Attack,Monster2Guard,MonsterRecover,Monster2_pic)
#canon characters for custom battle (C stands for canon, like I talked about above); in some cases, serve as beatable versions of a character
OverlordC = Character('Overlord C',200,100,30,OverlordAttack,OverlordGuard,OverlordRecover,Overlord_pic)
OverlordSoulC = Character('Overlord Soul C',200,100,30,OverlordAttack2,OverlordGuard2,OverlordRecover,OverlordSoul_pic)
OroborusTerminaC = Character('Oroborus Termina C',200,150,35,ExceedraDarkAttack2,ExceedraGuard,OverlordRecover,OroborusTermina_pic)
HydranoidC = Character('Hydranoid C',70,50,14,HydranoidAttack,ClassicGuard,ClassicRecover,Hydranoid_pic)
AkobosC = Character('Akobos C',100,50,19,AkobosAttack,ClassicGuard,AkobosRecover,Akobos_pic)
NightmareC = Character('Nightmare C',150,75,17,NightmareAttack,NightmareGuard,NightmareRecover,Nightmare_pic)
HunterC = Character('The Hunter C',100,100,16,HunterAttack,HunterGuard,HunterRecover,Hunter_pic)

#list of scenes, music and backgrounds for boss rush mode
musicRush_list = [BattleTheme1,AkobosBattle,NightmareBattle,NightmareBattle,AkobosBattle,OverlordBattle,DarkExceedraBattle,BattleTheme1,Exceedra_VS_Destiny,OverlordBattle,OverlordSoulBattle,OroborusTerminaBattle,MonsterBattle,MonsterBattle,AkobosBattle,NightmareBattle,NightmareBattle,OroborusTerminaBattle,AIBattle1,AIBattle2]
background_list = [school,hill,dreamspace,school_outside,warehouse,dreamspace,laboratory,exceedras_world_of_ice,in_between,dreamspace,dreamspace,dreamspace,exceedras_world_of_ice,fire_plain,grass_plain,grass_plain,grass_plain,grass_plain,grass_plain2,'///',library,house,roof,house2,prison] #/// is a separator between battle backgrounds and other backgrounds, won't affect Boss Rush
i = 0 #index for battle scenes list for battle rush mode
k = 0 #index for music list for battle rush mode

#list of all moves
moveList = [ExceedraMainAttack,ExceedraGuard,ExceedraRecover,HydranoidAttack,ClassicGuard,ClassicRecover,AkobosAttack,AkobosRecover,NightmareAttack,NightmareGuard,NightmareRecover,DestinyAttack,DestinyGuard,DestinyRecover,OverlordAttack,OverlordAttack2,OverlordGuard,OverlordGuard2,OverlordRecover,ExceedraDarkAttack1,ExceedraDarkAttack2,ExceedraDarkRecover,
            KyraAttack,KyraGuard,KyraRecover,HunterAttack,HunterGuard,HunterRecover,ExceedraMainAttack2,ExceedraGuard2,ExceedraRecover2,ClassicAttack,AbbyRecover,AiAttack,AiAttack2,AiGuard,AiRecover,Monster2Attack,Monster2Guard,MonsterRecover,Monster1Attack,Monster1Guard]
#list of all pictures
picList = [Exceedra1_pic,Exceedra4_pic,Hydranoid_pic,Overlord_pic,Destiny_pic,Akobos_pic,Grace_pic,Ken_pic,Finlay_pic,Junia_pic,Nightmare_pic,Abby_pic,OroborusTermina_pic,OverlordSoul_pic,DarkExceedra_pic,Kyra_pic,Hunter_pic,Sophie_pic,Denis_pic,AI_pic,AI_2_pic,Monster1_pic,Monster2_pic]
#list of all characters
#CH_List = [ExceedraMain,ExceedraMain2,Hydranoid,HydranoidC,Overlord,OverlordC,Destiny,Akobos,AkobosC,Nightmare,NightmareC,Abby,OroborusTermina,OroborusTerminaC,OverlordSoul,OverlordSoulC,ExceedraDark1,ExceedraDark2,Kyra,Hunter,HunterC,AI,AI_2,Monster1,Monster2]
CH_List = [ExceedraMain,Destiny,Hydranoid,HydranoidC,Overlord,OverlordC,Akobos,AkobosC,Nightmare,NightmareC]

#Starting here, all main functions used by the game (in the main while True loop)
#mass resetting of characters
def resetAll():
    '''reset all battle characters, before boss rush or custom battle'''   
    ExceedraMain.reset()
    ExceedraMain2.reset()
    Hydranoid.reset()
    Destiny.reset()
    Akobos.reset()
    Nightmare.reset()
    Overlord.reset()
    OverlordSoul.reset()
    OroborusTermina.reset()
    ExceedraDark1.reset()
    ExceedraDark2.reset()
    Hunter.reset()
    Abby.reset()
    Kyra.reset()
    AI.reset()
    AI_2.reset()
    Monster1.reset()
    Monster2.reset()
    OverlordC.reset()
    OverlordSoulC.reset()
    OroborusTerminaC.reset()
    AkobosC.reset()
    NightmareC.reset()
    HydranoidC.reset()
    HunterC.reset()
    
def retrieve_name(var):
    '''   
    var's variable name is returned as a string, which helps for the find function below
    kudos to juan Isaza and wjandrea for the function, from https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
    '''
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def find(category,what):
    '''return the move or picture variable of what
    ex: if find('move','Tail Block'), it will return the variable of the move whose name is 'Tail Block' (aka ExceedraGuard)
    if find('picture','Exceedra1_pic'), it will return the variable Exceedra1_pic rather than its string (using retrieve_name above)
    '''
    global moveList, picList #the reason we created those lists earlier are so that we could easily have access to all moves and pics here
    
    if category.lower() == 'move':
        for move in moveList:
            if what == move.name:
                return move

    if category.lower() == 'picture':
        for pic in picList:
            if what == retrieve_name(pic):
                return pic

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

#pause and unpause the game (you can only unpause after pausing)      
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
                if event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()

#wait a moment... functions
def wait(sound=None):
    '''
    wait untils a sound is done playing before you can continue with dialogue
    used for BattleWon, NightmareScream and NightmareDeath sounds
    '''
    global dialogue_index
    
    if sound != None:
        playMusic(sound,'sound')
    while pygame.mixer.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    dialogue_index -= 1
                if event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()

#These next 3 functions make the dialogue run smoothly (shows the text in a box)...
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
    draw_text_box()
    if dialogue_index < len(scene_list):
        draw_text(screen, scene_list[dialogue_index], DIALOGUE_FONT, 20, SCREEN_HEIGHT - 110)
    draw_hint_text()

#in-game BUTTONS! (not the ones you button your shirt with)
def make_button(text,font,text_size,text_color,x,y,button_width,button_height,button_color,highlight_color,Type,action):
    '''as per the name, function to make buttons. shows text made with make_text at text_color and size text_size, 
    button_color is the button's color and whenever the cursor is on the button, 
    its colors turns to highlight_color; if the button is associated to a task, 
    its name is placed at action; None is for the opponent's move in battle, 'Nope' is to tell you to use recover when you're out of energy 
    Type is for me, to see if it's a menu or battle button (though this function uses the scene to determine which action can be done when)
    '''
    global scene, dialogue_index, CH1, CH2, CH3, CH4, BACKGROUND, BACKGROUND2, ZE_BATTLE, MUSIC, battle_ON, picking, choosing, deciding, selecting, designing, b1v1, b2v1, b3v1, background_list #lots of global variables to consider
    
    #collision detection with the mouse (unfortunately we gotta redefine the mouse in here too)
    rect = pygame.Rect(x,y,button_width,button_height)
    mouse = pygame.mouse.get_pos()
    current_collision = rect.collidepoint(mouse)
    click = pygame.mouse.get_pressed()
    
    #if the mouse is clicked and on the button
    #all possible things with the buttons depending on the scene they are in
    if click[0] == 1 and current_collision:
        playMusic(press_button_sound,'sound')
        if scene == 'start_menu':
            scene = action
            dialogue_index = 0
            if action == 'scene_1' or scene == 'scene_19':
                playMusic(Dreamspace_theme,'music',True)
            elif action == 'scene_6' or action == 'scene_12':
                playMusic(aProblem,'music',True)
            elif action == 'choose':
                scene = 'choose'
        elif scene in ['choose','choose2','choose3','choose4']:
            if action == 'customCharacter':
                designing = True
                customCharacter()
            if action == 'randomCharacter':
                randomCharacter()
            if action == 'select Exceedra':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson: #if first character not yet picked
                    CH1 = ExceedraMain #make exceedra the first battler
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson: #if second character not yet picked
                    if CH1 == ExceedraMain:
                        CH2 = ExceedraMain.clone() #make the second
                    else:
                        CH2 = ExceedraMain
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson: #if third character not yet picked
                    if CH1 == ExceedraMain or CH2 == ExceedraMain:
                        CH3 = ExceedraMain.clone() #make the third
                    else:
                        CH3 = ExceedraMain
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson: #if fourth character not yet picked
                    if CH1 == ExceedraMain or CH2 == ExceedraMain or CH3 == ExceedraMain:
                        CH4 = ExceedraMain.clone() #make the fourth
                    else:
                        CH4 = ExceedraMain
                    pygame.time.delay(500)
            elif action == 'select Exceedra2':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = ExceedraMain2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraMain2:    
                        CH2 = ExceedraMain2.clone()
                    else:
                        CH2 = ExceedraMain2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraMain2 or CH2 == ExceedraMain2:
                        CH3 = ExceedraMain2.clone()
                    else:
                        CH3 = ExceedraMain2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraMain2 or CH2 == ExceedraMain2 or CH3 == ExceedraMain2:
                        CH4 = ExceedraMain2.clone()
                    else:
                        CH4 = ExceedraMain2
                    pygame.time.delay(500)
            elif action == 'select Hydranoid':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Hydranoid
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Hydranoid:    
                        CH2 = Hydranoid.clone()
                    else:
                        CH2 = Hydranoid
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Hydranoid or CH2 == Hydranoid:
                        CH3 = Hydranoid.clone()
                    else:
                        CH3 = Hydranoid
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Hydranoid or CH2 == Hydranoid or CH3 == Hydranoid:
                        CH4 = Hydranoid.clone()
                    else:
                        CH4 = Hydranoid
                    pygame.time.delay(500)
            elif action == 'select Destiny':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Destiny
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Destiny:    
                        CH2 = Destiny.clone()
                    else:
                        CH2 = Destiny
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Destiny or CH2 == Destiny:
                        CH3 = Destiny.clone()
                    else:
                        CH3 = Destiny
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Destiny or CH2 == Destiny or CH3 == Destiny:
                        CH4 = Destiny.clone()
                    else:
                        CH4 = Destiny
                    pygame.time.delay(500)
            elif action == 'select Akobos':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Akobos
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Akobos:    
                        CH2 = Akobos.clone()
                    else:
                        CH2 = Akobos
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Akobos or CH2 == Akobos:
                        CH3 = Akobos.clone()
                    else:
                        CH3 = Akobos
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Akobos or CH2 == Akobos or CH3 == Akobos:
                        CH4 = Akobos.clone()
                    else:
                        CH4 = Akobos
                    pygame.time.delay(500)
            elif action == 'select Nightmare':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Nightmare
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Nightmare:    
                        CH2 = Nightmare.clone()
                    else:
                        CH2 = Nightmare
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Nightmare or CH2 == Nightmare:
                        CH3 = Nightmare.clone()
                    else:
                        CH3 = Nightmare
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Nightmare or CH2 == Nightmare or CH3 == Nightmare:
                        CH4 = Nightmare.clone()
                    else:
                        CH4 = Nightmare
                    pygame.time.delay(500)
            elif action == 'select Overlord':
               if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   CH1 = Overlord
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == Overlord:    
                       CH2 = Overlord.clone()
                   else:
                       CH2 = Overlord
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == Overlord or CH2 == Overlord:
                       CH3 = Overlord.clone()
                   else:
                       CH3 = Overlord
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                   if CH1 == Overlord or CH2 == Overlord or CH3 == Overlord:
                       CH4 = Overlord.clone()
                   else:
                       CH4 = Overlord
                   pygame.time.delay(500)
            elif action == 'select ExceedraDark':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = ExceedraDark2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraDark2:    
                        CH2 = ExceedraDark2.clone()
                    else:
                        CH2 = ExceedraDark2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraDark2 or CH2 == ExceedraDark2:
                        CH3 = ExceedraDark2.clone()
                    else:
                        CH3 = ExceedraDark2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == ExceedraDark2 or CH2 == ExceedraDark2 or CH3 == ExceedraDark2:
                        CH4 = ExceedraDark2.clone()
                    else:
                        CH4 = ExceedraDark2
                    pygame.time.delay(500)
            elif action == 'select HydranoidC':
               if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   CH1 = HydranoidC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == HydranoidC:    
                       CH2 = HydranoidC.clone()
                   else:
                       CH2 = HydranoidC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == HydranoidC or CH2 == HydranoidC:
                       CH3 = HydranoidC.clone()
                   else:
                       CH3 = HydranoidC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                   if CH1 == HydranoidC or CH2 == HydranoidC or CH3 == HydranoidC:
                       CH4 = HydranoidC.clone()
                   else:
                       CH4 = HydranoidC
                   pygame.time.delay(500)
            elif action == 'select AkobosC':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = AkobosC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AkobosC:  
                        CH2 = AkobosC.clone()
                    else:
                        CH2 = AkobosC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AkobosC or CH2 == AkobosC:
                        CH3 = AkobosC.clone()
                    else:
                        CH3 = AkobosC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == AkobosC or CH2 == AkobosC or CH3 == AkobosC:
                        CH4 = AkobosC.clone()
                    else:
                        CH4 = AkobosC
                    pygame.time.delay(500)
            elif action == 'select NightmareC':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = NightmareC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == NightmareC:  
                        CH2 = NightmareC.clone()
                    else:
                        CH2 = NightmareC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == NightmareC or CH2 == NightmareC:
                        CH3 = NightmareC.clone()
                    else:
                        CH3 = NightmareC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == NightmareC or CH2 == NightmareC or CH3 == NightmareC:
                        CH4 = NightmareC.clone()
                    else:
                        CH4 = NightmareC
                    pygame.time.delay(500)
            elif action == 'select OverlordC':
               if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   CH1 = OverlordC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordC:    
                       CH2 = OverlordC.clone()
                   else:
                       CH2 = OverlordC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordC or CH2 == OverlordC:
                       CH3 = OverlordC.clone()
                   else:
                       CH3 = OverlordC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordC or CH2 == OverlordC or CH3 == OverlordC:
                       CH4 = OverlordC.clone()
                   else:
                       CH4 = OverlordC
                   pygame.time.delay(500)
            elif action == 'select Abby':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Abby
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Abby:    
                        CH2 = Abby.clone()
                    else:
                        CH2 = Abby
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Abby or CH2 == Abby:
                        CH3 = Abby.clone()
                    else:
                        CH3 = Abby
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Abby or CH2 == Abby or CH3 == Abby:
                        CH4 = Abby.clone()
                    else:
                        CH4 = Abby
                    pygame.time.delay(500)
            elif action == 'select OroborusTermina':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = OroborusTermina
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTermina:    
                        CH2 = OroborusTermina.clone()
                    else:
                        CH2 = OroborusTermina
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTermina or CH2 == OroborusTermina:
                        CH3 = OroborusTermina.clone()
                    else:
                        CH3 = OroborusTermina
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTermina or CH2 == OroborusTermina or CH3 == OroborusTermina:
                        CH4 = OroborusTermina.clone()
                    else:
                        CH4 = OroborusTermina
                    pygame.time.delay(500)
            elif action == 'select OroborusTerminaC':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = OroborusTerminaC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTerminaC:    
                        CH2 = OroborusTerminaC.clone()
                    else:
                        CH2 = OroborusTerminaC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTerminaC or CH2 == OroborusTerminaC:
                        CH3 = OroborusTerminaC.clone()
                    else:
                        CH3 = OroborusTerminaC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == OroborusTerminaC or CH2 == OroborusTerminaC or CH3 == OroborusTerminaC:
                        CH4 = OroborusTerminaC.clone()
                    else:
                        CH4 = OroborusTerminaC
                    pygame.time.delay(500)
            elif action == 'select OverlordSoul':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = OverlordSoul
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OverlordSoul:    
                        CH2 = OverlordSoul.clone()
                    else:
                        CH2 = OverlordSoul
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == OverlordSoul or CH2 == OverlordSoul:
                        CH3 = OverlordSoul.clone()
                    else:
                        CH3 = OverlordSoul
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == OverlordSoul or CH2 == OverlordSoul or CH3 == OverlordSoul:
                        CH4 = OverlordSoul.clone()
                    else:
                        CH4 = OverlordSoul
                    pygame.time.delay(500)
            elif action == 'select OverlordSoulC':
               if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   CH1 = OverlordSoulC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordSoulC:    
                       CH2 = OverlordSoulC.clone()
                   else:
                       CH2 = OverlordSoulC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordSoulC or CH2 == OverlordSoulC:
                       CH3 = OverlordSoulC.clone()
                   else:
                       CH3 = OverlordSoulC
                   pygame.time.delay(500)
               elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                   if CH1 == OverlordSoulC or CH2 == OverlordSoulC or CH3 == OverlordSoulC:
                       CH4 = OverlordSoulC.clone()
                   else:
                       CH4 = OverlordSoulC
                   pygame.time.delay(500)
            elif action == 'select Kyra':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Kyra
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Kyra:    
                        CH2 = Kyra.clone()
                    else:
                        CH2 = Kyra
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Kyra or CH2 == Kyra:
                        CH3 = Kyra.clone()
                    else:
                        CH3 = Kyra
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Kyra or CH2 == Kyra or CH3 == Kyra:
                        CH4 = Kyra.clone()
                    else:
                        CH4 = Kyra
                    pygame.time.delay(500)
            elif action == 'select Hunter':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Hunter
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Hunter:    
                        CH2 = Hunter.clone()
                    else:
                        CH2 = Hunter
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Hunter or CH2 == Hunter:
                        CH3 = Hunter.clone()
                    else:
                        CH3 = Hunter
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Hunter or CH2 == Hunter or CH3 == Hunter:
                        CH4 = Hunter.clone()
                    else:
                        CH4 = Hunter
                    pygame.time.delay(500)
            elif action == 'select HunterC':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = HunterC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == HunterC:    
                        CH2 = HunterC.clone()
                    else:
                        CH2 = HunterC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == HunterC or CH2 == HunterC:
                        CH3 = HunterC.clone()
                    else:
                        CH3 = HunterC
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == HunterC or CH2 == HunterC or CH3 == HunterC:
                        CH4 = HunterC.clone()
                    else:
                        CH4 = HunterC
                    pygame.time.delay(500)
            elif action == 'select AI':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = AI
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AI:    
                        CH2 = AI.clone()
                    else:
                        CH2 = AI
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AI or CH2 == AI:
                        CH3 = AI.clone()
                    else:
                        CH3 = AI
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == AI or CH2 == AI or CH3 == AI:
                        CH4 = AI.clone()
                    else:
                        CH4 = AI
                    pygame.time.delay(500)
            elif action == 'select AI_2':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = AI_2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AI_2:    
                        CH2 = AI_2.clone()
                    else:
                        CH2 = AI_2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == AI_2 or CH2 == AI_2:
                        CH3 = AI_2.clone()
                    else:
                        CH3 = AI_2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == AI_2 or CH2 == AI_2 or CH3 == AI_2:
                        CH4 = AI_2.clone()
                    else:
                        CH4 = AI_2
                    pygame.time.delay(500)
            elif action == 'select Monster1':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Monster1
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Monster1:    
                        CH2 = Monster1.clone()
                    else:
                        CH2 = Monster1
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Monster1 or CH2 == Monster1:
                        CH3 = Monster1.clone()
                    else:
                        CH3 = Monster1
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Monster1 or CH2 == Monster1 or CH3 == Monster1:
                        CH4 = Monster1.clone()
                    else:
                        CH4 = Monster1
                    pygame.time.delay(500)
            elif action == 'select Monster2':
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Monster2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Monster2:    
                        CH2 = Monster2.clone()
                    else:
                        CH2 = Monster2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    if CH1 == Monster2 or CH2 == Monster2:
                        CH3 = Monster2.clone()
                    else:
                        CH3 = Monster2
                    pygame.time.delay(500)
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    if CH1 == Monster2 or CH2 == Monster2 or CH3 == Monster2:
                        CH4 = Monster2.clone()
                    else:
                        CH4 = Monster2
                    pygame.time.delay(500)
            elif action == 'Nothing':
                print('Nuh-uh! Use backspace to deselect!')
                pygame.time.delay(500)
            elif action == 'b1v1':
                b1v1, b2v1, b3v1 = True, False, False
                pygame.time.delay(500)
            elif action == 'b2v1':
                b1v1, b2v1, b3v1 = False, True, False
                pygame.time.delay(500)
            elif action == 'b3v1':
                b1v1, b2v1, b3v1 = False, False, True
                pygame.time.delay(500)
            elif action in background_list:
                if b1v1 or b2v1:
                    BACKGROUND = action
                if b3v1:
                    if BACKGROUND == '' and BACKGROUND2 == '':
                        BACKGROUND = action
                    elif BACKGROUND != '' and BACKGROUND2 == '':
                        BACKGROUND2 = action
                pygame.time.delay(500)
            elif action == 'rival battle':
                MUSIC = BattleTheme1
                pygame.time.delay(500)
            elif action == 'akobos':
                MUSIC = AkobosBattle
                pygame.time.delay(500)
            elif action == 'agent of darkness':
                MUSIC = NightmareBattle
                pygame.time.delay(500)
            elif action == 'overlord phase 1':
                MUSIC = OverlordBattle
                pygame.time.delay(500)
            elif action == 'overlord phase 2':
                MUSIC = OverlordSoulBattle
                pygame.time.delay(500)
            elif action == 'overlord phase 3':
                MUSIC = OroborusTerminaBattle
                pygame.time.delay(500)
            elif action == 'monster':
                MUSIC = MonsterBattle
                pygame.time.delay(500)
            elif action == 'AI phase 1':
                MUSIC = AIBattle1
                pygame.time.delay(500)
            elif action == 'AI phase 2':
                MUSIC = AIBattle2
                pygame.time.delay(500)
            elif action == 'choose characters':
                picking, scene = False, 'choose2'
            elif action == 'select background(s)':
                choosing, scene = False, 'choose3'
            elif action == 'pick music':
                deciding, scene = False, 'choose4'
            elif action == CustomBattle:
                pygame.time.delay(100)
                ZE_BATTLE = '0a'
                selecting, battle_ON, scene = False, True, '0a'
                playMusic(MUSIC,'music',True)
            elif action == CustomBattle2:
                pygame.time.delay(100)
                ZE_BATTLE = '0b'
                selecting, battle_ON, scene = False, True, '0b'
                playMusic(MUSIC,'music',True)
            elif action == CustomBattle3:
                pygame.time.delay(100)
                ZE_BATTLE = '0c'
                selecting, battle_ON, scene = False, True, '0c'
                playMusic(MUSIC,'music',True)
        elif scene in ['try_again1','try_again2','try_again3','try_again4']:
            if action == 'quit': #to quit the game after losing a battle
                pygame.quit()
                sys.exit()
            elif action == Battle: #to restart the battle after losing, with the saved parameters
                #reset characters' stats
                CH1.reset()
                CH2.reset()
                if CH3 not in ['', NullPerson]:
                    CH3.reset()
                if CH4 not in ['', NullPerson]:
                    CH4.reset()
                #start the battle
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                battle_ON, scene = True, ZE_BATTLE
                playMusic(MUSIC,'music',True)
            elif action == 'restart':
                print()
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                scene = 'start_menu'
        elif scene in list_of_battle_scenes:
            if action == None:
                print("Nuh-Uh! Use your own moves!")
            elif action == 'Nope':
                print('Use Recover!') #aka do nothing; no worries, this won't cause a turn to go by, since the opponent also won't do anything (he only does things when Attack, Guard or Recover)
            elif action in [Attack,Guard,Recover]: #the battle moves
                pygame.time.delay(200)
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
    global score, max_score
    #background colour
    screen.fill(black)
    #title (game name)
    make_text("Z-Legends: Exceedra's Awakening",'comicsansms',70,white,SCREEN_WIDTH/2,100)
    #buttons for each episode
    if not Episode1_completed:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,red,green,'menu','scene_1')
    if Episode1_completed and not Episode2_completed:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,BLUE,blue,'menu','scene_1')
        make_button('Episode 2','Corbel',35,white,500,310,200,70,red,green,'menu','scene_6')
    if Episode2_completed and not Episode3_completed:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,BLUE,blue,'menu','scene_1')
        make_button('Episode 2','Corbel',35,white,500,310,200,70,BLUE,blue,'menu','scene_6')
        make_button('Episode 3','Corbel',35,white,500,410,200,70,red,green,'menu','scene_12')
    if Episode3_completed and not Game_completed:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,BLUE,blue,'menu','scene_1')
        make_button('Episode 2','Corbel',35,white,500,310,200,70,BLUE,blue,'menu','scene_6')
        make_button('Episode 3','Corbel',35,white,500,410,200,70,BLUE,blue,'menu','scene_12')
        make_button('Final Episode','Corbel',35,white,500,510,200,70,red,green,'menu','scene_19')
    if Game_completed and not max_score:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,BLUE,blue,'menu','scene_1')
        make_button('Episode 2','Corbel',35,white,500,310,200,70,BLUE,blue,'menu','scene_6')
        make_button('Episode 3','Corbel',35,white,500,410,200,70,BLUE,blue,'menu','scene_12')
        make_button('Final Episode','Corbel',35,white,500,510,200,70,BLUE,blue,'menu','scene_19')
        make_button('Boss Rush','Corbel',35,white,375,610,200,70,red,green,'menu','b1')
        make_button('Custom Battle','Corbel',35,white,625,610,200,70,red,green,'menu','choose')
        make_text(f"Score: {score}",'Corbel',25,white,470,700)
    if Game_completed and max_score:
        make_button('Episode 1','Corbel',35,white,500,210,200,70,BLUE,blue,'menu','scene_1')
        make_button('Episode 2','Corbel',35,white,500,310,200,70,BLUE,blue,'menu','scene_6')
        make_button('Episode 3','Corbel',35,white,500,410,200,70,BLUE,blue,'menu','scene_12')
        make_button('Final Episode','Corbel',35,white,500,510,200,70,BLUE,blue,'menu','scene_19')
        make_button('Boss Rush','Corbel',35,white,375,610,200,70,BLUE,blue,'menu','b1')
        make_button('Custom Battle','Corbel',35,white,625,610,200,70,red,green,'menu','choose')
        make_text("High Score: 14",'Corbel',25,white,470,700)
    
#the 19 battle-system functions (20 if you count make_button)
#game over (asks to try again or quit the game)
def try_again():
    '''tell the user to try again after losing a battle'''
    #buttons
    screen.fill(black)
    make_button('Try again?','Corbel',35,white,500,260,200,70,red,green,'battle',Battle)
    make_button('I give up...','Corbel',35,white,500,560,200,70,red,green,'battle','quit')
        
    pygame.display.flip()
    
def try_again2(rush=True):
    '''tell the user to restart the boss rush challenge or custom battle'''
    global i, k
    #buttons and text
    screen.fill(black)
    make_button('Try again?','Corbel',35,white,500,260,200,70,red,green,'battle','restart')
    if rush:
        make_text(f"Score: {score}",'Corbel',50,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+75)
        make_button('I give up...','Corbel',35,white,500,560,200,70,red,green,'battle','quit')
        i, k = 0, 0
    else:
        make_button('I\'m done...','Corbel',35,white,500,560,200,70,red,green,'battle','quit')
    
    pygame.display.flip()

#rock-paper-scissors like: rock=attack, paper=guard, scissors=recover
#these functions are what happens when character1 (you!) selects that corresponding move
def Attack(character1,character2):
    '''attack scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.GuardMove: #if opponent guards and you attack, no damage
        character2.losePower(0,character2.GuardMove.energy_consumption)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        if character1.energy < 0:
            character1.energy = 0
        print(character1.name,'did ATTACK;',character2.name,'did',opponent_move.specialty) #description of the turn
        
    elif opponent_move == character2.RecoverMove: #if opponent recovers and you attack, damage for the opponent
        character2.losePower(character1.AttackMove.damage,0)
        character1.losePower(0,character1.AttackMove.energy_consumption)
        if character1.energy < 0:
            character1.energy = 0
        print(character1.name,'did ATTACK;',character2.name,'did',opponent_move.specialty) #description of the turn
        
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
        pygame.display.flip() #helps truly get rid of the temporary message after the time has passed
            
        potential1 = character1.attack_potential + SPACEBAR_count
        potential2 = character2.attack_potential + randrange(1,11)
        if potential1 >= potential2:
            character2.losePower(character1.AttackMove.damage,0)
            character1.losePower(0,character1.AttackMove.energy_consumption)
            if character1.energy < 0:
                character1.energy = 0
            print(f"{character1.name} did ATTACK; {character2.name} did {opponent_move.specialty}, but {character1.name} landed damage!") #description of the turn if successfully attacked
        else:
            character1.losePower(character2.AttackMove.damage,0)
            character2.losePower(0,character2.AttackMove.energy_consumption)
            print(f"{character1.name} did ATTACK; {character2.name} did {opponent_move.specialty}, but {character2.name} landed damage!") #description of the turn if failed to attack
            if character1.health <= 0:
                print(f"{character1.name} was defeated!\n\n")
        

def Guard(character1,character2):
    '''guard scenarios'''
    opponent_move = character2.randomMove()
    if opponent_move == character2.AttackMove: #if the opponent attacks and you guard, no damage
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.AttackMove.energy_consumption)
        if character1.energy < 0:
            character1.energy = 0
        
    elif opponent_move == character2.GuardMove: #if the opponent guards and you guard, nothing
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.losePower(0,character2.GuardMove.energy_consumption)
        if character1.energy < 0:
            character1.energy = 0
        
    elif opponent_move == character2.RecoverMove: #if the opponent recovers and you guard, they recover, you nothing
        character1.losePower(0,character1.GuardMove.energy_consumption)
        character2.Recover(character2.RecoverMove.recovery)
        #if the opponent recovers up to max stats
        if character2.health > character2.og_health:
            character2.health = character2.og_health
        if character2.energy > character2.og_energy:
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
        if character2.health > character2.og_health:
            character2.health = character2.og_health
        if character2.energy > character2.og_energy:
            character2.energy = character2.og_energy 
        
    elif opponent_move == character2.AttackMove: #if the opponent attacks and you recover, you take damage
        character1.losePower(character2.AttackMove.damage,0)
        character2.losePower(0,character2.AttackMove.energy_consumption)
        if character1.energy < 0:
            character1.energy = 0
    
    #if you recover up to your min or max stats:
    if character1.health > character1.og_health:
        character1.health = character1.og_health
    if character1.energy > character1.og_energy:
        character1.energy = character1.og_energy
        
    print(character1.name,'did RECOVER;',character2.name,'did',opponent_move.specialty) #description of the turn
    if character1.health <= 0:
        print(f"{character1.name} was defeated!\n\n")
        
#run the battle
def Battle(character1,character2,background,battle_name,music):
    '''function for 1v1 battles in the story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    background is the battle's background
    battle_name is to keep track of what battle is going on; the battle's corresponding scene has the same name
    music is the battle theme playing
    '''
    #start the battle    
    global Locked1, Locked2, dialogue_index, battle_ON, CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene, battle_scenes_to_story_scenes
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
                if event.key == pygame.K_p: #press p to pause
                    pause = True
                    pause_the_game()
                if event.key == pygame.K_0: #press 0 to exit
                    pygame.quit()
                    sys.exit()
                
            #setup the background and character placements
            screen.blit(background,(0, 0))
            if battle_name == 'battle_e1_s2':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650) #hydranoid
            elif battle_name == 'battle_e2_s1':
                character1.BattlePosition(-50, SCREEN_HEIGHT-600) #hydranoid
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500) #hunter
            elif battle_name == 'battle_e2_s4':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550) #overlord
            else:
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                    
            #controlling energy and buttons for character 1 (usually Exceedra)
            if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                Locked1 = True
            elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                Locked1 = False
            
            if Locked1 == True:
                make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
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
                print(character1.name,'lost! Wanna try again, or quit?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again1'
            
            #winning
            elif character1.health > 0 and character2.health <= 0:
                print(character1.name,'won!')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                battle_ON, scene = False, battle_scenes_to_story_scenes[battle_name]
                dialogue_index += 1
        
        pygame.display.flip()

def Battle2Chars(character1,character2,character3,background,battle_name,music): #{TO UPDATE}
    '''
    special type of battle where you can use 2 characters for your side 
    by pressing s, you can switch between characters
    still 1 opponent, so this type is a 2v1 battle
    used for Final Episode monster battles in story
    '''
    global Locked1, Locked2, Locked3, dialogue_index, battle_ON, CH1, CH2, CH3, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene, battle_scenes_to_story_scenes
    
    CH1 = character1
    CH2 = character3 #save the opponent as 2 so that other battle functions can treat it as 2 (the NPC)
    CH3 = character2 #CH3 will be the playable fighter not currently used
    BACKGROUND = background
    ZE_BATTLE = battle_name
    MUSIC = music
    char1 = True #if you're using the first available character
    no_switch = False
    
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
                if event.key == pygame.K_s: #press s to switch between available fighters
                    if no_switch == False:
                        char1 = not char1
        
            screen.blit(background,(0, 0))
            character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500) #always blit the opponent to the right, no matter the CH1
            
            if char1:
                CH1 = character1 #if using the first fighter, make it CH1 for the other battle functions
                CH3 = character2 #and make CH3 the currently unused character2
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                
                #controlling character1's energy while on the field
                if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                    Locked1 = True
                elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                    Locked1 = False
                
                if Locked1 == True:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            else:
                CH1 = character2 #char1 = False means that you're currently using character2, so make it CH1
                CH3 = character1 #and make the other character CH3 (having all 3 CHs defined makes sure they are all reset if you try again after losing)
                if character2 != HydranoidC:
                    character2.BattlePosition(0, SCREEN_HEIGHT-500)
                else:
                    character2.BattlePosition(-50, SCREEN_HEIGHT-600)
                    
                #controlling character2's energy while on the field
                if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                    Locked2 = True
                elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                    Locked2 = False
                
                if Locked2 == True:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            
            #controlling the opponent's energy at all times
            if character3.energy < character3.AttackMove.energy_consumption or character3.energy < character3.GuardMove.energy_consumption:
                Locked3 = True
            elif character3.energy > character3.AttackMove.energy_consumption and character3.energy > character3.GuardMove.energy_consumption:
                Locked3 = False
            
            if Locked3 == True:
                character3.movepool = [character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character3.movepool = [character3.AttackMove, character3.GuardMove, character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            
            #if one of your characters dies in-battle, stay on the alive one and can no longer switch out
            if character1.health <= 0 and character2.health > 0 and character3.health > 0:
                char1 = False
                no_switch = True
            elif character1.health > 0 and character2.health <= 0 and character3.health > 0:
                char1 = True
                no_switch = True
                
            #losing
            elif character1.health <= 0 and character2.health <= 0 and character3.health > 0:
                print(f"{character1.name} and {character2.name} lost! Wanna try again, or quit?")
                print()
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again1'
            
            #winning
            elif character3.health <= 0:
                print(f"{character1.name} and {character2.name} won!")
                print()
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                battle_ON, scene = False, battle_scenes_to_story_scenes[battle_name]
                dialogue_index += 1
            
        pygame.display.flip()

def BattleRush(character1,character2,background,battle_name,music,for_story=False):
    '''function for 1v1 battles in boss rush mode and Overlord 3 phase battle in story
    next_scene is function call of following scene in story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    battle_name is to keep track of what battle is going on so we can move on to the next; same as the name of the scene
    for_story is for the final Overlord fight; will have specific tasks than for the regular mode
    '''
    #start the battle    
    global Locked1, Locked2, battle_ON, CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene, list_of_battle_scenes, musicRush_list, score, dialogue_index, i, k
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
            if for_story == False:
                make_text(f"Score: {score}",'arialblack',35,white,100,30)
            if battle_name == 'b1':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650) #hydranoid
            elif battle_name == 'b4':
                character1.BattlePosition(0, SCREEN_HEIGHT-650) #hydranoid
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500) #hunter
            elif battle_name == 'b10.1':
                character1.BattlePosition(0, SCREEN_HEIGHT-500) #exceedra
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550) #overlord
            else:
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                    
            #controlling energy and buttons for character 1 (usually Exceedra)
            if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                Locked1 = True
            elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                Locked1 = False
            
            if Locked1 == True:
                make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
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
                print('You lost! Would you like to try again, or quit?')
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again2'
            
            #winning
            elif character1.health > 0 and character2.health <= 0:
                if battle_name != 'b3': #b3 temporary #any battle scene in boss rush mode not the end
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, list_of_battle_scenes[i+1]
                    playMusic(musicRush_list[k+1],'music',True)
                elif battle_name == 'b3' and for_story == False: #last boss rush battle scene
                    print()
                    score += 1
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    battle_ON, scene = False, "start_menu"
                elif battle_name == 'battle_e3_s7_3' and for_story == True: #last boss rush battle scene in story
                    print()
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    battle_ON, scene = False, 'scene_18'
                    dialogue_index += 1

        pygame.display.flip()

def BattleRush2(character1,character2,character3,background,battle_name,music,for_story=False):
    '''function for 2v1 battles in boss rush mode and Exceedra+Kyra boss rushes in the story
    next_scene is function call of following scene in story
    character1 and character2 are playable characters
    character3 is npc opponent
    battle_name is to keep track of what battle is going on so we can move on to the next; same as the name of the scene
    for_story is for the end of story boss rush; will have specific tasks than for the regular mode
    '''
    #start the battle    
    global Locked1, Locked2, Locked3, battle_ON, CH1, CH2, CH3, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene, list_of_battle_scenes, musicRush_list, score, dialogue_index, i, k
    #save the parameters in the global variables so we can use them in external functions (functions not directly connected to this one) requiring them
    CH1 = character1
    CH2 = character3 #save the opponent as 2 so that other battle functions can treat it as 2 (the NPC)
    CH3 = character2 #CH3 will be the playable fighter not currently used
    BACKGROUND = background
    ZE_BATTLE = battle_name
    MUSIC = music
    char1 = True #if you're using the first available character
    no_switch = False
    
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
                if event.key == pygame.K_s: #press s to switch between available fighters
                    if no_switch == False:
                        char1 = not char1
        
            screen.blit(background,(0, 0))
            if for_story == False:
                make_text(f"Score: {score}",'arialblack',35,white,100,30)
            if character3 != Overlord:
                character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500) #always blit the opponent to the right, no matter the CH1
            else:
                character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550) #for the overlord, slight change in y position
            
            if char1:
                CH1 = character1 #if using the first fighter, make it CH1 for the other battle functions
                CH3 = character2 #and make CH3 the currently unused character2
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                
                #controlling character1's energy while on the field
                if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                    Locked1 = True
                elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                    Locked1 = False
                
                if Locked1 == True:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            else:
                CH1 = character2 #char1 = False means that you're currently using character2, so make it CH1
                CH3 = character1 #and make the other character CH3 (having all 3 CHs defined makes sure they are all reset if you try again after losing)
                if character2 != HydranoidC:
                    character2.BattlePosition(0, SCREEN_HEIGHT-500)
                else:
                    character2.BattlePosition(-50, SCREEN_HEIGHT-600)
                    
                #controlling character2's energy while on the field
                if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                    Locked2 = True
                elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                    Locked2 = False
                
                if Locked2 == True:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            
            #controlling the opponent's energy at all times
            if character3.energy < character3.AttackMove.energy_consumption or character3.energy < character3.GuardMove.energy_consumption:
                Locked3 = True
            elif character3.energy > character3.AttackMove.energy_consumption and character3.energy > character3.GuardMove.energy_consumption:
                Locked3 = False
            
            if Locked3 == True:
                character3.movepool = [character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character3.movepool = [character3.AttackMove, character3.GuardMove, character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            
            #if one of your characters dies in-battle, stay on the alive one and can no longer switch out
            if character1.health <= 0 and character2.health > 0 and character3.health > 0:
                char1 = False
                no_switch = True
            elif character1.health > 0 and character2.health <= 0 and character3.health > 0:
                char1 = True
                no_switch = True
                
            #losing
            if character1.health > 0 and character2.health <= 0 and character3.health > 0 and battle_name == 'b2':
                print('You lost! Remember that Hydranoid needs to be alive to face the Hunter! Would you like to try again, or quit?')
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again2'
            elif character1.health <= 0 and character2.health <= 0 and character3.health > 0:
                print('You lost! Would you like to try again, or quit?')
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again2'
            
            #winning
            elif character3.health <= 0:
                if battle_name != 'b3': #b3 temporary #any battle scene in boss rush mode not the end
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, list_of_battle_scenes[i+1]
                    playMusic(musicRush_list[k+1],'music',True)
                elif battle_name == 'b3' and for_story == False: #last boss rush battle scene
                    print()
                    score += 1
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    battle_ON, scene = False, "start_menu"
                elif battle_name == 'battle_e4_s6_4' and for_story == True: #last 2 player boss rush battle scene in story
                    print()
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    battle_ON, scene = False, 'scene_24'
                    dialogue_index += 1
            
        pygame.display.flip()
        
def BattleRush3(character1,character2,character3,character4,background,background2,battle_name,music,for_story=False):
    '''function for the final 3v1 battle in boss rush mode
    next_scene is function call of following scene in story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    battle_name is to keep track of what battle is going on so we can move on to the next; same as the name of the scene
    for_story is the final boss; will have specific tasks than for the regular mode
    '''
    #start the battle    
    global Locked1, Locked2, Locked3, Locked4, battle_ON, CH1, CH2, CH3, CH4, BACKGROUND, BACKGROUND2, ZE_BATTLE, MUSIC, pause, scene, list_of_battle_scenes, musicRush_list, score, max_score, i, k, dialogue_index
    #save the parameters in the global variables so we can use them in external functions (functions not directly connected to this one) requiring them
    CH1 = character1
    CH2 = character4 #opponent is always CH2
    CH3 = character2
    CH4 = character3
    BACKGROUND = background
    BACKGROUND2 = background2
    ZE_BATTLE = battle_name
    MUSIC = music
    char1, char2, char3 = True, False, False #we need 3 char variables for this one...
    no_switch, no_switch2, no_switch3 = False, False, False #and also 3 no_switch's
    
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
                if event.key == pygame.K_a: #press a to switch to character1
                    if no_switch == False:
                        char1,char2,char3 = True,False,False
                if event.key == pygame.K_s: #press s to switch to character2
                    if no_switch2 == False:
                        char1,char2,char3 = False,True,False
                if event.key == pygame.K_d: #press d to switch to character3
                    if no_switch3 == False:
                        char1,char2,char3 = False,False,True
                        
            if char1:
                screen.blit(background,(0, 0))
                
                CH1 = character1 #if using the first fighter, make it CH1 for the other battle functions
                CH3 = character2 #and make the other 2 fighters CH3 and CH4
                CH4 = character3
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character1's energy while on the field
                if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                    Locked1 = True
                elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                    Locked1 = False
                
                if Locked1 == True:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
                
            if char2:
                screen.blit(background,(0, 0))
                
                CH1 = character2 #char2 = True means that you're currently using character2, so make it CH1
                CH3 = character1 #and make the other 2 fighters CH3 and CH4
                CH4 = character3
                character2.BattlePosition(0, SCREEN_HEIGHT-500)
                character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character2's energy while on the field
                if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                    Locked2 = True
                elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                    Locked2 = False
                
                if Locked2 == True:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            
            if char3:
                screen.blit(background2,(0, 0)) #change to second world background if character3 (Akobos in laboratory vs dream world grass plain with others)
                
                CH1 = character3
                CH3 = character1 
                CH4 = character2
                character3.BattlePosition(0, SCREEN_HEIGHT-500)
                character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character3's energy while on the field
                if character3.energy < character3.AttackMove.energy_consumption or character3.energy < character3.GuardMove.energy_consumption:
                    Locked3 = True
                elif character3.energy > character3.AttackMove.energy_consumption and character3.energy > character3.GuardMove.energy_consumption:
                    Locked3 = False
                
                if Locked3 == True:
                    make_button(character3.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character3.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character3.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character3.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character3.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character3.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
            
            #controlling the opponent's energy at all times
            if character4.energy < character4.AttackMove.energy_consumption or character4.energy < character4.GuardMove.energy_consumption:
                Locked4 = True
            elif character4.energy > character4.AttackMove.energy_consumption and character4.energy > character4.GuardMove.energy_consumption:
                Locked4 = False
            
            if Locked4 == True:
                character4.movepool = [character4.RecoverMove]
                make_button(character4.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character4.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character4.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character4.movepool = [character4.AttackMove, character4.GuardMove, character4.RecoverMove]
                make_button(character4.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character4.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character4.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            
            #if one of your characters dies in-battle, stay on the alive ones and can no longer switch out to dead one
            if character1.health <= 0:
                char1 = False
                no_switch = True
            if character2.health <= 0:
                char2 = False
                no_switch2 = True
            if character3.health <= 0:
                char3 = False
                no_switch3 = True
             
            if no_switch and character2.health <= 0:
                char3 = True
            elif no_switch and character2.health > 0:
                if not char3: #this type of section is to make sure characters do not overlap
                    char2 = True
                else:
                    char3 = True
            if no_switch2 and character3.health <= 0:
                char1 = True
            elif no_switch2 and character3.health > 0:
                if not char1:
                    char3 = True
                else:
                    char1 = True
            if no_switch3 and character1.health <= 0:
                char2 = True
            elif no_switch3 and character1.health > 0:
                if not char2:
                    char1 = True
                else:
                    char2 = True
            
            #losing
            if character1.health <= 0 and character2.health <= 0 and character3.health <= 0 and character4.health > 0:
                print('You lost! Would you like to try again, or quit?')
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again2'
            
            #winning
            elif character4.health <= 0:
                if battle_name == 'battle_e4_s7_1' and for_story == True:
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, list_of_battle_scenes[i+1]
                    playMusic(musicRush_list[k+1],'music',True)
                elif battle_name == 'battle_e4_s7_2' and for_story == True:
                    print()
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    battle_ON, scene = False, 'scene_25'
                    dialogue_index += 1
                elif battle_name == 'b14.1' and for_story == False:
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, list_of_battle_scenes[i+1]
                    playMusic(musicRush_list[k+1],'music',True)
                elif battle_name == 'b14.2' and for_story == False:
                    score += 1/2
                    pygame.mixer.music.stop()
                    playMusic(BattleWon,'sound')
                    print('YOU DID IT!!! Congratulations!')
                    print()
                    max_score = True
                    battle_ON, scene = False, "credits2"
 
        pygame.display.flip()
    
#custom battle functions
def customCharacter():
    '''use console prompts to create a custom character as fighter for custom battle'''
    global designing, b1v1, b2v1, b3v1, CH1, CH2, CH3, CH4
    
    while designing:
        print("Please refer to the Custom Character Creation Guide in the Rulebook for the following questions.\n\n")
        name = input("Enter your character's name: ")
        health = input("Enter a number between 50 and 200 for health: ")
        energy = input("Enter a number between 30 and 150 for energy: ")
        attack = input("Enter a number between 15 and 35 for attack potential: ")
        a_move = input("Enter the name of your desired Attack move: ")
        g_move = input("Enter the name of your desired Guard move: ")
        r_move = input("Enter the name of your desired Recover move: ")
        picture = input("Enter the name of your character's sprite: ")
        print()
        
        #make sure all entries are valid
        if (health.isdigit() and 50 <= int(health) <= 200 and energy.isdigit() and 30 <= int(energy) <= 150 and attack.isdigit() and 15 <= int(attack) <= 35
            and a_move in ['Dragon Fist of Fury', 'Sword Slash', 'Trident of Demise', 'Mental Plague', 'Time Pulse', 'Dark En', 'Dark Missile', 'Dark Lightning', 'Dark Blast', 'Surprise Attack', 'Lightsaber Barrage', 'Galaxy Barrage', 'Jab-Cross', 'Distorsion Break', 'Cyber Barrage', 'Blaze Blitz', 'Subzero Spear']
            and g_move in ['Tail Block','Block','Dream Trapped','Time Stop','Black Shield','Spike Shield','Teleport','Energy Shield','Focus Block','Firewall','Flame Armor','Ice Armor']
            and r_move in ['Dragon Spirit', 'Heal', 'Demon Blood', 'Dream Eater', 'Centered', 'Shadow Bath', 'Spirit of Vengeance', 'Psychopower', 'Hunter\'s Way', 'Power of Love', 'Self Repair', 'Beast Mode']
            and picture in ['Exceedra1_pic', 'Exceedra4_pic','Hydranoid_pic','Overlord_pic','Destiny_pic','Akobos_pic','Grace_pic','Ken_pic','Finlay_pic','Junia_pic','Nightmare_pic','Abby_pic','OroborusTermina_pic','OverlordSoul_pic','DarkExceedra_pic','Kyra_pic','Hunter_pic','Sophie_pic','Denis_pic','AI_pic','AI_2_pic','Monster1_pic','Monster2_pic']):
            #then assign to correct CH            
            if b1v1:
                if CH1 == NullPerson:
                    CH1 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                else:
                    CH2 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
            if b2v1:
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson:
                    CH1 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson:
                    CH2 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson:
                    CH3 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
            if b3v1:
                if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH1 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH2 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
                    CH3 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
                elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
                    CH4 = Character(name,int(health),int(energy),int(attack),find('move',a_move),find('move',g_move),find('move',r_move),find('picture',picture))
                    pygame.time.delay(500)
                    designing = False
        else:
            print('Please try again.\n\n')
        
def randomCharacter():
    '''
    picks a random character from all playable characters
    '''
    global b1v1, b2v1, b3v1, CH1, CH2, CH3, CH4, CH_List
    
    if b1v1:
        if CH1 == NullPerson:
            CH1 = choice(CH_List)
            pygame.time.delay(500)
        else:
            CH2 = choice(CH_List)
            if CH2 is CH1:
                CH2 = CH2.clone()
            pygame.time.delay(500)
    if b2v1:
        if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson:
            CH1 = choice(CH_List)
            pygame.time.delay(500)
        elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson:
            CH2 = choice(CH_List)
            if CH2 is CH1:
                CH2 = CH2.clone()
            pygame.time.delay(500)
        elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson:
            CH3 = choice(CH_List)
            if (CH3 is CH1) or (CH3 is CH2):
                CH3 = CH3.clone()
            pygame.time.delay(500)
    if b3v1:
        if CH1 == NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
            CH1 = choice(CH_List)
            pygame.time.delay(500)
        elif CH1 != NullPerson and CH2 == NullPerson and CH3 == NullPerson and CH4 == NullPerson:
            CH2 = choice(CH_List)
            if CH2 is CH1:
                CH2 = CH2.clone()
            pygame.time.delay(500)
        elif CH1 != NullPerson and CH2 != NullPerson and CH3 == NullPerson and CH4 == NullPerson:
            CH3 = choice(CH_List)
            if CH3 is CH1 or CH3 is CH2:
                CH3 = CH3.clone()
            pygame.time.delay(500)
        elif CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 == NullPerson:
            CH4 = choice(CH_List)
            if CH4 is CH1 or CH4 is CH2 or CH4 is CH3:
                CH4 = CH4.clone()
            pygame.time.delay(500)
            
    pygame.display.flip()

def chooseYourBattle():
    '''
    first step is for player to choose their type of battle (1v1, 2v1, 3v1)
    '''
    global scene, pause, picking, b1v1, b2v1, b3v1
    
    while picking:
        battle_type_chosen = b1v1 != False or b2v1 != False or b3v1 != False
        #only when the battle type is chosen can they move on to the next step
        if battle_type_chosen == False:
            screen.fill(black)
            #instructions
            make_text("Choose your battle type, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
            #buttons for each type
            make_button('1 vs 1','Corbel',35,white,500,210,200,70,red,green,'menu','b1v1')
            make_button('2 vs 1','Corbel',35,white,500,310,200,70,red,green,'menu','b2v1')
            make_button('3 vs 1','Corbel',35,white,500,410,200,70,red,green,'menu','b3v1')
        else:
            screen.fill(black)
            make_text("Choose your battle type, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
            #buttons for each type; highlight the selected type in blue
            if b1v1:
                make_button('1 vs 1','Corbel',35,white,500,210,200,70,BLUE,BLUE,'menu','Nothing')
            else:
                make_button('1 vs 1','Corbel',35,white,500,210,200,70,black,black,'menu','Nothing')
            if b2v1:
                make_button('2 vs 1','Corbel',35,white,500,310,200,70,BLUE,BLUE,'menu','Nothing')
            else:
                make_button('2 vs 1','Corbel',35,white,500,310,200,70,black,black,'menu','Nothing')
            if b3v1:
                make_button('3 vs 1','Corbel',35,white,500,410,200,70,BLUE,BLUE,'menu','Nothing')
            else:
                make_button('3 vs 1','Corbel',35,white,500,410,200,70,black,black,'menu','Nothing')
            #show the continue button
            make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','choose characters')
            
        #controls
        for event in pygame.event.get():
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
                if event.key == pygame.K_1: #press 1 to get back to main menu
                    picking = False
                    scene = 'start_menu'
                if event.key == pygame.K_BACKSPACE:  #reset your pick (press Backspace)
                    b1v1, b2v1, b3v1 = False, False, False
                        
        pygame.display.flip()
    
def chooseYourCharacter(): #{TO UPDATE WITH ALL CHARACTERS AND THEIR POSITIONS}
    '''
    second step leads you to kinda like a smash bros character select screen before your cudtom battle
    '''
    global scene, CH1, CH2, CH3, CH4, choosing, pause, b1v1, b2v1, b3v1
    
    while choosing:
        if b1v1: #if they chose 1 vs 1
            the_two_are_selected = CH1 != NullPerson and CH2 != NullPerson
            #only when both characters have been selected that they show up with the GO! button    
            if the_two_are_selected == False:
                screen.fill(black)
                #instructions
                make_text("Choose 2 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #buttons for each character (all battle characters in the story available, even vilains)
                make_button('Custom','Corbel',15,blue,100,200,100,70,yellow,green,'menu','customCharacter')
                make_button('Random','Corbel',15,blue,250,200,100,70,yellow,green,'menu','randomCharacter')
                make_button(ExceedraMain.name,'Corbel',15,white,400,200,100,70,red,green,'menu','select Exceedra')
                make_button(Destiny.name,'Corbel',15,white,550,200,100,70,red,green,'menu','select Destiny')
                make_button(Hydranoid.name,'Corbel',15,white,700,200,100,70,red,green,'menu','select Hydranoid')       
                make_button(Overlord.name,'Corbel',15,white,850,200,100,70,red,green,'menu','select Overlord')
                make_button(Akobos.name,'Corbel',15,white,1000,200,100,70,red,green,'menu','select Akobos')
                make_button(Nightmare.name,'Corbel',15,white,100,300,100,70,red,green,'menu','select Nightmare')
                make_button(HydranoidC.name,'Corbel',15,white,250,300,100,70,red,green,'menu','select HydranoidC')
                make_button(OverlordC.name,'Corbel',15,white,400,300,100,70,red,green,'menu','select OverlordC')
                make_button(AkobosC.name,'Corbel',15,white,550,300,100,70,red,green,'menu','select AkobosC')
                make_button(NightmareC.name,'Corbel',15,white,700,300,100,70,red,green,'menu','select NightmareC')
            else:
                screen.fill(black)
                make_text("Choose 2 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #show your selects and start button
                #some problems with positioning Hydranoid nicely...
                make_text(CH1.name,'Corbel',35,white,200,350)
                make_text(CH2.name,'Corbel',35,white,SCREEN_WIDTH-400,350)
                if (CH1 == HydranoidC or CH1 == Hydranoid) and (CH2 == Hydranoid or CH2 == HydranoidC):
                    CH1.BattlePosition(0, SCREEN_HEIGHT-650)
                    CH2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                    make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
                elif (CH1 == HydranoidC or CH1 == Hydranoid) and (CH2 != Hydranoid and CH2 != HydranoidC):
                    CH1.BattlePosition(0, SCREEN_HEIGHT-650)
                    CH2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                    make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
                elif (CH1 != HydranoidC and CH1 != Hydranoid) and (CH2 == Hydranoid or CH2 == HydranoidC):
                    CH1.BattlePosition(0, SCREEN_HEIGHT-500)
                    CH2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                    make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
                else:
                    CH1.BattlePosition(0, SCREEN_HEIGHT-500)
                    CH2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                    make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
        
        if b2v1: #if they chose 2 vs 1
            the_three_are_selected = CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson
            if the_three_are_selected == False:
                screen.fill(black)
                #instructions
                make_text("Choose 3 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #buttons for each character (all battle characters in the story available, even vilains)
                make_button('Custom','Corbel',15,blue,100,200,100,70,yellow,green,'menu','customCharacter')
                make_button('Random','Corbel',15,blue,250,200,100,70,yellow,green,'menu','randomCharacter')
                make_button(ExceedraMain.name,'Corbel',15,white,400,200,100,70,red,green,'menu','select Exceedra')
                make_button(Destiny.name,'Corbel',15,white,550,200,100,70,red,green,'menu','select Destiny')
                make_button(Hydranoid.name,'Corbel',15,white,700,200,100,70,red,green,'menu','select Hydranoid')       
                make_button(Overlord.name,'Corbel',15,white,850,200,100,70,red,green,'menu','select Overlord')
                make_button(Akobos.name,'Corbel',15,white,1000,200,100,70,red,green,'menu','select Akobos')
                make_button(Nightmare.name,'Corbel',15,white,100,300,100,70,red,green,'menu','select Nightmare')
                make_button(HydranoidC.name,'Corbel',15,white,250,300,100,70,red,green,'menu','select HydranoidC')
                make_button(OverlordC.name,'Corbel',15,white,400,300,100,70,red,green,'menu','select OverlordC')
                make_button(AkobosC.name,'Corbel',15,white,550,300,100,70,red,green,'menu','select AkobosC')
                make_button(NightmareC.name,'Corbel',15,white,700,300,100,70,red,green,'menu','select NightmareC')
            else:
                screen.fill(black)
                make_text("Choose 3 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #show your selects and start button
                #some problems with positioning everyone nicely... simpler code
                make_text(CH1.name,'Corbel',35,white,200,350)
                make_text(CH2.name,'Corbel',35,white,500,350)
                make_text(CH3.name,'Corbel',35,white,SCREEN_WIDTH-400,350)
                if CH1 == HydranoidC or CH1 == Hydranoid:
                    CH1.BattlePosition(-250, SCREEN_HEIGHT-600)
                elif CH1 == OverlordC or CH1 == Overlord:
                    CH1.BattlePosition(-100,SCREEN_HEIGHT-500)
                elif CH1 == Destiny:
                    CH1.BattlePosition(-200,SCREEN_HEIGHT-500)
                elif CH1 == AkobosC or CH1 == Akobos:
                    CH1.BattlePosition(-130,SCREEN_HEIGHT-450)
                elif CH1 == NightmareC or CH1 == Nightmare:
                    CH1.BattlePosition(-200,SCREEN_HEIGHT-400)
                else:
                    CH1.BattlePosition(0,SCREEN_HEIGHT-500)
                    
                if CH2 == HydranoidC or CH2 == Hydranoid:
                    CH2.BattlePosition(150,SCREEN_HEIGHT-600)
                elif CH2 == ExceedraMain:
                    CH2.BattlePosition(350,SCREEN_HEIGHT-500)
                elif CH2 == AkobosC or CH2 == Akobos:
                    CH2.BattlePosition(150,SCREEN_HEIGHT-450)
                elif CH2 == NightmareC or CH2 == Nightmare:
                    CH2.BattlePosition(150,SCREEN_HEIGHT-400)
                elif CH2 == OverlordC or CH2 == Overlord:
                    CH2.BattlePosition(175,SCREEN_HEIGHT-500)
                else:
                    CH2.BattlePosition(150,SCREEN_HEIGHT-500)
                    
                if CH3 == Hydranoid or CH3 == HydranoidC:
                    CH3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                else:
                    CH3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
        
        if b3v1: #if they chose 3 vs 1
            the_four_are_selected = CH1 != NullPerson and CH2 != NullPerson and CH3 != NullPerson and CH4 != NullPerson
            if the_four_are_selected == False:
                screen.fill(black)
                #instructions
                make_text("Choose 4 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #buttons for each character (all battle characters in the story available, even vilains)
                make_button('Custom','Corbel',15,blue,100,200,100,70,yellow,green,'menu','customCharacter')
                make_button('Random','Corbel',15,blue,250,200,100,70,yellow,green,'menu','randomCharacter')
                make_button(ExceedraMain.name,'Corbel',15,white,400,200,100,70,red,green,'menu','select Exceedra')
                make_button(Destiny.name,'Corbel',15,white,550,200,100,70,red,green,'menu','select Destiny')
                make_button(Hydranoid.name,'Corbel',15,white,700,200,100,70,red,green,'menu','select Hydranoid')       
                make_button(Overlord.name,'Corbel',15,white,850,200,100,70,red,green,'menu','select Overlord')
                make_button(Akobos.name,'Corbel',15,white,1000,200,100,70,red,green,'menu','select Akobos')
                make_button(Nightmare.name,'Corbel',15,white,100,300,100,70,red,green,'menu','select Nightmare')
                make_button(HydranoidC.name,'Corbel',15,white,250,300,100,70,red,green,'menu','select HydranoidC')
                make_button(OverlordC.name,'Corbel',15,white,400,300,100,70,red,green,'menu','select OverlordC')
                make_button(AkobosC.name,'Corbel',15,white,550,300,100,70,red,green,'menu','select AkobosC')
                make_button(NightmareC.name,'Corbel',15,white,700,300,100,70,red,green,'menu','select NightmareC')
            else:
                screen.fill(black)
                make_text("Choose 4 characters, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #show your selects and start button
                make_text(CH1.name,'Corbel',35,white,200,350)
                make_text(CH2.name,'Corbel',35,white,400,350)
                make_text(CH3.name,'Corbel',35,white,600,350)
                make_text(CH4.name,'Corbel',35,white,SCREEN_WIDTH-400,350)
                #some problems with positioning everyone nicely... oh well!
                if CH1 == HydranoidC or CH1 == Hydranoid:
                    CH1.BattlePosition(-250, SCREEN_HEIGHT-600)
                elif CH1 == OverlordC or CH1 == Overlord:
                    CH1.BattlePosition(-100,SCREEN_HEIGHT-500)
                elif CH1 == Destiny:
                    CH1.BattlePosition(-200,SCREEN_HEIGHT-500)
                elif CH1 == AkobosC or CH1 == Akobos:
                    CH1.BattlePosition(-130,SCREEN_HEIGHT-450)
                elif CH1 == NightmareC or CH1 == Nightmare:
                    CH1.BattlePosition(-200,SCREEN_HEIGHT-400)
                else:
                    CH1.BattlePosition(0,SCREEN_HEIGHT-500)
                    
                if CH2 == HydranoidC or CH2 == Hydranoid:
                    CH2.BattlePosition(-50,SCREEN_HEIGHT-600)
                elif CH2 == ExceedraMain:
                    CH2.BattlePosition(250,SCREEN_HEIGHT-500)
                elif CH2 == AkobosC or CH2 == Akobos:
                    CH2.BattlePosition(100,SCREEN_HEIGHT-450)
                elif CH2 == NightmareC or CH2 == Nightmare:
                    CH2.BattlePosition(150,SCREEN_HEIGHT-400)
                elif CH2 == OverlordC or CH2 == Overlord:
                    CH2.BattlePosition(75,SCREEN_HEIGHT-500)
                elif CH2 == Destiny:
                    CH2.BattlePosition(0,SCREEN_HEIGHT-500)
                else:
                    CH2.BattlePosition(100,SCREEN_HEIGHT-500)
                    
                if CH3 == HydranoidC or CH3 == Hydranoid:
                    CH3.BattlePosition(175,SCREEN_HEIGHT-600)
                elif CH3 == ExceedraMain:
                    CH3.BattlePosition(450,SCREEN_HEIGHT-500)
                elif CH3 == AkobosC or CH3 == Akobos:
                    CH3.BattlePosition(250,SCREEN_HEIGHT-450)
                elif CH3 == NightmareC or CH3 == Nightmare:
                    CH3.BattlePosition(200,SCREEN_HEIGHT-400)
                elif CH3 == OverlordC or CH3 == Overlord:
                    CH3.BattlePosition(275,SCREEN_HEIGHT-500)
                elif CH3 == Destiny:
                    CH3.BattlePosition(200,SCREEN_HEIGHT-500)
                else:
                    CH3.BattlePosition(250,SCREEN_HEIGHT-500)
                    
                if CH4 == Hydranoid or CH4 == HydranoidC:
                    CH4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                else:
                    CH4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                make_button('Continue!','Corbel',25,white,1000,600,100,70,red,green,'menu','select background(s)')
        
        for event in pygame.event.get():
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
                if event.key == pygame.K_1: #press 1 to return to choosing battle type
                    CH1 = NullPerson
                    CH2 = NullPerson
                    CH3 = NullPerson
                    CH4 = NullPerson
                    b1v1, b2v1, b3v1 = False, False, False
                    choosing, scene = False, 'choose'
                if event.key == pygame.K_BACKSPACE:  #reset your picks (press Backspace)
                    CH1 = NullPerson
                    CH2 = NullPerson
                    CH3 = NullPerson
                    CH4 = NullPerson
    
        pygame.display.flip()

def chooseYourBackgrounds(): #{TO UPDATE WITH ALL BACKGROUNDS}
    '''
    third step is for player to choose the background(s)
    '''
    global scene, pause, deciding, BACKGROUND, BACKGROUND2, b1v1, b2v2
    
    while deciding:
        if b1v1 or b2v1:
            background_chosen = BACKGROUND != ''
        elif b3v1:
            background_chosen = BACKGROUND != '' and BACKGROUND2 != ''
        
        if b1v1 or b2v1:
            if background_chosen == False:
                screen.fill(black)
                #instructions
                make_text("Choose a background, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                #buttons for each character (all battle characters in the story available, even vilains)
                make_button("The Dreamspace",'Corbel',15,white,100,200,100,70,red,green,'menu',dreamspace)
                make_button("High Point Secondary School",'Corbel',15,white,250,200,100,70,red,green,'menu',school)
                make_button("HPSS Library",'Corbel',15,white,400,200,100,70,red,green,'menu',library)       
                make_button("Parliament Hill",'Corbel',15,white,550,200,100,70,red,green,'menu',hill)
                make_button("Junia's house",'Corbel',15,white,700,200,100,70,red,green,'menu',house)
            else:
                screen.blit(BACKGROUND,(0, 0))
                make_text("Choose a background, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                make_button("The Dreamspace",'Corbel',15,white,100,200,100,70,black,black,'menu','Nothing')
                make_button("High Point Secondary School",'Corbel',15,white,250,200,100,70,black,black,'menu','Nothing')
                make_button("HPSS Library",'Corbel',15,white,400,200,100,70,black,black,'menu','Nothing')       
                make_button("Parliament Hill",'Corbel',15,white,550,200,100,70,black,black,'menu','Nothing')
                make_button("Junia's house",'Corbel',15,white,700,200,100,70,black,black,'menu','Nothing')
                make_button('Continue!','Corbel',35,white,1000,600,100,70,red,green,'menu','pick music')

        
        if b3v1:
            if background_chosen == False:
                screen.fill(black)
                make_text("Choose 2 backgrounds, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                make_button("The Dreamspace",'Corbel',15,white,100,200,100,70,red,green,'menu',dreamspace)
                make_button("High Point Secondary School",'Corbel',15,white,250,200,100,70,red,green,'menu',school)
                make_button("HPSS Library",'Corbel',15,white,400,200,100,70,red,green,'menu',library)       
                make_button("Parliament Hill",'Corbel',15,white,550,200,100,70,red,green,'menu',hill)
                make_button("Junia's house",'Corbel',15,white,700,200,100,70,red,green,'menu',house)
            else:
                screen.blit(BACKGROUND,(-600, 0))
                screen.blit(BACKGROUND2,(600, 0))
                make_text("Choose 2 backgrounds, then Continue!",'comicsansms',65,white,SCREEN_WIDTH/2,100)
                make_button("The Dreamspace",'Corbel',15,white,100,200,100,70,black,black,'menu','Nothing')
                make_button("High Point Secondary School",'Corbel',15,white,250,200,100,70,black,black,'menu','Nothing')
                make_button("HPSS Library",'Corbel',15,white,400,200,100,70,black,black,'menu','Nothing')       
                make_button("Parliament Hill",'Corbel',15,white,550,200,100,70,black,black,'menu','Nothing')
                make_button("Junia's house",'Corbel',15,white,700,200,100,70,black,black,'menu','Nothing')
                make_button('Continue!','Corbel',35,white,1000,600,100,70,red,green,'menu','pick music')
        
        for event in pygame.event.get():
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
                if event.key == pygame.K_1: #press 1 to return to choosing characters
                    BACKGROUND = ''
                    BACKGROUND2 = ''
                    deciding, scene = False, 'choose2'
                if event.key == pygame.K_BACKSPACE:  #reset your picks (press Backspace)
                    BACKGROUND = ''
                    BACKGROUND2 = ''
                
        pygame.display.flip()
    
def chooseYourMusic(): #{TO UPDATE WITH ALL BATTLE MUSIC}
    '''
    final step is to choose music (I nearly forgot to add this to the steps! LOL)
    '''
    global scene, pause, selecting, MUSIC, b1v1, b2v1, b3v1
    
    while selecting:
        music_chosen = MUSIC != ''
        
        if music_chosen == False:
            screen.fill(black)
            #instructions
            make_text("Choose a music track, then GO!!",'comicsansms',70,white,SCREEN_WIDTH/2,100)
            #buttons for each character (all battle characters in the story available, even vilains)
            make_button("Rival Battle",'Corbel',15,white,100,200,100,70,red,green,'menu','rival battle')
            make_button("Akobos Battle",'Corbel',15,white,250,200,100,70,red,green,'menu','akobos')
            make_button("Agent of Darkness Battle",'Corbel',15,white,400,200,100,70,red,green,'menu','agent of darkness')       
        else:
            screen.fill(black)
            make_text("Choose a music track, then GO!!",'comicsansms',70,white,SCREEN_WIDTH/2,100)
            make_button("Rival Battle",'Corbel',15,white,100,200,100,70,black,black,'menu','Nothing')
            make_button("Akobos Battle",'Corbel',15,white,250,200,100,70,black,black,'menu','Nothing')
            make_button("Agent of Darkness Battle",'Corbel',15,white,400,200,100,70,black,black,'menu','Nothing')     
            if b1v1:
                make_button('GO!','Corbel',35,white,1000,600,100,70,red,green,'menu',CustomBattle)
            if b2v1:
                make_button('GO!','Corbel',35,white,1000,600,100,70,red,green,'menu',CustomBattle2)
            if b3v1:
                make_button('GO!','Corbel',35,white,1000,600,100,70,red,green,'menu',CustomBattle3)
        
        for event in pygame.event.get():
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
                if event.key == pygame.K_1: #press 1 to return to choosing background(s)
                    MUSIC = ''
                    selecting, scene = False, 'choose3'
                if event.key == pygame.K_BACKSPACE:  #reset your picks (press Backspace)
                    MUSIC = ''
        
        pygame.display.flip()

def CustomBattle(character1,character2,background,battle_name,music): #{TO UPDATE 3 BELOW WITH CHARACTER PLACEMENTS}
    '''function for 1v1 battles in custom battle mode
    next_scene is function call of following scene in story
    character1 is playable character (usually Exceedra)
    character2 is npc opponent
    battle_name is to keep track of what battle is going on so we can move on to the next; same as the name of the scene
    '''
    global Locked1, Locked2, battle_ON, CH1, CH2, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene
    CH1 = character1
    CH2 = character2
    BACKGROUND = background
    ZE_BATTLE = battle_name
    MUSIC = music
    
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
                if event.key == pygame.K_r:
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, 'try_again3'
                
            #setup the background and character placements
            #even more problems with positioning Hydranoid or the Overlord nicely...
            screen.blit(background,(0, 0))
            if (character1 == OverlordC or character1 == Overlord) and (character2 != Overlord and character2 != OverlordC) and (character2 != Hydranoid and character2 != HydranoidC):
                character1.BattlePosition(0, SCREEN_HEIGHT-550)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            elif (character2 == Overlord or character2 == OverlordC) and character1 != OverlordC and character1 != Overlord and character1 != HydranoidC and character1 != Hydranoid:
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
            elif (character1 == OverlordC or character1 == Overlord) and (character2 == Overlord or character2 == OverlordC):
                character1.BattlePosition(0, SCREEN_HEIGHT-550)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
            elif (character1 == HydranoidC or character1 == Hydranoid) and character2 != Hydranoid and character2 != HydranoidC and character2 != Overlord and character2 != OverlordC:
                character1.BattlePosition(0, SCREEN_HEIGHT-650)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            elif (character2 == Hydranoid or character2 == HydranoidC) and character1 != HydranoidC and character1 != Hydranoid and character1 != OverlordC and character1 != Overlord:
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
            elif (character1 == HydranoidC or character1 == Hydranoid) and (character2 == Hydranoid or character2 == OverlordC):
                character1.BattlePosition(0, SCREEN_HEIGHT-650)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
            elif (character1 == HydranoidC or character1 == Hydranoid) and (character2 == Overlord or character2 == OverlordC):
                character1.BattlePosition(0, SCREEN_HEIGHT-650)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
            elif (character1 == OverlordC or character1 == Overlord) and (character2 == Hydranoid or character2 == HydranoidC):
                character1.BattlePosition(0, SCREEN_HEIGHT-550)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
            else:
                character1.BattlePosition(0, SCREEN_HEIGHT-500)
                character2.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                    
            #controlling energy and buttons for character 1
            if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                Locked1 = True
            elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                Locked1 = False
            
            if Locked1 == True:
                make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
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
                print('You lost! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again3'
            
            #winning
            elif character1.health > 0 and character2.health <= 0:
                print('You won! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                battle_ON, scene = False, 'try_again3'
        
        pygame.display.flip()

def CustomBattle2(character1,character2,character3,background,battle_name,music):
    '''
    2v1 custom battles
    '''
    global Locked1, Locked2, Locked3, battle_ON, CH1, CH2, CH3, BACKGROUND, ZE_BATTLE, MUSIC, pause, scene
    
    CH1 = character1
    CH2 = character3 #save the opponent as 2 so that other battle functions can treat it as 2 (the NPC)
    CH3 = character2 #CH3 will be the playable fighter not currently used
    BACKGROUND = background
    ZE_BATTLE = battle_name
    MUSIC = music
    char1 = True #if you're using the first available character
    no_switch = False
    
    #during the battle
    while battle_ON:
        for event in pygame.event.get():
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
                if event.key == pygame.K_r:
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, 'try_again3'
                if event.key == pygame.K_s: #press s to switch between available fighters
                    if no_switch == False:
                        char1 = not char1
        
            screen.blit(background,(0, 0))
            #always blit the opponent to the right, no matter the CH1
            if character3 == Overlord or character3 == OverlordC:
                character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
            elif character3 == Hydranoid or character3 == HydranoidC:
                character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
            else:
                character3.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            
            if char1:
                CH1 = character1 #if using the first fighter, make it CH1 for the other battle functions
                CH3 = character2 #and make CH3 the currently unused character2
                if character1 == OverlordC or character1 == Overlord:
                    character1.BattlePosition(0, SCREEN_HEIGHT-550)
                elif character1 == HydranoidC or character1 == Hydranoid:
                    character1.BattlePosition(-50, SCREEN_HEIGHT-600)
                else:
                    character1.BattlePosition(0, SCREEN_HEIGHT-500)
                
                #controlling character1's energy while on the field
                if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                    Locked1 = True
                elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                    Locked1 = False
                
                if Locked1 == True:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            else:
                CH1 = character2 #char1 = False means that you're currently using character2, so make it CH1
                CH3 = character1 #and make the other character CH3 (having all 3 CHs defined makes sure they are all reset if you try again after losing)
                if character2 == OverlordC or character2 == Overlord:
                    character2.BattlePosition(0, SCREEN_HEIGHT-550)
                elif character2 == HydranoidC or character2 == Hydranoid:
                    character2.BattlePosition(-50, SCREEN_HEIGHT-600)
                else:
                    character2.BattlePosition(0, SCREEN_HEIGHT-500)
                
                #controlling character2's energy while on the field
                if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                    Locked2 = True
                elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                    Locked2 = False
                
                if Locked2 == True:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            
            #controlling the opponent's energy at all times
            if character3.energy < character3.AttackMove.energy_consumption or character3.energy < character3.GuardMove.energy_consumption:
                Locked3 = True
            elif character3.energy > character3.AttackMove.energy_consumption and character3.energy > character3.GuardMove.energy_consumption:
                Locked3 = False
            
            if Locked3 == True:
                character3.movepool = [character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character3.movepool = [character3.AttackMove, character3.GuardMove, character3.RecoverMove]
                make_button(character3.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character3.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character3.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            
            #if one of your characters dies in-battle, stay on the alive one and can no longer switch out
            if character1.health <= 0 and character2.health > 0 and character3.health > 0:
                char1 = False
                no_switch = True
            elif character1.health > 0 and character2.health <= 0 and character3.health > 0:
                char1 = True
                no_switch = True
                
            #losing
            elif character1.health <= 0 and character2.health <= 0 and character3.health > 0:
                print('You lost! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again3'
            
            #winning
            elif character3.health <= 0:
                print('You won! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                battle_ON, scene = False, 'try_again3'
            
        pygame.display.flip()

def CustomBattle3(character1,character2,character3,character4,background,background2,battle_name,music):
    '''
    3v1 custom battles
    '''
    global Locked1, Locked2, Locked3, Locked4, battle_ON, CH1, CH2, CH3, CH4, BACKGROUND, BACKGROUND2, ZE_BATTLE, MUSIC, pause, scene
    
    CH1 = character1
    CH2 = character4
    CH3 = character2
    CH4 = character3
    BACKGROUND = background
    BACKGROUND2 = background2
    ZE_BATTLE = battle_name
    MUSIC = music
    char1, char2, char3 = True, False, False #we need 3 char variables for this one...
    no_switch, no_switch2, no_switch3 = False, False, False #and also 3 no_switch's
    
    #during the battle
    while battle_ON:
        for event in pygame.event.get():
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
                if event.key == pygame.K_r:
                    print()
                    pygame.mixer.music.stop()
                    battle_ON, scene = False, 'try_again3'
                if event.key == pygame.K_a: #press a to switch to character1
                    if no_switch == False:
                        char1,char2,char3 = True,False,False
                if event.key == pygame.K_s: #press s to switch to character2
                    if no_switch2 == False:
                        char1,char2,char3 = False,True,False
                if event.key == pygame.K_d: #press d to switch to character3
                    if no_switch3 == False:
                        char1,char2,char3 = False,False,True
                        
            if char1:
                screen.blit(background,(0, 0))
                
                CH1 = character1 #if using the first fighter, make it CH1 for the other battle functions
                CH3 = character2 #and make the other 2 fighters CH3 and CH4
                CH4 = character3
                if (character1 == OverlordC or character1 == Overlord) and character4 not in [Overlord,Hydranoid,OverlordC,HydranoidC]:
                    character1.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Overlord or character4 == OverlordC) and character1 not in [Overlord,OverlordC,HydranoidC,Hydranoid]:
                    character1.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character1 == OverlordC or character1 == Overlord) and (character4 == Overlord or character4 == OverlordC):
                    character1.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character1 == HydranoidC or character1 == Hydranoid) and character4 not in [Hydranoid,HydranoidC,Overlord,OverlordC]:
                    character1.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Hydranoid or character4 == HydranoidC) and character1 not in [HydranoidC,Hydranoid,Overlord,OverlordC]:
                    character1.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character1 == HydranoidC or character1 == Hydranoid) and (character4 == Hydranoid or character4 == HydranoidC):
                    character1.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character1 == HydranoidC or character1 == Hydranoid) and (character4 == Overlord or character4 == OverlordC):
                    character1.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character1 == OverlordC or character1 == Overlord) and (character4 == HydranoidC or character4 == Hydranoid):
                    character1.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                else:
                    character1.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character1's energy while on the field
                if character1.energy < character1.AttackMove.energy_consumption or character1.energy < character1.GuardMove.energy_consumption:
                    Locked1 = True
                elif character1.energy > character1.AttackMove.energy_consumption and character1.energy > character1.GuardMove.energy_consumption:
                    Locked1 = False
                
                if Locked1 == True:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character1.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character1.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character1.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
                
            if char2:
                screen.blit(background,(0, 0))
                
                CH1 = character2 #char2 = True means that you're currently using character2, so make it CH1
                CH3 = character1 #and make the other 2 fighters CH3 and CH4
                CH4 = character3
                if (character2 == OverlordC or character2 == Overlord) and character4 not in [Overlord,Hydranoid,OverlordC,HydranoidC]:
                    character2.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Overlord or character4 == OverlordC) and character2 not in [Overlord,OverlordC,HydranoidC,Hydranoid]:
                    character2.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character2 == OverlordC or character2 == Overlord) and (character4 == Overlord or character4 == OverlordC):
                    character2.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character2 == HydranoidC or character2 == Hydranoid) and character4 not in [Hydranoid,HydranoidC,Overlord,OverlordC]:
                    character2.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Hydranoid or character4 == HydranoidC) and character2 not in [HydranoidC,Hydranoid,Overlord,OverlordC]:
                    character2.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character2 == HydranoidC or character2 == Hydranoid) and (character4 == Hydranoid or character4 == HydranoidC):
                    character2.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character2 == HydranoidC or character2 == Hydranoid) and (character4 == Overlord or character4 == OverlordC):
                    character2.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character2 == OverlordC or character2 == Overlord) and (character4 == HydranoidC or character4 == Hydranoid):
                    character2.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                else:
                    character2.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character2's energy while on the field
                if character2.energy < character2.AttackMove.energy_consumption or character2.energy < character2.GuardMove.energy_consumption:
                    Locked2 = True
                elif character2.energy > character2.AttackMove.energy_consumption and character2.energy > character2.GuardMove.energy_consumption:
                    Locked2 = False
                
                if Locked2 == True:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character2.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character2.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character2.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover) 
            
            if char3:
                screen.blit(background2,(0, 0)) #change to second world background if character3 (Akobos in laboratory vs dream world grass plain with others)
                
                CH1 = character3
                CH3 = character1 
                CH4 = character2
                if (character3 == OverlordC or character3 == Overlord) and character4 not in [Overlord,Hydranoid,OverlordC,HydranoidC]:
                    character3.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Overlord or character4 == OverlordC) and character3 not in [Overlord,OverlordC,HydranoidC,Hydranoid]:
                    character3.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character3 == OverlordC or character3 == Overlord) and (character4 == Overlord or character4 == OverlordC):
                    character3.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character3 == HydranoidC or character3 == Hydranoid) and character4 not in [Hydranoid,HydranoidC,Overlord,OverlordC]:
                    character3.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                elif (character4 == Hydranoid or character4 == HydranoidC) and character3 not in [HydranoidC,Hydranoid,Overlord,OverlordC]:
                    character3.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character3 == HydranoidC or character3 == Hydranoid) and (character4 == Hydranoid or character4 == HydranoidC):
                    character3.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                elif (character3 == HydranoidC or character3 == Hydranoid) and (character4 == Overlord or character4 == OverlordC):
                    character3.BattlePosition(0, SCREEN_HEIGHT-650)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-550)
                elif (character3 == OverlordC or character3 == Overlord) and (character4 == HydranoidC or character4 == Hydranoid):
                    character3.BattlePosition(0, SCREEN_HEIGHT-550)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-650)
                else:
                    character3.BattlePosition(0, SCREEN_HEIGHT-500)
                    character4.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
                
                #controlling character3's energy while on the field
                if character3.energy < character3.AttackMove.energy_consumption or character3.energy < character3.GuardMove.energy_consumption:
                    Locked3 = True
                elif character3.energy > character3.AttackMove.energy_consumption and character3.energy > character3.GuardMove.energy_consumption:
                    Locked3 = False
                
                if Locked3 == True:
                    make_button(character3.AttackMove.name,'Corbel',15,white,100,600,100,70,black,black,'battle','Nope')
                    make_button(character3.GuardMove.name,'Corbel',15,white,250,600,100,70,black,black,'battle','Nope')
                    make_button(character3.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
                    make_text('USE RECOVER!',"comicsansms",100,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                else:
                    make_button(character3.AttackMove.name,'Corbel',15,white,100,600,100,70,red,pale_red,'battle',Attack)
                    make_button(character3.GuardMove.name,'Corbel',15,white,250,600,100,70,green,pale_green,'battle',Guard)
                    make_button(character3.RecoverMove.name,'Corbel',15,GREEN,400,600,100,70,yellow,pale_yellow,'battle',Recover)
            
            #controlling the opponent's energy at all times
            if character4.energy < character4.AttackMove.energy_consumption or character4.energy < character4.GuardMove.energy_consumption:
                Locked4 = True
            elif character4.energy > character4.AttackMove.energy_consumption and character4.energy > character4.GuardMove.energy_consumption:
                Locked4 = False
            
            if Locked4 == True:
                character4.movepool = [character4.RecoverMove]
                make_button(character4.AttackMove.name,'Corbel',15,white,700,600,100,70,black,black,'battle',None)
                make_button(character4.GuardMove.name,'Corbel',15,white,850,600,100,70,black,black,'battle',None)
                make_button(character4.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            else:
                character4.movepool = [character4.AttackMove, character4.GuardMove, character4.RecoverMove]
                make_button(character4.AttackMove.name,'Corbel',15,white,700,600,100,70,red,pale_red,'battle',None)
                make_button(character4.GuardMove.name,'Corbel',15,white,850,600,100,70,green,pale_green,'battle',None)
                make_button(character4.RecoverMove.name,'Corbel',15,GREEN,1000,600,100,70,yellow,pale_yellow,'battle',None)
            
            #if one of your characters dies in-battle, stay on the alive ones and can no longer switch out to dead one
            if character1.health <= 0:
                char1 = False
                no_switch = True
            if character2.health <= 0:
                char2 = False
                no_switch2 = True
            if character3.health <= 0:
                char3 = False
                no_switch3 = True
             
            if no_switch and character2.health <= 0:
                char3 = True
            elif no_switch and character2.health > 0: #the if not/else of the no_switch's elifs are to make sure characters do not overlap
                if not char3:
                    char2 = True
                else:
                    char3 = True
            if no_switch2 and character3.health <= 0:
                char1 = True
            elif no_switch2 and character3.health > 0:
                if not char1:
                    char3 = True
                else:
                    char1 = True
            if no_switch3 and character1.health <= 0:
                char2 = True
            elif no_switch3 and character1.health > 0:
                if not char2:
                    char1 = True
                else:
                    char2 = True
            
            #losing
            if character1.health <= 0 and character2.health <= 0 and character3.health <= 0 and character4.health > 0:
                print('You lost! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleLost,'sound')
                battle_ON, scene = False, 'try_again3'
            
            #winning
            elif character4.health <= 0:
                print('You won! Wanna try again with new or same characters, or stop for now?')
                print()
                pygame.mixer.music.stop()
                playMusic(BattleWon,'sound')
                battle_ON, scene = False, 'try_again3'
                
        pygame.display.flip()

#final functions: the credits! when all episodes are beaten
def Credits():
    '''
    the credits!!! (not animated, though...) when the story is completed
    '''
    global scene, rollcall
    while rollcall:
        #black background
        screen.fill(blue)
        #the end (big)
        make_text('THE END','arialblack',60,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2-150)
        #names of the creators and collaborators and thank players
        make_text('THANK YOU FOR PLAYING!!!','arialblack',75,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        make_text('Made by:','arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+150)
        make_text('LordZagger (Story, OST, Rulebook, Coding+Debugging)','arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+200)
        make_text('Jin4843 (Drawings, Rulebook, Coding, Test)','arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+250)
        #to quit the credits and go back to menu, press 1, where custom battle and boss rush should now be available
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    rollcall = False
                    scene = 'start_menu'
                if event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
            
        pygame.display.flip()

def Credits2():
    '''
    credits after beating Battle Rush mode (at that point, all buttons except custom battle are blue, indicating they were completed)
    '''
    global scene, rollcall2
    while rollcall2:
        #black background
        screen.fill(red)
        #congratulate players
        make_text('THANK YOU FOR PLAYING!!!','arialblack',75,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2-150)
        make_text('Congrats on beating Boss Rush!','arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        make_text("You have 100% Exceedra's Awakening!",'arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+100)
        make_text("At this point... try Custom Battles! Have fun!",'arialblack',40,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+150)
        #to quit the credits and go back to menu, press 1, where boss rush mode is now blue, and all other buttons are blue except custom battle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    rollcall2 = False
                    scene = 'start_menu'
                if event.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
            
        pygame.display.flip()


#main while loop of the game, that takes all the variables and functions defined above
#to run the whole game smoothly
while True:
    #ok, one last new variable... get mouse position, continuously, while playing
    mouse = pygame.mouse.get_pos()
    #if the player quits, or to move along with the dialogue and story,
    #and do story-battle transitions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if battle_ON == False:
                if event.key == pygame.K_RETURN: #press return to keep going with the dialogue, handles story to battle transitions
                    if scene == "scene_1" and dialogue_index < len(scene_1_dialogue):
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 38:
                            pygame.mixer.music.stop()
                            playMusic(ExceedraLonelyTheme1,'music',True)
                        elif dialogue_index >= len(scene_1_dialogue):
                            pygame.mixer.music.stop()
                            scene = "scene_2"
                            dialogue_index = 0
                            playMusic(LibraryTheme,'music',True)
                            
                    elif scene == "scene_2" and dialogue_index != 22:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 22:
                            pygame.mixer.music.stop()
                            battle_ON, scene = True, 'battle_e1_s2'  # Trigger battle and get out of dialogue
                            playMusic(BattleTheme1,'music',True)
                        elif dialogue_index == 33:
                            pygame.mixer.stop()
                            pygame.mixer.music.stop()
                            playMusic(ExceedraLonelyTheme2,'music',True)
                        elif dialogue_index >= len(scene_2_dialogue):
                            pygame.mixer.music.stop()
                            ExceedraMain.reset()
                            Hydranoid.reset()
                            scene = "scene_3"
                            dialogue_index = 0
                            playMusic(LibraryTheme,'music',True)
                            
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
                            dialogue_index = 0
                            playMusic(DowntownTheme,'music',True)
                            
                    elif scene == "scene_4" and dialogue_index != 18:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 5:
                            pygame.mixer.music.stop()
                            playMusic(AkobosAppears,'music',True)
                        elif dialogue_index == 18:
                            pygame.mixer.music.stop()
                            battle_ON, scene = True, 'battle_e1_s4'  # Trigger battle and get out of dialogue
                            playMusic(AkobosBattle,'music',True)
                        elif dialogue_index >= len(scene_4_dialogue):
                            pygame.mixer.stop()
                            pygame.mixer.music.stop()
                            ExceedraMain.reset()
                            HydranoidC.reset()
                            Akobos.reset()
                            scene = "scene_5"
                            dialogue_index = 0
                            
                    elif scene == "scene_5" and dialogue_index != 37:
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        if dialogue_index == 32:
                            pygame.mixer.music.stop()
                            playMusic(NightmareAppears,'music',True)
                        elif dialogue_index == 37:
                            pygame.mixer.music.stop()
                            pygame.time.delay(100)
                            playMusic(NightmareScream,'sound')
                            battle_ON, scene = True, 'battle_e1_s5'  # Trigger battle and get out of dialogue
                            wait()
                            playMusic(NightmareBattle,'music',True)
                        elif dialogue_index == 41:
                            pygame.mixer.stop()
                            pygame.mixer.music.stop()
                            playMusic(NightmareDying,'music',True)
                        elif dialogue_index == 48:
                            pygame.mixer.music.stop()
                            ExceedraMain.reset()
                            Nightmare.reset()   
                            wait(NightmareDeath)
                        elif dialogue_index >= len(scene_5_dialogue):
                            Episode1_completed = True
                            Game_completed = True #TEMPORARY SO PLAYERS CAN TRY OUT CUSTOM BATTLE AND BOSS RUSH MODES (EARLY)
                            scene = "start_menu"
                            dialogue_index = 0
                    
                    elif scene == 'scene_6': #{TO UPDATE}
                        dialogue_index += 1
                        playMusic(press_button_sound,'sound')
                        pass
                    
                if event.key == pygame.K_BACKSPACE:  # On Backspace key
                    if dialogue_index > 0:
                        playMusic(press_button_sound,'sound')
                        if (scene == 'scene_2' and dialogue_index == 23) or (scene == 'scene_4' and dialogue_index == 19) or (scene == 'scene_5' and dialogue_index == 38): #{TO UPDATE}
                            dialogue_index += 0
                        else:
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
            if event.key == pygame.K_1 and scene == 'scene_6':
                pygame.mixer.music.stop()
                dialogue_index = 0
                scene = 'start_menu'
    
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
        if dialogue_index != 22:
            screen.blit(school, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            Destiny.BattlePosition(300,200)
            Hydranoid.BattlePosition(400,100)
            dialogueBox(scene_2_dialogue)
            if dialogue_index == 24: #wait for BattleWon to finish playing
                wait()
    
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
        if dialogue_index >= 22: #setting or character placement changes from now on have the below format
            screen.blit(school, (0, 0))
            ExceedraMain.BattlePosition(100, 200)
            Hydranoid.BattlePosition(20,100)
            dialogueBox(scene_3_dialogue)
    
    #episode 1, scene 4
    elif scene == "scene_4":
        screen.blit(hill, (0, 0))
        dialogueBox(scene_4_dialogue)
        if 5 <= dialogue_index < 8:
            screen.blit(hill, (0, 0))
            Akobos.BattlePosition(SCREEN_WIDTH-600, SCREEN_HEIGHT-500)
            dialogueBox(scene_4_dialogue)
        if 8 <= dialogue_index < 10:
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
            if dialogue_index == 20:
                wait()
    
    #battle in episode 1, scene 4: Exceedra VS Akobos
    elif scene == 'battle_e1_s4':
        Battle2Chars(ExceedraMain,HydranoidC,Akobos,hill,'battle_e1_s4',AkobosBattle)
    
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
            if dialogue_index == 39:
                wait()
    
    #battle in episode 1, scene 5: Exceedra VS Nightmare
    elif scene == 'battle_e1_s5':
        Battle(ExceedraMain,Nightmare,dreamspace,'battle_e1_s5',NightmareBattle)
            
    #{TO UPDATE ALL BELOW}
    #episode 2, scene 1 (aka scene 6)
    elif scene == 'scene_6':
        #starting placements
        screen.blit(school, (0,0))
        ExceedraMain.BattlePosition(100, 200)
        Hydranoid.BattlePosition(400,100)
        make_text('EPISODE 2 WILL BE READY SOON! :)',"comicsansms",65,white,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    
    #credits when the game is completed (after Game_completed is made True)
    elif scene == 'credits':
        rollcall = True
        Credits()
    
    #secret credits after 100% completing (aka beating the story and battle rush mode)
    elif scene == 'credits2':
        rollcall2 = True
        Credits2()
    
    elif scene == 'b1':
        if CH1 == '' and CH2 == '':
            score = 0
            battle_ON = True
            playMusic(BattleTheme1,'music',True)
            BattleRush(ExceedraMain,Hydranoid,background_list[0],'b1',musicRush_list[0])
        else:
            score = 0
            resetAll()
            battle_ON = True
            playMusic(BattleTheme1,'music',True)
            BattleRush(ExceedraMain,Hydranoid,background_list[0],'b1',musicRush_list[0])
    elif scene == 'b2':
        score += 1
        battle_ON = True
        BattleRush2(ExceedraMain,HydranoidC,Akobos,background_list[1],'b2',musicRush_list[1])
    elif scene == 'b3':
        score += 1
        Akobos.reset()
        battle_ON = True
        BattleRush(ExceedraMain,Nightmare,background_list[2],'b3',musicRush_list[2])
    elif scene == 'b4':
        score += 1
        Nightmare.reset()
        battle_ON = True
        BattleRush(HydranoidC,Hunter,background_list[3],'b4',musicRush_list[3])
    elif scene == 'b5':
        score += 1
        Hunter.reset()
        battle_ON = True
        BattleRush(Destiny,Akobos,background_list[4],'b5',musicRush_list[4])
    elif scene == 'b6':
        score += 1
        Akobos.reset()
        battle_ON = True
        BattleRush(ExceedraDark1,Overlord,background_list[5],'b6',musicRush_list[5])
    elif scene == 'b7':
        score += 1
        Overlord.reset()
        battle_ON = True
        BattleRush(ExceedraDark2,Abby,background_list[6],'b7',musicRush_list[6])
    elif scene == 'b8':
        score += 1
        battle_ON = True
        BattleRush(ExceedraDark2,Kyra,background_list[7],'b8',musicRush_list[7])
    elif scene == 'b9':
        score += 1
        Kyra.reset()
        battle_ON = True
        BattleRush(ExceedraDark2,Destiny,background_list[8],'b9',musicRush_list[8])
    elif scene == 'b10.1':
        score += 1/3
        battle_ON = True
        BattleRush(ExceedraDark2,Overlord,background_list[9],'b10.1',musicRush_list[9])
    elif scene == 'b10.2':
        score += 1/3
        battle_ON = True
        BattleRush(ExceedraDark2,OverlordSoul,background_list[10],'b10.2',musicRush_list[10])
    elif scene == 'b10.3':
        score += 1/3
        battle_ON = True
        BattleRush(ExceedraDark2,OroborusTermina,background_list[11],'b10.3',musicRush_list[11])
    elif scene == 'b11':
        score += 1
        OroborusTermina.reset()
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,Monster1,background_list[12],'b11',musicRush_list[12])
    elif scene == 'b12':
        score += 1
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,Monster2,background_list[13],'b12',musicRush_list[13])
    elif scene == 'b13.1':
        score += 1/4
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,Akobos,background_list[14],'b13.1',musicRush_list[14])
    elif scene == 'b13.2':
        score += 1/4
        Destiny.reset()
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,Nightmare,background_list[15],'b13.2',musicRush_list[15])
    elif scene == 'b13.3':
        score += 1/4
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,Hunter,background_list[16],'b13.3',musicRush_list[16])
    elif scene == 'b13.4':
        score += 1/4
        battle_ON = True
        BattleRush2(ExceedraDark2,Kyra,OroborusTermina,background_list[17],'b13.4',musicRush_list[17])
    elif scene == 'b14.1':
        score += 1
        battle_ON = True
        BattleRush3(ExceedraDark2,Kyra,AkobosC,AI,background_list[18],background_list[6],'b14.1',musicRush_list[18])
    elif scene == 'b14.2':
        score += 1/2
        battle_ON = True
        BattleRush3(ExceedraDark2,Kyra,AkobosC,AI,background_list[19],background_list[6],'b14.2',musicRush_list[19])

    #custom battle mode
    elif scene == 'choose':
        b1v1, b2v1, b3v1 = False, False, False
        picking = True
        chooseYourBattle()
    elif scene == 'choose2':
        resetAll()
        CH1 = NullPerson
        CH2 = NullPerson
        CH3 = NullPerson
        CH4 = NullPerson
        choosing = True
        chooseYourCharacter()
    elif scene == 'choose3':
        BACKGROUND = ''
        BACKGROUND2 = ''
        deciding = True
        chooseYourBackgrounds()
    elif scene == 'choose4':
        MUSIC = ''
        selecting = True
        chooseYourMusic()
    elif scene == '0a':
        CustomBattle(CH1,CH2,BACKGROUND,ZE_BATTLE,MUSIC)
    elif scene == '0b':
        CustomBattle2(CH1,CH2,CH3,BACKGROUND,ZE_BATTLE,MUSIC)
    elif scene == '0c':
        CustomBattle3(CH1,CH2,CH3,CH4,BACKGROUND,BACKGROUND2,ZE_BATTLE,MUSIC)
    
    #try agains
    elif scene == 'try_again1':
        try_again()
    elif scene == 'try_again2':
        try_again2()
    elif scene == 'try_again3':
        try_again2(False)
         
    #updates the display whenever needed
    #(WE LOVE U DISPLAY.FLIP(), THANK YOU FOR MAKING TRANSITIONS POSSIBLE!!!, AND FOR SOMEHOW WORKING EVERY TIME U NEED TO
    #EVEN THOUGH YOU'RE ONLY CALLED ONLY THIS ONE TIME IN THE MAIN LOOP!)
    pygame.display.flip()
