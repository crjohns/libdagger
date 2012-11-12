class InputMapper:
    """Input mapping class

    >>> mapper = InputMapper()
    >>> mapper.addHandler('/a/b/c/*', lambda x,y: 'a')
    >>> mapper.addHandler('/a/b/c/d', lambda x,y: 'b')
    >>> mapper.addHandler('*', lambda x,y: 'c')
    >>> mapper.mapInput('/a/b/c/d', None)
    'b'
    >>> mapper.mapInput('/a/b/c/e/f/g', None)
    'a'
    >>> mapper.mapInput('/a/b/f/f/', None)
    'c'
    """

    # Map of input sequence pattern to list of handlers
    _handlers = {}

    def __init__(self):
        pass

    def _sanitizePattern(self, pattern):
        """ Sanitize an input pattern

        >>> mapper = InputMapper()
        >>> mapper._sanitizePattern('/a/b/c/d/')
        'a/b/c/d'

        """
        return '/'.join(filter(lambda x: x != '', pattern.split('/')))

    def addHandler(self, pattern, handler):
        pattern = self._sanitizePattern(pattern)
        if pattern in self._handlers.iterkeys():
            self._handlers[pattern].prepend(handler)
        else:
            self._handlers[pattern] = [handler]

    def mapInput(self, pattern, extra):
        plist = self._sanitizePattern(pattern).split('/')

        appendstar = False
        while len(plist) > 0:
            pattern = '/'.join(plist)
            if appendstar:
                pattern += '/*'

            if(pattern in self._handlers.iterkeys()):
                for handler in self._handlers[pattern]:
                    if handler(pattern, extra): 
                        return True

            plist = plist[:-1]
            appendstar = True

        if '*' in self._handlers.iterkeys():
            for handler in self._handlers['*']:
                if handler(pattern, extra):
                    return True

        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
