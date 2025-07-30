import pyray as rl
import random
import sys
import os

rl.init_window(600, 640, "Snake")

rl.set_window_state(rl.FLAG_WINDOW_RESIZABLE)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon = rl.load_image(resource_path("assets/snake_icon.png"))

rl.image_format(icon, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)

rl.set_window_icon(icon)

rl.set_target_fps(12)

rl.unload_image(icon)


GAME_HEIGHT = 640
GAME_WIDTH = 600

head_x = (GAME_WIDTH // 2 // 20) * 20
head_y = (GAME_HEIGHT // 2 // 20) * 20

game_started = False
game_failed = False
game_won = False
score = 0


snake_parts = []

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
        
        total_grid_spots = (GAME_WIDTH // 20) * (GAME_HEIGHT // 20)
        occupied_spots = set()
        
        for (part_x, part_y) in snake_parts:
            occupied_spots.add((part_x, part_y))
        
        occupied_spots.add((head_x, head_y))
        
        occupied_spots.add((food_x, food_y))
        
        for (obstacle_x, obstacle_y) in obstacles:
            occupied_spots.add((obstacle_x, obstacle_y))
        
        if len(occupied_spots) >= total_grid_spots:
            game_started = False
            game_won = True
        
        for x in range(0, GAME_WIDTH, 20):
            for y in range(0, GAME_HEIGHT, 20):
                rl.draw_rectangle_lines(x, y, 20, 20, rl.GRAY)
        
        rl.draw_text(f"Score: {score}", 10, 10, 20, rl.WHITE)

        rl.draw_rectangle(food_x - 1, food_y - 1, 22, 22, rl.BLACK)
        rl.draw_rectangle(food_x, food_y, 20, 20, rl.RED)

        for (obstacle_x, obstacle_y) in obstacles:
            rl.draw_rectangle(obstacle_x - 1, obstacle_y - 1, 22, 22, rl.BLACK)
            rl.draw_rectangle(obstacle_x, obstacle_y, 20, 20, rl.BLUE)

        if rl.is_key_down(rl.KEY_RIGHT) or rl.is_key_down(rl.KEY_D):
            if direction_x != -1:
                direction_x = 1
                direction_y = 0
        if rl.is_key_down(rl.KEY_LEFT) or rl.is_key_down(rl.KEY_A):
            if direction_x != 1:
                direction_x = -1
                direction_y = 0
        if rl.is_key_down(rl.KEY_UP) or rl.is_key_down(rl.KEY_W):
            if direction_y != 1:
                direction_x = 0
                direction_y = -1
        if rl.is_key_down(rl.KEY_DOWN) or rl.is_key_down(rl.KEY_S):
            if direction_y != -1:
                direction_x = 0
                direction_y = 1

        head_x += direction_x * 20
        head_y += direction_y * 20

        old_head_x = head_x - direction_x * 20
        old_head_y = head_y - direction_y * 20


        if direction_x != 0 or direction_y != 0:
            snake_parts.append((old_head_x, old_head_y))

        if abs(head_x - food_x) < 20 and abs(head_y - food_y) < 20:
            score += 10
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20
        else:
            if len(snake_parts) > 0:
                snake_parts.pop(0)

        for (part_x, part_y) in snake_parts:
            rl.draw_rectangle(part_x, part_y, 20, 20, rl.GREEN)

        if (head_x, head_y) in snake_parts:
            game_started = False
            game_failed = True

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

        rl.draw_rectangle(head_x, head_y, 20, 20, rl.PINK)

    elif game_failed:
        rl.clear_background(rl.BLACK)
        rl.draw_text("Game Over!", 200, 200, 40, rl.RED)
        rl.draw_text(f"Final Score: {score}", 200, 250, 20, rl.YELLOW)
        rl.draw_text("Press R to restart", 200, 300, 20, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_R):
            game_started = True
            game_failed = False
            game_won = False
            score = 0
            head_x = (GAME_WIDTH // 2 // 20) * 20
            head_y = (GAME_HEIGHT // 2 // 20) * 20
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20
            obstacles = []
            snake_parts = [] 
            direction_x = 0 
            direction_y = 0
            next_obstacle_score = 20

    elif game_won:
        rl.clear_background(rl.BLACK)
        rl.draw_text("YOU WON!", 200, 200, 40, rl.GOLD)
        rl.draw_text("Perfect Game!", 200, 250, 30, rl.YELLOW)
        rl.draw_text(f"Final Score: {score}", 200, 300, 20, rl.WHITE)
        rl.draw_text("Press R to play again", 180, 350, 20, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_R):
            game_started = True
            game_failed = False
            game_won = False
            score = 0
            head_x = (GAME_WIDTH // 2 // 20) * 20
            head_y = (GAME_HEIGHT // 2 // 20) * 20
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20
            obstacles = []
            snake_parts = []
            direction_x = 0
            direction_y = 0
            next_obstacle_score = 20


    
    rl.end_drawing()

rl.close_window()
