import pygame as pg

BASEGREEN = (41, 122, 85)
DARKGREEN = (18, 97, 61)
LIGHTGREEN = (74, 150, 115)
HIGHLIGHT = (119, 181, 153)

LINETHICKNESS = 2

class Iso:
    def __init__(self, rows, cols):
        self.map = [[0] * rows for _ in range(cols)]
        self.TS = 150
        self.offsetX = 645
        self.offsetY = 57

    def draw(self, screen):
        for c in range(len(self.map)):
            for r in range(len(self.map[0])):
                z = self.map[c][r]
                # top surface
                coords = (self.worldToScreenWithElavation(c, r, z), self.worldToScreenWithElavation(c+1, r, z),
                          self.worldToScreenWithElavation(c+1, r+1, z), self.worldToScreenWithElavation(c, r+1, z))

                pg.draw.polygon(screen, LIGHTGREEN, coords)
                pg.draw.polygon(screen, HIGHLIGHT, coords, LINETHICKNESS)

                # If the height value is over zero, the left and right sides of the cube are visible and must be drawn.
                if z > 0:
                    # left surface
                    coords = (self.worldToScreen(c+1, r+1), self.worldToScreen(c, r+1),
                              self.worldToScreenWithElavation(c, r+1, z), self.worldToScreenWithElavation(c+1, r+1, z))

                    pg.draw.polygon(screen, BASEGREEN, coords)
                    pg.draw.polygon(screen, HIGHLIGHT, coords, LINETHICKNESS)

                    # right surface
                    coords = (self.worldToScreen(c+1, r+1), self.worldToScreen(c+1, r),
                              self.worldToScreenWithElavation(c+1, r, z), self.worldToScreenWithElavation(c+1, r+1, z))

                    pg.draw.polygon(screen, DARKGREEN, coords)
                    pg.draw.polygon(screen, HIGHLIGHT, coords, LINETHICKNESS)

    def worldToScreen(self, x, y):
        screenX = self.offsetX + (x-y) * (self.TS/2)
        screenY = self.offsetY + (x+y) * (self.TS/4)

        return screenX, screenY

    def worldToScreenWithElavation(self, x, y, z):
        # the screen Y value is directly affected by the z component which is stored in the tile map.
        screenX = self.offsetX + (x-y) * (self.TS/2)
        screenY = self.offsetY + (x+y) * (self.TS/4) - z * self.TS/4

        return screenX, screenY

    def ScreenToWorld(self, x, y):
        x -= self.offsetX
        y -= self.offsetY
        worldX = 0.5 * (x/(self.TS/2) + y/(self.TS/4))
        worldY = 0.5 * (-x/(self.TS/2) + y/(self.TS/4))

        return worldX, worldY
