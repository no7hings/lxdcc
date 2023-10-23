# coding:utf-8
import lxbasic.session.abstracts as bsc_abstracts


class GenerSession(bsc_abstracts.AbsSsnGener):
    def __init__(self, *args, **kwargs):
        super(GenerSession, self).__init__(*args, **kwargs)


class CommandSession(bsc_abstracts.AbsSsnCommand):
    def __init__(self, *args, **kwargs):
        super(CommandSession, self).__init__(*args, **kwargs)


class OptionGenerSession(bsc_abstracts.AbsSsnOptionGener):
    def __init__(self, *args, **kwargs):
        super(OptionGenerSession, self).__init__(*args, **kwargs)
