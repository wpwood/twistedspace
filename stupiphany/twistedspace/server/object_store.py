class ObjectStore(object):
    def __init__(self, initial_values = []):
        self.store = initial_values

    def size(self):
        return len(self.store)

    def put(self, value):
        self.store.append(value)

    def get(self, request):
        for o in self.store:
            matcher = ObjectMatcher(o)
            if matcher.matches(request):
                value = o
                self.store.remove(o)
                return o
        else:
            return {}

    def __str__(self):
        return str(self.store)

class ObjectMatcher(object):
    def __init__(self, to_be_matched):
        self.tbm = to_be_matched

    def matches(self, test):
        for key in list(test):
            if (key not in self.tbm or self.tbm[key] != test[key]):
                return False
        return True