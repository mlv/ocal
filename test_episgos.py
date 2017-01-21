import unittest
import ocal
import episgos
from gospel import fixed as gospel_fixed
from gospel import movable as gospel_movable
from epistle import fixed as epistle_fixed
from epistle import movable as epistle_movable

j=ocal.julian

def checkocal(oc):
    # movable inherits everything from ocal, so
    # give it a once-over, making sure ocal works.
    o = episgos.movable(year=1995, month=9, day=27,
                        calendar=ocal.GREGORIAN)
    oc.assertEqual(o.year, 1995, "Year wrong")
    oc.assertEqual(o.month, 9, "Month wrong")
    oc.assertEqual(o.dow, 3, "Dow wrong")

    o = episgos.movable(date=49987)
    oc.assertEqual(o.date, 49987, "date didn't return itself")

    o = episgos.movable(date=j(1995, 9, 14).date)
    oc.assertEqual(o.date, 49987, "Date wrong after julian init")


class test_movable(unittest.TestCase):
    def test_init(self):
        checkocal(self)

    def test_get_area_week(self):
        om = episgos.movable(year=2001, month=8, day=23,
                             calendar=ocal.GREGORIAN)
        om.get_area_week()
        self.assertEqual(om.p_offset, 130, "Offset for 2001/8/23 not 130")
        self.assertEqual(om.p_year, 2001, "offset year for 2001/8/23 not 2001")

        om = episgos.movable(year=2016, month=2, day=20,
                             calendar=ocal.GREGORIAN)
        om.get_area_week()
        self.assertEqual(om.p_offset, 314, "Offset 2/20/16, {} != 314 (2016)"
                         .format(om.p_offset))
        self.assertEqual(om.p_year, 2015, "Offset 2/20/16 {} != 2015"
                         .format(om.p_year))

        om = episgos.movable(year=2016, month=2, day=21,
                             calendar=ocal.GREGORIAN)
        om.get_area_week()
        self.assertEqual(om.p_offset, -70, "Offset 2/21 {} != -70"
                         .format(om.p_offset))

        om = episgos.movable(year=2016, month=5, day=1,
                             calendar=ocal.GREGORIAN)
        om.get_area_week()
        self.assertEqual(om.p_offset, 0, "Offset Pascha {} != 0"
                         .format(om.p_offset))
        
    def test_getreading(self):
        om = episgos.movable(year=2016, month=5, day=1,
                             calendar=ocal.GREGORIAN)
        ret = om.getreading({0: 123, 6: 234})
        self.assertEqual(ret, 123, "getreading returned {} != 123".format(ret))
        
        ret = om.getreading({1: 1, 2: 2, 3: 3})
        self.assertEqual(ret, None, "getreading returned {} not None"
                         .format(ret))

    def test_post_theophany(self):
        todo = [
            (1668, -1),
            (2132, -1),
            (1980, 0),
            (1912, 0),
            (2124, 0),
            (2140, 0),
            (2156, 0),
            (1920, 0),
            (1936, 0),
            (2148, 1),
            (2164, 1),
            (2180, 1),
            (2112, 1),
            (1960, 1),
            (2172, 1),
            (2104, 1),
            (2120, 2),
            (2136, 2),
            (1984, 2),
            (2196, 2),
            (2128, 2),
            (2144, 2),
            (2160, 2),
            (1924, 3),
            (1940, 3),
            (2152, 3),
            (2168, 3),
            (2184, 3),
            (2116, 3),
            (1964, 3),
            (2176, 4),
            (2108, 4),
            (1956, 4),
            (1804, 4),
            (2268, 4),
            (2105, -1),
            (1942, -1),
            (2143, -1),
            (2159, 0),
            (2102, 0),
            (2129, 0),
            (2151, 0),
            (2167, 0),
            (2110, 0),
            (2115, 0),
            (2153, 1),
            (2175, 1),
            (2107, 1),
            (2123, 1),
            (2139, 1),
            (2177, 1),
            (2109, 1),
            (2131, 2),
            (2147, 2),
            (2101, 2),
            (2106, 2),
            (2133, 2),
            (2155, 2),
            (2171, 2),
            (2103, 3),
            (2119, 3),
            (2157, 3),
            (2179, 3),
            (2111, 3),
            (2127, 3),
            (2154, 3),
            (1907, 4),
            (1945, 4),
            (2135, 4),
            (2173, 4),
        ]

        for y, exp in todo:
            om = episgos.movable(date=j(y, 1, 13).date)
            om.next_dow(1, 0)
            ret, idx = om.post_theophany()
            # print("For {}, got {} {}".format(om, ret, idx))
            self.assertEqual(ret, exp, "For {}, {} != {}".format(y, ret, exp))
            self.assertEqual(idx, 0, "For {}, {} != 0".format(y, idx))
            for expidx in range(1, ret):
                om += 7
                ret, idx = om.post_theophany()
                # print("For {}, got {}, {}".format(om, ret, idx))
                self.assertEqual(ret, exp, "For {}, {} != {}"
                                 .format(y, ret, exp))
                self.assertEqual(idx, expidx, "For {}, {} != {}"
                                 .format(y, idx, expidx))


class test_fixed(unittest.TestCase):
    def test_init(self):
        checkocal(self)

    def setUp(self):
        self.fixd = [
            None,
            {
                1: {'oneret':1},
                '6.-1.0': {'L':'SBTh'},
            },
            {}, {}, {}, {}, {},
            {}, {}, {}, {}, {},
            {
                12: {'L':'stherman'},
                '25.-2.0': {'L':'2SunBN'},
                '30.1.6': {'L':'SatA30'},
            },
        ]

    def test_get_fixed_normal(self):
        d = episgos.fixed(date=j(2012, 12, 12).date)
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, [{'L': 'stherman'}],
                         "normal, didn't get St. Herman. Got {}"
                         .format(ret))
        d += 1
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, [], "Got {}. Expected []".format(ret))

    def test_get_fixed_befaft(self):
        sth = episgos.fixed(date=j(2016, 12, 12).date)
        # print("sth:{} ({})".format(sth, sth.dow))
        
        fxd = sth.get_fixed(self.fixd)

        self.assertIn({'p': 1, 'L': '2SunBN'}, fxd, "Missing 2SunBN. Got {} for {}"
                      .format(fxd, sth))
        self.assertIn({'L':'stherman'}, fxd, "Missing stherman got {}".format(fxd))
        self.assertEqual(len(fxd), 2,
                         "fxd {}, expected just 2SunBN and stherman"
                         .format(fxd))

        d30 = episgos.fixed(date=j(2015, 1, 4).date)
        fxd = d30.get_fixed(self.fixd)
        self.assertEqual(fxd, [{'p':1, 'L': 'SatA30'}],
                         "Missing SatA30, got {}".format(fxd))

        prevyr = episgos.fixed(date=j(2001, 12, 31).date)
        ret = prevyr.get_fixed(self.fixd)
        self.assertEqual(ret, [{'p': 1, 'L': 'SBTh'}], 'Got {} expected SBTh'.format(ret))
        
        missing = episgos.fixed(date=j(2014, 4, 1).date)
        ret = missing.get_fixed(self.fixd)

        self.assertEqual(ret, [], "didn't return None")


class test_epistle(unittest.TestCase):
    def test_ep_get_area_week(self):
        def chk(d, area, off):
            # This little step allows me to use 'pentecost - 1'
            # (which retuns an ocal, not an epistle)
            ed = episgos.epistle(date=d.date)
            # And this little step saves me a pair of parens
            tup = (area, off)

            ed.get_area_week()
            self.assertEqual((ed.ep_area, ed.ep_week), tup,
                             "Expected {} got {}, {}"
                             .format(tup, ed.ep_area, ed.ep_week))

        # Easy ones
        pascha = ocal.pascha(2016)

        chk(pascha, "pascha", 1)
        chk(pascha+1, "pascha", 1)
        chk(pascha+6, "pascha", 1)
        chk(pascha+8, "pascha", 2)

        chk(pascha - 1, "lent", 7)
        chk(pascha - 76, "pentecost", 16)
        # chk(pascha - 70, "pentecost", 33)
        chk(pascha - 69, "pentecost", 34)
        # chk(pascha - 63, "pentecost", 34)
        chk(pascha - 62, "pentecost", 35)
        # chk(pascha - 56, "pentecost", 35)
        chk(pascha - 55, "lent", 0)

        lent = pascha - 49

        # chk(lent-0,  "lent", 0)
        chk(lent+1,  "lent", 1)
        chk(lent+13, "lent", 2)
        # chk(lent+14, "lent", 2)
        chk(lent+15, "lent", 3)

        w34 = j(2016, 2, 9)
        chk(w34,    "pentecost", 34)
        chk(w34-7,    "pentecost", 16)
        chk(w34-14,    "pentecost", 15)
        chk(w34-21,    "pentecost", 14)
        chk(w34-28,    "pentecost", 13)
        chk(w34-35,    "pentecost", 12)
        w12 = j(2016, 1, 5)

        chk(w12,    "pentecost", 12)
        chk(w12+5,  "pentecost", 12)
        chk(w12+7,  "pentecost", 13)
        chk(w12+14, "pentecost", 14)

        w69 = j(1983, 1, 6)
        w69.next_dow(1, 0)
        w69 += 7
        
        for exp in [29, 31, 32, 17, 34]:
            # print("{} ({}): {}?".format(w69, w69.dow, exp))
            chk(w69, "pentecost", exp)
            w69 += 7

        w69 = j(2016, 1, 6)
        w69.next_dow(1, 0)
        w69 += 7
        
        for exp in [29, 32, 17, 34]:
            # print("{} ({}): {}?".format(w69, w69.dow, exp))
            chk(w69, "pentecost", exp)
            w69 += 7

        pentecost = pascha + 49
        chk(pentecost - 1, "pascha", 7)
        chk(pentecost, "pascha", 8)
        chk(pentecost + 1, "pentecost", 1)

        chk(pentecost + 6, "pentecost", 1)
        chk(pentecost + 7, "pentecost", 1)
        chk(pentecost + 8, "pentecost", 2)

        chk(pentecost + 100, "pentecost", 15)

        afpent = j(2017, 11, 27)
        chk(afpent, "pentecost", 27)

        # Some random samplings from the calendar docs I have
        chk(j(2015, 3, 22), 'lent', 6)
        chk(j(2015, 7, 8), 'pentecost', 8)
        chk(j(2016, 11, 17), 'pentecost', 24)
        chk(j(2016, 12, 25), 'pentecost', 29)
        chk(j(2016, 2, 6), 'pentecost', 16)
        chk(j(2016, 1, 2), 'pentecost', 33)
        chk(j(2014, 1, 10), 'pentecost', 31)
        chk(j(2017, 1, 20), 'pentecost', 33)


class test_gospel(unittest.TestCase):
    def test_gos_get_area_week(self):
        """Test the Gospel get_area_off method.
        Reminder: it handles Lukan jump
        and all the following oddities"""

        def chk(d, area, week):
            # This little step allows me to use 'pentecost - 1'
            # (which retuns an ocal, not a movable)
            gd = episgos.gospel(date=d.date)
            # And this little step saves me a pair of parens
            areaweek = (area, week)
            gd.get_area_week()
            
            self.assertEqual((gd.g_area, gd.g_week), areaweek,
                             "For {} Expected {} got {} (o:{})"
                             .format(gd, areaweek,
                                     (gd.g_area, gd.g_week),
                                     gd.p_offset))
                            
        # Easy ones
        pascha = ocal.pascha(2016)
        
        chk(pascha,   "pascha", 1)
        chk(pascha+1, "pascha", 1)
        chk(pascha+7, "pascha", 2)
        chk(pascha+8, "pascha", 2)

        chk(pascha - 1, "lent", 7)
        lent = pascha - 49
        
        chk(lent,    "Luke", 19)  # Gospel has no lent,0
        chk(lent+1,  "lent", 1)
        chk(lent+7,  "lent", 1)
        chk(lent+8,  "lent", 2)
        chk(lent+14, "lent", 2)

        matt = pascha + 49
        chk(matt,    "pascha", 8)  # No 0 for Matt. Pentecost is pascha 8

        # Try some random sampled weekdays
        chk(j(2016, 5, 31), "pascha", 7)
        chk(j(2016, 6,  7), "Matthew",  1)
        chk(j(2016, 7, 10), "Matthew",  5)
        chk(j(2016, 8, 11), "Matthew", 10)
        chk(j(2016, 9, 17), "Matthew", 15)

        chk(j(2017,  1, 19), "Matthew", 16)

        chk(j(2016,  9, 20), "Luke",  1)
        chk(j(2016, 10, 15), "Luke",  4)
        chk(j(2016, 11, 22), "Luke", 10)
        chk(j(2016, 12, 20), "Luke", 14)
        chk(j(2017,  1,  4), "Luke", 16)
        chk(j(2017,  2,  4), "Luke", 18)
        chk(j(2017,  2,  7), "Luke", 19)
        chk(j(2017,  3, 12), "lent",  4)
        chk(j(2017,  3, 26), "lent",  6)
        chk(j(2017,  3, 29), "lent",  7)

        chk(j(2017,  6,  6), "Matthew", 3)
        chk(j(2017,  6, 28), "Matthew", 6)
        chk(j(2017,  7,  7), "Matthew", 7)

        # Now some Sundays
        chk(j(2016, 5, 2), "pascha", 3)
        chk(j(2016, 6, 6), "pascha", 8)
        chk(j(2016,  9,  5), "Matthew", 13)
        lukj = j(2016, 10,  3)
        for w in [2, 3, 4, 6, 5, 7, 8, 9, 13, 10, 11]:
            chk(lukj, "Luke",  w)
            lukj += 7
        self.assertEqual(lukj, j(2016, 12, 19),
                         "2016 Lukes don't line up. expected 12/19, got {}"
                         .format(lukj))

        chk(j(2017,  9,  4), "Matthew", 15)
        lukj = j(2017,  9, 25)
        for w in [1, 2, 3, 4, 6, 5, 7, 8, 9, 13, 10, 11]:
            chk(lukj, "Luke",  w)
            lukj += 7
        # Make sure we didn't miscount
        self.assertEqual(lukj, j(2017, 12, 18),
                         "2017 Lukes don't line up. expected Dec 18, got {}"
                         .format(lukj))

        chk(j(2016,  1, 18), "Luke", 12)
        chk(j(2016,  1, 25), "Luke", 15)
        chk(j(2016,  2,  1), "Matthew", 17)
        chk(j(2016,  2,  8), "Luke", 16)
        chk(j(2016,  2, 15), "Luke", 17)
        chk(j(2016,  2, 22), "Luke", 18)
        chk(j(2016,  2, 29), "Luke", 19)

        chk(j(2016,  4, 11), "lent",  6)
        chk(j(2017,  1, 16), "Luke", 15)
        chk(j(2017,  1, 23), "Luke", 16)
        chk(j(2017,  1, 30), "Luke", 17)
        chk(j(2017,  2,  6), "Luke", 18)
        chk(j(2017,  2, 13), "Luke", 19)

    def test_get_fixed_gospel(self):
        g = episgos.gospel(date=j(2011, 1, 7).date)
        gf = g.get_fixed_gospel()
        self.assertEqual(len(gf), 1, "Got {} for {}".format(gf, g))
        
        g = episgos.gospel(date=j(2010, 1, 7).date)
        gf = g.get_fixed_gospel()
        self.assertEqual(len(gf), 2, "Got {} for {}".format(gf, g))

    def test_get_week(self):
        g = episgos.gospel(date=j(2016, 5, 9).date)
        wk = g.get_week()
        self.assertEqual(wk, "4th week of Pascha")

if __name__ == "__main__":
    unittest.main(buffer=False)
