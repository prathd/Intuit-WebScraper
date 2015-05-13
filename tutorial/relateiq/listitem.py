from riq_obj import RIQObject

class ListItem(RIQObject) :
    # Object Attributes
    _id = None
    _createdDate = None
    _modifiedDate = None
    _name = None
    _listId = None
    _accountId = None
    _contactIds = None
    _fieldValues = None
    _list = None
    _linkedItemIds = None

    def __init__(self,
        _id=None,
        name=None,
        modifiedDate=None,
        createdDate=None,
        listId = None,
        accountId = None,
        fieldValues = None,
        linkedItemIds = None,
        contactIds = None,
        data = None,
        parent=None
    ) :
        if parent == None :
            raise ValueError("List Item Parent must be set")
        else :
            self.list(parent)

        if data != None :
            self.parse(data,parent=parent)
        elif self.id(_id) != None :
            self.get()

        self.name(name)
        self.createdDate(createdDate)
        self.modifiedDate(modifiedDate)
        self.accountId(accountId)
        self.contactIds(contactIds)
        self.fieldValues(fieldValues)
        self.linkedItemIds(linkedItemIds)
        self.listId(listId)

    def node(self) :
        return '/'+self.listId()+'/listitems'

    def endpoint(self) :
        return self.list().endpoint() + self.node()

    def parse(self,data,parent=None) :
        fieldValues = {}
        for field,valueList in data.get('fieldValues',{}).items() :
            fieldValue = []
            if len(valueList) == 1 :
                fieldValue = valueList[0].get('raw',None)
            else :
                for val in valueList :
                    fieldValue.append(val.get('raw',None))
            fieldValues[field] = fieldValue

        self.id(data.get('id',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.createdDate(data.get('createdDate',None))
        self.name(data.get('name',None))
        self.accountId(data.get('accountId',None))
        self.listId(data.get('listId',None))
        self.fieldValues(fieldValues)
        self.list(parent)
        self.contactIds(data.get('contactIds',None))
        self.linkedItemIds(data.get('linkedItemIds',None))
        return self

    # Data Payload
    def payload(self) :
        fieldValues = {}
        for field,value in self.fieldValues().items() :
            valueList = []
            if isinstance(value, basestring) :
                value = [value]
            for val in value :
                valueList.append({'raw':val})
            fieldValues[field] = valueList

        payload = {
            'name' : self.name(),
            'accountId' : self.accountId(),
            'contactIds' : self.contactIds(),
# TODO: See why the list check is failing
#            'listId' : self.listId(),
            'fieldValues' : fieldValues,
            'linkedItemIds' : self.linkedItemIds()
        }
        if self.id() :
            payload['id'] = self.id()

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

    def accountId(self,value=None) :
        if value != None :
            self._accountId = value
        return self._accountId

    def contactIds(self,value=None) :
        if value != None :
            if isinstance(value,basestring) :
                self._contactIds = [value]
            else :
                self._contactIds = value
        return self._contactIds or []

    def listId(self,value=None) :
        if value != None :
            self._listId = value
        if not self._listId and self.list() :
            self._listId = self.list().id()
        return self._listId

    def list(self,value=None) :
        if value != None :
            self._list = value
        return self._list

    def fieldValues(self,value=None) :
        if value != None :
            for key,val in value.items() :
                self.fieldValue(key,val)
        return self._fieldValues or {}

    def fieldValue(self,key,value=None) :
        key = self.list().fieldKey(key)
        if self._fieldValues == None :
            self._fieldValues = {}
        if value != None :
            #value = self.list().fieldOption(value)
            self._fieldValues[key] = value
        #value = self._fieldValues.get(key,None)
        return self.list().fieldValue(key, self._fieldValues.get(key,None))

    def linkedItemIds(self,value=None) :
        if value != None :
            self._linkedItemIds = value
        return self._linkedItemIds or {}

    def linkItem(self,item) :
        if self._linkedItemIds == None :
            self._linkedItemIds = {}
        links = self._linkedItemIds.get(item.itemTypeId())
        if links == None :
            links = []
        if item.id() not in [entry.get('itemId',None) for entry in links] :
            links.append({'itemId':item.id()})
        self._linkedItemIds[item.itemTypeId()] = links
        return self._linkedItemIds
