import json


class JsonSerializer(json.JSONEncoder):
    def default(self, obj):
        #if type(obj) is DeviceType:
        #    return {"__enum__": str(obj)}
        if hasattr(obj, 'working_serializer'):
            return obj.working_serializer()
        else:
            return json.JSONEncoder.default(self, obj)
