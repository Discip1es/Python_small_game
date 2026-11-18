"""
⭐ ЛОВЕЦ ЗВЁЗД ⭐
Ретро-аркада на встроенном модуле turtle — без установки библиотек.

Управление:
  ← →  или  A D   — двигать корабль
  Ловите жёлтые звёзды (+10 очков)
  Избегайте красных бомб (-1 жизнь)
  Игра заканчивается, когда жизни = 0

Запуск:  python star_catcher.py
"""

import turtle
import random

# ============================================================
#  НАСТРОЙКА ЭКРАНА
# ============================================================
WIDTH, HEIGHT = 600, 700

screen = turtle.Screen()
screen.title("⭐ Ловец Звёзд ⭐")
screen.bgcolor("#0a0a2e")      # 💡 попробуй другой цвет фона!
screen.setup(WIDTH, HEIGHT)
screen.tracer(0)               # отключаем авто-отрисовку → плавная анимация

# ============================================================
#  КОРАБЛЬ ИГРОКА
# ============================================================
player = turtle.Turtle()
player.shape("triangle")
player.color("#00ffff")
player.penup()
player.goto(0, -280)
player.setheading(90)
player.shapesize(1.5, 1.5)
player.speed(0)

# ============================================================
#  СОСТОЯНИЕ ИГРЫ
# ============================================================
score = 0
lives = 3
frame = 0
game_active = True

stars = []
bombs = []

# ============================================================
#  ИНТЕРФЕЙС (HUD)
# ============================================================
hud = turtle.Turtle()
hud.hideturtle()
hud.color("white")
hud.penup()
hud.goto(-280, 320)
hud.write("Счёт: 0   Жизни: 3", font=("Arial", 16, "bold"))

# ============================================================
#  СПАВНЕРЫ
# ============================================================
def spawn_star():
    s = turtle.Turtle()
    s.shape("circle")
    s.color("#ffe000")
    s.penup()
    s.shapesize(0.8)
    s.goto(random.randint(-270, 270), 350)
    s.fall_speed = random.uniform(2, 4)     # 💡 увеличь — станет сложнее
    s.speed(0)
    stars.append(s)

def spawn_bomb():
    b = turtle.Turtle()
    b.shape("circle")
    b.color("#ff3355")
    b.penup()
    b.shapesize(0.9)
    b.goto(random.randint(-270, 270), 350)
    b.fall_speed = random.uniform(2.5, 5)   # 💡 подними минимум для хардкора
    b.speed(0)
    bombs.append(b)

# ============================================================
#  УПРАВЛЕНИЕ
# ============================================================
def move_left():
    if game_active:
        player.setx(max(player.xcor() - 30, -270))

def move_right():
    if game_active:
        player.setx(min(player.xcor() + 30, 270))

screen.listen()
screen.onkeypress(move_left,  "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left,  "a")
screen.onkeypress(move_right, "d")

# ============================================================
#  КОНЕЦ ИГРЫ
# ============================================================
def end_game():
    global game_active
    game_active = False

    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("white")
    msg.penup()
    msg.goto(0, 60)
    msg.write("ИГРА ОКОНЧЕНА", align="center", font=("Arial", 34, "bold"))
    msg.goto(0, 0)
    msg.write(f"Финальный счёт: {score}", align="center",
              font=("Arial", 22, "normal"))
    msg.goto(0, -60)
    msg.write("Закрой окно, чтобы выйти", align="center",
              font=("Arial", 12, "normal"))
    screen.update()

# ============================================================
#  ГЛАВНЫЙ ЦИКЛ
# ============================================================
def game_loop():
    global score, lives, frame

    if not game_active:
        return

    frame += 1

    # --- спавн ---
    if frame % 25 == 0:
        spawn_star()
    if frame % 60 == 0:
        spawn_bomb()

    # --- падающие звёзды ---
    for s in stars[:]:
        s.sety(s.ycor() - s.fall_speed)
        if s.distance(player) < 28:
            score += 10
            s.hideturtle()
            stars.remove(s)
        elif s.ycor() < -350:
            s.hideturtle()
            stars.remove(s)

    # --- падающие бомбы ---
    for b in bombs[:]:
        b.sety(b.ycor() - b.fall_speed)
        if b.distance(player) < 28:
            lives -= 1
            b.hideturtle()
            bombs.remove(b)
        elif b.ycor() < -350:
            b.hideturtle()
            bombs.remove(b)

    # --- HUD ---
    hud.clear()
    hud.write(f"Счёт: {score}   Жизни: {lives}",
              font=("Arial", 16, "bold"))

    screen.update()

    if lives <= 0:
        end_game()
        return

    screen.ontimer(game_loop, 20)  # ~50 кадров/сек

# ============================================================
#  ПОЕХАЛИ!
# ============================================================
game_loop()
turtle.done()