import sys

class Sorter:
    def key(self, e):
        w = e['word']
        ud = e['user_data']
        hl = ud['match_highlight']

        # prefer less pieces
        pieces = len(hl)

        # prefer earlier match
        first_match = sys.maxsize
        if len(hl):
            first_match = hl[0][0]

        # prefer shorter span
        span = sys.maxsize
        if len(hl):
            span = hl[-1][1] - hl[0][0]

        # alphanum
        scw = w.swapcase()

        return [pieces, first_match, span, scw]

    def sort(self, matches: list):
        matches.sort(key=self.key)
        return matches
