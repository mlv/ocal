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
                1: 'oneret',
                '6.-1.0': 'SBTh',
            },
            {}, {}, {}, {}, {},
            {}, {}, {}, {}, {},
            {
                12: 'stherman',
                '25.-2.0': '2SunBN',
                '30.1.6': 'SatA30',
            },
        ]

    def test_get_fixed_normal(self):
        d = episgos.fixed(date=j(2012, 12, 12).date)
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, ['stherman'], "normal, didn't get St. Herman. Got {}"
                         .format(ret))
        d += 1
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, [], "Got {}. Expected []".format(ret))

    def test_get_fixed_befaft(self):
        sth = episgos.fixed(date=j(2016, 12, 12).date)
        
        fxd = sth.get_fixed(self.fixd)

        self.assertIn('2SunBN', fxd, "Missing 2SunBN. Got {} for {}"
                      .format(fxd, sth))
        self.assertIn('stherman', fxd, "Missing stherman")
        self.assertEqual(len(fxd), 2,
                         "fxd {}, expected just 2SunBN and stherman"
                         .format(fxd))

        d30 = episgos.fixed(date=j(2015, 1, 4).date)
        fxd = d30.get_fixed(self.fixd)
        self.assertEqual(fxd, ['SatA30'], "Missing SatA30, got {}".format(fxd))

        prevyr = episgos.fixed(date=j(2001, 12, 31).date)
        ret = prevyr.get_fixed(self.fixd)
        self.assertEqual(ret, ['SBTh'], 'Got {} expected SBTh'.format(ret))
        
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

        # chk(pascha, "pascha", 0)
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
        chk(pentecost, "pascha", 7)
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

r'''
class xtest_gospel(unittest.TestCase):
    def test_get_areaoff(self):
        """Test the Gospel get_area_off method.
        Reminder: it handles Lukan jump
        but not all the following oddities"""
        def chk(d, area, off):
            tup = (area, off)
            # This little step allows me to use 'pentecost - 1'
            # (which retuns an ocal, not a movable)
            ed = episgos.gospel(date=d.date)
            areaoff = ed.get_area_off()
            self.assertEqual(areaoff, tup, "Expected {} got {}"
                             .format(tup, areaoff))
                            
        # Easy ones
        pascha = ocal.pascha(2016)
        
        chk(pascha, "pascha", 0)

        chk(pascha - 1, "lent", 7)
        lent = pascha - 49
        
        chk(lent,    "lent", 0)
        chk(lent+1,  "lent", 0)
        chk(lent+13, "lent", 1)
        chk(lent+14, "lent", 2)
        chk(lent+15, "lent", 2)

'''    
if __name__ == "__main__":
    unittest.main(buffer=False)
