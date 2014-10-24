from limpyd import model

redis_settings = dict(
    host="localhost",
    port=6379,
    db=1
)

database = model.RedisDatabase(**redis_settings)


class Variables(model.RedisModel):
    """INSEE Variables: The list of existing variables"""
    database = database
    namespace = "insee"

    var_id = model.PKField()
    var_lib = model.InstanceHashField()
    var_lib_long = model.InstanceHashField()
    annee = model.InstanceHashField()
    source = model.InstanceHashField()


class Communes(model.RedisModel):
    database = database
    namespace = "insee"

    codgeo = model.PKField()
    libgeo = model.InstanceHashField()
