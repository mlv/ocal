#! /usr/binn/env python3

class ocal(object):
    """
ocal -- Orthodox calendar management class

The main purpose of this class is to provide conversion between various date formats.
The impetus is the algorithm for computing Pascha (which this class does not do). So 
the goal is whatever methods are needed to "give me the sunday after the Nth day after 
March 21st of this year".

To that end, it includes methods for initializing dates (using both Gregorian and Julian 
dates), adding and subtracting days, getting the next or previous <day of week>. Finally, 
it can return a date as a Gregorian or Julian year,month,day tuple or as a formatted 
string (either the Gregorian, Julian, or a combination of the two).

Care must be taken to avoid confusing the Julian calendar with Julian dates. The Julian 
calendar is a calendar system where every 4 years is a leap year. Julian dates are a way 
of counting days since an epoch (<julian> January 1 4713 BC or <gregorian> Nov 17, 1858).

This class will use the jdcal package of functions to provide some of the heavy lifting.
All days stored will be in MJD (possibly negative, if before 1858). jdcal functions often 
return two values: jdcal.MJD_0 (2400000.5) and the modified julian date. I'll just always 
pass that + jdcal.MJD_0.
"""
    def __init__(self, **kw):
        """Ideally called with constructor methods. Optional parameters include:
    year, month, day: year, month, day according to the calendar system.
    date: modified julian date 
    gregorian: if true (the default), use the Gregorian calendar to convert year,month,day to a julian date.
    julian: if true, use the Julian calendar to convert year,month,day to a julian date.
."""
        pass


    @classmethod
    def gregorian(cls, year, month, day):
        "Given year,month,day, create an ocal instance according to the Gregorian calendar."
        return cls(year=year, month=month, day=day, gregorian=True)

    @classmethod
    def julian(cls, year, month, day):
        "Given year,month,day, create an ocal instance according to the Julian calendar."
        return cls(year=year, month=month, day=day, julian=True)

    @classmethod
    def mj_date(cls, date):
        "Create an ocal instance with date as a modified julian date."
        return cls(date=date)


    def get_date(self):
        "Return the modified julian date"
        return self.date

    def get_ymd_g(self):
        "return the year, month, and day of the instance, according to the Gregorian calendar"
        pass


    def get_ymd_j(self):
        "return the year, month, and day of the instance, according to the Julian calendar"
        pass

    def get_dow(self):
        "return the day of week. 0: Sunday, 6: Saturday"
        # the MJD starts on a Wednesday. Advance to Sunday so modulo works.
        return (self.date+4) % 7

    # The above are all the gazintas/gazattas

    def add_days(self, ndays):
        "add (or subtract if negative) ndays to the date"
        pass

    def next_dow(self, dow, n=1):
        """advance the date to the next given day of week (dow. 0==Sunday)

If n>0 advance forward n days of week, including today. So if today is already 
dow and n==1, the date doesn't change.
eg. to find US election day (first Tuesday after the first Monday):
d=ocal.gregorian(year, 11, 1)
d.next_dow(1)
d.next_dow(2)

If n<0 go back n days of week, not including today.
So if you want to find the last Friday of November, you would do:
d=ocal.gregorian(year, 12, 1)
d.next_dow(5, -1)

n==0 raises a ValueError
"""
        pass

