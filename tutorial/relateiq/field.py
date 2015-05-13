from riq_obj import RIQObject

class Field(RIQObject) :
    # Object Attributes
    _id = None
    _createdDate = None
    _modifiedDate = None
    _name = None
    _itemTypeId = None
    _itemtype = None
    _fieldType = None
    _dateisDefaultNow = None
    _isEditable = None
    _isMultiSelect = None
    _optionMap = None
    _listOptions = None

    def __init__(self, 
        _id=None, 
        name=None, 
        modifiedDate=None, 
        createdDate=None, 
        itemTypeId = None,
        fieldType = None,
        dateisDefaultNow = None,
        isEditable = None,
        isMultiSelect = None,
        listOptions = None,
        data=None,
        parent = None
    ) :
        if parent == None :
            raise ValueError("Item Parent must be set")
        else :
            self.itemType(parent)
        
        if data != None :
            self.parse(data,parent=parent)
        elif self.id(_id) != None :
            self.get()

        self.modifiedDate(modifiedDate)
        self.createdDate(createdDate)
        self.name(name)
        self.fieldType(fieldType)
        self.dateisDefaultNow(dateisDefaultNow)
        self.isEditable(isEditable)
        self.isMultiSelect(isMultiSelect)
        self.listOptions(listOptions)
        self.itemTypeId(itemTypeId)
        self.itemType(parent)

    def node(self) :
        return '/'+self.itemTypeId()+'/fields'

    def endpoint(self) :
        return self.itemType().endpoint() + self.node()

    def parse(self,data,parent=None) :
        listOptions = {}
        for option in data.get('listOptions',[]) :
            listOptions[option['id']] = option.get('display',None)

        self.id(data.get('id',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.createdDate(data.get('createdDate',None))
        self.name(data.get('name',None))
        self.fieldType(data.get('fieldType',None))
        self.dateisDefaultNow(data.get('dateisDefaultNow',None))
        self.isEditable(data.get('isEditable',None))
        self.isMultiSelect(data.get('isMultiSelect',None))
        self.listOptions()
        self.itemTypeId(data.get('itemTypeId',None))
        self.itemType(parent)

        return self
        
    # Data Payload
    def payload(self) :
        listOptions = {}
        for pos,display in listOptions :
            break
        payload = {
            'name' : self.name(),
            'fieldType' : self.fieldType(),
            'dateisDefaultNow' : self.dateisDefaultNow(),
            'isEditable' : self.isEditable(),
            'isMultiSelect' : self.isMultiSelect(),
            'listOptions' : self.listOptions()
        #    'itemTypeId' : self.itemTypeId()
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

    def itemTypeId(self,value=None) :
        if value != None :
            self._itemTypeId = value
        if not self._itemTypeId and self.itemType() :
            self._itemTypeId = self.itemType().id()
        return self._itemTypeId

    def itemType(self,value=None) :
        if value != None :
            self._itemtype = value
        return self._itemtype

    def name(self,value=None) :
        if value != None :
            self._name = value
        return self._name

    def fieldType(self,value=None) :
        if value != None :
            self._fieldType = value
        return self._fieldType
        
    def dateisDefaultNow(self,value=None) :
        if value != None :
            self._dateisDefaultNow = value
        return self._dateisDefaultNow
        
    def isEditable(self,value=None) :
        if value != None :
            self._isEditable = value
        return self._isEditable
        
    def isMultiSelect(self,value=None) :
        if value != None :
            self._isMultiSelect = value
        return self._isMultiSelect
        
    def listOptions(self,value=None) :
        if value != None :
            self._listOptions = value
        return self._listOptions or []
