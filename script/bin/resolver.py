# coding:utf-8
from flask import Flask

from flask import request

from lxresolver import commands

app = Flask(__name__)


@app.route("/resolver")
def resolver():
    result = ''
    kwargs = request.args
    if 'file' in kwargs:
        k = kwargs['file']
        r = commands.get_resolver()
    return result


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=1, port=2526)

