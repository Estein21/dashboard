from suds.sudsobject import asdict
import json
from bson import json_util

class SudsConverter:
    def __init__(self):
        pass

    def recursive_asdict(self, d):
        """Convert Suds object into serializable format."""
        out = {}
        for k, v in asdict(d).iteritems():
            if hasattr(v, '__keylist__'):
                out[k] = self.recursive_asdict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(self.recursive_asdict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out

    def suds_to_json(self, data):
        return json.dumps(self.recursive_asdict(data), default=json_util.default)
