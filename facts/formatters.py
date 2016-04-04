import math

__all__ = ['mark']


class MetricType(int):

    base = 1000
    suffix = ''

    @property
    def human(self):
        value = abs(self)
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols, start=1):
            prefix[s] = pow(self.base, i)
        for s in reversed(symbols):
            if value >= prefix[s]:
                value = value / prefix[s]
                return self.format(value, s, self)
        return self.format(value, '', self)

    @classmethod
    def format(cls, value, prefix, origin=None):
        origin = origin or value
        a = '-' if origin < 0 else ''
        b = '%i' % value if int(value) == value else '%.2f' % value
        c = '%s%s' % (prefix, cls.suffix)
        if c:
            return '%s%s %s' % (a, b, c)
        return '%s%s' % (a, b)


class BytesType(MetricType):

    base = 1024
    suffix = 'B'


class PercType(float):

    @property
    def human(self):
        if int(self) == self:
            return '%i%%' % self
        return '%.2f%%' % self


class TimeType(float):

    @property
    def human(self):
        d, h, m, s = 0, 0, 0, 0
        m = math.floor(self / 60)
        s = self % 60
        if m > 59:
            h = math.floor(m / 60)
            m = m % 60
        if h > 24:
            d = math.floor(h / 24)
            h = h % 24

        # result = ['P']
        result = []
        if d:
            result.append('P')
            result.append('%iD' % d)
        result.append('T')

        if h:
            result.append('%02iH' % h)
        if m:
            result.append('%02iM' % m)
        if s:
            result.append('%02iS' % int(s))
        return ''.join(result)


def mark(obj, type=None):
    if type in ('metric',):
        return MetricType(obj)
    if type in ('bytes',):
        return BytesType(obj)
    if type in ('percentage',):
        return PercType(obj)
    if type in ('duration',):
        return TimeType(obj)
    return obj
