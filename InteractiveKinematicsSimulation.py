import pygame, random, math, os, sys #sys isnt technically required

panel = 325
WIDTH = 1200 + panel
HEIGHT = 800

current_path = os.path.dirname(__file__)
resource_path = os.path.join(current_path, 'resources')

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#BACKGROUND/HELPINFO
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background = pygame.transform.scale(pygame.image.load(os.path.join(resource_path, "background.png")).convert_alpha(), (round((WIDTH - panel) * (.5 * (math.sqrt(100)) + .5)), round(HEIGHT * (.5 * (math.sqrt(100)) + .5))))
background_rect = background.get_rect(bottomleft = (0, HEIGHT))
helpicon = pygame.transform.scale(pygame.image.load(os.path.join(resource_path, "help icon.png")).convert_alpha(), (25, 25))
helpicon_rect = helpicon.get_rect(topright = (WIDTH - 10, 10))
helpinfo = pygame.transform.rotozoom(pygame.image.load(os.path.join(resource_path, "help info.png")), 0, .9)
helpinfo_rect = helpinfo.get_rect(center = (round(WIDTH / 2), round(HEIGHT / 2)))
helpinfo_page = False
xbutton = pygame.image.load(os.path.join(resource_path, "x.png")).convert_alpha()
xbutton_rect = xbutton.get_rect(topright = (helpinfo_rect[0] + helpinfo_rect.width - 10, helpinfo_rect[1] + 10))

#CURSOR
pygame.mouse.set_visible(False)
cursor_point = pygame.image.load(os.path.join(resource_path, "cursor.png")).convert_alpha()
cursor_scroll = pygame.image.load(os.path.join(resource_path, "scroll.png")).convert_alpha()
cursor_select = pygame.image.load(os.path.join(resource_path, "select.png")).convert_alpha()
cursor_block = pygame.image.load(os.path.join(resource_path, "block.png")).convert_alpha()
cursor_state = cursor_point
cursor_rect = cursor_state.get_rect(topright = (0, 0))
editable_text_object = []

#TEXT FONT
text = pygame.font.Font("CallingCode-Regular.ttf", 45)
text_medium = pygame.font.Font("CallingCode-Regular.ttf", 34)
text_small = pygame.font.Font("CallingCode-Regular.ttf", 20)
text_micro = pygame.font.Font("CallingCode-Regular.ttf", 15)

#INITIAL STATES
mouse_state = False
mouse_click_pos = (0, 0)
moving = False
editing = False

#CUBE
cube_surface = pygame.image.load(os.path.join(resource_path, "wood box.png")).convert()
cubes = []

#SETTING VARIABLES
conversion = 100 #pixel per meters
gravity = -9.8
increment_option = (1, 1, 7)
increment = .01
time = True

def cursor_draw(cursor_state, cursor_rect): #TIMES_RECT = time bool
	if editable_text_object != None:
		editable_text_setting.extend(editable_text_object)

	for texts in editable_text_setting:#CHECKS CURSOR ON ANY EDITABLE TEXT BOX
		if mousepos[0] >= texts[0] and mousepos[0] <= (texts[0] + texts.width) and mousepos[1] >= texts[1] and mousepos[1] <= (texts[1] + texts.height):
			if pygame.Rect(texts) == scale_rect or pygame.Rect(texts) == gravitys_rect or pygame.Rect(texts) == mass_rect or pygame.Rect(texts) == time_rect or pygame.Rect(texts) == positionx_rect or pygame.Rect(texts) == positiony_rect or pygame.Rect(texts) == velocityx_rect or pygame.Rect(texts) == velocityy_rect or pygame.Rect(texts) == accelerationx_rect or pygame.Rect(texts) == accelerationy_rect:
				cursor_state = cursor_scroll
				if time == True:
					cursor_state = cursor_block

			elif pygame.Rect(texts) == times_rect or pygame.Rect(texts) == helpicon_rect:
				cursor_state = cursor_select

			else:
				cursor_state = cursor_point

			if pygame.Rect(texts) == xbutton_rect and helpinfo_page == True:
				cursor_state = cursor_select

	for cube in cubes:
		if mousepos[0] >= cube.x_f * conversion and mousepos[0] <= ((cube.x_f * conversion) + cube.width) and mousepos[1] >= HEIGHT - (cube.y_f * conversion) and mousepos[1] <= ((HEIGHT - (cube.y_f * conversion)) + cube.height):
			cursor_state = cursor_select

	if mousepos[0] >= (WIDTH - panel + 13) and mousepos[0] <= (WIDTH - panel + 27) and mousepos[1] >= (125 - 7) and mousepos[1] <= (165 + 7):
		cursor_state = cursor_select

	if editing == False and mousepos[0] >= (WIDTH - panel) and mousepos[1] >= 180:
		cursor_state = cursor_point

	cursor_rect = cursor_state.get_rect(topleft = (mousepos[0], mousepos[1]))
	screen.blit(cursor_state, cursor_rect)

def details_display():#DISPLAYS DETAILS ON BOTTOM PANEL
	detail_title = text_medium.render(("Details"), True, BLACK)
	detail_title_rect = detail_title.get_rect(center = (round(WIDTH - panel / 2), 630)) #RIGHT CLICK TO EDIT, SPACE TO SPAWN

	detail1 = text_micro.render(("◦no air resistance"), True, BLACK)
	detail1_rect = detail1.get_rect(topleft = (round(WIDTH - panel + 5), 650))

	detail2 = text_micro.render(("◦no friction"), True, BLACK)
	detail2_rect = detail2.get_rect(topleft = (round(WIDTH - panel + 5), 675))

	detail3 = text_micro.render(("◦no object collision"), True, BLACK)
	detail3_rect = detail3.get_rect(topleft = (round(WIDTH - panel + 5), 700))

	detail4 = text_micro.render(("◦SPACE to spawn box"), True, BLACK)
	detail4_rect = detail4.get_rect(topleft = (round(WIDTH - panel + 5), 725))

	detail5 = text_micro.render(("◦L_SHIFT to switch time state"), True, BLACK)
	detail5_rect = detail4.get_rect(topleft = (round(WIDTH - panel + 5), 750))

	screen.blit(detail_title, detail_title_rect)
	screen.blit(detail1, detail1_rect)
	screen.blit(detail2, detail2_rect)
	screen.blit(detail3, detail3_rect)
	screen.blit(detail5, detail5_rect)
	screen.blit(detail4, detail4_rect)
	screen.blit(detail5, detail5_rect)

def settings_panel_edit_select(increment, time, helpinfo_page):
	global increment_option
	if mouse_state[0] == 1:
		if mouse_click_pos[0] >= (WIDTH - panel + 13) and mouse_click_pos[0] <= (WIDTH - panel + 27):
			if mouse_click_pos[1] >= (125 - 7) and mouse_click_pos[1] <= (125 + 7):
				increment = 1
				increment_option = (7, 1, 1)
			if mouse_click_pos[1] >= (145 - 7) and mouse_click_pos[1] <= (145 + 7):
				increment = 0.1
				increment_option = (1, 7, 1)
			if mouse_click_pos[1] >= (165 - 7) and mouse_click_pos[1] <= (165 + 7):
				increment = 0.01
				increment_option = (1, 1, 7)

		elif mouse_click_pos[0] >= times_rect[0] and mouse_click_pos[0] <= (times_rect[0] + times_rect.width) and mouse_click_pos[1] >= times_rect[1] and mouse_click_pos[1] <= (times_rect[1] + times_rect.height):
			if time == False:
				time = True
			else:
				time = False

		elif mouse_click_pos[0] >= helpicon_rect[0] and mouse_click_pos[0] <= (helpicon_rect[0] + helpicon_rect.width) and mouse_click_pos[1] >= helpicon_rect[1] and mouse_click_pos[1] <= (helpicon_rect[1] + helpicon_rect.height):
			helpinfo_page = True
		if helpinfo_page == True:
			if mouse_click_pos[0] >= xbutton_rect[0] and mouse_click_pos[0] <= (xbutton_rect[0] + xbutton_rect.width) and mouse_click_pos[1] >= xbutton_rect[1] and mouse_click_pos[1] <= (xbutton_rect[1] + xbutton_rect.height):
				helpinfo_page = False
	return increment, time, helpinfo_page

def helpinfo_display():#DISPLAYS IMPORTED IMG PNG FILE
	pygame.draw.rect(screen, WHITE, (helpinfo_rect[0] - 10, helpinfo_rect[1] - 10, helpinfo_rect.width + 20, helpinfo_rect.height + 20))
	screen.blit(helpinfo, helpinfo_rect)
	screen.blit(xbutton, xbutton_rect)

def settings_panel_edit_scroll(sign, conversion, gravity, background, background_rect):
	if mousepos[0] >= scale_rect[0] and mousepos[0] <= (scale_rect[0] + scale_rect.width) and mousepos[1] >= scale_rect[1] and mousepos[1] <= (scale_rect[1] + scale_rect.height):
		if (conversion + (sign * increment)) >= 1 and (conversion + (sign * increment)) <= 100:
			conversion = round(conversion + (sign * increment), 2)#CHANGES VALUE OF SCALE/CONVERSION
			background = pygame.transform.scale(pygame.image.load("background.png").convert_alpha(), (round((WIDTH - panel) * (.5 * (math.sqrt(conversion)) + .5)), round(HEIGHT * (.5 * (math.sqrt(conversion)) + .5))))
			background_rect = background.get_rect(bottomleft = (0, HEIGHT))#CHANGES BACKGROUND SIZE BASED ON SCALE/CONVERSION
			for cube in cubes:
				Cube.scale_adjust(cube)

	if mousepos[0] >= gravitys_rect[0] and mousepos[0] <= (gravitys_rect[0] + gravitys_rect.width) and mousepos[1] >= gravitys_rect[1] and mousepos[1] <= (gravitys_rect[1] + gravitys_rect.height):
		gravity = round(gravity + (sign * increment), 2)#CHANGES GRAVITY VALUE
	return conversion, gravity, background, background_rect

def setting_panel_display():#DISPLAYS SETTING INFO ON TOP PANEL
	settings = text.render(("Settings "), True, WHITE)
	settings_rect = settings.get_rect(center = (round(WIDTH - panel/2), 50))

	scale = text_small.render(("scale:" + str(conversion)), True, WHITE)
	scale_rect = scale.get_rect(topright = (round(WIDTH - 10), 150))

	gravitys = text_small.render(("gravity:" + str(gravity)) + "m/s^2", True, WHITE)
	gravitys_rect = gravitys.get_rect(topright = (WIDTH - 10, 120))

	increments = text_small.render(("increment:" + str(increment)), True, WHITE)
	increments_rect = increments.get_rect(topleft = (WIDTH - panel + 10, 90))
	increments_1 = text_small.render("1", True, WHITE)
	increments_1_rect = increments_1.get_rect(topleft = (WIDTH - panel + 35, 112))
	increments_01 = text_small.render("0.1", True, WHITE)
	increments_01_rect = increments_01.get_rect(topleft = (WIDTH - panel + 35, 132))
	increments_001 = text_small.render("0.01", True, WHITE)
	increments_001_rect = increments_001.get_rect(topleft = (WIDTH - panel + 35, 152))
	pygame.draw.circle(screen, WHITE, (WIDTH - panel + 20, 125), 7, increment_option[0])
	pygame.draw.circle(screen, WHITE, (WIDTH - panel + 20, 145), 7, increment_option[1])
	pygame.draw.circle(screen, WHITE, (WIDTH - panel + 20, 165), 7, increment_option[2])

	times = text_small.render(("time:" + str(time)), True, WHITE)
	times_rect = times.get_rect(topright = (round(WIDTH - 10), 90))

	pygame.draw.rect(screen, WHITE, (WIDTH - panel, 210, panel, 5))
	pygame.draw.rect(screen, WHITE, (WIDTH - panel, 550, panel, 5))
	pygame.draw.rect(screen, WHITE, (WIDTH - panel - 5, 0, 5, HEIGHT))

	screen.blit(settings, settings_rect)
	screen.blit(scale, scale_rect)
	screen.blit(gravitys, gravitys_rect)
	screen.blit(increments, increments_rect)
	screen.blit(increments_1, increments_1_rect)
	screen.blit(increments_01, increments_01_rect)
	screen.blit(increments_001, increments_001_rect)
	screen.blit(times, times_rect)
	editable_text_setting = [scale_rect, gravitys_rect, times_rect, helpicon_rect, xbutton_rect]
	return settings_rect, scale_rect, gravitys_rect, increments_rect, times_rect, editable_text_setting

class Cube:
	def __init__(self, x, y):
		self.x_i = x / conversion
		self.y_i = (HEIGHT / conversion) - (y / conversion)
		self.x_f = self.x_i 
		self.y_f = self.y_i
		self.vi_x = 0
		self.vi_y = 0
		self.vf_x = self.vi_x
		self.vf_y = self.vf_x
		self.a_x = 0
		self.a_y = gravity
		self.speed = round(math.sqrt((self.vf_x * self.vf_x) + (self.vf_y * self.vf_y)), 2)
		self.t = 0
		self.width = 20
		self.height = 20
		self.mass = ((self.width / conversion) * (self.height / conversion))
		self.surface = pygame.transform.scale(cube_surface, (round(self.width), round(self.height)))

		#TEMP VARIABLES
		self.move_check = False
		self.edit_checkT = False

#_____________________________________________________________________________________________________

	def time_change(self, sign):#CHANGES TIME FROM EDIT PANEL
		if time == False:
			self.t = round(self.t + (sign * increment), 2)
			Cube.kinematics(self)

	def scale_adjust(self):#ADJUST CUBE SIZE BASED ON MASS AND CONVERSION/SCALE
		self.width = round(math.sqrt(self.mass) * conversion)
		self.height = round(math.sqrt(self.mass) * conversion)
		self.surface = pygame.transform.scale(cube_surface, (self.width, self.height))
		self.rect = self.surface.get_rect(topleft = (round(self.x_f), round(self.y_f)))

	def move(self, moving): #CHECKING IF OBJECT IS BEING MOVED/DRAGGED
		if self.move_check == False and mouse_state[0] == 1 and moving == False:
			if mousepos[0] >= self.x_f * conversion and mousepos[0] <= ((self.x_f * conversion) + self.width) and mousepos[1] >= HEIGHT - (self.y_f * conversion) and mousepos[1] <= ((HEIGHT - (self.y_f * conversion)) + self.height):
				self.move_check = True
				moving = True

		if self.move_check == True: #CONVERTING PIXELS TO METERS
			self.x_f = mousepos[0] / conversion
			self.y_f = (HEIGHT / conversion) - (mousepos[1] / conversion)
			self.x_i = self.x_f
			self.y_i = self.y_f
			self.t = 0
		return moving

	def edit_check(self, editing, *mouse_click_position):
		if self.edit_checkT == False and mouse_state[2] == 1 and editing == False: #EDIT CHECK
			if mousepos[0] >= self.x_f * conversion and mousepos[0] <= ((self.x_f * conversion) + self.width) and mousepos[1] >= HEIGHT - (self.y_f * conversion) and mousepos[1] <= ((HEIGHT - (self.y_f * conversion)) + self.height):
				self.edit_checkT = True
				editing = True

		if self.edit_checkT == True:#EXIT EDIT CHECK
			if len(mouse_click_position) > 0:
				if mouse_click_position[0] < self.x_f or mouse_click_position[0] > (self.x_f + self.width) or mouse_click_position[1] < self.y_f or mouse_click_position[1] > (self.y_f + self.height):#CHECK:NO CLICK ON OBJECT
					if mouse_click_position[0] < (WIDTH - panel): #CHECK:NO CLICK ON PANEL
						self.edit_checkT = False
						editing = False
		return editing

	def edit_panel_edit(self, sign):
		if self.edit_checkT == True:
			if mousepos[0] >= mass_rect[0] and mousepos[0] <= (mass_rect[0] + mass_rect.width) and mousepos[1] >= mass_rect[1] and mousepos[1] <= (mass_rect[1] + mass_rect.height):
				if round(self.mass + (sign * increment), 2) > 0:
					self.mass = round(self.mass + (sign * increment), 2)
					Cube.scale_adjust(self)
			elif mousepos[0] >= time_rect[0] and mousepos[0] <= (time_rect[0] + time_rect.width) and mousepos[1] >= time_rect[1] and mousepos[1] <= (time_rect[1] + time_rect.height):
				self.t = round(self.t + (sign * increment), 2)
			elif mousepos[0] >= positionx_rect[0] and mousepos[0] <= (positionx_rect[0] + positionx_rect.width) and mousepos[1] >= positionx_rect[1] and mousepos[1] <= (positionx_rect[1] + positionx_rect.height):
				self.x_i = round(self.x_i + (sign * increment), 2) + (round(.5 * self.a_x * self.t * self.t, 2))
				self.y_i = self.y_f
				self.vi_x = self.vf_x
				self.vi_y = self.vf_y
				self.t = 0
			elif mousepos[0] >= positiony_rect[0] and mousepos[0] <= (positiony_rect[0] + positiony_rect.width) and mousepos[1] >= positiony_rect[1] and mousepos[1] <= (positiony_rect[1] + positiony_rect.height):
				self.y_i = round(self.y_i + (sign * increment), 2) + (round(.5 * self.a_y * self.t * self.t, 2))
				self.x_i = self.x_f
				self.vi_x = self.vf_x
				self.vi_y = self.vf_y
				self.t = 0
			elif mousepos[0] >= velocityx_rect[0] and mousepos[0] <= (velocityx_rect[0] + velocityx_rect.width) and mousepos[1] >= velocityx_rect[1] and mousepos[1] <= (velocityx_rect[1] + velocityx_rect.height):
				self.vi_x = round(self.vf_x + (sign * increment), 2)
				self.vf_x = self.vi_x
				self.vi_y = self.vf_y
				self.x_i = self.x_f
				self.y_i = self.y_f
				self.t = 0
			elif mousepos[0] >= velocityy_rect[0] and mousepos[0] <= (velocityy_rect[0] + velocityy_rect.width) and mousepos[1] >= velocityy_rect[1] and mousepos[1] <= (velocityy_rect[1] + velocityy_rect.height):
				self.vi_y = round(self.vf_y + (sign * increment), 2)
				self.vf_y = self.vi_y
				self.vi_x = self.vf_x
				self.x_i = (self.x_f)
				self.y_i = self.y_f
				self.t = 0

			elif mousepos[0] >= accelerationx_rect[0] and mousepos[0] <= (accelerationx_rect[0] + accelerationx_rect.width) and mousepos[1] >= accelerationx_rect[1] and mousepos[1] <= (accelerationx_rect[1] + accelerationx_rect.height):
				self.a_x = round(self.a_x + (sign * increment), 2)
				self.x_i = self.x_f
				self.y_i = self.y_f
				self.vi_x = self.vf_x
				self.vi_y = self.vf_y
				self.t = 0

			elif mousepos[0] >= accelerationy_rect[0] and mousepos[0] <= (accelerationy_rect[0] + accelerationy_rect.width) and mousepos[1] >= accelerationy_rect[1] and mousepos[1] <= (accelerationy_rect[1] + accelerationy_rect.height):
				self.a_y = round(self.a_y + (sign * increment), 2)
				self.x_i = self.x_f
				self.y_i = self.y_f
				self.vi_x = self.vf_x
				self.vi_y = self.vf_y
				self.t = 0

	def edit_panel_display(self):
		global title_rect, mass_rect, time_rect, position_title_rect, positionx_rect, positiony_rect, velocity_title_rect, velocityx_rect, velocityy_rect, speed_rect, acceleration_title_rect, accelerationx_rect, accelerationy_rect
		if self.edit_checkT == True:
			title = text_medium.render(("Wooden Box"), True, WHITE)
			title_rect = title.get_rect(center = (round(WIDTH - panel/2), 240))

			mass = text_small.render(("Mass:" + str(round(self.mass, 2)) + "Kg"), True, WHITE)
			mass_rect = mass.get_rect(topleft = (round(WIDTH - panel + 10), 270))

			time = text_small.render(("Time:" + str(round(self.t, 2)) + "s"), True, WHITE)
			time_rect = time.get_rect(topright = (round(WIDTH - 10), 270))

			position_title = text_medium.render("Position", True, WHITE)
			position_title_rect = position_title.get_rect(center = (round(WIDTH - panel/2), 310))

			positionx = text_small.render(("x:" + str(round(self.x_f, 2)) + "m"), True, WHITE)
			positionx_rect = positionx.get_rect(topleft = (round(WIDTH - panel + 10), 330))

			positiony = text_small.render(("y:"  + str(round(self.y_f, 2)) + "m"), True, WHITE)
			positiony_rect = positiony.get_rect(topright = (round(WIDTH -10), 330))

			velocity_title = text_medium.render("Velocity", True, WHITE)
			velocity_title_rect = velocity_title.get_rect(center = (round(WIDTH - panel/2), 380))

			velocityx = text_small.render(("Vx:" + str(round(self.vf_x, 2)) + "m/s"), True, WHITE)
			velocityx_rect = velocityx.get_rect(topleft = (round(WIDTH - panel + 10), 400))

			velocityy = text_small.render(("Vy:" + str(round(self.vf_y, 2)) + "m/s"), True, WHITE)
			velocityy_rect = velocityy.get_rect(topleft = (round(WIDTH - panel + 10), 430))

			speed = text_small.render(("Speed:" + str(round(self.speed, 2)) + "m/s"), True, WHITE)
			speed_rect = speed.get_rect(topright = (round(WIDTH - 10), 400))

			acceleration_title = text_medium.render("Acceleration", True, WHITE)
			acceleration_title_rect = acceleration_title.get_rect(center = (round(WIDTH - panel/2), 480))

			accelerationx = text_small.render(("Ax:" + str(round(self.a_x, 2)) + "m/s^s"), True, WHITE)
			accelerationx_rect = accelerationx.get_rect(topleft = (round(WIDTH - panel + 10), 500))

			accelerationy = text_small.render(("Ay:" + str(round(self.a_y, 2)) + "m/s^s"), True, WHITE)
			accelerationy_rect = accelerationy.get_rect(topright = (round(WIDTH - 10), 500))

			screen.blit(title, title_rect)
			screen.blit(mass, mass_rect)
			screen.blit(time, time_rect)
			screen.blit(position_title, position_title_rect)
			screen.blit(positionx, positionx_rect)
			screen.blit(positiony, positiony_rect)
			screen.blit(velocity_title, velocity_title_rect)
			screen.blit(velocityx, velocityx_rect)
			screen.blit(velocityy, velocityy_rect)
			screen.blit(speed, speed_rect)
			screen.blit(acceleration_title, acceleration_title_rect)
			screen.blit(accelerationx, accelerationx_rect)
			screen.blit(accelerationy, accelerationy_rect)
		editable_text_object = [mass_rect, time_rect, positionx_rect, positiony_rect, velocityx_rect, velocityy_rect, speed_rect, accelerationx_rect, accelerationy_rect]
		return editable_text_object

#_____________________________________________________________________________________________________
	
	def time_update(self):#UPDATES EACH CUBE'S TIME
		self.t = round(self.t + .01, 2)
	
	def kinematics(self):#UPDATES EACH CUBE'S POSITION/VELOCITY BASED ON THEIR TIME
		self.x_f = self.x_i + (self.vi_x * self.t) + (0.5 * self.a_x * self.t * self.t)
		self.y_f = self.y_i + (self.vi_y * self.t) + (0.5 * self.a_y * self.t * self.t)
		self.vf_x = self.vi_x + (self.a_x * self.t)
		self.vf_y = self.vi_y + (self.a_y * self.t)

		self.speed = round(math.sqrt((self.vf_x * self.vf_x) + (self.vf_y * self.vf_y)), 2)

	def void(self):#CHECKS CUBE OUTSIDE SCREEN TO THE LEFT/BOTTOM TO DELETE IT
		global editing

		if self.x_f < 0 or self.y_f < 0:
			if self.edit_checkT == True:
				editing = False
				self.edit_checkT = False

			cubes.remove(self)
			return cubes #RETURNS LIST 
		return cubes
	
	def draw(self): #CONVERTS METERS TO PIXELS: meter * pixels/meters = pixels
		screen.blit(self.surface, (round(self.x_f * conversion), round(HEIGHT - (self.y_f * conversion))))

#INITAL SUMMON
cubes.append(Cube(WIDTH / 2, HEIGHT / 2))
editing = True
for cube in cubes:
	cube.edit_checkT = True

while True:
	mousepos = pygame.mouse.get_pos()
	mouse_state = pygame.mouse.get_pressed()

	for cube in cubes:
		print(cube.width, cube.height)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_state = pygame.mouse.get_pressed()
			mouse_click_pos = pygame.mouse.get_pos()
			increment, time, helpinfo_page = settings_panel_edit_select(increment, time, helpinfo_page)
			for cube in cubes:
				editing = Cube.edit_check(cube, editing, mouse_click_pos[0], mouse_click_pos[1])

			if time == False:
				if event.button == 4:
					conversion, gravity, background, background_rect = settings_panel_edit_scroll(1, conversion, gravity, background, background_rect)
					for cube in cubes:
						Cube.edit_panel_edit(cube, 1)
					
				elif event.button == 5:
					conversion, gravity, background, background_rect = settings_panel_edit_scroll(-1, conversion, gravity, background, background_rect)
					for cube in cubes:
						Cube.edit_panel_edit(cube, -1)

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_state = pygame.mouse.get_pressed()
			if mouse_state[0] == 0 and mouse_state[2] == 0:
				for cube in cubes:
					cube.move_check = False #RESET TEMP VARIABLE
		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_SPACE and len(cubes) <= 15:
				cubes.append(Cube(mousepos[0], mousepos[1]))

			if event.key == pygame.K_LSHIFT:
				if time == True:
					time = False
				else:
					time = True

			if event.key == pygame.K_RIGHT:
				for cube in cubes:
					Cube.time_change(cube , 1)
			if event.key == pygame.K_LEFT:
				for cube in cubes:
					Cube.time_change(cube, -1)

	#MOUSE
	if mouse_state[0] == 0:
		moving = False

	#BACKGROUND
	screen.blit(background, background_rect)

	#CUBE
	if len(cubes) > 0:
		for cube in cubes:
			cubes = Cube.void(cube)
			if time == False:
				editing = Cube.edit_check(cube, editing)
				moving = Cube.move(cube, moving)
			else:
				Cube.time_update(cube)
			Cube.kinematics(cube)
			Cube.draw(cube)

	#PANEL
	pygame.draw.rect(screen, (180, 220, 255), (WIDTH - panel, 0, panel, HEIGHT))

	#SETTINGS PANEL
	settings_rect, scale_rect, gravitys_rect, increments_rect, times_rect, editable_text_setting = setting_panel_display()

	#EDIT PANEL INFO DISPLAY
	if editing == True:
		for cube in cubes:
			editable_text_object = Cube.edit_panel_display(cube)

	#DETAILS PANEL
	details_display()
	screen.blit(helpicon, helpicon_rect) #HELPICON

	#HELP INFO
	if helpinfo_page == True:
		helpinfo_display()

	#MOUSE CURSOR
	cursor_draw(cursor_state, cursor_rect)

	#TIME
	clock.tick(100)

	pygame.display.update()