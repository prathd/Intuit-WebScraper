import client as riq

class Organization(object):
    _id = None
    _name = None

    def __init__(self, data=None):
        if data is not None:
            self.parse(data)

    def parse(self, data):
        self.id(data.get('id', None))
        self.name(data.get('name', None))

    def payload(self):
        pass

    def id(self, value=None):
        if value is not None:
            self._id = value
        return self._id

    def name(self, value=None):
        if value is not None:
            self._name = value
        return self._name

    def fetch(self):
        self.parse(riq.get("organizations"))
        return self