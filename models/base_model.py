#!/usr/bin/python3
"""
module base_model
"""
import uuid
from datetime import datetime, date, time, timezone
from models import storage

class BaseModel:
    """
    defines all common attributes/methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """Constructor of a class"""
        if kwargs is not None:
            my_dict = self.__dict__.copy()
            if 'created_at' in my_dict:
                my_dict['created_at'] = datetime.now()
            if 'updated_at' in my_dict:
                my_dict['updated_at'] = datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)

    def __str__(self):
        """prints [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {} ".format(self.__class__.__name__, self.id, str(self.__dict__))

    def save(self):
        """
        updates the public instance attribute updated_at with current datetime
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys of __dict__ of the instance
        """
        dic = vars(self)
        dic['__class__'] = self.__class__.__name__
        dic['updated_at'] = self.updated_at.isoformat()
        dic['created_at'] = self.created_at.isoformat()
        return vars(self)
