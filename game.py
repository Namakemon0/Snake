import tkinter as tk
import random


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
        """
        Добавляет новую часть к телу змейки, когда она съедает еду.
        """
        new_part = Snake(self.canvas, food.x, food.y)
        self.body.append(new_part)

    def draw(self):
        """
        Рисует тело змейки на холсте.
        """
        for part in self.body:
            self.canvas.create_oval(part.x * 10, part.y * 10, (part.x + 1) * 10, (part.y + 1) * 10, fill="green")


class Food:
    """
    Представляет еду, которую змейка может съесть.
    """
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self):
        """
        Рисует еду на холсте.
        """
        self.canvas.create_oval(self.x * 10, self.y * 10, (self.x + 1) * 10, (self.y + 1) * 10, fill="red")


class Game:
    """
    Управляет общей логикой игры и пользовательским интерфейсом.
    """
    def __init__(self, width, height):
        # Инициализируем окно игры и холст
        self.root = tk.Tk()
        self.root.title("Змейка")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=width * 10, height=height * 10 + 80, highlightthickness=0)
        self.canvas.pack()

        # Создаем змейку и еду
        self.snake = Snake(self.canvas, width // 2, height // 2)
        self.food = Food(self.canvas, random.randint(0, width - 1), random.randint(0, height - 1))

        # Устанавливаем игровые переменные
        self.direction = (1, 0)
        self.width = width
        self.height = height
        self.paused = False
        self.score = 0
        self.speed = 100
        self.speed_multiplier = 1.0
        self.high_scores = []
        self.high_scores_button = None
        self.high_scores_window = None
        self.high_scores_label = None
        self.high_scores_listbox = None

        # Создаем элементы интерфейса
        self.score_label = tk.Label(self.root, text="Счет: 0", font=("Arial", 18))
        self.score_label.place(x=10, y=self.height * 10 + 20)
        self.speed_label = tk.Label(self.root, text="Скорость: 1.0", font=("Arial", 18))
        self.speed_label.place(x=self.width * 10 - 170, y=self.height * 10 + 20)
        self.restart_button = tk.Button(self.root, text="Перезапуск", command=self.restart_game)
        self.quit_button = tk.Button(self.root, text="Выход", command=self.root.destroy)
        self.start_button = tk.Button(self.root, text="Старт", command=self.start_game, font=("Arial", 18))
        self.start_button.place(x=self.width * 5 - 50, y=self.height * 5 + 10)

        # Создаем границу игры, разделитель и кнопки
        self.create_border()
        self.create_separator()
        self.create_restart_and_quit_buttons()

    def create_border(self):
        """
        Рисует границу игры на холсте.
        """
        self.canvas.create_rectangle(0, 0, self.width * 10, self.height * 10, outline="gray")

    def create_separator(self):
        """
        Рисует разделительную линию между игровой областью и элементами интерфейса.
        """
        self.canvas.create_line(0, self.height * 10, self.width * 10, self.height * 10, fill="gray", width=2)

    def create_restart_and_quit_buttons(self):
        """
        Добавляет кнопки "Перезапуск" и "Выход" в окно игры.
        """
        self.restart_button.place(x=self.width * 5 - 75, y=self.height * 10 + 50)
        self.quit_button.place(x=self.width * 5 + 25, y=self.height * 10 + 50)

    def start_game(self):
        self.start_button.place_forget()  # Скрываем кнопку старта
        if self.high_scores_button:
            self.high_scores_button.place_forget()  # Скрываем кнопку рекордов
        self.reset_game()
        self.play()

    def reset_game(self):
        """
        Сбрасывает все игровые переменные и элементы.
        """
        self.canvas.delete("all")
        self.snake = Snake(self.canvas, self.width // 2, self.height // 2)
        self.food = Food(self.canvas, random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        self.direction = (1, 0)
        self.paused = False
        self.score = 0
        self.score_label.config(text="Счет: 0")
        self.speed_label.config(text="Скорость: 1.0")
        self.speed = 100
        self.speed_multiplier = 1.0
        self.create_border()
        self.create_separator()

    def play(self):
        """
        Обрабатывает основной игровой цикл, включая движение змейки, сбор еды и обнаружение столкновений.
        """
        if not self.paused:
            new_x = (self.snake.body[0].x + self.direction[0]) % self.width
            new_y = (self.snake.body[0].y + self.direction[1]) % self.height
            self.snake.body.insert(0, Snake(self.canvas, new_x, new_y))

            # Проверяем, съела ли змейка еду
            if self.snake.body[0].x == self.food.x and self.snake.body[0].y == self.food.y:
                self.food = Food(self.canvas, random.randint(0, self.width - 1), random.randint(0, self.height - 1))
                self.score += 5
                self.score_label.config(text=f"Счет: {self.score}")
                if self.score >= 100 and self.score % 100 == 0:
                    self.speed_multiplier += 0.5
                    self.speed_label.config(text=f"Скорость: {self.speed_multiplier:.1f}")
                self.speed = int(100 / self.speed_multiplier)
            else:
                self.snake.body.pop()

            # Проверяем на столкновения
            if self.check_collision():
                self.game_over()
            else:
                self.canvas.delete("all")
                self.create_border()
                self.create_separator()
                self.snake.draw()
                self.food.draw()
                self.root.after(self.speed, self.play)

    def check_collision(self):
        """
        Проверяет, столкнулась ли змейка сама с собой.
        """
        head = self.snake.body[0]
        for part in self.snake.body[1:]:
            if head.x == part.x and head.y == part.y:
                return True
        return False

    def game_over(self):
        """
        Обрабатывает сценарий окончания игры, включая обновление рекордов и отображение сообщения об окончании игры.
        """
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:3]
        self.canvas.create_text(self.width * 5, self.height * 5 - 5, text="Игра окончена!", font=("Arial", 24), fill="red")
        self.create_high_scores_button()
        self.start_button.place(x=self.width * 5 - 50, y=self.height * 5 + 10)  # Показываем кнопку старта

    def create_high_scores_button(self):
        """
        Добавляет кнопку "Рекорды" в окно игры.
        """
        self.high_scores_button = tk.Button(self.root, text="Рекорды", command=self.create_high_scores_window)
        self.high_scores_button.place(x=self.width * 5 - 35, y=self.height * 5 + 60)

    def create_high_scores_window(self):
        """
        Создает новое окно для отображения рекордов.
        """
        self.high_scores_window = tk.Toplevel(self.root)
        self.high_scores_window.title("Рекорды")
        self.high_scores_window.resizable(False, False)
        self.high_scores_label = tk.Label(self.high_scores_window, text="Рекорды:", font=("Arial", 18))
        self.high_scores_label.pack(pady=10)
        self.high_scores_listbox = tk.Listbox(self.high_scores_window, width=20, height=3, font=("Arial", 16))
        self.high_scores_listbox.pack(pady=10)
        for i, score in enumerate(self.high_scores, start=1):
            self.high_scores_listbox.insert(tk.END, f"{i}. {score}")

    def pause(self):
        """
        Приостанавливает игру и отображает сообщение "Пауза".
        """
        self.paused = True
        self.canvas.create_text(self.width * 5, self.height * 5 + 40, text="Пауза", font=("Arial", 24), fill="red")
        self.create_restart_and_quit_buttons()
        if self.high_scores_button:
            self.high_scores_button.place_forget()

    def restart_game(self):
        """
        Перезапускает игру, сбрасывая все игровые переменные и элементы.
        """
        self.reset_game()
        self.start_button.place(x=self.width * 5 - 50, y=self.height * 5 + 30)  # Показываем кнопку старта
        if self.high_scores_button:
            self.high_scores_button.place_forget()
        self.create_restart_and_quit_buttons()

    def key_press(self, event):
        """
        Обрабатывает нажатия клавиш пользователем, включая паузу/возобновление игры и изменение направления змейки.
        """
        if event.keysym == "space":
            if self.paused:
                self.paused = False
                self.play()
                self.create_restart_and_quit_buttons()
                if self.high_scores_button:
                    self.high_scores_button.place_forget()
            else:
                self.paused = True
                self.pause()
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
        """
        Запускает игру и входит в основной цикл событий.
        """
        self.root.bind("<Key>", self.key_press)
        self.root.mainloop()


game = Game(40, 40)
game.run()
