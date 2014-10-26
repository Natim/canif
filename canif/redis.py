# -*- coding: utf-8 -*-
import json
import redis

default_redis_settings = dict(
    host="localhost",
    port=6379,
    db=1
)


class RedisBackend(object):
    def __init__(self, settings=None):
        if settings is None:
            settings = default_redis_settings
        self.connection = redis.StrictRedis(**settings)

    def set_variable(self, key, value):
        return self.connection.set(
            "insee_variable:%s" % key.lower(),
            json.dumps(value))

    def get_variable(self, key):
        var = self.connection.get("insee_variable:%s" % key.lower())
        if var:
            return json.loads(var.decode('utf-8'))

    def get_variables(self, keys):
        entries = self.connection.mget(
            *["insee_variable:%s" % key.lower() for key in keys if key]
        )
        return [json.loads(entry.decode('utf-8'))
                for entry in entries if entry]

    def search_variables(self, query):
        query = query.split()[0].lower()
        keys = self.connection.keys("insee_variable:*")
        entries = []
        if keys:
            entries = self.connection.mget(*keys)
        results = []
        for entry in entries:
            entry = json.loads(entry.decode('utf-8'))
            if query in entry['var_id'].lower() or \
               query in entry['var_lib'].lower() \
               or query in entry['var_lib_long'].lower():
                results.append(entry)
        return results

    def set_commune(self, key, value):
        return self.connection.set(
            "insee_commune:%s" % key.lower(),
            json.dumps(value))

    def get_commune(self, key):
        var = self.connection.get("insee_commune:%s" % key.lower())
        if var:
            return json.loads(var.decode('utf-8'))

    def get_communes(self, keys):
        entries = self.connection.mget(
            *["insee_commune:%s" % key.lower() for key in keys if key]
        )
        return [json.loads(entry.decode('utf-8'))
                for entry in entries if entry]

    def search_communes(self, query):
        query = query.split()[0].lower()
        keys = self.connection.keys("insee_commune:*")
        entries = []
        if keys:
            entries = self.connection.mget(*keys)
        results = []
        for entry in entries:
            entry = json.loads(entry.decode('utf-8'))
            if query in entry['codgeo'].lower() or \
               query in entry['libgeo'].lower():
                results.append(entry)
        return results

    def set_data(self, var_lib, codgeo, obj):
        return self.connection.set(
            "insee_data_%s:%s" % (var_lib, codgeo),
            obj['value'])

    def get_data(self, var_lib, codgeo):
        data = self.connection.get(
            "insee_data_%s:%s" % (var_lib, codgeo))
        return {"value": data.decode('utf-8')}
