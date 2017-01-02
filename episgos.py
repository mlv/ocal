import ocal
import re
from gospel import fixed as gospel_fixed
from gospel import movable as gospel_movable
from epistle import fixed as epistle_fixed
from epistle import movable as epistle_movable


class movable(ocal.ocal):
    """Various generic movable functions, including:
    pascha_offset()
    getreading()
    post_theophany()"""

    def __init__(self, **kw):
        super(movable, self).__init__(**kw)

    def get_area_week(self):
        """return tuple, offset in days between self and pascha
        and relevant year"""
        
        for year in (self.year, self.year-1):
            p = ocal.pascha(year)
            offset = self - p
            # print("p:{}, offset:{}".format(p, offset))
            if offset >= -70:
                break

        self.p_year = year
        self.p_offset = offset

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

        return (dif - 78) / 7, (self - theo - 8) // 7


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
        for m in range(self.jmonth-1, self.jmonth+2, 1):
            y = self.jyear
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

        if self.jday in fixedict[self.jmonth]:
            fixeds.append(fixedict[self.jmonth][self.jday])

        for m, k in befafts:
            fixeddict[m][k]['p'] = 1
            fixeds.append(fixedict[m][k])

        return fixeds


class epistle(movable, fixed):
    """Includes methods for epistles. Makes good use of
    movable and fixed."""

    def __init__(self, **kw):
        super(epistle, self).__init__(**kw)

    def _get_area_week_sunday(self):
        assert self.dow == 0

        if self.p_offset < 0:
            if self.p_offset < -49:
                self.ep_area = 'pentecost'
                self.ep_week = 34 + ((self.p_offset + 70) // 7)
            else:
                self.ep_area = 'lent'
                self.ep_week = (self.p_offset + 49) // 7
        elif self.p_offset <= 49:
            # Yes, <=: Pentecost is considered part of 'pascha'
            self.ep_area = 'pascha'
            self.ep_week = self.p_offset // 7
        else:
            off = (self.p_offset - 49) // 7
            self.ep_area = 'pentecost'
            self.ep_week = off

            self.calendar = ocal.JULIAN
            if off <= 33:
                return

            off -= 34
            waftTh = [
                [],
                [32],
                [29, 32],
                [29, 32, 17],
                [29, 31, 32, 17],
            ]

            thoff, thidx = self.post_theophany()
            # print("thoff: {}, thidx: {}".format(thoff, thidx))
            if thoff <= 0:
                return  # This'll be handled by Theophany, et.al
            self.ep_week = waftTh[thoff][thidx]
            return

    def _get_area_week_weekday(self):
        assert self.dow != 0
        
        if self.p_offset < 0:
            triod_off = self.p_offset + 70
            if triod_off < 14:  # 34 or 35W afP
                self.ep_week = 34 + (triod_off // 7)
                self.ep_area = 'pentecost'
            else:
                self.ep_week = (triod_off - 14) // 7
                self.ep_area = 'lent'
        elif self.p_offset < 49:  # Pascha
            self.ep_week = (self.p_offset + 6) // 7
            self.ep_area = 'pascha'
        else:
            self.ep_area = 'pentecost'

            # -7: starts with week 1 after Pentecost, not 0
            offset = self.p_offset - (49 - 7)
            w = offset // 7
            if w > 33:
                nextp = ocal.pascha(self.year)
                nextp -= 70
                needed = (nextp + 6 - self) // 7
                self.ep_week = range(16, 9, -1)[needed - 1]
#                print("for {:39} offset: {}, week {}"
#                      .format(self, w, self.ep_week))
            else:
                self.ep_week = w
#                print("For {:39} w{}".format(self, self.ep_week))
#        print("For {:39} week: {}{}".format(self, self.ep_area[0], self.ep_week))
        
    def get_area_week(self):
        """Returns time period we're in ("lent", "pascha",
        "pentecost") and weeks after start thereof"""
        super(epistle, self).get_area_week()

        # These two are debugging, in case it doesn't get set
        self.ep_area = repr(self)
        self.ep_week = self.p_offset
        if self.dow == 0:
            self._get_area_week_sunday()
        else:
            self._get_area_week_weekday()
                    
    def get_movable_epistle(self):
        """Simple. Just returns getreading for self.ep_area/week/dow
        """
        return self.getreading(epistle_movable[self.ep_area][self.ep_week])

    def get_fixed_epistle(self):
        """Gets the fixed calendar epistle(s) for the day. Returns []
        if none.
        """
        return self.get_fixed(epistle_fixed)


class gospel(fixed, movable):
    """                SunAftCross = ocal.julian(self.year, 9, 14)
                SunAftCross.next_dow(1, 0)
                if self < SunAftCross:
                    self.ep_area = "
"""
    pass

