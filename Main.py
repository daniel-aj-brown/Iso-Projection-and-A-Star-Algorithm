import pygame as pg
from Iso import *
from AStar import *

SCROLLSPEED = 1
BLUE = (43, 84, 113)
LIGHTBLUE = (115, 146, 169)
WHITE = (255, 255, 255)
LIGHTYELLOW = (255, 217, 169)
YELLOW = (218, 170, 107)

ROWS = 10
COLS = 8

class Engine:
    def __init__(self, width, height, fps):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = width, height
        self.FPS = fps
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.dt = 0

        # create an instance of a tile map of dimensions decided above
        self.map = Iso(ROWS, COLS)
        # Give some cells some height to start with
        self.map.map[0][1] = 1
        self.map.map[1][1] = 1
        self.map.map[2][1] = 2
        self.map.map[5][2] = 3

        self.path = None
        self.mx, self.my = 0, 0

        self.start = (0, 0)
        self.end = (3, 3)

    def input(self):
        keys = pg.key.get_pressed()
        # Scroll the screen with the arrow keys
        if keys[pg.K_LEFT]:
            self.map.offsetX += SCROLLSPEED * self.dt
        if keys[pg.K_RIGHT]:
            self.map.offsetX -= SCROLLSPEED * self.dt
        if keys[pg.K_UP]:
            self.map.offsetY += SCROLLSPEED * self.dt
        if keys[pg.K_DOWN]:
            self.map.offsetY -= SCROLLSPEED * self.dt

        # Find the current cell the mouse is hovering over
        self.mx, self.my = pg.mouse.get_pos()
        self.mx, self.my = self.map.ScreenToWorld(self.mx, self.my)
        self.mx, self.my = int(self.mx), int(self.my)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # check that the click occurec over the isometric tile map
                if 0 <= self.mx < len(self.map.map) and 0 <= self.my < len(self.map.map[0]):
                    if event.button == 1:
                        # if the left mouse button was clicked, raise the terrain
                        if self.map.map[self.mx][self.my] < 5:
                            self.map.map[self.mx][self.my] += 1
                    elif event.button == 3:
                        # if the right mouse button was clicked, lower the terrain
                        if self.map.map[self.mx][self.my] > 0:
                            self.map.map[self.mx][self.my] -= 1

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # check that both the start and ends points are on the ground level.
                    if self.map.map[self.start[0]][self.start[1]] == 0 and self.map.map[self.end[0]][self.end[1]] == 0:
                        # Perform the a_star algorithm
                        self.path = a_star(self.map.map, self.start, self.end)
                if 0 <= self.mx < len(self.map.map) and 0 <= self.my < len(self.map.map[0]):
                    # Designate a start or end cell providing the mouse is hovering over the tile map
                    if event.key == pg.K_s:
                        self.start = (self.mx, self.my)
                    elif event.key == pg.K_e:
                        self.end = (self.mx, self.my)

    def draw(self):
        self.screen.fill(BLUE)
        self.map.draw(self.screen)

        # Draw the currently highlighted cell
        coords = (self.map.worldToScreen(self.mx, self.my), self.map.worldToScreen(self.mx + 1, self.my),
                  self.map.worldToScreen(self.mx + 1, self.my + 1), self.map.worldToScreen(self.mx, self.my + 1))
        pg.draw.polygon(self.screen, LIGHTBLUE, coords, 4)

        # Draw the current start cell
        coords = (self.map.worldToScreen(self.start[0], self.start[1]), self.map.worldToScreen(self.start[0] + 1, self.start[1]),
                  self.map.worldToScreen(self.start[0] + 1, self.start[1] + 1), self.map.worldToScreen(self.start[0], self.start[1] + 1))
        pg.draw.polygon(self.screen, YELLOW, coords, 2)

        # Draw the current end cell
        coords = (self.map.worldToScreen(self.end[0], self.end[1]), self.map.worldToScreen(self.end[0] + 1, self.end[1]),
                  self.map.worldToScreen(self.end[0] + 1, self.end[1] + 1), self.map.worldToScreen(self.end[0], self.end[1] + 1))
        pg.draw.polygon(self.screen, LIGHTYELLOW, coords, 2)


        if self.path is not None:
            for i in range(len(self.path)-1):
                # Draw a node and a line between it and the next node on the list
                x, y = self.map.worldToScreen(self.path[i][0] + 0.5, self.path[i][1] + 0.5)
                x2, y2 = self.map.worldToScreen(self.path[i+1][0] + 0.5, self.path[i+1][1] + 0.5)
                pg.draw.circle(self.screen, WHITE, (x, y), 10)
                pg.draw.line(self.screen, WHITE, (x, y), (x2, y2), 5)
            # Draw the last remaining node. No line is necessary because it is the last on the list
            x, y = self.map.worldToScreen(self.path[-1][0] + 0.5, self.path[-1][1] + 0.5)
            pg.draw.circle(self.screen, WHITE, (x, y), 10)

    def run(self):
        while True:
            self.input()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.dt = self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = Engine(1280, 720, 0)
    app.run()