import pyray as rl
import random

rl.init_window(600, 630, "Snake")

icon = rl.load_image("assets/snake_icon.png")

rl.image_format(icon, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)

rl.set_window_icon(icon)

rl.set_target_fps(15)

rl.unload_image(icon)


GAME_HEIGHT = 630
GAME_WIDTH = 600

# Align head position to 20x20 grid
head_x = (GAME_WIDTH // 2 // 20) * 20
head_y = (GAME_HEIGHT // 2 // 20) * 20

game_started = False
game_failed = False
score = 0

obstacles = []
next_obstacle_score = 20

food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

direction_x = 0
direction_y = 0

while not rl.window_should_close():
    rl.begin_drawing()
    
    if not game_started and game_failed == False:
        rl.clear_background(rl.BLACK)
        rl.draw_text("Snake Game", 150, 200, 40, rl.GREEN)
        rl.draw_text("Press SPACE to start", 150, 250, 20, rl.WHITE)
        rl.draw_text("Press ESC to close", 150, 300, 15, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_SPACE):
            game_started = True
    elif game_started == True:
        rl.clear_background(rl.DARKGRAY)
        rl.draw_text(f"Score: {score}", 10, 10, 20, rl.WHITE)

        rl.draw_rectangle(food_x, food_y, 20, 20, rl.RED)

        for (obstacle_x, obstacle_y) in obstacles:
            rl.draw_rectangle(obstacle_x, obstacle_y, 20, 20, rl.BLUE)

        if rl.is_key_down(rl.KEY_RIGHT):
            if direction_x != -1:
                direction_x = 1
                direction_y = 0
        if rl.is_key_down(rl.KEY_LEFT):
            if direction_x != 1:
                direction_x = -1
                direction_y = 0
        if rl.is_key_down(rl.KEY_UP):
            if direction_y != 1:
                direction_x = 0
                direction_y = -1
        if rl.is_key_down(rl.KEY_DOWN):
            if direction_y != -1:
                direction_x = 0
                direction_y = 1

        head_x += direction_x * 20
        head_y += direction_y * 20


        if abs(head_x - food_x) < 20 and abs(head_y - food_y) < 20:
            score += 10
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

        if (head_x < 0 or head_x >= GAME_WIDTH or 
            head_y < 0 or head_y >= GAME_HEIGHT):
            game_started = False
            game_failed = True

        if score >= next_obstacle_score:
            obstacle_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            obstacle_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

            test = random.randint(0, 2)

            if test == 1:
                obstacles.append((obstacle_x, obstacle_y))
                
                test2 = random.randint(0, 1)

                if test2 == 1:
                    if obstacle_y + 20 < GAME_HEIGHT and obstacle_x - 20 >= 0:
                        obstacles.append((obstacle_x, obstacle_y + 20))
                        obstacles.append((obstacle_x - 20, obstacle_y))
                    elif obstacle_y - 20 >= 0 and obstacle_x + 20 < GAME_WIDTH:
                        obstacles.append((obstacle_x + 20, obstacle_y))
                        obstacles.append((obstacle_x, obstacle_y - 20))

            else:
                obstacles.append((obstacle_x, obstacle_y))
            next_obstacle_score += 20

        if (head_x, head_y) in obstacles:
            game_started = False
            game_failed = True

        if (food_x, food_y) in obstacles:
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

        rl.draw_rectangle(head_x, head_y, 20, 20, rl.GREEN)

    elif game_failed:
        rl.clear_background(rl.BLACK)
        rl.draw_text("Game Over!", 200, 200, 40, rl.RED)
        rl.draw_text(f"Final Score: {score}", 200, 250, 20, rl.YELLOW)
        rl.draw_text("Press R to restart", 200, 300, 20, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_R):
            game_started = True
            game_failed = False
            score = 0
            head_x = (GAME_WIDTH // 2 // 20) * 20
            head_y = (GAME_HEIGHT // 2 // 20) * 20
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20
            obstacles = []
            next_obstacle_score = 20


    
    rl.end_drawing()

rl.close_window()
