import random
from config import *

class Tile:
    def __init__(self):
        self.possibilities = list(tile_rules.keys())
        self.entropy = len(self.possibilities)
        self.neightbors = dict()

    def add_neighbor(self, direction, tile):
        self.neightbors[direction] = tile

    def get_neighbor(self, direction):
        return self.neightbors[direction]

    def get_directions(self):
        return list(self.neightbors.keys())
    
    def get_possibilities(self):
        return self.possibilities
    
    def collapse(self):
        weights = [tile_weights[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights=weights, k=1)
        self.entropy = 0

    def constrain(self, neighbor_possiblities, direction):
        """
        updates each tile to see which possible tiles can be placed next to self

        @param neighbor_possiblities: a list of possible neighboring tiles
        @param direction: the direction to be checked -> N, S, E, W

        @return reduced: the filtered tiles that are allowed to be placed
        """
        reduced = 0

        if self.entropy > 0:
            connectors = []
            for neighbor_possibility in neighbor_possiblities:
                connectors.append(tile_rules[neighbor_possibility][direction])

            if direction == NORTH:
                opposite = SOUTH
            elif direction == EAST:
                opposite = WEST
            elif direction == SOUTH:
                opposite = NORTH
            else:
                opposite = EAST

            for possibility in self.possibilities.copy():
                if tile_rules[possibility][opposite] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True
            self.entropy = len(self.possibilities)

        return reduced