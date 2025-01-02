class Makeable:
    @classmethod
    def make(cls, *args, **kwargs):
        return cls(*args, **kwargs)
