import unittest
import ocal
import episgos


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

    o = episgos.movable(year=1995, month=9, day=14, calendar=ocal.JULIAN)
    oc.assertEqual(o.date, 49987, "Date wrong after julian init")

    
class test_movable(unittest.TestCase):
    def test_init(self):
        checkocal(self)

    def test_pascha_offset(self):
        om = episgos.movable(year=2001, month=8, day=23,
                             calendar=ocal.GREGORIAN)
        r = om.pascha_offset()
        self.assertEqual(r[0], 130, "Offset for 2001/8/23 not 130")
        self.assertEqual(r[1], 2001, "offset year for 2001/8/23 not 2001")

        om = episgos.movable(year=2016, month=2, day=20,
                             calendar=ocal.GREGORIAN)
        r = om.pascha_offset()
        self.assertEqual(r[0], 314, "Offset 1/31/16, {} != 314 (2015)"
                         .format(r[0]))
        self.assertEqual(r[1], 2015, "Offset 1/31/16 {} != 2015"
                         .format(r[1]))

        om = episgos.movable(year=2016, month=2, day=21,
                             calendar=ocal.GREGORIAN)
        r = om.pascha_offset()
        self.assertEqual(r[0], -70, "Offset 2/21 {} != -70".format(r[0]))

        om = episgos.movable(year=2016, month=5, day=1,
                             calendar=ocal.GREGORIAN)
        r = om.pascha_offset()
        self.assertEqual(r[0], 0, "Offset Pascha {} != 0".format(r[0]))
        
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
            om = episgos.movable(year=y, month=1, day=31, calendar=ocal.JULIAN)
            ret = om.post_theophany()
            self.assertEqual(ret, exp, "For {}, {} != {}".format(y, ret, exp))


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
        d = episgos.fixed(year=2012, month=12, day=12, calendar=ocal.JULIAN)
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, ['stherman'], "normal, didn't get St. Herman. Got {}"
                         .format(ret))
        d += 1
        ret = d.get_fixed(self.fixd)
        self.assertEqual(ret, [], "Got {}. Expected []".format(ret))

    def test_get_fixed_befaft(self):
        sth = episgos.fixed(year=2016, month=12, day=12, calendar=ocal.JULIAN)
        
        fxd = sth.get_fixed(self.fixd)

        self.assertIn('2SunBN', fxd, "Missing 2SunBN. Got {} for {}"
                      .format(fxd, sth))
        self.assertIn('stherman', fxd, "Missing stherman")
        self.assertEqual(len(fxd), 2,
                         "fxd {}, expected just 2SunBN and stherman"
                         .format(fxd))

        d30 = episgos.fixed(year=2015, month=1, day=4, calendar=ocal.JULIAN)
        fxd = d30.get_fixed(self.fixd)
        self.assertEqual(fxd, ['SatA30'], "Missing SatA30, got {}".format(fxd))

        prevyr = episgos.fixed(year=2001, month=12, day=31,
                               calendar=ocal.JULIAN)
        ret = prevyr.get_fixed(self.fixd)
        self.assertEqual(ret, ['SBTh'], 'Got {} expected SBTh'.format(ret))
        
        missing = episgos.fixed(year=2014, month=4, day=1,
                                calendar=ocal.JULIAN)
        ret = missing.get_fixed(self.fixd)

        self.assertEqual(ret, [], "didn't return None")

if __name__ == "__main__":
    unittest.main(buffer=False)
