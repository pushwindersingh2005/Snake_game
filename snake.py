from tkinter import Tk, Label, Canvas
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
SCORE_FONT = ('consolas', 40)
GAME_OVER_FONT = ('consolas', 70)

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.canvas = canvas
        
        # Initialize snake body in a vertical line
        for i in range(BODY_PARTS, 0, -1):
            self.coordinates.append([0, i * SPACE_SIZE])
        
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, outline=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.spawn_food()
    
    def spawn_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, outline=FOOD_COLOR, tag="food"
        )

class SnakeGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        self.score = 0
        self.direction = 'down'
        self.game_active = True
        
        # Score label
        self.label = Label(
            window, text=f"Score: {self.score}", 
            font=SCORE_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR
        )
        self.label.pack()
        
        # Game canvas
        self.canvas = Canvas(
            window, bg=BACKGROUND_COLOR, 
            height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()
        
        # Center window
        self.center_window()
        
        # Initialize game elements
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        
        # Bind controls
        self.bind_controls()
        
        # Start game loop
        self.next_turn()
    
    def center_window(self):
        self.window.update()
        
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def bind_controls(self):
        self.window.bind('<Right>', lambda e: self.change_direction('right'))
        self.window.bind('<Left>', lambda e: self.change_direction('left'))
        self.window.bind('<Up>', lambda e: self.change_direction('up'))
        self.window.bind('<Down>', lambda e: self.change_direction('down'))
        self.window.bind('<r>', lambda e: self.reset_game())
        self.window.bind('<R>', lambda e: self.reset_game())
    
    def change_direction(self, new_direction):
        if not self.game_active:
            return
            
        opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def next_turn(self):
        if not self.game_active:
            return
            
        x, y = self.snake.coordinates[0]
        
        # Move head based on direction
        if self.direction == 'up':
            y -= SPACE_SIZE
        elif self.direction == 'down':
            y += SPACE_SIZE
        elif self.direction == 'left':
            x -= SPACE_SIZE
        elif self.direction == 'right':
            x += SPACE_SIZE
        
        # Insert new head position
        self.snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=SNAKE_COLOR, outline=SNAKE_COLOR
        )
        self.snake.squares.insert(0, square)
        
        # Check if food eaten
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            # Remove tail if no food eaten
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]
        
        # Check for collisions
        if self.check_collision():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)
    
    def check_collision(self):
        x, y = self.snake.coordinates[0]
        
        # Wall collision
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        
        # Self collision
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        
        return False
    
    def game_over(self):
        self.game_active = False
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            font=GAME_OVER_FONT, fill="red", text="GAME OVER", tag="gameover"
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 70,
            font=('consolas', 20), fill=TEXT_COLOR,
            text="Press R to restart", tag="restart"
        )
    
    def reset_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.label.config(text=f"Score: {self.score}")
        self.direction = 'down'
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.game_active = True
        self.next_turn()

# Create and run the game
window = Tk()
game = SnakeGame(window)
window.mainloop()