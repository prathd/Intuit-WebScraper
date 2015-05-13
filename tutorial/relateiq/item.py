from riq_obj import RIQObject

class Item(RIQObject) :
    # Object Attributes
    _id = None
    _createdDate = None
    _modifiedDate = None
    _name = None
    _itemTypeId = None
    _externalId = None
    _fieldValues = {}
    _itemType = None

    def __init__(self,
        _id=None, 
        name=None, 
        modifiedDate=None, 
        createdDate=None, 
        itemTypeId = None,
        externalId = None,
        fieldValues = None,
        data=None,
        parent=None
    ) :
        if parent == None :
            raise ValueError("Item Parent must be set")
        else :
            self.itemType(parent)

        if data != None :
            self.parse(data,parent=parent)

        self.id(None if _id == None else str(_id))
        self.name(name)
        self.createdDate(createdDate)
        self.modifiedDate(modifiedDate)
        self.externalId(externalId)
        self.fieldValues(fieldValues)
        self.itemTypeId(itemTypeId)

    def node(self) :
        return '/'+self.itemTypeId()+'/items'

    def endpoint(self) :
        return self.itemType().endpoint() + self.node()

    def parse(self,data,parent=None) :
        fieldValues = {}
        for field,valueList in data.get('fieldValues',{}).items() :
            fieldValue = []
            #print "value list: "+valueList
            if len(valueList) == 1 :
                fieldValue = valueList[0]['raw']
            else :
                for val in valueList :
                    fieldValue.append(val['raw'])
            fieldValues[field] = fieldValue

        self.id(data.get('id',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.createdDate(data.get('createdDate',None))
        self.name(data.get('name',None))
        self.externalId(data.get('externalId',None))
        self.itemTypeId(data.get('itemTypeId',None))
        self.fieldValues(fieldValues)
        self.itemType(parent)

        return self

    # Data Payload
    def payload(self) :
        fieldValues = {}
        for field,value in self.fieldValues().items() :
            valueList = []
            # if isinstance(value, basestring) :
            #     value = [value]
            value = value if isinstance(value, list) else [value]
            for val in value :
                valueList.append({'raw':val})
            fieldValues[field] = valueList

        payload = {
            'name' : self.name(),
            'externalId' : self.externalId(),
# TODO: See why the itemType check is failing
#            'itemTypeId' : self.itemTypeId(),
            'fieldValues' : fieldValues
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

    def externalId(self,value=None) :
        if value != None :
            self._externalId = value
        return self._externalId

    def itemTypeId(self,value=None) :
        if value != None :
            self._itemTypeId = value
        if not self._itemTypeId and self.itemType() :
            self._itemTypeId = self.itemType().id()
        return self._itemTypeId

    def itemType(self,value=None) :
        if value != None :
            self._itemType = value
        return self._itemType

    def fieldValues(self,value=None) :
        if value != None :
            self._fieldValues = value
        return self._fieldValues or {}
