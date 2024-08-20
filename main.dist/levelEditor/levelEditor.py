import pygame as py
import json
import fileLoader
import os
class LevelGenerator:
    def __init__(self):
        self.data : dict = self.load_data(os.path.join(os.path.dirname(__file__), "data.json"))

    def load_data(self,file)->dict:
        with open(file, 'r') as f:
            data = json.load(f)
        mydata = self.convert_to_loadImage(data,"blocks",2)
        return mydata
    
    def convert_to_loadImage(self, data: dict, key:str, index:int) -> dict:
        for level, content in data.items():
            for item in content[key]:
                item[index] = fileLoader.loadImage(item[index])
        return data
    
    def generate_object(self, level:str, cls ,key:str) :
        self.myobject: list[cls] = [cls(*item) for item in self.data[level][key]]
        return self.myobject
    

    def get(self,level:str,key:str):
        try:
         return self.data[level][key]
        except KeyError:
            print("Key not found")
            return None