class DeferredMessage(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def __str__(self):
        return 'Message {0}'.format(self.func(*self.args))
