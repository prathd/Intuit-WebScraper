from abc import ABCMeta, abstractmethod
import client as riq
import json

class RIQObject(object) :
    __metaclass__ = ABCMeta

    _parent = None

    @abstractmethod
    def id(self) :
        pass

    @abstractmethod
    def payload(self) :
        pass

    @abstractmethod
    def parse(cls,data) :
        pass

    @abstractmethod
    def node(cls) :
        pass

    def __str__(self) :
        return json.dumps(self.payload(), sort_keys=True, indent=4, separators=(',', ' : '))

    def __repr__(self) :
        return self.__str__()

    def save(self,options={}) :
        if self.exists() :
            return self.update(options)
        else :
            return self.create(options)

    def create(self,options={}) :
        return self.parse(riq.post(self.endpoint(),self.payload(),options))

    def get(self,options={}) :
        return self.parse(riq.fetch(self.endpoint() + '/' + self.id(),options))

    def update(self,options={}) :
        return self.parse(riq.put(self.endpoint() + '/' + self.id(),self.payload(),options))

    def delete(self,options={}) :
        return riq.delete(self.endpoint() + '/' + self.id(),options)

    def exists(self) :
        if self.id() == None :
            return False
        return riq.fetch(self.endpoint() + '/' + self.id()) != {}
