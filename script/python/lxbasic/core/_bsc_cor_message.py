# coding:utf-8
from lxbasic.core import _bsc_cor_raw, _bsc_cor_log


class MsgBaseMtd(object):
    class ArkServer(object):
        Url = 'http://cg-ark.papegames.com'
        Port = 61112
    #
    @classmethod
    def send_mail(cls, addresses, subject, content):
        import requests

        import urllib

        url_p = '{url}:{port}/sendMail?to={addresses}&title={subject}&content={content}&html=0'

        url = url_p.format(
            url=cls.ArkServer.Url,
            port=cls.ArkServer.Port,
            addresses='::'.join(addresses),
            subject=_bsc_cor_raw.auto_encode(subject),
            content=urllib.quote(_bsc_cor_raw.auto_encode(content))
        )

        result = requests.get(url.decode('utf-8')).text

        _bsc_cor_log.LogMtd.trace_method_result(
            'send mail',
            'result is "{}"'.format(result)
        )
    @classmethod
    def send_feishu(cls, addresses, subject, content):
        import requests

        import urllib

        url_p = '{url}:{port}/feishu?email={addresses}&content={content}'

        url = url_p.format(
            url=cls.ArkServer.Url,
            port=cls.ArkServer.Port,
            addresses='::'.join(addresses),
            content=urllib.quote(
                '\n'.join(
                    [
                        _bsc_cor_raw.auto_encode(subject),
                        _bsc_cor_raw.auto_encode(content)
                    ]
                )
            )
        )

        result = requests.get(url.decode('utf-8')).text

        _bsc_cor_log.LogMtd.trace_method_result(
            'send feishu',
            'result is "{}"'.format(result)
        )
