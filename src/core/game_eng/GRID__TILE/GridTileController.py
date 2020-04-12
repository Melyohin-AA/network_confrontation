import pygame
from random import randint
from constants import Color
from objects.text import Text
from objects.base import DrawObject


class GridTileController():
    def __init__(self, game, model, view):
        self.game = game
        self.model = model
        self.view = view

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.on_scroll(1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.on_scroll(-1)

    def on_click(self, event):
        clicked_cell = self.model.inPolygon

        if clicked_cell.return_color() == Color.WHITE:
            self.model.make_cells_white()
            self.model.make_cell_red(clicked_cell.x,clicked_cell.y)
            self.model.make_cells_green(clicked_cell)
        elif clicked_cell.return_color() == Color.RED:
            self.model.make_cells_white()
        elif clicked_cell.return_color() == Color.GREEN:
            self.model.make_cell_orange(clicked_cell.x,clicked_cell.y)
        elif clicked_cell.return_color() == Color.ORANGE:
            self.model.make_cell_green(clicked_cell)

    def on_scroll(self,value):
        self.model.move_units(self.model.getCellByColor(Color.RED),self.model.getCellByColor(Color.ORANGE),value)