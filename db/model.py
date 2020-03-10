import copy
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = None
        self.created_at = datetime.utcnow()

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if '_id' in dic:
            setattr(model, 'id', dic['_id'])

        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        return result


class UserModel(BaseModel):
    pass

    def __init__(self):
        super().__init__()
        self.email = None
        self.password = None
        self.roles = []
        self.user_name = ''
        self.company = ''
        self.position = ''
        self.new_message_notified_at = None
