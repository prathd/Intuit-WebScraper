from riq_obj import RIQObject
from riq_base import RIQBase

class Contact(RIQObject,RIQBase) :
    # Object Attributes
    _id = None
    _modifiedDate = None
    _properties = None

    def __init__(self,
        _id=None,
        name=None,
        email=None,
        phone=None,
        address=None,
        company=None,
        title=None,
        properties=None,
        modifiedDate=None,
        twhan=None,
        data=None
    ):
        if data != None :
            self.parse(data)
        elif self.id(_id) != None :
            self.get()

        self.properties(properties)
        self.name(name)
        self.email(email)
        self.phone(phone)
        self.address(address)
        self.company(company)
        self.title(title)
        self.modifiedDate(modifiedDate)
        self.twhan(twhan)

    @classmethod
    def node(cls) :
        return 'contacts'

    @classmethod
    def fetchByIds(cls,contactIds) :
        contactsById = {}
        for contact in cls.fetchBatch('_ids',contactIds,cls._page_length) :
            contactsById[contact.id()] = contact
        cls.setFetchOptions()
        return contactsById

    def parse(self,data) :
        self.id(data.get('id',None))
        self.modifiedDate(data.get('modifiedDate',None))
        self.properties(data.get('properties',{}))
        return self

    # Data Payload
    def payload(self) :
        payload = {'properties' : self._properties }
        if self.modifiedDate() :
            payload['modifiedDate'] = self.modifiedDate()
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

    def properties(self,value=None) :
        if value != None :
            self._properties = value
        return self._properties or {}

    # value should either be a string or a list of strings
    # returns: if multiple values exist for key, a list of strings of values
    #          if a single value exists, return the single string value (not in a list)
    #          if no values exist, return None
    def property(self,key,value=None) :
        if self._properties == None :
            self._properties = {}

        # set value if passed in
        if value != None :
            new_values = value if isinstance(value, list) else [value]
            existing_values = set([cur['value'] for cur in self._properties.get(key,[])])
            # do not update a value if it already exists in order to keep any existing metadata
            values_to_add = [{'value':val} for val in new_values if val not in existing_values]
            values_to_keep = [val for val in self._properties.get(key,[]) if val['value'] in new_values]
            self._properties[key] = values_to_add + values_to_keep

        # get value to return
        retval = [cur['value'] for cur in self._properties.get(key,[])]

        # return scalar if only one item, list otherwise (or None if empty)
        if len(retval) == 0 :
            return None
        elif len(retval) == 1 :
            return retval[0]
        else :
            return retval

    # value should be of the form: [{'value':string , 'metadata':{string:string}}]
    # returns a list of objects if multiple values, a single object if one value, or None
    # if there are no values
    def propertyWithMetadata(self,key,value=None):
        if self._properties == None :
            self._properties = {}

        if value != None :
            values = value if isinstance(value, list) else [value]
            # update even if key,value pair already exists. If existing metadata should be preserved,
            # it should be included in the passed in object
            self._properties[key] = values

        retval = self._properties.get(key,[])
        if len(retval) == 0 :
            return None
        elif len(retval) == 1 :
            return retval[0]
        else :
            return retval


    def name(self,value=None) :
        if value != None :
            self.property('name',value)
        return self.property('name')

    def email(self,value=None) :
        if value != None :
            self.property('email',value)
        return self.property('email')

    def phone(self,value=None) :
        if value != None :
            self.property('phone',value)
        return self.property('phone')

    def address(self,value=None) :
        if value != None :
            self.property('address',value)
        return self.property('address')

    def company(self,value=None) :
        if value != None :
            self.property('company',value)
        return self.property('company')

    def title(self,value=None) :
        if value != None :
            self.property('title',value)
        return self.property('title')

    def twhan(self,value=None) :
        if value != None :
            self.property('twhan',value)
        return self.property('twhan')
