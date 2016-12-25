import ocal


class movable(ocal.ocal):
    """Various generic movable functions, including:
    pascha_offset()
    getreading()
    post_theophany()"""

    def __init__(self, **kw):
        super(movable, self).__init__(**kw)

    def pascha_offset(self):
        """return tuple, offset in days between self and pascha
        and relevant year"""
        
        for year in (self.year, self.year-1):
            p = ocal.pascha(year)
            offset = self - p
            if offset >= -70:
                break

        return offset, year

    def getreading(self, wk):
        """Given a week (dict containing keys 0..6).
        returns dict[self.dow]"""

        try:
            return wk[self.dow]
        except KeyError:
            return None

    def post_theophany(self):
        """handle the Sunday Epistle and Gospel readings
        for the time between Theophany and Triodion.
        Returns -1 if Sunday after Theophany is Publican/Pharisee
        Returns 0 if there's just Sunday after Theophany before P/P
        Returns 1..4 (N sundays between SunAftTheo and P/P)"""

        p = ocal.pascha(self.year)
        theo = ocal.julian(year=self.year, month=1, day=6)
        dif = p-theo

        return (dif - 78) / 7
