import pyray as rl
import random

rl.init_window(500, 500, "SnakeY")

rl.set_window_icon(rl.load_image("assets/testpic.png"))

rl.set_target_fps(60)

GAME_HEIGHT = 500
GAME_WIDTH = 500

# Initialize snake head position OUTSIDE the loop
head_x = GAME_WIDTH // 2  # Use integer division
head_y = GAME_HEIGHT // 2

game_started = False
game_failed = False
score = 0

# Food variables
food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

while not rl.window_should_close():
    rl.begin_drawing()
    
    if not game_started and game_failed == False:
        # Menu screen
        rl.clear_background(rl.BLACK)
        rl.draw_text("Snake Game", 150, 200, 40, rl.GREEN)
        rl.draw_text("Press SPACE to start", 150, 250, 20, rl.WHITE)
        rl.draw_text("Press ESC to close", 150, 300, 15, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_SPACE):
            game_started = True
    elif game_started == True:
        rl.clear_background(rl.DARKGRAY)

        rl.draw_text(f"Score: {score}", 10, 10, 20, rl.WHITE)

        # Draw food
        rl.draw_rectangle(food_x, food_y, 20, 20, rl.RED)

        if rl.is_key_down(rl.KEY_RIGHT):
            head_x += 5
        if rl.is_key_down(rl.KEY_LEFT):
            head_x -= 5
        if rl.is_key_down(rl.KEY_UP):
            head_y -= 5
        if rl.is_key_down(rl.KEY_DOWN):
            head_y += 5

        # Check if snake ate food
        if abs(head_x - food_x) < 20 and abs(head_y - food_y) < 20:
            score += 10
            # Spawn new food
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20

        if (head_x < 0 or head_x >= GAME_WIDTH or 
            head_y < 0 or head_y >= GAME_HEIGHT):
            game_started = False
            game_failed = True

        rl.draw_rectangle(head_x, head_y, 20, 20, rl.GREEN)

    elif game_failed:
        rl.clear_background(rl.BLACK)
        rl.draw_text("Game Over!", 200, 200, 40, rl.RED)
        rl.draw_text(f"Final Score: {score}", 200, 250, 20, rl.YELLOW)
        rl.draw_text("Press R to restart", 200, 300, 20, rl.WHITE)
        
        if rl.is_key_pressed(rl.KEY_R):
            # Reset game
            game_started = False
            game_failed = False
            score = 0
            head_x = GAME_WIDTH // 2
            head_y = GAME_HEIGHT // 2
            food_x = random.randint(0, (GAME_WIDTH - 20) // 20) * 20
            food_y = random.randint(0, (GAME_HEIGHT - 20) // 20) * 20


    
    rl.end_drawing()

rl.close_window()
