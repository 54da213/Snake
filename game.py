# -*- coding: utf-8 -*-
import Tkinter
import threading
import random
import enum
import time


def app():
    con = Controller()
    con.start_game()


VIEW_WIDTH = 400
VIEW_HIGH = 400
BODY = 20


# 方向控制
class Direction(enum.Enum):
    up = "w"
    down = "s"
    left = "a"
    right = "d"


# 绘制地图
class View(object):
    def __init__(self):
        self.top = Tkinter.Tk()
        self.top.geometry("400x400")
        self.cv = Tkinter.Canvas(self.top, bg="green", height=VIEW_HIGH, width=VIEW_WIDTH)

    def draw(self):
        # 绘地图
        for i in xrange(0, 20):
            for j in xrange(0, 20):
                self.cv.create_rectangle(20 * i, 20 * j, 20 * i + 50, 20 * j + 20, fill="red")
        self.cv.pack()

    def food(self, points):
        x1, y1, x2, y2 = points
        self.cv.create_rectangle(x1, y1, x2, y2, fill="green")

    def snake(self):
        # 绘蛇
        color = snake.body_color
        snake_len = len(snake.bodys)
        for i in xrange(0, snake_len):
            if i == 2:
                color = snake.head_color
            x1, y1, x2, y2 = snake.bodys[i]
            self.cv.create_rectangle(x1, y1, x2, y2, fill=color)
        # self.top.mainloop()

    def update(self, **kwargs):
        # 新蛇头
        x1, y1, x2, y2 = snake.bodys[-1]
        self.cv.create_rectangle(x1, y1, x2, y2, fill=snake.head_color)
        # 旧蛇头
        x1, y1, x2, y2 = snake.bodys[-2]
        self.cv.create_rectangle(x1, y1, x2, y2, fill=snake.body_color)
        # 删除一个尾巴
        x1, y1, x2, y2 = snake.bodys[0]
        self.cv.create_rectangle(x1, y1, x2, y2, fill="red")
        # 新食物
        food = kwargs.get("food")
        if food:
            fp = kwargs.get("fp")
            self.food(fp)


# 蛇
class Snake(object):
    def __init__(self):
        self.bodys = []
        for i in xrange(0, 3):
            self.bodys.append((20 * i, 20 * 0, 20 * i + 20, 20 * 0 + 20))
        self.head_color = "yellow"
        self.body_color = "black"


# 全局蛇
snake = Snake()
my_direction = 'd'


class Controller(threading.Thread):
    def __init__(self):
        '''
        游戏初始化
        '''
        super(Controller, self).__init__()
        self.direction = Direction.right
        self.fx = 0
        self.fy = 0
        self._View = View()

    def move(self):
        # 旧蛇头
        x1, y1, x2, y2 = snake.bodys[-1]
        if self.direction == Direction.up:
            y1 = y1 - BODY
            y2 = y2 - BODY
        elif self.direction == Direction.down:
            y1 = y1 + BODY
            y2 = y2 + BODY
        elif self.direction == Direction.left:
            x1 = x1 - BODY
            x2 = x2 - BODY
        elif self.direction == Direction.right:
            x1 = x1 + BODY
            x2 = x2 + BODY
        # 新蛇头
        points = (x1, y1, x2, y2)
        snake.bodys.append(points)
        food = False
        fp = (0,)
        if x1 == self.fx and y1 == self.fy:
            food = True
            fp = self.foot()
            self.fx, self.fy, _, _ = fp
        # 碰撞检测
        border, body = self.checking(points)
        over = True if border or body else False
        self._View.update(food=food, fp=fp, over=over)
        if not food:
            snake.bodys.pop(0)
        self._View.cv.after(1000, self.move)

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

    def over(self):
        pass

    def start_game(self):
        # 初始化地图
        self._View.draw()
        self.fx, self.fy, x2, y2 = self.foot()
        self._View.food((self.fx, self.fy, x2, y2))
        self._View.snake()
        self.move()
        self._View.top.bind('<Key>', self.key_pressed)
        self._View.cv.mainloop()

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

    def foot(self):
        # 绘食物
        x = random.randint(0, VIEW_WIDTH / BODY)
        y = random.randint(0, VIEW_HIGH / BODY)
        # 遍历一遍蛇身保证食物不能出现在蛇身上
        return tuple([BODY * x, BODY * y, BODY * x + BODY, BODY * y + BODY])


if __name__ == '__main__':
    app()
