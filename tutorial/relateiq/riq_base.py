from abc import ABCMeta, abstractmethod
import client as riq
from requests import HTTPError
import math

class RIQBase(object):
    __metaclass__ = ABCMeta

    _cache = []
    _cache_index = 0
    _page_index = 0
    _page_length = 200
    _fetch_options = {}

    @classmethod
    @abstractmethod
    def node(cls) :
        pass

    @classmethod
    def endpoint(cls) :
        return cls.node()

    @classmethod
    def fetchBatch(cls,param,values,maxSize) :
        chunks = [values[x:x+maxSize] for x in xrange(0, len(values), maxSize)]
        objects = []
        for i, chunk in enumerate(chunks):
            try:
                cls.setFetchOptions({param:','.join(chunk)})
                objects += cls.fetchPage()
            except HTTPError, e:
                if e.response.status_code == 414 or e.response.status_code == 413: #max url length is 8192 (2^13). If longer, will give a 414 error.
                    objects += cls.fetchBatch(param, chunk, int(math.ceil(maxSize/2)))
                else:
                    raise
        return objects

    @classmethod
    def fetchPage(cls,index=0,limit=None) :
        if limit == None :
            limit = cls._page_length
        cls._fetch_options['_start'] = str(index)
        cls._fetch_options['_limit'] =  str(limit)
        data = riq.get(cls.endpoint(),cls._fetch_options)
        objects = []
        for obj in data.get('objects',[]) :
            objects.append(cls(data=obj))
        return objects

    @classmethod
    def next(cls) :
        if cls._cache_index == 0 :
            cls._cache = []
            cls._cache_index = 0
            cls._page_index = 0
        if cls._cache_index == len(cls._cache) :
            if len(cls._cache) not in [0,cls._page_length] :
                return None
            del cls._cache[:]
            cls._cache.extend(cls.fetchPage(cls._page_index,cls._page_length))
            cls._page_index += len(cls._cache)
            cls._cache_index = 0
        if cls._cache_index < len(cls._cache) :
            obj = cls._cache[cls._cache_index]
            cls._cache_index += 1
            return obj
        else :
            return None

    @classmethod
    def resetCache(cls) :
        cls._fetch_options = {}
        cls._cache = []
        cls._cache_index = 0
        cls._page_index = 0
        cls._last_modified_date = None

    @classmethod
    def setPageSize(cls,limit) :
        cls._page_length = limit

    @classmethod
    def setFetchOptions(cls, options = {}):
        cls.resetCache()
        cls._fetch_options = options

    @classmethod
    def createBatch(cls,objs):
        return_objs = {}
        while len(objs) > 0:
            chunk_size = cls._page_length if len(objs) > cls._page_length else len(objs)
            chunk = objs[0:chunk_size]
            objs = objs[chunk_size:] if chunk_size < len(objs) else []
            batch_objs = cls.createBatchHelper('/createBatch',chunk)
            return_objs['successObjects'] = return_objs.setdefault('successObjects',[]) + batch_objs['successObjects']
            return_objs['errorObjects'] =   return_objs.setdefault('errorObjects', [])  + batch_objs['errorObjects']
        return return_objs

    @classmethod
    def updateBatch(cls,objs):
        return_objs = {}
        while len(objs) > 0:
            chunk_size = cls._page_length if len(objs) > cls._page_length else len(objs)
            chunk = objs[0:chunk_size]
            objs = objs[chunk_size:] if chunk_size < len(objs) else []
            batch_objs = cls.updateBatchHelper('/updateBatch',chunk)
            return_objs['successObjects'] = return_objs.setdefault('successObjects',[]) + batch_objs['successObjects']
            return_objs['errorObjects'] =   return_objs.setdefault('errorObjects', [])  + batch_objs['errorObjects']
        return return_objs

    @classmethod
    def updateBatchHelper(cls, endpoint, objs):
        batch_results = riq.put(cls.endpoint()+endpoint, {"objects":[obj.payload() for obj in objs]})
        batch_results['successObjects'] = [cls(data=obj) for obj in batch_results['successObjects']]
        for errorObj in batch_results['errorObjects']:
            errorObj['object'] = cls(data=errorObj['object'])
        return batch_results

    @classmethod
    def createBatchHelper(cls, endpoint, objs):
        batch_results = riq.post(cls.endpoint()+endpoint, {"objects":[obj.payload() for obj in objs]})
        batch_results['successObjects'] = [cls(data=obj) for obj in batch_results['successObjects']]
        for errorObj in batch_results['errorObjects']:
            errorObj['object'] = cls(data=errorObj['object'])
        return batch_results

    @classmethod
    def dummyClassMethod(cls):
        print
