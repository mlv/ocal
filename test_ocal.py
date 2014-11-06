import unittest

import ocal

class ocaltest(unittest.TestCase):
    def test_ocal_init(self):
        o=ocal.ocal(year=1995, month=9, day=27, gregorian=True)
        self.assertEqual(o.date, 49987, "init with gregorian didn't return correct mjd date")

        o=ocal.ocal(year=1995, month=9, day=14, julian=True)
        self.assertEqual(o.date, 49987, "init with julian didn't return correct mjd date")

        o=ocal.ocal(date=49987)
        self.assertEqual(o.date, 49987, "init with date didn't return itself!")

    def test_ocal_gregorian(self):
        o=ocal.ocal.gregorian(1995, 9, 27)
        self.assertEqual(o.date, 49987, "gregorian init didn't return correct mjd date")

    def test_ocal_julian(self):
        o=ocal.ocal.julian(1995, 9, 14)
        self.assertEqual(o.date, 49987, "julian init didn't return correct mjd date")

    def test_ocal_mjdate(self):
        o=ocal.ocal.mj_date(49987)
        self.assertEqual(o.date, 49987, "mj_date init didn't return correct mjd date")

    def test_ocal_get_date(self):
        o=ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_date(), 49987, "get_date didn't return correct mjd date")

    def test_ocal_get_ymd_g(self):
        o=ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_ymd_g(), (1995, 9, 27), "get_ymd_g() didn't return expected year,month,day")

    def test_ocal_get_ymd_j(self):
        o=ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_ymd_j(), (1995, 9, 14), "get_ymd_j() didn't return expected year,month,day")

    def test_ocal_get_dow(self):
        o=ocal.ocal.mj_date(49987)
        self.assertEqual(o.get_dow(), 3, "get_dow didn't return expected day of week")


    # modifying methods
    def test_ocal_add_days(self):
        o=ocal.ocal.mj_date(100)
        self.assertEqual(o.get_date(), 100, "add_days test didn't start with 100")
        o.add_days(10)
        self.assertEqual(o.get_date(), 110, "add_days failed adding 10")
        o.add_days(-200)
        self.assertEqual(o.get_date(), -90, "add_days failed subtracting 200")

    def test_ocal_next_dow(self):
        o=ocal.ocal.mj_date(49987)
        o.next_dow(0)
        self.assertEqual(o.get_ymd_g(), (1995, 10, 1), "first sunday after 9/27/1995 failed")

if __name__ == "__main__":
    unittest.main()
