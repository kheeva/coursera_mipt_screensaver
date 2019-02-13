import random

import pygame


class Vec2d:
    """
        Points on screen and operations we able to do with them
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = self.generate_speed()
        self.speed_y = self.generate_speed()

    @staticmethod
    def generate_speed():
        return random.random() * 2

    def speedup_point(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def int_pair(self):
        return int(self.x), int(self.y)

    def __add__(self, other_vec):
        new_x = self.x + other_vec.x
        new_y = self.y + other_vec.y
        return Vec2d(new_x, new_y)

    def __sub__(self, other_vec):
        new_x = other_vec.x - self.x
        new_y = other_vec.y - self.y
        return Vec2d(new_x, new_y)

    def __mul__(self, k):
        if isinstance(k, int) or isinstance(k, float):
            return Vec2d(self.x*k, self.y*k)
        elif isinstance(k, Vec2d):
            return self.x * k.x + self.y * k.y

    def __len__(self):
        return int((self.x * self.x + self.y * self.y) ** 0.5)


class Polyline:
    """
        Defines a set of a polyline points and methods to add/del and draw them
    """
    def __init__(self, steps):
        self.steps = steps
        self._points = []

    def add_vec2d(self, vec):
        self._points.append(vec)

    def set_points(self, display):
        for p in range(len(self._points)):
            self._points[p].speedup_point()
            if self._points[p].x > display.get_width() or self._points[p].x < 0:
                self._points[p].speed_x = - self._points[p].speed_x
            if self._points[p].y > display.get_height() or (
                    self._points[p].y < 0):
                self._points[p].speed_y = - self._points[p].speed_y

    def draw_points(self, display, color=(255, 255, 255), width=3):
        for point in self._points:
            pygame.draw.circle(
                display,
                color,
                point.int_pair(),
                width,
            )

    def flush_points(self):
        self._points = []


class Knot(Polyline):
    """
        Set of methods which help to draw lines by set of knots
    """
    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + (
                Knot.get_point(points, alpha, deg-1) * (1-alpha))

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i*alpha))
        return res

    def get_knot(self):
        if len(self._points) < 3:
            return []
        res = []
        for i in range(-2, len(self._points) - 2):
            ptn = []
            ptn.append((self._points[i] + self._points[i+1])*0.5)
            ptn.append(self._points[i+1])
            ptn.append((self._points[i+1] + self._points[i+2])*0.5)
            res.extend(self.get_points(ptn, self.steps))
        return res

    def draw_lines(self, display, color=(255, 255, 255), width=3):
        knots = self.get_knot()
        for knot_index in range(-1, len(knots) - 1):
            pygame.draw.line(
                display,
                color,
                knots[knot_index].int_pair(),
                knots[knot_index + 1].int_pair(),
                width,
            )


class Display:
    """
        Defines pygame display settings and methods
    """
    def __init__(self, width, height, name, steps):
        self.width = width
        self.height = height
        self.name = name
        self.steps = steps
        self.pause = True
        self.show_help = False

        self.__events = {
            'key_pressed': pygame.KEYDOWN,
            'quit': pygame.QUIT,
        }
        self.__bindings = {
            'set_point': pygame.MOUSEBUTTONDOWN,
            'escape': pygame.K_ESCAPE,
            'reload': pygame.K_r,
            'pause': pygame.K_p,
            'increase_steps': pygame.K_KP_PLUS,
            'decrease_steps': pygame.K_KP_MINUS,
            'help': pygame.K_F1,
        }

    def __init_window(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name)
        self.color = pygame.Color(0)
        self.hue = 0

    def __set_color(self):
        self.display.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

    def draw_help(self):
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def start(self):
        self.__init_window()
        knot = Knot(steps=self.steps)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == self.__events['quit']:
                    run = False

                if event.type == self.__events['key_pressed']:
                    if event.key == self.__bindings['escape']:
                        run = False
                    if event.key == self.__bindings['pause']:
                        self.pause = not self.pause
                    if event.key == self.__bindings['reload']:
                        knot.flush_points()
                    if event.key == self.__bindings['increase_steps']:
                        self.steps += 1
                    if event.key == self.__bindings['decrease_steps']:
                        self.steps -= 1 if self.steps > 1 else 0
                    if event.key == self.__bindings['help']:
                        self.show_help = not self.show_help

                if event.type == self.__bindings['set_point']:
                    knot.add_vec2d(Vec2d(*event.pos))

            self.__set_color()
            knot.draw_points(self.display)
            knot.draw_lines(self.display, color=self.color)

            if not self.pause:
                knot.set_points(self.display)

            if self.show_help:
                self.draw_help()

            pygame.display.flip()

        self.__stop()

    @staticmethod
    def __stop():
        pygame.display.quit()
        pygame.quit()


if __name__ == '__main__':
    screensaver = Display(width=800, height=600, name="Screensaver", steps=35)
    screensaver.start()
