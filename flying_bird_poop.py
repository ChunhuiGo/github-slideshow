#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小鸟边飞边拉屎的动画演示
使用 pygame 实现简单的动画效果
"""

import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("小鸟边飞边拉屎")

# 颜色定义
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)

# 时钟
clock = pygame.time.Clock()
FPS = 60

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity_y = 0
        self.gravity = 0.5
        self.lift = -10
        self.width = 40
        self.height = 30
        self.wing_angle = 0
        self.wing_direction = 1
        
    def fly(self):
        # 重力作用
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # 边界检测
        if self.y > HEIGHT - 100:
            self.y = HEIGHT - 100
            self.velocity_y = 0
        if self.y < 50:
            self.y = 50
            self.velocity_y = 0
            
        # 翅膀扇动
        self.wing_angle += 0.3 * self.wing_direction
        if abs(self.wing_angle) > 0.5:
            self.wing_direction *= -1
    
    def flap(self):
        self.velocity_y += self.lift
    
    def draw(self, surface):
        # 画身体
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(surface, YELLOW, body_rect)
        
        # 画头
        head_rect = pygame.Rect(self.x + self.width - 10, self.y - 10, 20, 20)
        pygame.draw.circle(surface, YELLOW, (self.x + self.width, self.y), 12)
        
        # 画眼睛
        pygame.draw.circle(surface, BLACK, (self.x + self.width + 3, self.y - 3), 3)
        
        # 画嘴巴
        beak_points = [
            (self.x + self.width + 10, self.y + 2),
            (self.x + self.width + 20, self.y + 5),
            (self.x + self.width + 10, self.y + 8)
        ]
        pygame.draw.polygon(surface, (255, 165, 0), beak_points)
        
        # 画翅膀（扇动效果）
        wing_y_offset = int(self.wing_angle * 20)
        wing_points = [
            (self.x + 10, self.y + 10),
            (self.x - 10, self.y + 10 + wing_y_offset),
            (self.x + 15, self.y + 15)
        ]
        pygame.draw.polygon(surface, (255, 215, 0), wing_points)
        
        # 画尾巴
        tail_points = [
            (self.x, self.y + 15),
            (self.x - 15, self.y + 10),
            (self.x - 15, self.y + 20)
        ]
        pygame.draw.polygon(surface, YELLOW, tail_points)

class Poop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.gravity = 0.3
        self.size = random.randint(5, 10)
        
    def fall(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
    def draw(self, surface):
        # 画便便（水滴形状）
        points = []
        for i in range(20):
            angle = i * 3.14159 / 20
            r = self.size * (1 - 0.3 * (angle / (3.14159 / 2)))
            px = self.x + r * pygame.math.Vector2(1, 0).rotate_rad(-angle - 3.14159/2).x
            py = self.y + r * pygame.math.Vector2(1, 0).rotate_rad(-angle - 3.14159/2).y
            points.append((px, py))
        
        if len(points) > 2:
            pygame.draw.polygon(surface, BROWN, points)
        
        # 简单版本：画个椭圆
        poop_rect = pygame.Rect(self.x - self.size//2, self.y - self.size, 
                                self.size, self.size * 1.5)
        pygame.draw.ellipse(surface, BROWN, poop_rect)

class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.randint(30, 60)
        
    def move(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = WIDTH + 100
            self.y = random.randint(50, 200)
            
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, WHITE, (int(self.x) + self.size, int(self.y)), self.size * 0.8)
        pygame.draw.circle(surface, WHITE, (int(self.x) - self.size, int(self.y)), self.size * 0.8)

def main():
    bird = Bird()
    poops = []
    clouds = []
    
    # 创建一些云
    for i in range(5):
        clouds.append(Cloud(random.randint(0, WIDTH), random.randint(50, 200), random.uniform(0.5, 1.5)))
    
    poop_timer = 0
    poop_interval = 30  # 每 30 帧拉一次屎
    
    running = True
    auto_fly = True
    
    font = pygame.font.Font(None, 36)
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:
                    auto_fly = not auto_fly
        
        # 自动飞行模式
        if auto_fly:
            if bird.y > HEIGHT - 150:
                bird.flap()
            elif bird.y < 150:
                pass  # 让鸟掉下来一点
            else:
                if random.random() < 0.02:
                    bird.flap()
        
        # 更新鸟的位置
        bird.fly()
        
        # 生成便便
        poop_timer += 1
        if poop_timer >= poop_interval:
            poop_timer = 0
            poops.append(Poop(bird.x + bird.width // 2, bird.y + bird.height))
        
        # 更新所有便便
        for poop in poops[:]:
            poop.fall()
            if poop.y > HEIGHT:
                poops.remove(poop)
        
        # 更新云
        for cloud in clouds:
            cloud.move()
        
        # 绘制
        screen.fill(SKY_BLUE)
        
        # 画云
        for cloud in clouds:
            cloud.draw(screen)
        
        # 画地面
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
        
        # 画便便（先画，这样会在鸟下面）
        for poop in poops:
            poop.draw(screen)
        
        # 画鸟
        bird.draw(screen)
        
        # 显示说明
        text = font.render("空格键：拍打翅膀 | A键：切换自动飞行 | ESC：退出", True, BLACK)
        screen.blit(text, (10, 10))
        
        mode_text = font.render(f"模式：{'自动飞行' if auto_fly else '手动控制'}", True, BLACK)
        screen.blit(mode_text, (10, 50))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
