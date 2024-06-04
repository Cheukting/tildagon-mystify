import asyncio
import app
import display
import random

from events.input import Buttons, BUTTON_TYPES

class Polygon():
    def __init__(self,
            points=None,
            color=None,
            speed=0.05):

        # init color
        if color is None:
            self.color = [random.random(), random.random(), random.random()]
        else:
            self.color = color
        self.color_change = [random.choice([1, -1]),
                random.choice([1, -1]),
                random.choice([1, -1])]

        # init points
        if points is None:
            self.points = []
            for _ in range(4):
                ran_x = int((random.random()-0.5)*200)
                ran_y = int((random.random()-0.5)*200)
                self.points.append([ran_x, ran_y])
        else:
            self.points = points

        # init targets
        self.targets = []
        for _ in range(4):
            ran_x = int((random.random()-0.5)*200)
            ran_y = int((random.random()-0.5)*200)
            self.targets.append([ran_x, ran_y])

        # init steps
        self.speed = speed
        self.steps = []
        for i in range(4):
            x_diff = (self.targets[i][0] - self.points[i][0])*speed
            y_diff = (self.targets[i][1] - self.points[i][1])*speed
            self.steps.append([x_diff, y_diff])

    def __str__(self):
        return str(self.points)

    def __print__(self):
        return str(self.points)

class MystifyApp(app.App):
    def __init__(self, num_of_poly = None, poly_speed = None):
        self.button_states = Buttons(self)

        if poly_speed is None:
            self.poly_speed = 0.05
        else:
            self.poly_speed = poly_speed

        if num_of_poly is None:
            self.num_of_poly = 2
        else:
            self.num_of_poly = num_of_poly

        self.polygons=[]
        for _ in range(self.num_of_poly):
            self.polygons.append(Polygon(speed=self.poly_speed))

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            self.__init__(self.num_of_poly, self.poly_speed)
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            if self.num_of_poly < 10:
                self.__init__(self.num_of_poly+1, self.poly_speed)
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            if self.num_of_poly > 1:
                self.__init__(self.num_of_poly-1, self.poly_speed)
        elif self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            if self.poly_speed > 0.01:
                self.__init__(self.num_of_poly, self.poly_speed-0.01)
        elif self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.button_states.clear()
            if self.poly_speed < 0.09:
                self.__init__(self.num_of_poly, self.poly_speed+0.01)

        for polygon in self.polygons:
            self.update_polygon(polygon)

    def update_polygon(self, polygon):
        # update color
        for i in range(3):
            polygon.color[i] += 0.01 * polygon.color_change[i]
            if polygon.color[i] >= 1:
                polygon.color_change[i] *= -1
                polygon.color[i] = 1
            elif polygon.color[i] <= 0:
                polygon.color_change[i] *= -1
                polygon.color[i] = 0

        # update point pos
        for i in range(4):
            x_diff = (polygon.targets[i][0] - polygon.points[i][0])
            y_diff = (polygon.targets[i][1] - polygon.points[i][1])
            if abs(x_diff) < abs(polygon.steps[i][0]) or abs(y_diff) < abs(polygon.steps[i][1]):
                # update target
                ran_x = int((random.random()-0.5)*200)
                ran_y = int((random.random()-0.5)*200)
                polygon.targets[i] = [ran_x, ran_y]
                polygon.steps[i][0] = (ran_x - polygon.points[i][0])*polygon.speed
                polygon.steps[i][1] = (ran_y - polygon.points[i][1])*polygon.speed
            else:
                polygon.points[i][0] += polygon.steps[i][0]
                polygon.points[i][1] += polygon.steps[i][1]

    def draw_line(self, ctx, start, finish, color):
        ctx.rgb(color[0], color[1], color[2]).begin_path()
        ctx.move_to(start[0],start[1])
        ctx.line_to(finish[0],finish[1])
        ctx.stroke()

    def draw_poly(self, ctx, polygon):
        for i in range(3):
            self.draw_line(ctx, polygon.points[i], polygon.points[i+1], polygon.color)
        self.draw_line(ctx, polygon.points[3], polygon.points[0], polygon.color)

    def draw(self, ctx):
        ctx.save()
        ctx.rgb(0,0,0).rectangle(-120,-120,240,240).fill()
        for polygon in self.polygons:
            self.draw_poly(ctx, polygon)
        ctx.restore()

__app_export__ = MystifyApp
