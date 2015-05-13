from riq_obj import RIQObject
from riq_base import RIQBase

class Account(RIQObject,RIQBase) :
    # Object Attributes
    _id = None
    _name = None
    _modifiedDate = None

    def __init__(self, _id=None, name=None, modifiedDate=None, data=None) :
        if data != None :
            self.parse(data)
        elif self.id(_id) != None :
            self.get()

        self.name(name)
        self.modifiedDate(modifiedDate)

    @classmethod
    def node(cls) :
        return 'accounts'

    def parse(self,data) :
        self.id(data.get('id',None))
        self.name(data.get('name',None))
        self.modifiedDate(data.get('modifiedDate',None))
        return self

    # Data Payload
    def payload(self) :
        payload = {
            'name' : self.name()
        }
        if self.id() :
            payload['id'] = self.id()
        return payload

    # Hybrid
    def id(self,value=None) :
        if value != None :
            self._id = value
        return self._id

    def modifiedDate(self,value=None) :
        if value != None :
            self._modifiedDate = value
        return self._modifiedDate

    def name(self,value=None) :
        if value != None :
            self._name = value
        return self._name