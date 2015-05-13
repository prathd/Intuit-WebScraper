from abc import ABCMeta, abstractmethod
import client as riq
from requests import HTTPError
import math

class RIQChild(object) :
    __metaclass__ = ABCMeta

    _cache = []
    _cache_index = 0
    _page_index = 0
    _page_length = 200
    _fetch_options = {}

    _parent = None
    _object_class = None

    @abstractmethod
    def node(self) :
        pass

    def endpoint(self) :
        return self._parent.endpoint() + self.node()

    def fetchBatch(self,param,values,maxSize) :
        chunks = [values[x:x+maxSize] for x in xrange(0, len(values), maxSize)]
        objects = []
        for i, chunk in enumerate(chunks):
            try:
                self.setFetchOptions({param:','.join(chunk)})
                objects += self.fetchPage()
            except HTTPError, e:
                if e.response.status_code == 414 or e.response.status_code == 413: #max url length is 8192 (2^13). If longer, will give a 414 error.
                    objects += self.fetchBatch(param, chunk, int(math.ceil(maxSize/2)))
                else:
                    raise
        return objects

    def fetchPage(self,index=None,limit=None) :
        if index != None :
            if limit == None :
                limit = self._page_length
            self._fetch_options['_start'] = str(index)
            self._fetch_options['_limit'] =  str(limit)
        data = riq.get(self.endpoint(),self._fetch_options)
        objects = []
        for obj in data.get('objects',[]) :
            objects.append(self._object_class(data=obj,parent=self._parent))
        return objects

    def next(self) :
        if self._cache_index == 0 :
            self._cache = []
            self._cache_index = 0
            self._page_index = 0
        if self._cache_index == len(self._cache) :
            if len(self._cache) not in [0,self._page_length] :
                return None
            del self._cache[:]
            self._cache.extend(self.fetchPage(self._page_index,self._page_length))
            self._page_index += len(self._cache)
            self._cache_index = 0
        if self._cache_index < len(self._cache) :
            obj = self._cache[self._cache_index]
            self._cache_index += 1
            return obj
        else :
            return None

    def resetCache(self) :
        self._cache = []
        self._cache_index = 0
        self._page_index = 0
        self._fetch_options = {}

    def setPageSize(self,limit) :
        self._page_length = limit

    def setFetchOptions(self,options = {}):
        self.resetCache()
        self._fetch_options = options

    def createBatch(self,_objs):
        return_objs = {}
        objs = list(_objs)
        while len(objs) > 0:
            chunk_size = self._page_length if len(objs) > self._page_length else len(objs)
            chunk = objs[0:chunk_size]
            objs = objs[chunk_size:] if chunk_size < len(objs) else []
            batch_objs = self.createBatchHelper('/createBatch',chunk)
            return_objs['successObjects'] = return_objs.setdefault('successObjects',[]) + batch_objs['successObjects']
            return_objs['errorObjects'] =   return_objs.setdefault('errorObjects', [])  + batch_objs['errorObjects']
        return return_objs

    def updateBatch(self,_objs):
        return_objs = {}
        objs = list(_objs)
        while len(objs) > 0:
            chunk_size = self._page_length if len(objs) > self._page_length else len(objs)
            chunk = objs[0:chunk_size]
            objs = objs[chunk_size:] if chunk_size < len(objs) else []
            batch_objs = self.updateBatchHelper('/updateBatch',chunk)
            return_objs['successObjects'] = return_objs.setdefault('successObjects',[]) + batch_objs['successObjects']
            return_objs['errorObjects'] = return_objs.setdefault('errorObjects', []) + batch_objs['errorObjects']
        return return_objs

    def updateBatchHelper(self, endpoint, objs):
        batch_results = riq.put(self.endpoint()+endpoint, {"objects":[obj.payload() for obj in objs]})
        batch_results['successObjects'] = [self._object_class(parent=self._parent,data=obj) for obj in batch_results['successObjects']]
        for errorObj in batch_results['errorObjects']:
            errorObj['object'] = self._object_class(parent=self._parent,data=errorObj['object'])
        return batch_results

    def createBatchHelper(self, endpoint, objs):
        batch_results = riq.post(self.endpoint()+endpoint, {"objects":[obj.payload() for obj in objs]})
        batch_results['successObjects'] = [self._object_class(parent=self._parent,data=obj) for obj in batch_results['successObjects']]
        for errorObj in batch_results['errorObjects']:
            errorObj['object'] = self._object_class(parent=self._parent,data=errorObj['object'])
        return batch_results
