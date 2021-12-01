# coding:utf-8


a = {
    "A": {
        "A": "A"
    }
}

b = {
    "A": {
        "A": {
            'A': "A"
        }
    },
    "B": {
        "B": "B"
    }
}


def set_layer_load():
    def _rcs_fnc(old_raw_, new_raw_):
        for k, v in new_raw_.items():
            if k in old_raw_:
                if isinstance(v, dict):
                    _old_raw = old_raw_[k]
                    _new_raw = new_raw_[k]
                    _rcs_fnc(_old_raw, _new_raw)
                else:
                    if isinstance(old_raw_, dict):
                        old_raw_[k] = v
            else:
                old_raw_[k] = v

    old_raw = a
    new_raw = b
    _rcs_fnc(a, b)


set_layer_load()

print a
