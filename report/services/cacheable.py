class Cacheable(object):
    def __init__(self, prefix):
        super(Cacheable, self).__init__()
        self.prefix = prefix

    def has_cache(self, key):
        full_key = self.prefix + key
        return False

    def cache(self, key, value, expires_in):
        full_key = self.prefix + key

    def get_cache(self, key):
        full_key = self.prefix + key
