#!/usr/bin/python3
from datetime import datetime, date, time, timezone
import uuid
class BaseModel:
    """
    defines all common attributes/methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """Constructor of a class"""
        if kwargs is not None:
            my_dict = self.__dict__.copy()
            if 'created_at' in my_dict:
                time = datetime.now().isoformat()
                my_dict['created_at'] = datetime.fromisoformat(time)
            if 'updated_at' in my_dict:
                time = datetime.now().isoformat()
                my_dict['updated_at'] = datetime.fromisoformat(time)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        """public instance attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """prints [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {} ".format(self.__class__.__name__, self.id, str(self.__dict__))

    def save(self):
        """
        updates the public instance attribute updated_at with current datetime
        """
        self.__dict__['updated_at'] = datetime.now()

    def to_dict(self):
        """
        returns a dictionary containing all keys of __dict__ of the instance
        """
        self.__dict__['__class__'] = self.__class__.__name__
        return self.__dict__
