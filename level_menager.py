import math
import pygame

class Level:
    def __init__(self, level_num, shape, num_balls, lives):
        self.level_num = level_num
        self.shape = shape  # string
        self.num_balls = num_balls
        self.lives = lives

# Levels 1-20
shapes = [
    "circle", "square", "triangle", "eight", "infinity",
    "u", "parallel_v", "reverse_u", "x", "parallel_diagonals"
]

levels = [
    Level(1, 'circle', 1, 3),
    Level(2, 'square', 1, 3),
    Level(3, 'triangle', 1, 3),
    Level(4, 'eight', 1, 3),
    Level(5, 'infinity', 1, 3),
    Level(6, 'u', 1, 3),
    Level(7, 'parallel_v', 1, 3),
    Level(8, 'reverse_u', 1, 3),
    Level(9, 'x', 1, 3),
    Level(10, 'parallel_diagonals', 1, 3),
    Level(11, 'circle', 2, 3),
    Level(12, 'square', 2, 3),
    Level(13, 'triangle', 2, 3),
    Level(14, 'eight', 2, 3),
    Level(15, 'infinity', 2, 3),
    Level(16, 'u', 2, 3),
    Level(17, 'parallel_v', 2, 3),
    Level(18, 'reverse_u', 2, 3),
    Level(19, 'x', 2, 3),
    Level(20, 'parallel_diagonals', 2, 3)
]
for i in range(20):
    shape = shapes[i % len(shapes)]
    num_balls = 1 if i < 10 else 2
    levels.append(Level(i+1, shape, num_balls, 3))
