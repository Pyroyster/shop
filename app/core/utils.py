from collections import namedtuple
from flask import current_app, request
from flask.json import dumps


def jsonify(*args, **kwargs):
    indent = None
    separators = (',', ':')

    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] or current_app.debug:
        indent = 2
        separators = (', ', ': ')

    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs
    return current_app.response_class(
        dumps(data, indent=indent, separators=separators) + '\n',
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    ).json


def as_namedtuple(dict_obj):
    key_list, value_list = [], []
    for key, value in dict_obj.items():
        if value is not None:
            key_list.append(key)
            value_list.append(value)
    NamedTuple = namedtuple('NamedTuple', [key for key in key_list])
    return NamedTuple(*value_list)


def get_request_args(as_dict: bool=False):
    data, args = request.get_json(silent=True), request.args.to_dict()
    args_json = dict(data, **args) if data is not None else args
    data = {
        key: value for key, value in args_json.items() if value
    }
    return data if as_dict else as_namedtuple(data)