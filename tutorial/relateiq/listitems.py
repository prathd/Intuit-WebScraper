from riq_child import RIQChild
from listitem import ListItem

class ListItems(RIQChild) :
    _cache = []
    _cache_index = 0
    _page_index = 0
    _page_length = 200

    _parent = None

    def __init__(self, _list) :
        self._parent = _list
        self._object_class = ListItem

    def node(self) :
        return '/'+self._parent.id()+'/listitems'