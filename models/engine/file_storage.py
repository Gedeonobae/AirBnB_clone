#!/usr/bin/python3
import os
import json
import datetime
class FileStorage:
        """class to serializes and deserializes the base class"""
        script_dir = os.path.dirname(__file__)
        __file_path = os.path.join(script_dir, 'file.json')
        __objects = {}

        def all(self):
                """return eturns the dictionary __objects"""
                return FileStorage.__objects

        def new(self, obj):
                """sets in the dictionary obj"""
                key = "{}.{}".format(type(obj).__name__, obj.id)
                FileStorage.__objects[key] = obj

        def save(self):
                """serializes __objects to the json file"""
                with open(FileStorage.__file_path, 'w') as file:
                        d = {k: v.to_dict()
                             for k, v in FileStorage.__objects.items()}
                        json.dump(d, file)
        def classes(self):
                """Returns a dictionary of valid classes and their references."""
                from models.base_model import BaseModel

                classes = {"BaseModel":BaseModel}
                return classes

        def reload(self):
                """deserializes the json file to __objects"""
                if not self.__file_path:
                        return
                with open(FileStorage.__file_path) as file:
                        obj_dict = json.load(file)
                        obj_dict = {k: self.classes()[v["__class__"]](**v)
                                    for k, v in obj_dict.items()}
                        FileStorage.__objects = obj_dict

        def attributes(self):
                """Returns valid attributes and their types for classname."""
                attributes = {
                        "BaseModel":
                        {"id": str,
                         "created_at": datetime.datetime,
                         "updated_at": datetime.datetime}
                }
                return attributes
