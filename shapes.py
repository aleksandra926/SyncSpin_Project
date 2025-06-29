import math
import pygame

CENTER = 144, 256
RADIUS = 70

def get_shape_position(shape, angle_deg, radius=70):
    angle_rad = math.radians(angle_deg)
    cx, cy = CENTER

    if shape == "circle":
        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
    elif shape == "square":
        t = (angle_deg % 360) / 90
        side = int(t)
        progress = (t - side) * 140
        if side == 0:
            x = cx - 70 + progress
            y = cy - 70
        elif side == 1:
            x = cx + 70
            y = cy - 70 + progress
        elif side == 2:
            x = cx + 70 - progress
            y = cy + 70
        else:
            x = cx - 70
            y = cy + 70 - progress
    elif shape == "triangle":
        t = angle_deg % 360
        a = [(-60, 60), (0, -60), (60, 60)]
        p1, p2 = a[int((t % 360) / 120)], a[(int((t % 360) / 120)+1)%3]
        f = ((t % 120) / 120)
        x = cx + (1 - f) * p1[0] + f * p2[0]
        y = cy + (1 - f) * p1[1] + f * p2[1]
    elif shape == "eight":
        x = cx + radius * math.sin(angle_rad) * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
    elif shape == "infinity":
        x = cx + radius * math.sin(angle_rad)
        y = cy + radius * math.sin(angle_rad) * math.cos(angle_rad)
    elif shape == "u":
        t = angle_deg % 360
        shorten_factor = 0.75
        vertical_travel = 2 * radius * shorten_factor

        if t < 90:
            x = cx - radius
            y = cy - radius + (t / 90) * vertical_travel - 30
        elif t < 270:
            theta = math.radians((t - 90) * 180 / 180)
            x = cx - radius * math.cos(theta)
            y = cy + radius * shorten_factor + radius * math.sin(theta) - 40
        else:
            x = cx + radius
            y = cy + radius - ((t - 270) / 90) * vertical_travel - 50
    elif shape == "parallel_v":
        x = cx + 30 if angle_deg % 360 < 180 else cx - 30
        y = cy - radius + (angle_deg % 180) * (2 * radius / 180)
    elif shape == "reverse_u":
        t = angle_deg % 360
        shorten_factor = 0.75
        vertical_travel = 2 * radius * shorten_factor
        if t < 90:
            x = cx - radius
            y = cy + radius - (t / 90) * vertical_travel + 30
        elif t < 270:
            theta = math.radians((t - 90) * 180 / 180)
            x = cx - radius * math.cos(theta)
            y = cy - radius * shorten_factor - radius * math.sin(theta) + 40
        else:
            x = cx + radius
            y = cy - radius + ((t - 270) / 90) * vertical_travel + 50
    elif shape == "x":
        if angle_deg % 360 < 180:
            t = angle_deg % 180
            x = cx - radius + (t / 180) * (2 * radius)
            y = cy - radius + (t / 180) * (2 * radius)
        else:
            t = angle_deg % 180
            x = cx + radius - (t / 180) * (2 * radius)
            y = cy - radius + (t / 180) * (2 * radius)
    elif shape == "parallel_diagonals":
        diagonal_line_angle_deg = -45
        diagonal_line_angle_rad = math.radians(diagonal_line_angle_deg)

        line_separation_distance = 30
        progress = (angle_deg % 180) / 180.0

        x_relative_to_center = -radius + progress * (2 * radius)
        y_relative_to_center = x_relative_to_center * math.tan(diagonal_line_angle_rad)

        perp_angle_rad = diagonal_line_angle_rad + math.radians(90)

        offset_x_comp = line_separation_distance * math.cos(perp_angle_rad)
        offset_y_comp = line_separation_distance * math.sin(perp_angle_rad)

        if angle_deg % 360 < 180:
            x = cx + x_relative_to_center + offset_x_comp
            y = cy + y_relative_to_center + offset_y_comp
        else:
            x = cx + x_relative_to_center - offset_x_comp
            y = cy + y_relative_to_center - offset_y_comp
    else:
        x = cx
        y = cy
    return round(x), round(y)


def draw_background_path(surface, shape_name, ball_radius, center_pos, thickness, color):
    cx, cy = center_pos
    angle_step = 1

    def draw_path(points_outer, points_inner):
        for i in range(len(points_outer) - 1):
            pygame.draw.polygon(surface, color, [
                points_outer[i], points_outer[i+1],
                points_inner[i+1], points_inner[i]
            ])

    if shape_name == "circle":
        outer_points, inner_points = [], []
        for angle in range(0, 360, angle_step):
            ox, oy = get_shape_position("circle", angle, radius=ball_radius + thickness//2)
            ix, iy = get_shape_position("circle", angle, radius=ball_radius - thickness//2)
            outer_points.append((ox, oy))
            inner_points.append((ix, iy))
        pygame.draw.polygon(surface, color, outer_points + inner_points[::-1])


    elif shape_name == "square":
        s_outer = ball_radius + thickness // 2
        s_inner = ball_radius - thickness // 2

        # Поголем квадрат (надворешен раб)

        outer_square = [
            (cx - s_outer, cy - s_outer), (cx + s_outer, cy - s_outer),
            (cx + s_outer, cy + s_outer), (cx - s_outer, cy + s_outer)
        ]
        # Помал квадрат (внатрешен раб)
        inner_square = [
            (cx - s_inner, cy - s_inner), (cx + s_inner, cy - s_inner),
            (cx + s_inner, cy + s_inner), (cx - s_inner, cy + s_inner)
        ]
        # Комбинираме точки за полигон кој го пополнува просторот помеѓу двата квадрати

        # Лева линија
        pygame.draw.polygon(surface, color, [
            (cx - s_outer, cy - s_outer), (cx - s_inner, cy - s_inner),
            (cx - s_inner, cy + s_inner), (cx - s_outer, cy + s_outer)
        ])

        # Десна линија
        pygame.draw.polygon(surface, color, [
            (cx + s_inner, cy - s_inner), (cx + s_outer, cy - s_outer),
            (cx + s_outer, cy + s_outer), (cx + s_inner, cy + s_inner)
        ])

        # Горна линија
        pygame.draw.polygon(surface, color, [
            (cx - s_outer, cy - s_outer), (cx + s_outer, cy - s_outer),
            (cx + s_inner, cy - s_inner), (cx - s_inner, cy - s_inner)
        ])

        # Долна линија
        pygame.draw.polygon(surface, color, [
            (cx - s_outer, cy + s_outer), (cx + s_outer, cy + s_outer),
            (cx + s_inner, cy + s_inner), (cx - s_inner, cy + s_inner)
        ])


    elif shape_name == "triangle":
        a = [(-60, 60), (0, -60), (60, 60)]
        triangle = [(cx + x, cy + y) for x, y in a]
        pygame.draw.polygon(surface, color, triangle, width=thickness)

    elif shape_name == "eight":
        outer_points, inner_points = [], []
        for angle in range(0, 360, angle_step):
            ox, oy = get_shape_position("eight", angle, radius=ball_radius + thickness//2)
            ix, iy = get_shape_position("eight", angle, radius=ball_radius - thickness//2)
            outer_points.append((ox, oy))
            inner_points.append((ix, iy))
        draw_path(outer_points, inner_points)

    elif shape_name == "infinity":
        outer_points, inner_points = [], []
        for angle in range(0, 360, angle_step):
            ox, oy = get_shape_position("infinity", angle, radius=ball_radius + thickness//2)
            ix, iy = get_shape_position("infinity", angle, radius=ball_radius - thickness//2)
            outer_points.append((ox, oy))
            inner_points.append((ix, iy))
        draw_path(outer_points, inner_points)


    elif shape_name == "u":
        vertical_height = ball_radius * 1.8  # Висина на вертикалните линии
        curve_radius = ball_radius + 7  # Полупречник на долниот полукруг
        offset = ball_radius  # Х-растојание од центар до секоја вертикала
        # Лева вертикална линија
        pygame.draw.line(
            surface, color,
            (cx - offset, cy - vertical_height + 12),
            (cx - offset, cy + 12),
            thickness
        )
        # Десна вертикална линија
        pygame.draw.line(
            surface, color,
            (cx + offset - 1.5, cy - vertical_height + 12),
            (cx + offset - 1.5, cy + 12),
            thickness
        )

        pygame.draw.arc(
            surface, color,
            (cx - curve_radius, cy - curve_radius + 12, curve_radius * 2, curve_radius * 2),
            math.pi, 2 * math.pi,
            thickness
        )

    elif shape_name == "reverse_u":
        vertical_height = ball_radius * 1.8
        curve_radius = ball_radius + 7
        offset = ball_radius

        pygame.draw.line(
            surface, color,
            (cx - offset, cy + vertical_height - 12),
            (cx - offset, cy - 12),
            thickness
        )

        pygame.draw.line(
            surface, color,
            (cx + offset - 1.5, cy + vertical_height - 12),
            (cx + offset - 1.5, cy - 12),
            thickness
        )

        pygame.draw.arc(
            surface, color,
            (
                cx - curve_radius,
                cy - curve_radius - 12,
                curve_radius * 2,
                curve_radius * 2
            ),
            0, math.pi,
            thickness
        )


    elif shape_name == "x":
        half_len = ball_radius  # половина од страната на квадратот околу кој ќе го цртаме X
        # Дијагонала од горе-лево до долу-десно
        pygame.draw.line(
            surface, color,
            (cx - half_len, cy - half_len),
            (cx + half_len, cy + half_len),
            thickness
        )
        # Дијагонала од горе-десно до долу-лево
        pygame.draw.line(
            surface, color,
            (cx + half_len, cy - half_len),
            (cx - half_len, cy + half_len),
            thickness
        )
    elif shape_name == "parallel_v":
        line_height = ball_radius * 2  # висина на линиите (од центарот ± радиус)
        line_offset = ball_radius // 2.4  # растојание од центарот до лево/десно линија

        # Лева линија
        pygame.draw.line(
            surface, color,
            (cx - line_offset, cy - ball_radius),
            (cx - line_offset, cy + ball_radius),
            thickness
        )

        # Десна линија
        pygame.draw.line(
            surface, color,
            (cx + line_offset, cy - ball_radius),
            (cx + line_offset, cy + ball_radius),
            thickness
        )


    elif shape_name == "parallel_diagonals":
        offset = ball_radius // 1.7  # колку да се оддалечени една од друга
        length = ball_radius * 2  # должина на дијагоналата
        # Прва дијагонала
        pygame.draw.line(
            surface, color,
            (cx + length // 2 - offset, cy - length // 2),
            (cx - length // 2 - offset, cy + length // 2),
            thickness
        )
        # Втора дијагонала (паралелна, лево од првата)
        pygame.draw.line(
            surface, color,
            (cx + length // 2 + offset, cy - length // 2),
            (cx - length // 2 + offset, cy + length // 2),
            thickness
        )
# def render_track_path(surface, shape_name, center_pos, ball_radius, color, thickness=20):
#     outer_radius = ball_radius + thickness // 2
#     inner_radius = ball_radius - thickness // 2
#
#     outer_points = []
#     inner_points = []
#
#     angle_step = 1
#     for angle in range(0, 360, angle_step):
#         ox, oy = get_shape_position(shape_name, angle, radius=outer_radius)
#         ix, iy = get_shape_position(shape_name, angle, radius=inner_radius)
#
#         outer_points.append((ox, oy))
#         inner_points.append((ix, iy))
#
#     # За затворени форми, затвори ги контурите
#     closed_shapes = ["circle", "square", "triangle", "eight", "infinity", "x", "parallel_diagonals"]
#     if shape_name in closed_shapes:
#         path_points = outer_points + inner_points[::-1]
#         pygame.draw.polygon(surface, color, path_points)
#     else:
#         for op, ip in zip(outer_points, inner_points):
#             pygame.draw.line(surface, color, op, ip)