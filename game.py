# -*- coding: utf-8 -*-
import Tkinter
import random
import enum

BODY = 10
SPEED = 500
MAP_BG = "#030915"
FOOD_BG = "green"
SNAKE_BG = "#2EB7DE"
VIEW_HIGH = 400
VIEW_WIDTH = 400


# 方向控制
class Direction(enum.Enum):
    up = "w"
    down = "s"
    left = "a"
    right = "d"


class Snake(object):
    def __init__(self):
        self.bodys = []
        self.head_color = SNAKE_BG
        self.body_color = SNAKE_BG

    def del_tail(self):
        return self.bodys.pop(0)

    def add_head(self, head):
        self.bodys.append(head)

    def init_body(self, body):
        self.bodys.append(body)

    def get_head(self):
        return self.bodys[-1]


# 全局单例蛇
snake = Snake()


# 画面
class View(object):
    '''
    画面渲染
    '''

    def __init__(self):
        self.top = Tkinter.Tk()
        self.top.geometry("400x400")
        self.top.title("贪吃蛇")
        self.top.resizable(width=False, height=False)
        self.cv = Tkinter.Canvas(self.top, bg=MAP_BG, height=VIEW_HIGH, width=VIEW_WIDTH)
        self.cv.pack(side="left", ipadx=135, ipady=130)

    def move_food(self, points, food):
        x1, y1, x2, y2 = points
        self.cv.coords(food, x1, y1, x2, y2)

    def create_food(self, points):
        x1, y1, x2, y2 = points
        food = self.cv.create_rectangle(x1, y1, x2, y2, fill=FOOD_BG)
        return food

    def snake(self):
        color = snake.body_color
        for i in xrange(0, 3):
            if i == 2:
                color = snake.head_color
            cv = self.cv.create_rectangle(i * BODY, 0, i * BODY + BODY, BODY, fill=color)
            snake.init_body(cv)

    def set_head(self, points):
        x1, y1, x2, y2 = points
        head = self.cv.create_rectangle(x1, y1, x2, y2, fill=SNAKE_BG)
        return head

    def get_head_points(self, head):
        return tuple(self.cv.coords(head))

    def over(self):
        self.cv.delete("all")
        b = Tkinter.Button(self.cv, text="继续游戏", width=15)
        b.pack(side='bottom', pady=20)
        w = Tkinter.Label(self.cv, text="游戏结束", bg="#030915", fg="white", font=(None, 15))
        w.pack(side="bottom", pady=140)


# 控制器
class Controller(object):
    '''
    游戏逻辑控制
    '''

    def __init__(self):
        self.direction = Direction.right
        self.fx = 0
        self.fy = 0
        self.food = -1
        self.over = False
        self.view = View()

    def move(self):
        if self.over:
            return
        head = snake.get_head()
        x1, y1, x2, y2 = self.view.get_head_points(head)
        if self.direction == Direction.up:
            y1 -= BODY
            y2 -= BODY
        elif self.direction == Direction.down:
            y1 += BODY
            y2 += BODY
        elif self.direction == Direction.left:
            x1 -= BODY
            x2 -= BODY
        elif self.direction == Direction.right:
            x1 += BODY
            x2 += BODY
        new_head = self.view.set_head((x1, y1, x2, y2))
        snake.add_head(new_head)
        # 被吃后重新移动食物
        if x1 == self.fx and y1 == self.fy:
            fp = self.set_foot()
            self.view.move_food(fp, self.food)
        else:
            tail = snake.del_tail()
            self.view.cv.delete(tail)
        # 碰撞检测
        points = (x1, y1, x2, y2)
        border, body = self.checking(points)
        if border or body:
            self.over = True
            self.view.over()
        self.view.cv.after(SPEED, self.move)

    def checking(self, points):
        '''
        碰边界 碰蛇身 碰食物
        :param points:
        :return:
        '''
        border = False
        body = False
        x1, y1, x2, y2 = points
        if x2 > 400 or x1 < 0 or y1 < 0 or y2 > 400:
            border = True
        return border, body

    def start_game(self):
        x1, y1, x2, y2 = self.set_foot()
        self.food = self.view.create_food((x1, y1, x2, y2))
        self.view.snake()
        self.move()
        self.view.top.bind('<Key>', self.key_pressed)
        self.view.top.mainloop()

    def key_pressed(self, e):
        direction = e.char
        if direction == 'w':
            if self.direction != Direction.down:
                self.direction = Direction.up
        elif direction == 's':
            if self.direction != Direction.up:
                self.direction = Direction.down
        elif direction == 'a':
            if self.direction != Direction.right:
                self.direction = Direction.left
        elif direction == 'd':
            if self.direction != Direction.left:
                self.direction = Direction.right

    def set_foot(self):
        # 绘食物
        r = VIEW_WIDTH / BODY
        x = random.randint(0, r - 1)
        y = random.randint(0, r - 1)
        self.fx = BODY * x
        self.fy = BODY * y
        return tuple([BODY * x, BODY * y, BODY * x + BODY, BODY * y + BODY])


def Game():
    con = Controller()
    con.start_game()


if __name__ == '__main__':
    Game()
