import unittest

import ocal


class ocaltest(unittest.TestCase):
    def assertYMD(self, o, cal, year, mon, day, dow, msg):
        self.assertEqual(o.calendar, cal,
                         "{} showed the wrong calendar".format(msg))
        self.assertEqual(o.year, year, "{} in year {} gave year {}"
                         .format(msg, year, o.year))
        self.assertEqual(o.month, mon, "{} in month {} gave month {}"
                         .format(msg, mon,  o.month))
        self.assertEqual(o.day,   day, "{} in day {} gave day {}"
                         .format(msg, day,  o.day))
        self.assertEqual(o.dow,   dow, "{} in dow {} gave dow {}"
                         .format(msg, dow,  o.dow))

    def test_ocal_init(self):
        o = ocal.ocal(year=1995, month=9, day=27, calendar=ocal.GREGORIAN)
        self.assertEqual(o.date, 49987,
                         "init with gregorian didn't return correct mjd date")
        self.assertYMD(o, ocal.GREGORIAN, 1995, 9, 27,
                       3, "init with given gregorian")

        self.assertEqual(type(o.date), int, "o.date is {}, not int"
                         .format(type(o.date)))

        o = ocal.ocal(year=1995, month=9, day=27)
        self.assertEqual(o.date, 49987,
                         "init default:gregorian returned wrong mjd date")
        self.assertYMD(o, ocal.GREGORIAN, 1995, 9, 27, 3,
                       "init with default gregorian")

        o = ocal.ocal(year=1995, month=9, day=14, calendar=ocal.JULIAN)
        self.assertEqual(o.date, 49987,
                         "init with julian didn't return correct mjd date")
        self.assertYMD(o, ocal.JULIAN, 1995, 9, 14, 3,
                       "init with given julian")
        self.assertEqual(type(o.date), int, "o.date is {}, not int"
                         .format(type(o.date)))


        try:
            o = ocal.ocal(year=1995, month=9, day=14, calendar=47)
        except ValueError as e:
            self.assertEqual(e.args[0], "Unknown calendar:47", "Invalid error")
        except BaseException as e:
            self.fail(
                "init with invalid calendar raised unexpected exception:{}"
                .format(repr(e)))
        else:
            self.fail("init with invalid calendar failed to raise exception")

        o = ocal.ocal(date=49987)
        self.assertEqual(o.date, 49987, "init with date didn't return itself!")
        self.assertYMD(o, ocal.GREGORIAN, 1995, 9, 27, 3, "init with date")

        try:
            o = ocal.ocal(month=9, day=27, calendar=ocal.GREGORIAN)
        except KeyError:
            pass
        except e:
            self.fail("Raised unexpected exception (with missing year):", e)
        else:
            self.fail("Missing exception when year missing")

        try:
            o = ocal.ocal(year=1995, day=27, calendar=ocal.GREGORIAN)
        except KeyError:
            pass
        except e:
            self.fail("Raised unexpected exception (with missing month):", e)
        else:
            self.fail("Missing exception when month missing")

        try:
            o = ocal.ocal(year=1995, month=9, calendar=ocal.ocal.gregorian)
        except KeyError:
            pass
        except e:
            self.fail("Raised unexpected exception (with missing day):", e)
        else:
            self.fail("Missing exception when day missing")

    def test_ocal_gregorian(self):
        o = ocal.gregorian(1995, 9, 27)
        self.assertEqual(
            o.date, 49987, "gregorian init didn't return correct mjd date")
        self.assertYMD(o, ocal.GREGORIAN, 1995, 9, 27,
                       3, "init with gregorian function")

    def test_ocal_julian(self):
        o = ocal.julian(1995, 9, 14)
        self.assertEqual(
            o.date, 49987, "julian init didn't return correct mjd date")
        self.assertYMD(o, ocal.JULIAN, 1995, 9, 14,
                       3, "init with julian function")

    def test_ocal_mjdate(self):
        o = ocal.ocal.mj_date(49987)
        self.assertEqual(
            o.date, 49987, "mj_date init didn't return correct mjd date")
        self.assertYMD(o, ocal.GREGORIAN, 1995, 9, 27, 3, "init with mj_date")

    def test_ocal_get_date(self):
        o = ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_date(), 49987,
                         "get_date didn't return correct mjd date")

    def test_ocal_get_ymd_g(self):
        o = ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_ymd_g(), (1995, 9, 27),
                         "get_ymd_g() didn't return expected year,month,day")

    def test_ocal_get_ymd_j(self):
        o = ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_ymd_j(), (1995, 9, 14),
                         "get_ymd_j() didn't return expected year,month,day")

    def test_ocal_get_dow(self):
        o = ocal.ocal.mj_date(49987)
        self.assertEqual(
            o.get_dow(), 3, "get_dow didn't return expected day of week")

    # modifying methods
    def test_ocal_add_days(self):
        o = ocal.ocal.mj_date(100)
        self.assertEqual(o.get_date(), 100,
                         "add_days test didn't start with 100")
        o.add_days(10)
        self.assertEqual(o.get_date(), 110, "add_days failed adding 10")
        o.add_days(-200)
        self.assertEqual(o.get_date(), -90, "add_days failed subtracting 200")

    def test_ocal_next_dow(self):
        o = ocal.ocal.mj_date(49987)
        o.next_dow(1, 0)
        self.assertEqual(o.get_ymd_g(), (1995, 10, 1),
                         "first sunday after 9/27/1995 failed")
        self.assertEqual(
            o.dow, 0, "went to dow 0, but made it to {} instead".format(o.dow))

        o = ocal.ocal.gregorian(2014, 6, 1)
        o.next_dow(1, 0)  # advance to Sunday, but 6/1/2014 IS a Sunday
        self.assertEqual(o.get_ymd_g(), (2014, 6, 8),
                         "Advancing to same day failed")

        o = ocal.ocal.gregorian(2014, 6, 1)
        o.next_dow(-1, 0)  # advance to last Sunday in May
        self.assertEqual(o.get_ymd_g(), (2014, 5, 25),
                         "Advancing to last day in prev month failed")

        o.next_dow(-2, 4)  # advance back a couple weeks
        self.assertEqual(o.get_ymd_g(), (2014, 5, 15),
                         "Advancing back 2 weeks failed")

        o.next_dow(2, 4)  # advance forward a couple weeks
        self.assertEqual(o.get_ymd_g(), (2014, 5, 29),
                         "Advancing forward 2 weeks failed")

        try:
            o.next_dow(0, 3)  # 0: ValueError
        except ValueError:
            pass
        except BaseException as e:
            self.fail("Unexpected exception thrown:", e)
        else:
            self.fail("No exception thrown. Expected ValueError")

        o = ocal.ocal.gregorian(2014, 6, 2)
        o.next_dow(-1, 0)
        self.assertEqual(o.get_ymd_g(), (2014, 6, 1),
                         "Going back to yesterday failed")

        o = ocal.ocal.gregorian(2014, 6, 1)
        o.next_dow(1, 0, offset=-1)
        self.assertEqual(o.get_ymd_g(), (2014, 6, 1),
                         '"Advancing" to self (via offset=-1) failed"')

        o = ocal.ocal.gregorian(2014, 6, 1)
        o.next_dow(-1, 0, offset=1)
        self.assertEqual(o.get_ymd_g(), (2014, 6, 1),
                         '"Advancing" to self (via offset=1) failed"')

    def test_ocal_repr(self):
        o = ocal.julian(2015, 12, 25)
        rp = repr(o)
        exp = "ocal.ocal.julian(2015, 12, 25)"
        self.assertEqual(rp, exp,
                         "repr failure. Expected '{}', got '{}'"
                         .format(exp, rp))

        o.calendar = ocal.GREGORIAN
        rp = repr(o)
        exp = "ocal.ocal.gregorian(2016, 1, 7)"
        self.assertEqual(rp, exp,
                         "repr failure. Expected '{}', got '{}'"
                         .format(exp, rp))

    def test__add(self):
        n = ocal.julian(2015, 12, 25)
        th = n + 12
        self.assertYMD(th, ocal.JULIAN, 2016, 1, 6,
                       2, "__add from Nativity 2015")
        self.assertEqual(th.get_ymd_j(), (2016, 1, 6),
                         "__add__ failed. Nativity+12 is {}"
                         .format(th.get_ymd_j()))

    def test__sub(self):
        th = ocal.julian(2016, 1, 6)
        n = th - 12
        self.assertYMD(n, ocal.JULIAN, 2015, 12, 25,
                       4, "__sub__from Theophany (")
        self.assertEqual(n.get_ymd_j(), (2015, 12, 25),
                         "__sub__ failed. Theophany-12 is {}"
                          .format(n.get_ymd_j()))

        self.assertEqual(th - n, 12, "relative difference failed."
                         "Difference between Theophany and Nativity is {} days"
                         .format(th - n))

    def test__iadd(self):
        th = ocal.julian(2016, 1, 6)
        svth = th
        th += 3
        self.assertEqual(id(th), id(svth), "+= changed th object")
        nth = ocal.julian(2016, 1, 9)
        self.assertEqual(th, nth, "+= {} not the 9th".format(th))
        
    def test__isub(self):
        th = ocal.julian(2016, 1, 6)
        svth = th
        th -= 3
        self.assertEqual(id(th), id(svth), "-= changed th object")
        nth = ocal.julian(2016, 1, 3)
        self.assertEqual(th, nth, "-= {} not the 3rd".format(th))
        
    def test__cmp(self):
        d1 = ocal.gregorian(2016, 1, 5)
        d2 = ocal.gregorian(2016, 1, 6)
        self.assertLess(d1, d2, "failure: {} not less than {}".format(d1, d2))
        d1 += 1
        self.assertEqual(d1, d2, "failure: {} not equal to {}".format(d1, d2))
        d1 += 1
        self.assertGreater(
            d1, d2, "failure: {} not greater than {}".format(d1, d2))


class ocalpascha(unittest.TestCase):

    def test_pascha(self):
        ydates = (
            (2014, 56767),
            (2001, 52014),
            (2000, 51664),
            (1960, 37041),
            (1958, 36306),
            (1977, 43243)
        )
        for yd in ydates:
            o = ocal.pascha(yd[0])
            self.assertEqual(
                o.dow, 0, "Pascha for {} not on Sunday according to o.dow")
            self.assertEqual(
                o.get_dow(), 0, "Pascha for year {} not on Sunday!")
            self.assertEqual(o.get_date(), yd[1],
                             "Pascha failed for year {} ({} != {})"
                             .format(yd[0], o.get_date(), yd[1]))

if __name__ == "__main__":
    unittest.main()
