# -*- coding: utf-8 -*-
import Tkinter
import threading
import random
import enum
import time


def app():
    con = Controller()
    con.init_map()
    con.rule()


MAP_WIDTH = 400
MAP_HIGH = 400
BODY = 20


# 方向控制
class Direction(enum.Enum):
    up = "w"
    down = "s"
    left = "a"
    right = "d"


# 绘制地图
class Map(object):
    def __init__(self):
        self.top = Tkinter.Tk()
        self.top.geometry("400x400")
        self.cv = Tkinter.Canvas(self.top, bg="green", height=400, width=400)

    def draw(self):
        # 绘地图
        for i in xrange(0, 20):
            for j in xrange(0, 20):
                self.cv.create_rectangle(20 * i, 20 * j, 20 * i + 50, 20 * j + 20, fill="red")
        self.cv.pack()

    def food(self):
        # 绘食物
        foot_x = random.randint(0, MAP_WIDTH / BODY)
        foot_y = random.randint(0, MAP_HIGH / BODY)
        self.cv.create_rectangle(20 * foot_x, 20 * foot_y, 20 * foot_x + 20, 20 * foot_y + 20, fill="green")

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

    def update_snake(self):
        # 新蛇头
        _x1,_y1,_x2,_y2=snake.bodys[-1]
        self.cv.create_rectangle(_x1,_y1,_x2,_y2, fill=snake.head_color)
        # 旧蛇头
        x1, y1, x2, y2 = snake.bodys[-2]
        self.cv.create_rectangle(x1,y1,x2,y2,fill=snake.body_color)
        # 删除一个尾巴
        __x1, __y1,__x2,__y2 = snake.bodys[0]
        self.cv.create_rectangle(__x1, __y1, __x2, __y2, fill="red")
        snake.bodys.pop(0)


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


class Controller(threading.Thread):
    def __init__(self):
        '''
        游戏初始化
        '''
        super(Controller, self).__init__()
        self.direction = Direction.left
        self._map = Map()

    def rule(self):
        if self.direction == Direction.up:
            pass
        elif self.direction == Direction.down:
            pass
        elif self.direction == Direction.left:
            # 旧蛇头
            x1, y1 ,x2, y2= snake.bodys[-1]
            # 新蛇头
            _x1, _y1 = x1 + BODY, y1
            _x2, _y2 = x2 + BODY, y2

            snake.bodys.append((_x1, _y1, _x2, _y2))
            self._map.cv.after(1000, self.rule)
            self._map.update_snake()
            self._map.top.mainloop()
        elif self.direction == Direction.right:
            pass

    def init_map(self):
        self._map.draw()
        self._map.food()
        self._map.snake()

    def start_game(self):
        pass

    def key_pressed(self, e):
        self.direction = e.keysym


if __name__ == '__main__':
    app()
