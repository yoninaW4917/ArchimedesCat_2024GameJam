import pygame as py
import json
from objects.block import Block
import fileLoader

class LevelGenerator:
    def __init__(self):
        self.level = 1
        self.data = self.load_data("data.txt")
        self.update(self.level)
    def load_data(self,file:str)->dict:
        with open(file, 'r') as f:
            data = json.load(f)
        return self.convert(data)
    def convert(self, data: dict) -> dict:
        for level, content in data.items():
            for item in content["blocks"]:
                item[0] = tuple(item[0])
                item[1] = tuple(item[1])
                item[2] = fileLoader.loadImage(item[2])
        return data
    def update(self, level:int):
        self.blocks: list[Block] = [Block(block[0], block[1], block[2]) for block in self.data[level]["blocks"]]
