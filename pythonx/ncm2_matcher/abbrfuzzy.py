import re

chcmp_smartcase = lambda a,b: a==b if a.isupper() else a==b.lower()
chcmp_case = lambda a,b: a==b
chcmp_icase = lambda a,b: a.lower()==b.lower()

class Matcher:
    def __init__(self, c='smartcase', key='abbr'):
        if c == 'smartcase':
            self.chcmp = chcmp_smartcase
        elif c == 'icase':
            self.chcmp = chcmp_icase
        else:
            self.chcmp = chcmp_case

        self.key = key

    def match(self, b, m):
        hl = self.fuzzy_match(b, m[self.key])
        if hl is None:
            return False
        m['user_data']['match_key'] = self.key
        m['user_data']['match_highlight'] = hl
        return True

    def get_abbrev(self, s):
        res = []
        if len(s) == 0:
            return res
        # always append 0 so that it should also detects prefix match
        res.append(0)
        for i in range(1, len(s)):
            cp = s[i - 1]
            c = s[i]
            if not c.isalpha():
                if c.isdecimal() and not cp.isdecimal():
                    res.append(i)
                continue
            elif c.isupper():
                res.append(i)
                continue
            elif not cp.isalpha():
                res.append(i)
                continue
            else:
                continue
        return res

    def fuzzy_match(self, b, s):
        if len(b) == 0:
            return []
        abbr = self.get_abbrev(s)
        return self.abbr_fuzzy_match(abbr, b, s, 0)

    def abbr_fuzzy_match(self, abbr, b, s, off):
        for i, p in enumerate(abbr):
            p = p - off
            if p < 0:
                continue
            mcp = self.max_common_prefix(b, s[p:])
            if len(mcp) == len(b):
                return [[off + p, off + p + len(mcp)]]
            # max(mcpl-3, 0) don't fallback too deep for performance
            mcpl = len(mcp)
            for l in range(mcpl, max(mcpl-3, 0), -1):
                b2 = b[l:]
                s2 = s[p + l:]
                m = self.abbr_fuzzy_match(abbr[i+1:], b2, s2, off + p + l)
                if m:
                    return [[off + p, off + p + l]] + m
        return None

    def max_common_prefix(self, b, s):
        res = ''
        for c1, c2 in zip(b, s):
            if self.chcmp(c1, c2):
                res += c1
            else:
                return res
        return res

    def test_abbrev(self, s):
        res = self.get_abbrev(s)
        ls = [' '] * len(s)
        for i in res:
            ls[i] = '^'
        print(s)
        print(''.join(ls))

# if __name__  == '__main__':
#     s = 'abbr_fuzzy_match'
#     b = 'abbrfuzzy'
#     test_abbrev(s)
#     print(fuzzy_match('abbrfuzzy', 'abbr_fuzzy_match', chcmp_smartcase))
#     print(max_common_prefix(b, s))

