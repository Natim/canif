# -*- coding: utf-8 -*-
from __future__ import absolute_import
from elasticsearch import Elasticsearch


class ElasticsearchBackend(object):
    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        self.es = Elasticsearch(**settings)

    def set_variable(self, key, value):
        res = self.es.index("insee", doc_type="variable",
                            id=key.lower(), body=value)
        return res['created']

    def get_variable(self, key):
        res = self.es.get(index="insee", doc_type='variable',
                          id=key.lower())
        return res['_source']

    def get_variables(self, keys):
        res = self.es.mget(index="insee", doc_type="variable", body={
            "ids": [k.lower() for k in keys]
        })
        results = [d['_source'] for d in res['docs'] if '_source' in d]
        return results

    def search_variables(self, query):
        res = self.es.search(
            index="insee", doc_type="variable",
            body={"query": {"match": {"_all": query.lower()}}}
        )
        return [hit['_source'] for hit in res['hits']['hits']]

    def set_commune(self, key, value):
        res = self.es.index("insee", doc_type="commune",
                            id=key.lower(), body=value)
        return res['created']

    def get_commune(self, key):
        res = self.es.get(index="insee", doc_type='commune',
                          id=key.lower())
        return res['_source']

    def get_communes(self, keys):
        res = self.es.mget(index="insee", doc_type="commune", body={
            "ids": [k.lower() for k in keys]
        })
        results = [d['_source'] for d in res['docs'] if '_source' in d]
        return results

    def search_communes(self, query):
        res = self.es.search(
            index="insee", doc_type="commune",
            body={"query": {"match": {"_all": query.lower()}}}
        )
        return [hit['_source'] for hit in res['hits']['hits']]

    def set_data(self, var_lib, codgeo, value):
        res = self.es.index("insee", doc_type="data",
                            id="%s_%s" % (var_lib.lower(), codgeo), body=value)
        return res['created']

    def get_data(self, var_lib, codgeo):
        res = self.es.get(index="insee", doc_type='data',
                          id="%s_%s" % (var_lib.lower(), codgeo))
        return res['_source']
