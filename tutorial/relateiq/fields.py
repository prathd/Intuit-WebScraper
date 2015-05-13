from riq_child import RIQChild
from field import Field

class Fields(RIQChild) :
    _cache = []
    _cache_index = 0
    _page_index = 0
    _page_length = 50

    _parent = None

    def __init__(self, itemtype) :
        self._parent = itemtype
        self._object_class = Field

    def node(self) :
        return '/'+self._parent.id()+'/fields'