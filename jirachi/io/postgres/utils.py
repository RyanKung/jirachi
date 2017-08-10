def wrap_key(x: str) -> str:
    return '%s' % str(x)


def wrap_value(x: str) -> str:
    return "'%s'" % str(x)


def concat(xs: list) -> str:
    return ','.join(xs)


def escape(x: str) -> str:
    x = str(x)
    x.replace("'", '"')
    return x


def get_and_seg(d: dict) -> str:
    return ' and '.join("%s='%s'" % (str(k), str(v)) for k, v in d.items())


def get_pairs(dct):
    return ' , '.join("%s='%s'" % (str(k), str(v)) for k, v in dct.items())
