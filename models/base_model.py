#!/usr/bin/python3
from datetime import datetime, date, time, timezone
import uuid
class BaseModel:
    """
    defines all common attributes/methods for other classes
    """
    def __init__(self):
    """Initialize the uuid
    assign with the current datetime when an instance is created
    assign with the current datetime when an instance is updated
    """
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
