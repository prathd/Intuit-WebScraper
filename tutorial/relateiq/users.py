from riq_obj import RIQObject
from riq_base import RIQBase

class User(RIQObject,RIQBase) :
    # Object Attributes
    _id = None
    _name = None
    _email = None
    _email = None

    def __init__(self, _id=None, name=None, email=None, data=None) :
        if data != None :
            self.parse(data)
        elif self.id(_id) != None :
            self.get()

        self.name(name)
        self.email(email)

    @classmethod
    def node(cls) :
        return 'users'

    def parse(self,data) :
        self.id(data.get('id',None))
        self.name(data.get('name',None))
        self.email(data.get('email',None))
        return self

    # Data Payload
    def payload(self) :
        payload = {
            'name' : self.name(),
            'email' : self.email()
        }
        if self.id() :
            payload['id'] = self.id()
        return payload

    # Hybrid
    def id(self,value=None) :
        if value != None :
            self._id = value
        return self._id

    def email(self,value=None) :
        if value != None :
            self._email = value
        return self._email

    def name(self,value=None) :
        if value != None :
            self._name = value
        return self._name