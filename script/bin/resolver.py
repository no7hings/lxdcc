# coding:utf-8
from flask import Flask

from flask import request


app = Flask(__name__)


@app.route("/resolver")
def resolver():
    result = ''
    kwargs = request.args
    import lxresolver.core as rsv_core
    if 'file' in kwargs:
        k = kwargs['file']
        r = rsv_core.RsvBase.generate_root()
    return result


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=1, port=2526)

