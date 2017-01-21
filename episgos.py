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
        # super(movable, self).get_area_week()
        
        for year in (self.year, self.year-1):
            p = ocal.pascha(year)
            offset = self - p
            # print("p:{}, offset:{}".format(p, offset))
            if offset >= -70:
                break

        self.p_year = year
        self.p_offset = offset
#        print("---for {} {}--p_offset={}"
#              .format(ocal.dows[self.dow], self, self.p_offset))
        
    def g_maparea(self):
        mapping = {
            "pascha": "of Pascha",
            "lent": "of Great Lent",
            "pentecost": "after Pentecost",
        }
        self.get_area_week()
        try:
            return mapping[self.g_area]
        except IndexError:
            return self.g_area

    def e_maparea(self):
        mapping = {
            "pascha": "of Pascha",
            "lent": "of Great Lent",
            "pentecost": "after Pentecost",
        }
        self.get_area_week()
        try:
            return mapping[self.e_area]
        except IndexError:
            return self.e_area

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
        self.befaft_re = re.compile("^(?P<day>[0-9]+)[\.:]"
                                    "(?P<befaft>[-0-9]+)[\.:]"
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
            fixedict[m][k]['p'] = 1
            fixeds.append(fixedict[m][k])

        return fixeds


class epistle(fixed, movable):
    """Includes methods for epistles. Makes good use of
    movable and fixed."""

    def __init__(self, **kw):
        super(epistle, self).__init__(**kw)

    def _get_area_week_sunday(self):
        "Given the offset, find the Sunday Epistle area and week"
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
            self.ep_week = 1 + self.p_offset // 7
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
        "Given the offset, find the weekday Epistle area and week"
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
            self.ep_week = 1 + self.p_offset // 7
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
                # print("For {:39} w{}".format(self, self.ep_week))
        # print("For {:39} week: {}{}".format(self, self.ep_area[0], self.ep_week))
        
    def get_area_week(self):
        """Returns time period we're in ("lent", "pascha",
        "pentecost") and weeks after start thereof"""
        # print("in epistle.get_area_week")
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
        self.get_area_week()
        return self.getreading(epistle_movable[self.ep_area][self.ep_week])

    def get_fixed_epistle(self):
        """Gets the fixed calendar epistle(s) for the day. Returns []
        if none.
        """
        self.get_area_week()
        return self.get_fixed(epistle_fixed)


class gospel(fixed, movable):
    """Includes methods for epistles. Makes good use of
    movable and fixed."""

    def __init__(self, **kw):
        super(gospel, self).__init__(**kw)

    def _get_gospel_area_week_sunday(self, p_off):
        "For Luke, find the Sunday Gospel reading"
        assert self.dow == 0
        # Story thus far: p_off is self-SunAftCross, ang g_area is "Luke"
        # So first we have to do all the fall jumping,
        # then the fun time before the Triodion

        # print("g_gawsun poff: {}".format(p_off))

        p_off = ((p_off + 6) // 7)
        
        luke_nonjumpers = (0, 1, 2, 3, 6, 7, 8, 9, 13)

        afters = {
            4: (10, 10),
            5: (10, 29),
            10: (12, 3),
            11: (12, 10),
        }

        jumpers = {}
        
        for k in afters.keys():
            d = ocal.julian(self.p_year, *afters[k])
            d.next_dow(1, 0)
            jumpers[d] = k

        jumpcnt = 0
        for d in jumpers.keys():
            if self == d:
                # print("Got a jump week. Returning it")
                self.g_week = jumpers[d]
                return
            if d < self:
                # print("{} ({}) has passed".format(d, jumpers[d]))
                jumpcnt += 1

        try:
            # print("jumpcnt: {}, p_off:{}, gweek: {}"
            # .format(jumpcnt, p_off, self.g_week))
            self.g_week = luke_nonjumpers[p_off - jumpcnt]
            return
        except IndexError:
            pass

        SunAftTheo = ocal.julian(self.year, 1, 6)
        SunAftTheo.next_dow(1, 0)
        if self <= SunAftTheo:
            self.g_week = None
            return
        
        pt, p_off = self.post_theophany()
        # print("In post_theophany: pt {} off: {}".format(pt, p_off))
        # pt < 0 can't happen. We'd be in the Triodion

        ptweeks = (
            (),
            (15,),
            (12, 15),
            (12, 15, 17),
            (12, 14, 15, 17),
            )
        self.g_week = ptweeks[pt][p_off]
        if self.g_week == 17:
            self.g_area = "Matthew"
        
    def _get_gospel_area_week_weekday(self, p_off):
        "Given the offset, find the weekday Gospel area and week"
        assert self.dow != 0
        # print("gawweek poff:{}".format(self.p_offset))

        if p_off <= 16 * 7:
            self.g_week = (p_off + 6) // 7
            return
        
        # print("Week Luke? p_off: {} g_week:{}".format(p_off, self.g_week))
        self.g_area = "Matthew"
        nxtp = ocal.pascha(self.year)
        nxtp -= 70
        delt = nxtp - self
        delt //= 7
        # print("nxtp:{}, delt:{}".format(nxtp, delt))
        self.g_week = 16 - delt

    def get_area_week(self):
        """Returns time period we're in ("lent", "pascha",
        "pentecost") and weeks after start thereof.
        Ultimately, this is the meat of this module.
        Going from area / week to an actual reading is just
        get_movable_gospel, a one-liner."""
        # print("in gospel.get_area_week")
        super(gospel, self).get_area_week()

        # These two are debugging, in case it doesn't get set
        self.g_area = repr(self)
        self.g_week = self.p_offset

        # p_off will contain the offset from the current area we're considering
        p_off = self.p_offset

        # Common code between daily and Sunday goes here
        if p_off < 0:
            p_off += 70
            # print("triod: p_off: {}".format(p_off))
            if p_off <= 21:
                self.g_week = 16 + ((p_off + 6) // 7)
                self.g_area = "Luke"
            else:
                self.g_area = "lent"
                self.g_week = ((p_off-1) // 7) - 2
                # print("lent: {}".format(p_off))
            return None

        if p_off <= 49:
            self.g_area = "pascha"
            self.g_week = 1 + p_off // 7
            return None

        p_off -= 49
        self.g_area = "Matthew"
        self.g_week = (p_off + 6) // 7
        
        SunAftCross = ocal.julian(self.p_year, 9, 14)
        SunAftCross.next_dow(1, 0)
        if self <= SunAftCross:
            return None
        
        self.g_area = "Luke"
        p_off = self - SunAftCross
        # print("end of lucan jump check, Luke/{}".format(p_off))

        if self.dow == 0:
            self._get_gospel_area_week_sunday(p_off)
        else:
            self._get_gospel_area_week_weekday(p_off)

    def get_movable_gospel(self):
        """Simple. Just returns getreading for self.g_area/week/dow
        """
        self.get_area_week()
        if self.g_week is None:
            return None
        return self.getreading(gospel_movable[self.g_area][self.g_week])

    def get_fixed_gospel(self):
        """Gets the fixed calendar gospel(s) for the day. Returns []
        if none. Handles weird edge case of Jan 7/20 (for years where Pashca
        is March 22 or 23) where the Sunday after Theophany Gospel readings
        are moved.
        """

        # From the Scripture Readings doc (section e)
        # If Pascha falls between March 22nd and March 24th, the Sunday
        # after Theophany does not occur because the first Sunday after
        # Theophany is the Sunday of the Publican and Pharisee; in this
        # instance the Epistle and Gospel readings for the Sunday after
        # Theophany are read on January 7th before the readings for St.
        # John the Baptist.
        
        jan7 = ocal.julian(self.year, 1, 7)
        jan7
        
        ret = []
        
        if self == jan7 and self.post_theophany()[0] < 0:
            ret.append(gospel_fixed[1]['6.1.0'])

        return ret + self.get_fixed(gospel_fixed)

    def get_week(self):
        def ordinal(n):
            return "%d%s" % (n, "tsnrhtdd"[
                (n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
        
        if self.dow == 0:
            area = self.g_maparea()
            return "{} week {}".format(ordinal(self.g_week), area)
        else:
            mon = gospel(date=self.date)
            mon.calendar = ocal.JULIAN
            
            if mon.dow > 1:
                mon.next_dow(-1, 1)
            mon.get_area_week()

            x = mon.get_fixed_gospel()
            ath = any(['Afterfeast of Theophany' in y for y in x])

            sat = gospel(date=mon.date)
            sat.calendar = ocal.JULIAN

            weeks = [
                [mon, None, ath]
            ]

            for ii in range(6):
                x = sat.get_fixed_gospel()
                n_ath = any(['Afterfeast of Theophany' in y for y in x])

                if ath != n_ath or mon.month != sat.month:
                    weeks[-1][1] = sat
                    weeks[-1][1] -= 1
                    weeks.append([sat, None, n_ath])
                ath = n_ath
                sat += 1

            for ii, st, en, ath in enumerate(weeks):
                rg = "{}-{}".format(st.day, en.day)
                if ath:
                    weeks[ii] = "{}, Afterfeast of Theophany" \
                                .format(rg)
                else:
                    weeks[ii] = "{}, {} week {}".format(
                        rg, st.g_week, st.g_maparea())

