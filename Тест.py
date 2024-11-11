import tkinter as tk
import random
import pygame


# Класс для управления звуковыми эффектами
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.eat_sound = pygame.mixer.Sound("eat.wav")
        self.collision_sound = pygame.mixer.Sound("collision.wav")

    def play_eat_sound(self):
        self.eat_sound.play()

    def play_collision_sound(self):
        self.collision_sound.play()


class Snake:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.body = [self]
        self.direction = (1, 0)

    def move(self, dx, dy):
        new_head = Snake(self.canvas, self.x + dx, self.y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def eat(self, food):
        new_part = Snake(self.canvas, food.x, food.y)
        self.body.append(new_part)

    def draw(self):
        for part in self.body:
            self.canvas.create_oval(part.x * 10, part.y * 10, (part.x + 1) * 10, (part.y + 1) * 10, fill="green")


class Food:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.create_oval(self.x * 10, self.y * 10, (self.x + 1) * 10, (self.y + 1) * 10, fill="red")


class Wall:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.create_rectangle(self.x * 10, self.y * 10, (self.x + 1) * 10, (self.y + 1) * 10, fill="gray")


class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0
        self.high_scores = []

    def increase(self, amount):
        self.score += amount

    def reset(self):
        self.score = 0

    def save_high_score(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:3]

    def draw(self):
        self.canvas.create_text(50, 10, text=f"Счет: {self.score}", font=("Arial", 18), fill="black")


class SpeedManager:
    def __init__(self):
        self.speed = 100
        self.multiplier = 1.0

    def increase_speed(self):
        self.multiplier += 0.5
        self.speed = int(100 / self.multiplier)

    def reset(self):
        self.speed = 100
        self.multiplier = 1.0


class UIManager:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.score_label = tk.Label(root, text="Счет: 0", font=("Arial", 18))
        self.score_label.place(x=10, y=self.game.height * 10 + 20)
        self.speed_label = tk.Label(root, text="Скорость: 1.0", font=("Arial", 18))
        self.speed_label.place(x=self.game.width * 10 - 170, y=self.game.height * 10 + 20)
        self.start_button = tk.Button(root, text="Старт", command=self.game.start_game, font=("Arial", 18))
        self.start_button.place(x=self.game.width * 5 - 50, y=self.game.height * 5 + 10)
        self.quit_button = tk.Button(root, text="Выход", command=root.quit)
        self.quit_button.place(x=self.game.width * 5 + 50, y=self.game.height * 10 + 50)
        self.pause_label = None
        self.high_scores_button = None
        self.high_scores_window = None

    def update_score(self, score):
        self.score_label.config(text=f"Счет: {score}")

    def update_speed(self, speed_multiplier):
        self.speed_label.config(text=f"Скорость: {speed_multiplier:.1f}")

    def hide_start_button(self):
        self.start_button.place_forget()

    def reset(self):
        self.start_button.place(x=self.game.width * 5 - 50, y=self.game.height * 5 + 10)
        self.quit_button.place(x=self.game.width * 5 + 50, y=self.game.height * 10 + 50)
        if self.high_scores_button:
            self.high_scores_button.place_forget()

    def show_pause(self):
        if self.pause_label:
            self.pause_label.place_forget()
        self.pause_label = tk.Label(self.root, text="Пауза", font=("Arial", 24), fg="red")
        self.pause_label.place(x=self.game.width * 5 - 40, y=self.game.height * 5 + 40)

    def hide_pause(self):
        if self.pause_label:
            self.pause_label.place_forget()

    def create_high_scores_button(self):
        self.high_scores_button = tk.Button(self.root, text="Рекорды", command=self.show_high_scores)
        self.high_scores_button.place(x=self.game.width * 5 - 35, y=self.game.height * 5 + 60)

    def show_high_scores(self):
        self.high_scores_window = tk.Toplevel(self.root)
        self.high_scores_window.title("Рекорды")
        self.high_scores_window.resizable(False, False)
        label = tk.Label(self.high_scores_window, text="Рекорды:", font=("Arial", 18))
        label.pack(pady=10)
        listbox = tk.Listbox(self.high_scores_window, width=20, height=3, font=("Arial", 16))
        listbox.pack(pady=10)
        for i, score in enumerate(self.game.score_manager.high_scores, start=1):
            listbox.insert(tk.END, f"{i}. {score}")


class CollisionManager:
    def check_collision_with_self(self, snake):
        head = snake.body[0]
        for part in snake.body[1:]:
            if head.x == part.x and head.y == part.y:
                return True
        return False

    def check_collision_with_walls(self, snake, walls):
        head = snake.body[0]
        for wall in walls:
            if head.x == wall.x and head.y == wall.y:
                return True
        return False


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = tk.Tk()
        self.root.title("Змейка")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=width * 10, height=height * 10 + 80, highlightthickness=0)
        self.canvas.pack()

        self.snake = Snake(self.canvas, width // 2, height // 2)
        self.food = Food(self.canvas, random.randint(0, width - 1), random.randint(0, height - 1))
        self.walls = []
        self.score_manager = Score(self.canvas)
        self.speed_manager = SpeedManager()
        self.collision_manager = CollisionManager()
        self.sound_manager = SoundManager()

        self.ui_manager = UIManager(self.root, self)

        self.direction = (1, 0)
        self.paused = False

        self.create_border()
        self.create_separator()

    def create_border(self):
        self.canvas.create_rectangle(0, 0, self.width * 10, self.height * 10, outline="gray")

    def create_separator(self):
        self.canvas.create_line(0, self.height * 10, self.width * 10, self.height * 10, fill="gray", width=2)

    def start_game(self):
        self.ui_manager.hide_start_button()
        self.ui_manager.quit_button.place_forget()
        self.reset_game()
        self.play()

    def reset_game(self):
        self.canvas.delete("all")
        self.snake = Snake(self.canvas, self.width // 2, self.height // 2)
        self.food = Food(self.canvas, random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        self.direction = (1, 0)
        self.paused = False
        self.score_manager.reset()
        self.speed_manager.reset()
        self.walls.clear()
        self.ui_manager.reset()  # Скрыть кнопку "Рекорды" при перезапуске игры
        self.create_border()
        self.create_separator()

    def update_walls(self):
        self.walls.clear()
        for _ in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.walls.append(Wall(self.canvas, x, y))

    def play(self):
        if not self.paused:
            new_x = (self.snake.body[0].x + self.direction[0]) % self.width
            new_y = (self.snake.body[0].y + self.direction[1]) % self.height
            self.snake.body.insert(0, Snake(self.canvas, new_x, new_y))

            if self.snake.body[0].x == self.food.x and self.snake.body[0].y == self.food.y:
                self.food = Food(self.canvas, random.randint(0, self.width - 1), random.randint(0, self.height - 1))
                self.score_manager.increase(5)
                self.ui_manager.update_score(self.score_manager.score)
                self.sound_manager.play_eat_sound()

                if self.score_manager.score % 100 == 0:
                    self.speed_manager.increase_speed()
                self.ui_manager.update_speed(self.speed_manager.multiplier)

                if self.score_manager.score >= 500 and self.score_manager.score % 200 == 0:
                    self.update_walls()
            else:
                self.snake.body.pop()

            if self.collision_manager.check_collision_with_self(self.snake) or \
                    self.collision_manager.check_collision_with_walls(self.snake, self.walls):
                self.sound_manager.play_collision_sound()
                self.game_over()
            else:
                self.canvas.delete("all")
                self.create_border()
                self.create_separator()
                self.snake.draw()
                self.food.draw()
                for wall in self.walls:
                    wall.draw()
                self.root.after(self.speed_manager.speed, self.play)

    def game_over(self):
        self.score_manager.save_high_score()
        self.canvas.create_text(self.width * 5, self.height * 5 - 5, text="Игра окончена!", font=("Arial", 24),
                                fill="red")
        self.ui_manager.create_high_scores_button()
        self.ui_manager.reset()

    def key_press(self, event):
        if event.keysym == "space":
            if self.paused:
                self.paused = False
                self.ui_manager.hide_pause()
                self.play()
            else:
                self.paused = True
                self.ui_manager.show_pause()
        elif not self.paused:
            if event.keysym == "Up" and self.direction != (0, 1):
                self.direction = (0, -1)
            elif event.keysym == "Down" and self.direction != (0, -1):
                self.direction = (0, 1)
            elif event.keysym == "Left" and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif event.keysym == "Right" and self.direction != (-1, 0):
                self.direction = (1, 0)

    def run(self):
        self.root.bind("<Key>", self.key_press)
        self.root.mainloop()


game = Game(40, 40)
game.run()
