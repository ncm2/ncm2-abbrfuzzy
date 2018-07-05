import re

def get_abbrev(s):
    res = []
    if len(s) == 0:
        return res
    # always append 0 so that it should also detects prefix match
    res.append(0)
    for i in range(1, len(s)):
        cp = s[i - 1]
        c = s[i]
        if not c.isalpha():
            continue
        elif not cp.isalpha():
            res.append(i)
            continue
        elif cp.islower() and c.isupper():
            res.append(i)
            continue
    return res

def fuzzy_match(b, s):
    abbr = get_abbrev(s)
    b = b.lower()
    s = s.lower()
    return abbr_fuzzy_match(abbr, b, s, 0)

# n
def abbr_fuzzy_match(abbr, b, s, off):
    for i, p in enumerate(abbr):
        p = p - off
        if p < 0:
            continue
        mcp = max_common_prefix(b, s[p:])
        if len(mcp) == len(b):
            return [[off + p, off + p + len(mcp)]]
        if len(mcp) == 0:
            continue
        b2 = b[len(mcp):]
        s2 = s[p + len(mcp):]
        m = abbr_fuzzy_match(abbr[i+1:], b2, s2, off + p + len(mcp))
        if m is None:
            continue
        return [[off + p, off + p + len(mcp)]] + m
    return None


def max_common_prefix(b, s):
    res = ''
    for c1, c2 in zip(b, s):
        if c1 == c2:
            res += c1
        else:
            return res
    return res


class Matcher:
    def match(self, b, m):
        hl = fuzzy_match(b, m['word'])
        if hl is None:
            return False
        m['user_data']['match_highlight'] = hl
        return True


def test_abbrev(s):
    res = get_abbrev(s)
    ls = [' '] * len(s)
    for i in res:
        ls[i] = '^'
    print(s)
    print(''.join(ls))

if __name__  == '__main__':
    s = 'abbr_fuzzy_match'
    b = 'abbrfuzzy'
    test_abbrev(s)
    print(fuzzy_match('abbrfuzzy', 'abbr_fuzzy_match'))
    print(max_common_prefix(b, s))

