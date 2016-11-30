import pygame
import time
import random
import string
import math

# Initializing all modules in pygame
pygame.init()

# screen object referrring to real screen, next giving game a name
screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
pygame.display.set_caption('Catch your type!!')

screen_width, screen_height = screen.get_size()

Bucket_height = 78
Bucket_width = 90
ballon_radius = 30
ballon_speed = 3 
font_size = 15

small_font = pygame.font.SysFont("purisa",  font_size)
med_font = pygame.font.SysFont("purisa",  font_size*2)
large_font = pygame.font.SysFont("purisa",  int(font_size*3.5))
alpha = string.lowercase[:26]

clock = pygame.time.Clock()
FPS = 100 


#colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 105, 0)
android  = (0, 255, 87)
gold = (255, 215, 0)
light_Silver = (230, 230, 230)
light_green = (0, 255, 0)
blue = (17, 22, 181)


run = True
gameOver = False
score = 0
highscore = 0

scorecard = pygame.image.load('scorecard.png')
#scoreSymbol = pygame.image.load('scoreSymbol.png')
#scoreSymbol2 = pygame.image.load('arrowRight.png')
Bucket = pygame.image.load('Bucket.jpg')

DataTypes = ["int", "float", "string", "char"]
ballon_coord = [2*i for i in range( int(math.ceil(screen_width/(2*ballon_radius))) )]
ballon_coord = ballon_coord[1:-1]
ballon_info = []
selected_Data_Type = ''


def text_Button(msg, color, buttonx, buttony, buttonwidth, buttonheight):
	
	textSurface = small_font.render(msg, True, color)
	textRect = textSurface.get_rect()
	textRect.center = buttonx + buttonwidth/2, buttony + buttonheight/2
	screen.blit(textSurface, textRect)

def Button(msg, color, x, y, width, height, inactive_color, active_color):

	pointerPos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if pointerPos[0] > x and pointerPos[0] < (x+width) and pointerPos[1] > y and pointerPos[1] < y+height:
		pygame.draw.rect(screen, active_color, (x, y, width, height))
		if click[0] == 1:
			return True
	else:
		pygame.draw.rect(screen, inactive_color, (x, y, width, height))

	text_Button(msg, color, x, y, width, height)
	pygame.display.update()

	return False

def Generate_ballon():

	x = random.randrange(0, len(ballon_coord))
	dataType = random.randrange(0, len(DataTypes))
	data = 0

	if DataTypes[dataType] == "int":
		data = random.randrange(0, 100)
	elif DataTypes[dataType] == "float":
		data = random.randrange(0, 100)*1.0

	elif DataTypes[dataType] == "char":
		data = alpha[random.randrange(0, 26)]
	
	elif DataTypes[dataType] == "string":
		data = ''
		r = random.randrange(2, 5)
		for i in range(r):
			data += alpha[random.randrange(0, 26)]

	return [DataTypes[dataType], ballon_coord[x]*ballon_radius, 0, data]


def Draw_ballons(ballon_info):

	for ballon in ballon_info:
		pygame.draw.circle(screen, black, (ballon[1], ballon[2]), ballon_radius, 2)
		display_message_for_data_type(str(ballon[-1]), black, ballon[1], ballon[2], "med")

def Check_catching(ballon_info, x_cord, y_cord):

	for ballon in ballon_info:
		if ( x_cord <= ballon[1] and ballon[1] <= x_cord + Bucket_width ) and ( ballon[2] >= screen_height- Bucket_height and ballon[2] <= screen_height):
			if ballon[0] == selected_Data_Type:
				return [1, ballon_info.index(ballon)]
			else:
				return [-2, -2] # Implying Game Over!!

	return [-1, -1] 

def display_message_for_data_type(msg, color, x, y, size="small"):
	
	if size == "small":
		textSurface = small_font.render(msg, True, color)
	elif size == "med":
		textSurface = med_font.render(msg, True, color)
	if size == "large":
		textSurface = large_font.render(msg, True, color)

	textRect = textSurface.get_rect()
	textRect.center = x, y
	screen.blit(textSurface, textRect)

def display_message(msg, color, y_displace = 0, size="small"):
	
	if size == "small":
		textSurface = small_font.render(msg, True, color)
	elif size == "med":
		textSurface = med_font.render(msg, True, color)
	if size == "large":
		textSurface = large_font.render(msg, True, color)

	textRect = textSurface.get_rect()
	textRect.center = screen_width/2, screen_height/2 + y_displace
	screen.blit(textSurface, textRect)

def is_Game_Over(ballon_info):

	for ballon in ballon_info:
		if ballon[2] + ballon_radius >= screen_height:
			if ballon[0] == selected_Data_Type:
				return True
	return False

def pause():

	screen.fill(white)
	display_message("Paused", black, -100, "large")
	display_message("Press Space to Resume, q to Quit", black, 40, "med")
	pygame.display.update()

	while 1:
		for events in pygame.event.get():
			if events.type == pygame.QUIT:
				return False

			if events.type == pygame.KEYDOWN:
				if events.key == pygame.K_SPACE:
					return True
				elif events.key == pygame.K_q:
					return False


def introduction_Screen():

	global gameOver
	global highscore
	global score
	global selected_Data_Type

	run = True
	gameOver = False
	ballon_info = []

	score = 0
	filee = open('Highscore.txt')
	highscore = filee.read()
	filee.close()
	

	screen.fill(white)
	display_message("CATCH YOUR TYPE", blue, -170, "large")
	display_message("Catch only specified Data Types .", black, -50, "med")
	display_message("Do not catch other Data Types. ", black, 10, "med")
	display_message("Press Spcae-Bar to pause the game", black, 70, "med")
	display_message("Choose any Data Type to continue !!", black, 130, "med")
	
	screen.blit(scorecard, (screen_width/2 - 150, 10))
	#screen.blit(scoreSymbol, (screen_width/2 - 150, 0))
	#screen.blit(scoreSymbol2, (screen_width/2 + 110, 0))

	display_message(("HighScore: " + str(highscore)), black, -350, "med")
	pygame.display.update()


	intro = True
	while intro:
		for events in pygame.event.get():
			
			if events.type == pygame.QUIT:
				intro = False
				return False
				break
	
			isClicked1 = Button("Int", black, int(screen_width*1.0/12), 575, screen_width/6, 50, green, light_green)
			isClicked2 = Button("String", black, int(screen_width*(1.0/12 + 1.0/6 + 1.0/18)), 575, screen_width/6, 50, green, light_green)
			isClicked3 = Button("Float", black, int(screen_width*(1.0/12 + 2.0/6+ 2.0/18)), 575, screen_width/6, 50, green, light_green)
			isClicked4 = Button("Char", black, int(screen_width*(1.0/12 + 3.0/6 + 3.0/18)), 575, screen_width/6, 50, green, light_green)
	
			if isClicked1 == True:
				selected_Data_Type = "int"
				return start()
			
			elif isClicked2 == True:
				selected_Data_Type = "string"
				return start()
			
			elif isClicked3 == True:
				selected_Data_Type = "float"
				return start()
			
			elif isClicked4 == True:
				selected_Data_Type = "char"
				return start()
				

def start():

	global score
	global highscore
	global gameOver
	global run
	global ballon_info

	score = 0	
	count = 0
	ballon_info = []

	x_cord = (screen_width - Bucket_width) /2
	y_cord = screen_height - Bucket_height
	x_change = 0

	screen.fill(white)
	pygame.display.update()

	run = True
	gameOver = False
	
	while run:

		if gameOver == True:

			time.sleep(1)
			screen.fill(white)
			pygame.display.update()

		
		while gameOver == True:
		
			try:

				display_message("Game Over !!", red, -240, "large")

				filee = open('Highscore_Sainath.txt', 'w')

				if int(score) > int(highscore):
					
					filee.write(str(score))
					display_message("New High Score " + str(score) + " !! Congo !!", green, -180, "med") 
					display_message("Press P to play again, Q to quit", green, -120, "med") 
	
				else:
					filee.write(str(highscore))
					display_message("Your Score :"+str(score), green, -160, "med")
					#display_message("\n\n") 
					display_message("Press P to play again, Q to quit", green, -130, "med") 

				filee.close()
				pygame.display.update()

				for events in pygame.event.get():
					if events.type == pygame.QUIT:
						return False

					if events.type == pygame.KEYDOWN:
						if events.key == pygame.K_p:
							return True

						elif events.key == pygame.K_q:
							return False

			except Exception,e:
				print str(e)
	
		if run == False:
			break

		for events in pygame.event.get():

			if events.type == pygame.QUIT:
				run = False
				return False
				break

			elif events.type == pygame.KEYDOWN:
				if events.key == pygame.K_SPACE:
					resume = pause()
					if resume == False:
						return False
					else:
						screen.fill(white)
						screen.blit(Bucket, (x_cord, y_cord))
						Draw_ballons(ballon_info)
						pygame.display.update()		
						time.sleep(2)
				
			mouse_pos = pygame.mouse.get_pos()
			x_cord = mouse_pos[0]
			
			
		if x_cord < 0:
			x_cord = 0
		elif x_cord + Bucket_width > screen_width:
			x_cord = screen_width - Bucket_width
			

		screen.fill(white)

		#display_message_for_data_type(msg, color, x, y, size="small")
		display_message_for_data_type("Score - "+ str(score), black, screen_width/2, 25, "med")
		screen.blit(Bucket, (x_cord, y_cord))
		
		# Info -> Data Type, x, y
		for ballon in ballon_info:
			ballon[2] += ballon_speed


		if count%100 == 0:
			ballon_info.append( Generate_ballon() )
	
		Draw_ballons(ballon_info)
		pygame.display.update()		

		l = Check_catching(ballon_info, x_cord, y_cord)
		if l[0] == -2:
			gameOver = True
		
		elif l[0] == 1:
			score += 10
			ballon_info.pop(l[1])
		

		if is_Game_Over(ballon_info) == True:
			gameOver = True

		clock.tick(FPS)
		count += 1	

while 1:

	again = introduction_Screen()
	if again == False:
	
		screen.fill(white)
		pygame.display.update()
		display_message("Game Over", red, 0, "large")
		pygame.display.update()
		time.sleep(1)
		break

pygame.quit()
