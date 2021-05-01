# coding: utf-8

"""Payload (de)serialization utility functions.

The implemented functions wrap json.loads/json.dumps,
adding support for numpy arrays and scalar types.
"""

import json


def serialize_payload(payload):
    """Serialize a payload to a JSON string."""
    return json.dumps(payload, default=_pack)


def deserialize_payload(payload):
    """Deserialize a payload from a JSON string."""
    return json.loads(payload, object_hook=_unpack)


def _pack(obj):
    """Serialize non-default object types in JSON."""
    if isinstance(obj, np.ndarray):
        spec = [obj.tobytes().hex(), obj.dtype.name, list(obj.shape)]
        return {'__type__': 'np.ndarray', 'value': spec}
    if isinstance(obj, np.generic):
        spec = [obj.tobytes().hex(), obj.dtype.name]
        return {'__type__': 'np.generic', 'value': spec}
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable.")


def _unpack(obj):
    """De-serialize non-default object types in MessagePack."""
    objtype = obj.get('__type__', None)
    if objtype is None:
        return obj
    if objtype == 'np.ndarray':
        data, dtype, shape = obj['value']
        return np.frombuffer(bytes.fromhex(data), dtype=dtype).reshape(shape)
    if objtype == 'np.generic':
        data, dtype = obj['value']
        return np.frombuffer(bytes.fromhex(data), dtype=dtype)[0]
    return obj
