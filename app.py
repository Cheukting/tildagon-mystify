import asyncio
import app
import display
import random

from events.input import Buttons, BUTTON_TYPES

class Polygon():
    def __init__(self, points=None):
        self.color = (random.random(), random.random(), random.random())
        if points is None:
            self.points = []
        else:
            self.points = points
        for _ in range(4):
            ran_x = int((random.random()-0.5)*200)
            ran_y = int((random.random()-0.5)*200)
            self.points.append([ran_x, ran_y])

    def __str__(self):
        return str(self.points)

    def __print__(self):
        return str(self.points)

    def diff(self, other):
        result = []
        for i in range(4):
            x_diff = (self.points[i][0] - other.points[i][0])
            y_diff = (self.points[i][1] - other.points[i][1])
            result.append([x_diff, y_diff])
        return Polygon(result)

    def div(self, num):
        result = []
        for i in range(4):
            x = self.points[i][0]/num
            y = self.points[i][1]/num
            result.append([x, y])
        return Polygon(result)

class MystifyApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)

        self.num_of_poly = 2
        self.step_div = 20

        self.polygons=[]
        for _ in range(self.num_of_poly):
            self.polygons.append(Polygon())

        self.future_polygons = []
        for _ in range(self.num_of_poly):
            self.future_polygons.append(Polygon())

        self.steps = []
        for i in range(self.num_of_poly):
            self.steps.append(self.future_polygons[i].diff(self.polygons[i]).div(self.step_div))

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.minimise()
    # def __init__(self):
    #     super().__init__()
    #     self.color = (1, 0, 0)

    def update_polygon(self, polygon, future_polygon, steps):
        for i in range(4):
            x_diff = (future_polygon.points[i][0] - polygon.points[i][0])
            y_diff = (future_polygon.points[i][1] - polygon.points[i][1])
            if abs(x_diff) < abs(steps.points[i][0]) or abs(y_diff) < abs(steps.points[i][1]):
                # update target
                ran_x = int((random.random()-0.5)*200)
                ran_y = int((random.random()-0.5)*200)
                future_polygon.points[i] = [ran_x, ran_y]
                steps.points[i][0] = (ran_x - polygon.points[i][0])/self.step_div
                steps.points[i][1] = (ran_y - polygon.points[i][1])/self.step_div
            else:
                polygon.points[i][0] += steps.points[i][0]
                polygon.points[i][1] += steps.points[i][1]


    async def run(self, render_update):
        # Render initial state
        await render_update()

        while True:
            await asyncio.sleep(0.1)

            for i in range(self.num_of_poly):
                self.update_polygon(
                    self.polygons[i],
                    self.future_polygons[i],
                    self.steps[i])
            # self.polygons[0].color = (random.random(), random.random(), random.random())
            await render_update()

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

        # self.draw_overlays(ctx)

__app_export__ = MystifyApp
