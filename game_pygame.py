# -*- coding: utf-8 -*-
import copy
import random
import pygame

from pygame.locals import *
from sys import exit

body_group = []
W = 800
H = 400
BODY_W = W / 40
BODY_H = H / 20


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Body(Point):
    def __init__(self, x, y):
        super(Body, self).__init__(x, y)
        self.rect = pygame.draw.rect(screen, [0, 255, 255], [self.x * BODY_W, self.y * BODY_H, 20, 20], 0)

    def __eq__(self, other):
        # 因为要两个块比较是否相等
        return self.rect.x == other.rect.x and self.rect.y == other.rect.y

    def drawing(self, *args, **kwargs):
        self.rect = pygame.draw.rect(screen, [0, 255, 255], [self.x * BODY_W, self.y * BODY_H, 20, 20], 0)


class Food(Point):
    def __init__(self, x=0, y=0):
        super(Food, self).__init__(x, y)
        self.rect = pygame.draw.rect(screen, [122, 139, 139], [self.x * BODY_W, self.y * BODY_H, 20, 20], 0)

    @staticmethod
    def get_new_point(*args, **kwargs):
        # 绘食物
        w = W / BODY_W
        h = H / BODY_H
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        return x, y

    def set(self, x, y):
        self.x = x
        self.y = y

    def drawing(self):
        self.rect = pygame.draw.rect(screen, [122, 139, 139], [self.x * BODY_W, self.y * BODY_H, 20, 20], 0)


class ScorerController(object):
    def __init__(self):
        self.scorer = 0

    def set_scorer(self, scorer):
        self.scorer = scorer

    def get_scorer(self):
        return self.scorer

    def drawing(self, *args, **kwargs):
        # 绘画分数
        font = pygame.font.SysFont("", 40)
        text_surface = font.render("Scores:{}".format(scorer.get_scorer()), True, (0, 0, 255))
        screen.blit(text_surface, (0, 0))


class Snake(object):
    def __init__(self, head):
        body_group.append(head)
        self.head = head
        self.speed = 5

    @staticmethod
    def is_food(head, food):
        return pygame.Rect.colliderect(head.rect, food.rect)

    @staticmethod
    def is_boundary(head):
        if head.x < 0 or head.x >= 40:
            return True
        elif head.y < 0 or head.y > 20:
            return True
        return False

    @staticmethod
    def is_body(head, body_group):
        # 注意
        # 1.这里要把蛇头自己去掉
        # 2.深拷贝不能影响原蛇身
        copy_body_group = copy.deepcopy(body_group)
        for body in copy_body_group:
            if head == body:
                copy_body_group.remove(body)
        return head.rect.collidelist([body.rect for body in copy_body_group])

    def drawing(self, *args, **kwargs):
        for body in body_group:
            body.drawing()

    def get_head(self):
        return body_group[len(body_group) - 1]

    def get_speed(self):
        return self.speed

    def move(self, *args, **kwargs):
        head = Body(args[0], args[1])
        self.set_head(head)

    def set_head(self, head):
        body_group.append(head)
        self.head = head

    def set_speed(self, speed):
        self.speed = speed

    def pop_tail(self):
        body_group.pop(0)


pygame.init()

screen = pygame.display.set_mode((W, H), 0, 32)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

HEAD_INIT_X = 0
HEAD_INIT_Y = 0
FOOD_INIT_X = 14
FOOD_INIT_Y = 4
direction = "right"

head = Body(HEAD_INIT_X, HEAD_INIT_Y)
snake = Snake(head)
food = Food(FOOD_INIT_X, FOOD_INIT_Y)
scorer = ScorerController()

while True:
    screen.fill((225, 225, 225))
    for event in pygame.event.get():
        if event.type == QUIT:
            # 接收到退出事件后退出程序
            exit()
        elif event.type == pygame.KEYDOWN:
            head = snake.get_head()
            if event.key == 119:
                direction = "up"
            elif event.key == 115:
                direction = "down"
            elif event.key == 97:
                direction = "left"
            elif event.key == 100:
                direction = "right"
    # 碰边界 碰蛇身
    if Snake.is_boundary(snake.head) or Snake.is_body(snake.get_head(), body_group) != -1:
        # 游戏结束
        font = pygame.font.SysFont("", 40)
        text_surface = font.render("Game Over Scores:{}".format(scorer.get_scorer()), True, (0, 0, 255))
        screen.blit(text_surface, (screen.get_width() / 2 - 120, screen.get_height() / 2))
    else:
        head = snake.get_head()
        head_x, head_y = head.x, head.y
        if direction == "up":
            head_y -= 1
        elif direction == "down":
            head_y += 1
        elif direction == "left":
            head_x -= 1
        elif direction == "right":
            head_x += 1
        head = Body(head_x, head_y)
        snake.set_head(head)
        # 没有撞食物则把尾巴砍掉,如果撞到食物则不用砍尾巴视觉看来就是把食物吃掉增加蛇身长度
        if not snake.is_food(snake.get_head(), food):
            snake.pop_tail()
        else:
            x, y = Food.get_new_point()
            food.set(x, y)
            scorer.set_scorer(scorer.get_scorer() + 1)
            snake.set_speed(snake.get_speed() + scorer.get_scorer() / 2)
        scorer.drawing()
        snake.drawing()
        food.drawing()
    time_passed = clock.tick(snake.get_speed())
    pygame.display.update()
