import pygame as py
import json
from objects.block import Block
import fileLoader
import os
class LevelGenerator:
    def __init__(self):
        self.data : dict = self.load_data(os.path.join(os.path.dirname(__file__), "data.json"))

    def load_data(self,file)->dict:
        with open(file, 'r') as f:
            data = json.load(f)
        return self.convert(data)
    
    def convert(self, data: dict) -> dict:
        for level, content in data.items():
            for item in content["blocks"]:
                item[2] = fileLoader.loadImage(item[2])
        return data
    
    def generate_blocks(self, level:str) -> list[Block]:
        self.blocks: list[Block] = [Block(block[0], block[1], block[2]) for block in self.data[level]["blocks"]]
        return self.blocks
    
    def get(self,level:str,key:str):
        try:
         return self.data[level][key]
        except KeyError:
            print("Key not found")
            return None