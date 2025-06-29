# SyncSpin

import random
import pygame
import os

from objects import Balls, Coins, Tiles, Particle, Message, Button
from level_menager import levels
from shapes import draw_background_path

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption('SyncSpin')

clock = pygame.time.Clock()
FPS = 90

# COLORS **********************************************************************

RED = (255,0,0)
GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
YELLOW = (254,221,0)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (25, 25, 25)

color_list = [PURPLE, GREEN, BLUE, ORANGE, YELLOW, RED]
color_index = 0
color = color_list[color_index]

# SOUNDS **********************************************************************

flip_fx = pygame.mixer.Sound('Sounds/flip.mp3')
score_fx = pygame.mixer.Sound('Sounds/point.mp3')
dead_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/bgm.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
score_font = "Fonts/DroneflyRegular-K78LA.ttf"
game_over_font = "Fonts/ghostclan.ttf"
final_score_font = "Fonts/DalelandsUncialBold-82zA.ttf"
new_high_font = "Fonts/BubblegumSans-Regular.ttf"

syncspin = Message(WIDTH // 2, 120, 55, "SyncSpin", title_font, WHITE, win)
score_msg = Message(WIDTH//2, 100, 60, "0", score_font, (150, 150, 150), win)
game_msg = Message(80, 120, 40, "GAME", game_over_font, BLACK, win)
over_msg = Message(210, 120, 40, "OVER!", game_over_font, WHITE, win)
final_score = Message(WIDTH//2, HEIGHT//2 - 40, 90, "0", final_score_font, RED, win)
new_high_msg = Message(WIDTH//2, HEIGHT//2 + 20, 20, "New High", None, GREEN, win)

# Button images

home_img = pygame.image.load('Assets/homeBtn.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")
lock_icon = pygame.image.load("Assets/lock_icon.png")
lock_icon = pygame.transform.scale(lock_icon, (20, 20))

# Buttons

home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, HEIGHT//2 + 150)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT//2 + 150)
play_btn = Button(pygame.Surface((100, 40)), (100, 40), WIDTH//2 - 50, HEIGHT//2 + 120)
play_btn.image.fill((50, 200, 50))
font_btn = pygame.font.Font("Fonts/Aladin-Regular.ttf", 24)
play_text = font_btn.render("Play", True, WHITE)

next_level_btn = Button(pygame.Surface((80, 30)), (80, 30), WIDTH // 2 - 90, HEIGHT // 2 + 60)
retry_btn = Button(pygame.Surface((80, 30)), (80, 30), WIDTH // 2 + 10, HEIGHT // 2 + 60)

next_level_btn.image.fill((0, 200, 0))
retry_btn.image.fill((200, 0, 0))

font_btn = pygame.font.Font("Fonts/ghostclan.ttf", 20)
next_level_text = font_btn.render("Next", True, WHITE)
retry_text = font_btn.render("Retry", True, WHITE)
back_level_btn = Button(pygame.Surface((80, 30)), (80, 30), WIDTH // 2 - 90, HEIGHT // 2 + 60)
back_level_btn.image.fill(YELLOW)
back_level_text = font_btn.render("Back", True, WHITE)

try_again_msg = Message(WIDTH // 4 + 17, HEIGHT // 2 + 73, 15, "Let's try again", None, YELLOW, win)

#Levels

level_buttons = []
rows, cols = 5, 4
button_width, button_height = 40, 30
margin_x, margin_y = 20, 30

total_width = cols * button_width + (cols - 1) * margin_x
start_x = (WIDTH - total_width) // 2

total_height = rows * button_height + (rows - 1) * margin_y
start_y = (HEIGHT - total_height) // 2 + 10

level_img = pygame.Surface((button_width, button_height))
level_img.fill((100, 100, 100))

highest_unlocked = 1
progress_file = "progress.txt"
if os.path.exists(progress_file):
	try:
		with open(progress_file) as f:
			content = f.read().strip()
			if content.isdigit():
				highest_unlocked = max(1, int(content))
	except:
		pass
else:
	highest_unlocked = 1

for i in range(20):
	col = i % cols
	row = i // cols
	x = start_x + col * (button_width + margin_x)
	y = start_y + row * (button_height + margin_y)
	color = color_list[i % len(color_list)]
	level_img = pygame.Surface((button_width, button_height))
	level_img.fill(color)
	btn = Button(level_img, (button_width, button_height), x, y)
	btn.enabled = (i + 1 <= highest_unlocked)
	level_buttons.append((btn, i+1))

# Groups **********************************************************************

RADIUS = 70
ball_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

ball = Balls((CENTER[0], CENTER[1]+RADIUS), RADIUS, 90, win)
ball_group.add(ball)
ball = Balls((CENTER[0], CENTER[1]-RADIUS), RADIUS, 270, win)
ball_group.add(ball)

# TIME ************************************************************************

start_time = pygame.time.get_ticks()
current_time = 0
coin_delta = 850
tile_delta = 2000

# VARIABLES *******************************************************************

clicked = False
new_coin = True
num_clicks = 0

player_alive = True
sound_on = True

running = True

selected_level = None
lives_left = 3
score = 0
highscore = 0

show_intro_page = True
show_level_page = False
home_page = False
game_page = False
score_page = False


passed_levels = []

while running:
	win.fill(GRAY)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			if not clicked:
				clicked = True
				for ball in ball_group:
					ball.dtheta *= -1
					flip_fx.play()

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0

					color = color_list[color_index]

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			clicked = False

	if home_page:
		syncspin.update()

		if selected_level:
			background_shape_name = selected_level.shape
		else:
			background_shape_name = "circle"  # Default форма за home_page

		draw_background_path(win, background_shape_name, RADIUS, CENTER, 15, BLACK)
		ball_group.update(color)

		for btn, level_num in level_buttons:
			if btn.draw(win):
				selected_level = levels[level_num - 1]

				ball_group.empty()
				for i in range(selected_level.num_balls):
					angle = 90 if i == 0 else 270
					ball = Balls(CENTER, RADIUS, angle, win, shape=selected_level.shape)
					ball_group.add(ball)

				home_page = False
				game_page = True
				lives_left = selected_level.lives
				score = 0
			btn.enabled = False

	if show_intro_page:
		preview_level = levels[11]  # 12-ти левел (индекс 11)
		draw_background_path(win, preview_level.shape, RADIUS, CENTER, 15, BLACK)

		# Креирање на preview топчиња (само ако ги нема веќе)
		if 'preview_balls' not in globals():
			preview_balls = pygame.sprite.Group()
			for i in range(preview_level.num_balls):
				angle = 90 if i == 0 else 270
				ball = Balls(CENTER, RADIUS, angle, win, shape=preview_level.shape)
				preview_balls.add(ball)

		# Ажурирај движење на preview топчињата
		preview_balls.update(color)

		syncspin.update()
		win.blit(play_text, (play_btn.rect.x + 20, play_btn.rect.y + 5))
		for btn, _ in level_buttons:
			btn.enabled = True
		if play_btn.draw(win):
			show_intro_page = False
			show_level_page = True

			with open("progress.txt") as f:
				highest_unlocked = int(f.read().strip())

			for i, (btn, level_num) in enumerate(level_buttons):
				btn.clicked = False
				btn.enabled = (level_num <= highest_unlocked)

			preview_balls.empty()
			del preview_balls

		text_rect = play_text.get_rect(center=play_btn.rect.center)
		win.blit(play_text, text_rect)

	elif show_level_page:
		font = pygame.font.Font("Fonts/DalelandsUncialBold-82zA.ttf", 18)
		title_font_obj = pygame.font.Font("Fonts/DalelandsUncialBold-82zA.ttf", 26)
		title_text = title_font_obj.render("Select Level", True, WHITE)
		title_rect = title_text.get_rect(center=(WIDTH // 2, 60))
		win.blit(title_text, title_rect)
		overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
		overlay.fill((50, 50, 50, 150))
		for btn, level_num in level_buttons:
			win.blit(overlay, btn.rect.topleft)
			if btn.enabled:
				if btn.draw(win):
					selected_level = levels[level_num - 1]

					ball_group.empty()
					for i in range(selected_level.num_balls):
						angle = 90 if i == 0 else 270
						ball = Balls(CENTER, RADIUS, angle, win, shape=selected_level.shape)
						ball_group.add(ball)

					show_level_page = False
					game_page = True
					lives_left = selected_level.lives
					score = 0

				level_text = font.render(str(level_num), True, WHITE)
				text_rect = level_text.get_rect(center=btn.rect.center)
				win.blit(level_text, text_rect)
			else:
				win.blit(lock_icon, (btn.rect.centerx - lock_icon.get_width() // 2,
									 btn.rect.centery - lock_icon.get_height() // 2))
	elif score_page:
		game_msg.update()
		over_msg.update()

		if score:
			final_score.update(score, color)
		else:
			final_score.update("0", color)
		if score and (score >= highscore):
			new_high_msg.update(shadow=False)

		if home_btn.draw(win):
			show_level_page = True
			show_intro_page = False
			home_page = False
			score_page = False
			game_page = False
			player_alive = True

			ball_group.empty()
			tile_group.empty()
			coin_group.empty()
			particle_group.empty()

			with open("progress.txt") as f:
				highest_unlocked = int(f.read().strip())

			for i, (btn, level_num) in enumerate(level_buttons):
				btn.clicked = False
				btn.enabled = (level_num <= highest_unlocked)

			score = 0
			score_msg = Message(WIDTH//2, 100, 60, "0", score_font, (150, 150, 150), win)

		if retry_btn.draw(win):
			ball_group.empty()
			for i in range(selected_level.num_balls):
				angle = 90 if i == 0 else 270
				ball = Balls(CENTER, RADIUS, angle, win, shape=selected_level.shape)
				ball_group.add(ball)

			score_page = False
			game_page = True
			player_alive = True
			lives_left = selected_level.lives
			score = 0
			score_msg = Message(WIDTH // 2, 100, 60, "0", score_font, (150, 150, 150), win)

		retry_rect = retry_text.get_rect(center=retry_btn.rect.center)
		win.blit(retry_text, retry_rect)

		if (score>=10 or selected_level.level_num < highest_unlocked) and selected_level.level_num < 20:
			if next_level_btn.draw(win):
				selected_level = levels[selected_level.level_num]  # next level (index +1)
				ball_group.empty()
				for i in range(selected_level.num_balls):
					angle = 90 if i == 0 else 270
					ball = Balls(CENTER, RADIUS, angle, win, shape=selected_level.shape)
					ball_group.add(ball)

				score_page = False
				game_page = True
				player_alive = True
				lives_left = selected_level.lives
				score = 0
				score_msg = Message(WIDTH // 2, 100, 60, "0", score_font, (150, 150, 150), win)

			next_rect = next_level_text.get_rect(center=next_level_btn.rect.center)
			win.blit(next_level_text, next_rect)

		elif score < 10 and selected_level.level_num >= highest_unlocked:
			try_again_msg.update(shadow=False)

		if score >= 10 and selected_level.level_num == highest_unlocked and highest_unlocked <= 20:
			highest_unlocked += 1
			try:
				with open("progress.txt", "w") as f:
					f.write(str(highest_unlocked))
				level_buttons[highest_unlocked - 1][0].enabled = True
			except:
				print("error")
			passed_levels.append(selected_level.level_num)

		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	elif game_page:

		if selected_level:
			background_shape_name = selected_level.shape
		else:
			background_shape_name = "circle"

		draw_background_path(win, background_shape_name, RADIUS, CENTER,15, BLACK)

		ball_group.update(color)
		coin_group.update(color)
		tile_group.update()
		score_msg.update(score)
		particle_group.update()

		if player_alive:
			for ball in ball_group:
				if pygame.sprite.spritecollide(ball, coin_group, True):
					score_fx.play()
					score += 1
					if highscore <= score:
							highscore = score

					x, y = ball.rect.center
					for i in range(10):
						particle = Particle(x, y, color, win)
						particle_group.add(particle)

				if pygame.sprite.spritecollide(ball, tile_group, True):
					x, y = ball.rect.center
					for _ in range(30):
						particle = Particle(x, y, color, win)
						particle_group.add(particle)

					lives_left -= 1
					if lives_left <= 0:
						player_alive = False
						dead_fx.play()

			font = pygame.font.Font("Fonts/Aladin-Regular.ttf", 18)
			text_lives = font.render(f"Lives: {lives_left}", True, WHITE)
			win.blit(text_lives, (15, 15))

			current_time = pygame.time.get_ticks()
			delta = current_time- start_time
			if  coin_delta < delta < coin_delta + 100 and new_coin:
				y = random.randint(CENTER[1]-RADIUS, CENTER[1]+RADIUS)
				coin = Coins(y, win)
				coin_group.add(coin)
				new_coin = False

			if current_time- start_time >= tile_delta:
				y = random.choice([CENTER[1]-80, CENTER[1], CENTER[1]+80])
				type_ = random.randint(1,3)
				t = Tiles(y, type_, win)
				tile_group.add(t)

				start_time = current_time
				new_coin = True

		if not player_alive and len(particle_group) == 0:
			for btn, _ in level_buttons:
				btn.enabled = False
			score_page = True
			game_page = False

			score_page_fx.play()

			ball_group.empty()
			tile_group.empty()
			coin_group.empty()

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()


pygame.quit()