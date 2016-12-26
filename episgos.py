import ocal
import re


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


class fixed(ocal.ocal):
    """Class that includes tools for fixed calendar-based
    readings (like 3/25, or Saturday before Nativity ('25.-1.6').
    Nothing really here except get_fixed()"""
    def __init__(self, **kw):
        super(fixed, self).__init__(**kw)
        self.befaft_re = re.compile("^(?P<day>[0-9]+)\."
                                    "(?P<befaft>[-0-9]+)\."
                                    "(?P<dow>[0-6]+)$")
        
    def get_fixed(self, fixedict):
        """Basic fixed. Includes 6.-1.0 parsing.
        Return value: dict: {'book':..., 'chverse':..., ?'see':...}
        Easy part: look through fixed dictionary for current day.
        Hard(er) part. Parse 6.-1.0 parsing, which means, relative
        to the <6>th day of this month, look <-1> weeks (ago) for
        day <0>. In other words, 6.-1.0 means "Sunday before Theophany"
        """

        fixeds = []
        befafts = []

        # print("checking {}".format(self))
        # Do the hard part first
        for m in range(self.month-1, self.month+2, 1):
            y = self.year
            if m == 0:
                m = 12
                y = y - 1
            elif m == 13:
                m = 1
                y = y + 1

            for k in fixedict[m].keys():
                if type(k) == int:
                    continue
                mat = self.befaft_re.match(k)
                if mat is None:
                    print("{} doesn't match proper pattern".format(k))
                    continue
                
                md = mat.groupdict()
                for mk in md:
                    md[mk] = int(md[mk])
                    
                if md['dow'] != self.dow:
                    # print("{} wrong dow, expected {} got {}"
                    #       .format(k, md['dow'], self.dow))
                    continue
                d = ocal.julian(year=y, month=m, day=md['day'])
                # print("before next dow:{} {}".format(d, d.dow))
                d.next_dow(md['befaft'], md['dow'])
                # print("after next dow:{} {}".format(d, d.dow))
                if d == self:
                    # print("match for {},{}".format(m, k))
                    befafts.append((m, k))
                else:
                    pass  # print("Not a match for {},{}".format(m, k))

        if self.day in fixedict[self.month]:
            fixeds.append(fixedict[self.month][self.day])

        for m, k in befafts:
            fixeds.append(fixedict[m][k])

        return fixeds
