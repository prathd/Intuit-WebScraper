from riq_obj import RIQObject
from riq_base import RIQBase
from listitems import ListItems
from listitem import ListItem

# TODO: Add version, externalId, category
# TODO: Payload exception if missing required fields


class List(RIQObject,RIQBase) :
    # Object Attributes
    _id = None
    _modifiedDate = None
    _title = None
    _listType = None
    _fields = None

    def __init__(self, _id=None, title=None, modifiedDate=None, fields=None, data=None) :
        if data != None :
            self.parse(data)
        elif self.id(_id) != None :
            self.get()

        self.title(title)
        self.modifiedDate(modifiedDate)
        self.fields(fields)
    
        self.ListItems = ListItems(self)

    @classmethod
    def node(cls) :
        return 'lists'

    def parse(self,data) :
        self.id(data.get('id',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.title(data.get('title',None))
        self.listType(data.get('listType',None))
        self.fields(data.get('fields',None))
        return self

    # Data Payload
    def payload(self) :
        payload = {
            'title' : self.title(),
            'fields' : self.fields()
        }
        if self.id() != None :
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

    def title(self,value=None) :
        if value != None :
            self._title = value
        return self._title

    def listType(self,value=None) :
        if value != None :
            self._listType = value
        return self._listType

    def fields(self,value=None) :
        if value != None :
            self._fields = value
        return self._fields or []

    # Sub Endpoints
    def ListItem(self,*args,**kwargs) :
        kwargs['parent'] = self
        return ListItem(*args,**kwargs)

    # Lookup Functions
    # Convert a field name to a field key (eg "Status" --> "0")
    def fieldKey(self,name) :
        #if the "name" is already a key, just return it
        for field in self.fields() :
            if field.get('id',None) == name :
                return name
        #otherwise, find the field whose "name" is name, and return that field's id
        for field in self.fields() :
            if field.get('name',None) == name :
                return field.get('id',name)
        #print "[WARN] Field is a Linked Field and has no Schema in List: " + name
        return name

    def fieldValue(self,key,value=None) :
        for field in self.fields() :
            if field.get('id',None) == key :
                return key
        for field in self.fields() :
            if field.get('display',None) == key :
                return field.get('id',key)
        return key

    def fieldOption(self,key,value=None) :
        for field in self.fields() :
            if field.get('id',None) == key :
                return key
        for field in self.fields() :
            if field.get('display',None) == key :
                return field.get('id',key)
        return key