from riq_obj import RIQObject
from riq_base import RIQBase
from items import Items
from item import Item
from fields import Fields
from field import Field

# TODO: Add version, externalId, category
# TODO: Payload exception if missing required fields


class ItemType(RIQObject,RIQBase) :
    # Object Attributes
    _id = None
    _name = None
    _createdDate = None
    _modifiedDate = None
    _externalId = None

    Items = None
    Fields = None

    def __init__(self, _id=None, name=None, modifiedDate=None, createdDate=None, externalId=None, data=None) :
        if data != None :
            self.parse(data)
        elif self.id(_id) != None :
            self.get()

        self.name(name)
        self.createdDate(createdDate)
        self.modifiedDate(modifiedDate)
        self.externalId(externalId)

        self.Items = Items(self)
        self.Fields = Fields(self)

    @classmethod
    def node(cls) :
        return 'itemtypes'

    def parse(self,data) :
        self.id(data.get('id',None))
        self.name(data.get('name',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.createdDate(data.get('createdDate',None))
        return self

    # Data Payload
    def payload(self) :
        payload = {
            'name' : self.name()
        }
        if self.id() :
            payload['id'] = self.id()
        if self.externalId() :
            payload['externalId'] = self.externalId()
        return payload

    # Hybrid
    def id(self,value=None) :
        if value != None :
            self._id = value
        return self._id

    def createdDate(self,value=None) :
        if value != None :
            self._createdDate = value
        return self._createdDate

    def modifiedDate(self,value=None) :
        if value != None :
            self._modifiedDate = value
        return self._modifiedDate

    def name(self,value=None) :
        if value != None :
            self._name = value
        return self._name

    def externalId(self, value=None):
        if value != None:
            self._externalId = value
        return self._externalId

    def schema(self) :
        self._schema = {}
        while True :
            field = self.Fields.next()
            if field != None :
                self._schema[field.name()] = field
            else :
                break
        return self._schema

    def field(self,name) :
        schema = self.schema()
        return schema.get(name,self.Field(name=name))

    # Sub Endpoints
    def Item(self,*args,**kwargs) :
        kwargs['parent'] = self
        return Item(*args,**kwargs)

    def Field(self,*args,**kwargs) :
        kwargs['parent'] = self
        return Field(*args,**kwargs)