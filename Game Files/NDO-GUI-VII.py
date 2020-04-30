

import NaDiOhEngineVIII
import pygame



white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

global cardDim
cardDim = (90,110) # The used card dimension

global fieldStudentNames # lists holding names of cards in field
global fieldSpecialNames
global oppStudentNames
global oppSpecialNames
fieldStudentNames = [None]*3 
fieldSpecialNames = [None]*3
oppStudentNames = [None]*3
oppSpecialNames = [None]*3


################################ HELPER FUNCTONS ###################################################

def noneField(field): # Turns all items in a given list to None

	if field == 1:

		for i in range(3):

			fieldStudentNames[i] = None

	elif field == 2:

		for i in range(3):

			fieldSpecialNames[i] = None

	elif field == 3:

		for i in range(3):

			oppStudentNames[i] = None

	elif field == 4:

		for i in range(3):

			oppSpecialNames[i] = None

def addOppCardsToField(): # adding opponent's cards to his fields

	index1 = 0
	index2 = 0

	noneField(3)
	noneField(4)

	for i in NaDiOhEngineVIII.Player2.field.studentField:
		oppStudentNames[index1] = i
		index1 += 1

	for i in NaDiOhEngineVIII.Player2.field.specialField:

		oppSpecialNames[index2] = i
		index2 += 1

def addMyCardsToField(): # Adding my cards in the field

	index1 = 0
	index2 = 0

	noneField(1)
	noneField(2)

	for i in NaDiOhEngineVIII.Player1.field.studentField:

		fieldStudentNames[index1] = i
		index1 += 1

	for i in NaDiOhEngineVIII.Player1.field.specialField:

		fieldSpecialNames[index2] = i
		index2 += 1


### Initializing
pygame.init()
pygame.font.init()


########################### PLAYER 1 DRAWING FUNCTIONS ############################

def drawHand(): # Draws cards in Player 1's hand on screen

	handLocation = [(20,680) , (120,680) , (220,680) ,
					(320,680) , (420,680) , (520,680)]
	
	for i in range(len(NaDiOhEngineVIII.Player1.playerHand)):

		Card = NaDiOhEngineVIII.Player1.playerHand[i]
		image = pygame.image.load(Card.cardImage)

		screen.blit(image,handLocation[i])

def drawStudents(): 

	studentLocation = [(395,420) , (650,420) , (905,420)]
	index = 0


	for i in NaDiOhEngineVIII.Player1.field.studentField:

		Card = NaDiOhEngineVIII.Player1.field.studentField[i]
		image = pygame.image.load(Card.cardImage)

		if Card.position == "Attack":
			screen.blit(image,studentLocation[index])
			index += 1

		elif Card.position == "Defence":
			rotatedImage = pygame.transform.rotate(image,90)
			screen.blit(rotatedImage,studentLocation[index])
			index += 1

		elif Card.position == "Face Down Defence":
			rotatedRect = pygame.transform.rotate(blackRect,90)
			screen.blit(rotatedRect,studentLocation[index])
			index += 1

def drawSpecials():

	specialLocation = [(395,535) , (650,535) , (905,535)]
	index = 0

	for i in NaDiOhEngineVIII.Player1.field.specialField:

		Card = NaDiOhEngineVIII.Player1.field.specialField[i]
		image = pygame.image.load(Card.cardImage)

		if Card.position == "Face Down":
			pygame.draw.rect(screen,black,[specialLocation[index][0],specialLocation[index][1],cardDim[0],cardDim[1]])
			index += 1

		elif Card.position == "Active":
			screen.blit(image,specialLocation[index])
			index += 1

################################## PLAYER 2 DRAWING FUNCTIONS ################################

def drawOppHand():

	oppHandLoc = [(1351,8) , (1254,8) , (1159,8) , (1064,8) , (969,8) , (874,8)]

	for i in range(len(NaDiOhEngineVIII.Player2.playerHand)):

		pygame.draw.rect(screen,black,[oppHandLoc[i][0],oppHandLoc[i][1],cardDim[0],cardDim[1]])

def drawOppStudents():

	oppStudentLoc = [(395,279) , (650,279) , (904,279)]
	index = 0

	for i in NaDiOhEngineVIII.Player2.field.studentField:
		
		Card = NaDiOhEngineVIII.Player2.field.studentField[i]
		image = pygame.image.load(Card.cardImage)

		if Card.position == "Attack":
			screen.blit(image,oppStudentLoc[index])
			index += 1

		elif Card.position == "Defence":
			rotatedImage = pygame.transform.rotate(image,90)
			screen.blit(rotatedImage,oppStudentLoc[index])
			index += 1

		elif Card.position == "Face Down Defence":
			rotatedRect = pygame.transform.rotate(blackRect,90)
			screen.blit(rotatedRect,oppStudentLoc[index])
			index += 1

def drawOppSpecials():

	oppSpecialLoc = [(395,162) , (650,163) , (904,162)]
	index = 0

	for i in NaDiOhEngineVIII.Player2.field.specialField:

		Card = NaDiOhEngineVIII.Player2.field.specialField[i]
		image = pygame.image.load(Card.cardImage)

		if Card.position == "Face Down":
			pygame.draw.rect(screen,black,[oppSpecialLoc[index][0],oppSpecialLoc[index][1],cardDim[0],cardDim[1]])
			index += 1

		elif Card.position == "Active":
			screen.blit(image,oppSpecialLoc[index])
			index += 1

####### GENERAL DRAWING FUNCTIONS #######

def drawHealths():
	
	P1health = NaDiOhEngineVIII.Player1.playerHealth
	P2health = NaDiOhEngineVIII.Player2.playerHealth

	health1 = pygame.font.SysFont('Stencil',35)
	health2 = pygame.font.SysFont('Stencil',35)

	screenHealth1 = health1.render(str(P1health),False,black)
	screenHealth2 = health2.render(str(P2health),False,black)

	screen.blit(screenHealth1,(115,395))
	screen.blit(screenHealth2,(1230,389))

def drawEverything():

	drawHand()
	drawStudents()
	drawSpecials()
	drawOppHand()
	drawOppStudents()
	drawOppSpecials()
	drawHealths()


###################################### GAMELOOP ##########################################

blackRect = pygame.image.load("BlackRect.png") # A black rectangle of dim(90,110)
background = pygame.image.load('Game Layout.png')
instructions = pygame.image.load('Instructions.png')
introscreen = pygame.image.load('Main Menu.png')
screen = pygame.display.set_mode((1450,800))
pygame.display.set_caption('Na-Di-Oh!')
clock = pygame.time.Clock()

### MAIN MENU SCREEN ###
def gameIntro():

	intro = True
	selected = introscreen

	while intro:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				x , y = pygame.mouse.get_pos() # gets (x,y)
				left , middle , right = pygame.mouse.get_pressed() # left == 1 if pressed, etc.

				if selected == introscreen and (555<x<870) and (265<y<315): # if 'PLAY GAME' selected
					intro = False

				elif selected == introscreen and (510<x<935) and (400<y<446): # if 'INSTRUCTIONS' is selected
					selected = instructions

				if selected == introscreen and (1224<x<1420) and (15<y<63): # if 'QUIT :(' is selected 
					pygame.quit()
					quit()

				if selected == instructions and (18<x<99) and (16<y<35): # if '< BACK' is selected
					selected = introscreen

			screen.blit(selected,(0,0))
			pygame.display.flip()

gameIntro()

### GAME SCREEN ###
done = False

command = None
v1 = None
v2 = None

addMyCardsToField()
addOppCardsToField()


while not done:


	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			pygame.quit()
			quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			
			x , y = pygame.mouse.get_pos() # gets (x,y)
			left , middle , right = pygame.mouse.get_pressed() # left == 1 if pressed, etc.
			
			### CLICKING ON HAND OR DECK OR END ###
			if (680 < y < 790): 
				
				if (20 < x < 110): # Clicking on first card

					if command != None and left: # playing card in attack mode
						v2 = 'a'
					elif command != None and right: # playing card in defence mode
						v2 = 'd'

					command = 'p'
					v1 = 'a'

				elif (120 < x < 210): # Clicking on second card

					if command != None and left:
						v2 = 'a'
					elif command != None and right: 
						v2 = 'd'

					command = 'p'
					v1 = 's'

				elif (220 < x < 310): # Clicking on third card

					if command != None and left: 
						v2 = 'a'
					elif command != None and right:
						v2 = 'd'

					command = 'p'
					v1 = 'd'

				elif (320 < x < 410): # Clicking on fourth card

					if command != None and left: 
						v2 = 'a'
					elif command != None and right:
						v2 = 'd'

					command = 'p'
					v1 = 'f'

				elif (420 < x < 510): # Clicking on fifth card

					if command != None and left:
						v2 = 'a'
					elif command != None and right: 
						v2 = 'd'

					command = 'p'
					v1 = 'g'

				elif (520 < x < 610): # Clicking on sixth card

					if command != None and left: 
						v2 = 'a'
					elif command != None and right: 
						v2 = 'd'

					command = 'p'
					v1 = 'h'

				elif (785 < x < 875): # Clicking on deck
					command = 'd'

				elif (1150 < x < 1390): # Clicking on end
					command = 'e'

			### CLICKING ON YOUR SPECIAL FIELD ###
			if (535 < y < 645) and right:

				command = 'c'   # v1 must be the card name

				if (395 < x < 485): # Right-Clicking first special card in your field

					v1 = fieldSpecialNames[0]

				elif (650 < x < 740):

					v1 = fieldSpecialNames[1]

				elif (905 < x < 995):

					v1 = fieldSpecialNames[2]

			### CLICKING ON YOUR STUDENT FIELD ###
			if (420 < y < 530):

				## Changing position
				if (395 < x < 485) and right: # Right-Clicking first student card in your field

					command = 'c'
					v1 = fieldStudentNames[0]

				elif (650 < x < 740) and right:

					command = 'c'
					v1 = fieldStudentNames[1]

				elif (905 < x < 995) and right:

					command = 'c'
					v1 = fieldStudentNames[2]

				## Choosing card to attack with
				if (395 < x < 485) and left:  # First card in student deck

					command = 'a'
					v1 = fieldStudentNames[0]

				elif (650 < x < 740) and left: # Second

					command = 'a'
					v1 = fieldStudentNames[1]

				elif (905 < x < 995) and left: # Third

					command = 'a'
					v1 = fieldStudentNames[2]

			### CLICKING ON OPPONENT'S STUDENT FIELD ###
			if (280 < y < 390):

				if (395 < x < 485): # First opponent student card

					v2 = oppStudentNames[0]

				elif (650 < x < 740): # Second

					v2 = oppStudentNames[1]

				elif (905 < x < 995): # Third

					v2 = oppStudentNames[2]


		### EXECUTING COMMANDS ###
		if NaDiOhEngineVIII.gameLoop(command,v1,v2):
			command = None
			v1 = None
			v2 = None

		addMyCardsToField()
		addOppCardsToField()

		### DRAWING EVERYTHING ###	
		screen.fill(white) 
		screen.blit(background , (0,0))
		drawEverything()
		#Drawing Win message:
		if NaDiOhEngineVIII.Player1.playerHealth <= 0 and NaDiOhEngineVIII.Player2.playerHealth > 0:
			winner = pygame.font.SysFont('Stencil',90)
			winText = winner.render("Player 2 Wins!",False,red)
			screen.blit(winText,(525,300))
		elif NaDiOhEngineVIII.Player2.playerHealth <= 0 and NaDiOhEngineVIII.Player1.playerHealth > 0:
			winner = pygame.font.SysFont('Stencil',90)
			winText = winner.render("Player 1 Wins!",False,red)
			screen.blit(winText,(525,300))
		elif NaDiOhEngineVIII.Player1.playerHealth <= 0 and NaDiOhEngineVIII.Player2.playerHealth <= 0:
			winner = pygame.font.SysFont('Stencil',90)
			winText = winner.render("It's a Draw!",False,red)
			screen.blit(winText,(525,300))
		pygame.display.flip() 

	clock.tick(30)

pygame.quit()
quit()