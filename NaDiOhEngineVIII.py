

import random


################################################## THE CLASSES #######################################################

class Field:

    def __init__(self):

        self.studentField = {} # cardName : Card
        self.specialField = {}

class Player:

    def __init__(self,health,deck,graveyard,hand,current,field):
        
        self.playerHealth = health # value
        self.playerDeck = deck # list of Cards
        self.playerGrave = graveyard # list of Cards
        self.playerHand = hand # list of Cards
        self.currentPlayer = current
        self.field = Field()

class Cards:

    def __init__(self,name,attack,defence,effect,image,cType,manipulated,position):

        self.cardName = name
        self.cardAtk = attack
        self.cardDef = defence
        self.cardEffect = effect
        self.cardImage = image       
        self.cardType = cType # Student or Special
        self.manipulated = manipulated # True/False, for in each phase, you can only manipulate a card once
        self.position = position # Position of card in Field (Attack, Defence, Face Down Defence, Active, Face Down)


################################## HELPER FUNCTIONS ##########################################

def attack(player,opponent,v1,v2): # Does the attacking 
   
    attackerName = v1 # v1 is a name
    if attackerName in player.field.studentField.keys():

        attacker = player.field.studentField[attackerName]
        attacker.manipulated = True
        
        if len(opponent.field.studentField) == 0: # Checking for empty field
            opponent.playerHealth -= attacker.cardAtk
            return True
       
        else:
           
            attackedName = v2
            if attackedName in opponent.field.studentField.keys():
                
                attacked = opponent.field.studentField[attackedName]
                if attacked.position == "Attack":
                   
                    if attacked.cardAtk > attacker.cardAtk:
                        player.playerHealth -= (attacked.cardAtk - attacker.cardAtk) # Remove from health
                        player.playerGrave.append(attacker) # Add Card to Graveyard
                        del player.field.studentField[attackerName] # Remove cardName/Card from field
                        return True
                   
                    elif attacked.cardAtk < attacker.cardAtk:
                        opponent.playerHealth -= (attacker.cardAtk - attacked.cardAtk)
                        opponent.playerGrave.append(attacked)
                        del opponent.field.studentField[attackedName]
                        return True
                   
                    else:
                        player.playerGrave.append(attacker)
                        del player.field.studentField[attackerName]
                        opponent.playerGrave.append(attacked)
                        del opponent.field.studentField[attackedName]
                        return True
                
                elif attacked.position == "Defence" or attacked.position == "Face Down Defence":
                   
                    if attacked.position == "Face Down Defence":
                        attacked.position = "Defence"

                    if attacked.cardDef > attacker.cardAtk:
                        player.playerHealth -= (attacked.cardDef - attacker.cardAtk)
                        player.playerGrave.append(attacker)
                        del player.field.studentField[attackerName]
                        return True

                    elif attacked.cardDef < attacker.cardAtk:
                        opponent.playerGrave.append(attacked)
                        del opponent.field.studentField[attackedName]
                        return True
    return False

def attackValid(player,key): # checks if an attempt to attack a card is valid

    if key in player.field.studentField.keys():

        card = player.field.studentField[key]
        if card.position == "Attack" and card.manipulated == False:
            return True

    return False

def playValid(player,key): # checks if an attempt to play a certain card is valid

    if key in keys: # keys is a global variable (located below)

        cardInHand = keys.index(key) # Gives index of card in hand to be chosen
        if len(player.playerHand) > cardInHand: # Check if chosen card exists in hand

            if player.playerHand[cardInHand].cardType == 'Student':

                if len(player.field.studentField) < 3: # Check if there is space for card in student field
                    return True

            elif player.playerHand[cardInHand].cardType == 'Special':

                if len(player.field.specialField) < 3: # Check if there is space for card in special field
                    return True
    return False

def changeValid(player,key): # Checks if an attempt to change a card position is valid (key is card.cardName)

    if key in player.field.studentField.keys(): # if card is a student

        card = player.field.studentField[key] # card is the Card object with the same name as key
        if card.manipulated == False:
            return True

    elif key in player.field.specialField.keys(): # if card is a special

        card = player.field.specialField[key] # card is the Card object with the same name as key
        if card.manipulated == False:
            return True

    return False


#################################### GAME FUNCTIONS ##################################################

def createHand(): # Creates a hand to give to player

    choices = [] # new list that will have elements removed

    for i in PlayingCards:
        choices.append(i)

    inHand = []

    for i in range(4):
        card = random.choice(choices)
        choices.remove(card) # ensure each card can only be picked once
        inHand.append(card)

    return inHand

def createDeck(hand): # Creates a deck that excludes the hand

    newList = []

    for i in PlayingCards:
        if i not in hand: # making sure cards in hand don't reappear in deck
            newList.append(i)

    newDeck = []

    for i in range(len(PlayingCards)-4):
        card = random.choice(newList)
        newDeck.append(card)
        newList.remove(card)

    return newDeck

def drawCard(player):

    if len(player.playerHand) < 6: # Max Hand is six cards
        card = player.playerDeck[0]
        player.playerHand.append(card)
        player.playerDeck.remove(card)

def attackCard(player,opponent,v1,v2): # see attack()

    key = v1

    if attackValid(player,key):
        return attack(player,opponent,v1,v2)

def changePosition(player,v1):

    key = v1 # key is a card.cardName

    if changeValid(player,key):

        if key in player.field.studentField: # if Card is a student

            card = player.field.studentField[key]

            if card.position == "Attack":
                card.position = "Defence"
                card.manipulated = True

            else:
                card.position = "Attack"
                card.manipulated = True

        else: # if card is a special
            card = player.field.specialField[key]
            card.position = "Active" # Special cards' position can only be changed when they are Face down
            card.manipulated = True
            card.cardEffect()
            del player.field.specialField[card.cardName]

def playCard(player,v1,v2):

    key = v1
    
    global stuplayed
    global speplayed
    global oppplayed

    if playValid(player,key):

        loc = keys.index(key) # index of card in hand
        card = player.playerHand[loc]

        key = v2

        if key == 'a':

            if card.cardType == "Student" and stuplayed == False:
                player.playerHand.remove(card)
                card.manipulated = True
                stuplayed = True
                card.position = "Attack"
                player.field.studentField[card.cardName] = card

            elif card.cardType == "Special" and speplayed == False:
                player.playerHand.remove(card)
                card.manipulated = True
                speplayed = True
                card.position = "Active"
                player.field.specialField[card.cardName] = card
                card.cardEffect()
                del player.field.specialField[card.cardName]

        elif key == 'd':

            if card.cardType == "Student" and stuplayed == False:
                player.playerHand.remove(card)
                card.manipulated = True
                stuplayed = True
                card.position = "Face Down Defence"
                player.field.studentField[card.cardName] = card

            elif card.cardType == "Special" and speplayed == False:
                player.playerHand.remove(card)
                card.manipulated = True
                speplayed = True
                card.position = "Face Down"
                player.field.specialField[card.cardName] = card

        

def endTurn(player,state):

    global stuplayed
    global speplayed

    stuplayed = False # Revert to original state
    speplayed = False

    for i in player.field.studentField: # Change state of manipulation of each card back to False
        player.field.studentField[i].manipulated = False
    for j in player.field.specialField:
        player.field.specialField[j].manipulated = False

    if state == 2: # Switch players if at Attack phase (Ending at Main phase moves on to Attack phase)
        if player == Player1: 
            Player1.currentPlayer = 0
            Player2.currentPlayer = 1
        elif player == Player2:
            Player2.currentPlayer = 0
            Player1.currentPlayer = 1

def deducePlayer():

    if Player1.currentPlayer == 1:
        return (Player1,Player2)
    else:
        return (Player2,Player1)


################################################# SPECIAL CARD EFFECTS ################################

def Confusion(): # IconicSideeg card effect

    Player1.playerHealth = 1
    Player2.playerHealth = 1

def Unamused(): # UnamusedSideeg card effect

    Player1.playerHealth -= 1000
    Player2.playerHealth -= 1000

def Harrass(): # Professor Harras card effect 
    
    Player1.playerHealth += 1000
    Player2.playerHealth += 1000

def Oliver(): # Professor Oliver card effect 

    Player2.playerHealth -= 500

def Saquib(): # Professor Saquib card effect

    Player1.playerHealth += 500

##################################### AI FUNCTIONS ##################################

def checkCards(): # Check for best card to play

    strongestval = 0
    defensestval = 0
    strongest = None
    defensest = None

    for i in Player2.playerHand:

        if i.cardType == "Student":

            if i.cardAtk > strongestval:

                strongestval = i.cardAtk
                strongest = i

            if i.cardDef > defensestval:

                defensestval = i.cardDef
                defensest = i

    if defensestval > strongestval:

        return (defensest , 'd')

    else:

        return (strongest , 'a')

    return (None , None)

def doAIstuff():

    global oppplayed

    drawCard(Player2)

    ## Choosing card to play by choosing card with highest atk/def
    attackestCard = None
    defensestCard = None
    attackestName = None
    defensestName = None
    defval = 0
    atkval = 0
    for i in Player2.playerHand:
        if i.cardType == 'Student' and i.cardAtk > atkval:
            attackestCard = i
            attackestName = i.cardName
            atkval = i.cardAtk
        elif i.cardType == 'Student' and i.cardAtk > defval:
            defensestCard = i
            defensestName = i.cardName
            defval = i.cardDef

    ## Playing card
    if defval > atkval and defensestCard != None:
        Player2.playerHand.remove(defensestCard)
        defensestCard.manipulated = True
        oppplayed = True
        defensestCard.position = "Defence"
        Player2.field.studentField[defensestName] = defensestCard
    elif attackestCard != None:
        Player2.playerHand.remove(attackestCard)
        attackestCard.manipulated = True
        oppplayed = True
        attackestCard.position = "Attack"
        Player2.field.studentField[attackestName] = attackestCard

    ## Attacking
    for i in Player2.field.studentField:
        c2 = None
        c1 = Player2.field.studentField[i] 
        if len(Player1.field.studentField.keys()) > 0:
            c2 = Player1.field.studentField.keys()[0]
            if Player1.field.studentField[c2].cardAtk < i.cardAtk: # Attacks only if attacked card has lower atk value
                attackCard(Player2,Player1,c1.cardName,c2)         # than attacking card

    ## Ending turn 
    oppplayed = False       
    Player2.currentPlayer = 0
    Player1.currentPlayer = 1



################################### OBJECTS ###################################

PlayingCards = [ Cards('Samar',2500,500,None,'Samar.jpg','Student',False,None),
                 Cards('Nadim',600,2000,None,'Nadim.jpg','Student',False,None),
                 Cards('SinisterSideeg',1200,1000,None,'SinisterSideeg.jpg','Student',False,None),
                 Cards('Omar',1300,1000,None,'OB.jpeg','Student',False,None),
                 Cards('Andria',1300,767,None,'Andrea.jpg','Student',False,None),
                 Cards('Yusuf',1600,800,None,'Yusuf.jpg','Student',False,None),
                 Cards('Djordje',2000,0,None,'Djordje.jpg','Student',False,None),
                 Cards('Ammar',1400,1000,None,'Ammar.jpg','Student',False,None),
                 Cards('Waad',1200,1600,None,'Waad.jpeg','Student',False,None),
                 Cards('SHRESTHA',1400,700,None,'SHRESTHA.jpg','Student',False,None),
                 Cards('Sakir',1100,1500,None,'Sakir.jpg','Student',False,None),
                 Cards('Syed',1000,500,None,'Syed.jpg','Student',False,None),
                 Cards('Hao',1800,2500,None,'Hao.jpg','Student',False,None),
                 Cards('Yousef',2000,0,None,'Khanfara.jpg','Student',False,None),
                 Cards('Hanif',1600,1500,None,'Hanif.jpg','Student',False,None),
                 Cards('Stefan',1700,1100,None,'Stefan.jpg','Student',False,None),
                 Cards('Bouthaina',1500,1500,None,'Bathbooth.jpg','Student',False,None),
                 Cards('Mubarak',1900,1400,None,'MSNaimi.jpg','Student',False,None), 
                 Cards('Asra',900,1600,None,'Asratchet.jpg','Student',False,None), 
                 Cards('RoyalSideeg',2000,500,None,'RoyalSideeg.jpg','Student',False,None),
                 Cards('SmokeySideeg',1700,1900,None,'SmokeySideeg.jpg','Student',False,None),

                 Cards('ProfHarras',None,None,Harrass,'ProfHarras.jpg','Special',False,None),
                 Cards('ProfSaquib',None,None,Saquib,'ProfSaquib.jpg','Special',False,None),
                 Cards('ProfOliver',None,None,Oliver,'ProfOliver.jpg','Special',False,None),
                 Cards('IconicSideeg',None,None,Confusion,'IconicSideeg.jpg','Special',False,None), 
                 Cards('UnamusedSideeg',None,None,Unamused,'UnamusedSideeg.jpg','Special',False,None)   ] # name,attack,defence,effect,image,cType,manipulated,position


### Player Initializations ###
hand1 = createHand()
hand2 = createHand()
deck1 = createDeck(hand1)
deck2 = createDeck(hand2)

field1 = Field() 
field2 = Field() 

Player1 = Player(4000,deck1,[],hand1,1,field1) # Health, Deck, Grave, Hand, Current, Field
Player2 = Player(4000,deck2,[],hand2,0,field2)


### STATE VARIABLES ##
global keys
keys = ['a','s','d','f','g','h'] # used in playValid() 
stuplayed = False
speplayed = False
oppplayed = False
state = 0 # 0 for Draw phase, 1 for Main, 2 for Attack
inGame = True

############################# GAMELOOP #######################################

def gameLoop(command,v1=None,v2=None):

    player = deducePlayer()[0]
    opponent = deducePlayer()[1]
    key = command 

    global inGame
    global state
    global speplayed
    global stuplayed
    global oppplayed

    if inGame:

        if player.playerHealth <= 0: # Checking win conditions
            inGame = False
            print str(opponent) + " wins!"
        if opponent.playerHealth <= 0:
            inGame = False
            print str(player) + " wins!"

        ### DRAW PHASE ###
        if state == 0:

            if len(player.playerDeck) == 0: # Checking win condition
                inGame = False
                print str(opponent) + " wins!"

            elif key == 'd':
                drawCard(player)
                state = 1
                return True

        ### MAIN PHASE ###
        elif state == 1:

            if key == 'p' and v1 != None and v2 != None:

                playCard(player,v1,v2) 
                return True

            elif key == 'c' and v1 != None:

                changePosition(player,v1) 
                return True

            elif key == 'e':

                endTurn(player,1)
                state = 2
                return True

        ### ATTACK PHASE ###
        elif state == 2:

            if key == 'a' and v1 != None and v2 != None: # v2 could be None in the case that there are no students on opponent field

                if attackCard(player,opponent,v1,v2):

                    if player.playerHealth <= 0: # Checking win conditions
                        inGame = False
                        print str(opponent) + " wins!"
                    if opponent.playerHealth <= 0:
                        inGame = False
                        print str(player) + " wins!"

                    return True

            elif key == 'e':

                endTurn(player,2)
                state = 0
                doAIstuff() 
                return True

    else:

        print "Game is over."

    return False