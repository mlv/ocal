#! /usr/binn/env python3

import jdcal

GREGORIAN = 1
JULIAN = 2

class ocal(object):
    """
ocal -- Orthodox calendar management class

The main purpose of this class is to provide conversion between various date formats.
The impetus is the algorithm for computing Pascha (which this class does not do). So 
the goal is whatever methods are needed to "give me the sunday after the Nth day after 
March 21st of this year".

To that end, it includes methods for initializing dates (using both Gregorian and Julian 
calendar dates), adding and subtracting days, getting the next or previous <day of week>. 
Finally, it can return a date as a Gregorian or Julian year,month,day tuple or as a formatted 
string (either the Gregorian, Julian, or a combination of the two).

Care must be taken to avoid confusing the Julian calendar with Julian dates. The Julian 
calendar is a calendar system where every 4 years is a leap year. Julian dates are a way 
of counting days since an epoch (<julian> January 1 4713 BC or <gregorian> Nov 17, 1858).

This class will use the jdcal package of functions to provide some of the heavy lifting.
All days stored will be in MJD (possibly negative, if before 1858). jdcal functions often 
return two values: jdcal.MJD_0 (2400000.5) and the modified julian date. I'll just always 
pass that + jdcal.MJD_0.
"""

    @classmethod
    def gregorian(cls, year, month, day):
        "Given year,month,day, create an ocal instance according to the Gregorian calendar."
        return cls(year=year, month=month, day=day, calendar=GREGORIAN)

    @classmethod
    def julian(cls, year, month, day):
        "Given year,month,day, create an ocal instance according to the Julian calendar."
        return cls(year=year, month=month, day=day, calendar=JULIAN)

    @classmethod
    def mj_date(cls, date):
        "Create an ocal instance with date as a modified julian date."
        return cls(date=date)

    def __init__(self, **kw):
        """Initialize.

        Ideally called with constructor methods. Optional parameters include:
        * year, month, day: year, month, day according to the calendar system.
        * date: modified julian date 
        * gregorian: if true (the default), use the Gregorian calendar to convert year,month,day to a julian date.
        * julian: if true, use the Julian calendar to convert year,month,day to a julian date.
"""
        if 'calendar' in kw:
            cal = kw['calendar']
        else:
            # default calendar: Gregorian
            cal = GREGORIAN
        if 'date' in kw:
            self.date = kw['date']
        else:
            y=kw['year']
            m=kw['month']
            d=kw['day']
            if cal == GREGORIAN:
                self.date = jdcal.gcal2jd(y,m,d)[1]
            elif cal == JULIAN:
                self.date = jdcal.jcal2jd(y,m,d)[1]
            else:
                raise ValueError("Unknown calendar:{}".format(cal))
        self.calendar = cal
        self.sync_ymd()
            
    def sync_ymd(self):
        def setymdat(p, ymd):
            setattr(self, p+'year' , ymd[0])
            setattr(self, p+'month', ymd[1])
            setattr(self, p+'day'  , ymd[2])
        setymdat('g', self.get_ymd_g())
        setymdat('j', self.get_ymd_j())
        if self.calendar == GREGORIAN:
            ymd=self.get_ymd_g()
        else:
            ymd=self.get_ymd_j()
        setymdat('', ymd)
        setattr(self, 'dow'  , self.get_dow())

    def get_date(self):
        "Return the modified julian date"
        return self.date

    def get_ymd_g(self):
        "return the year, month, and day of the instance, according to the Gregorian calendar"
        return jdcal.jd2gcal(jdcal.MJD_0, self.date)[:3]


    def get_ymd_j(self):
        "return the year, month, and day of the instance, according to the Julian calendar"
        return jdcal.jd2jcal(jdcal.MJD_0, self.date)[:3]

    def __repr__(self):
        if self.calendar == GREGORIAN:
            return "ocal.gregorian({}, {}, {})".format(*self.get_ymd_g())
        else:
            return "ocal.julian({}, {}, {})".format(*self.get_ymd_j())

    def get_dow(self):
        "return the day of week. 0: Sunday, 6: Saturday"
        # the MJD starts on a Wednesday. Offset it from Sunday so modulo works.
        return (self.date+3) % 7

    # The above are all the gazintas/gazattas

    def add_days(self, ndays):
        "add (or subtract if negative) ndays to the date"
        self.date += ndays
        self.sync_ymd()

    def __cmp__(self, oocal):
        try:
            return self.date - oocal.date 
        except AttributeError:
            return NotImplemented

    def __add__(self, ndays):
        return ocal(date=self.date + ndays, calendar=self.calendar)

    def __sub__(self, o): # o could be int (get date n days ago), or ocal (diff between 2 ocals)
        if hasattr(o, 'date'):
            return int(self.date - o.date)
        else:
            return ocal(date=self.date - o, calendar=self.calendar)

    def next_dow(self, nweeks, dow, offset=0):
        """advance the date to the next given day of week (dow. 0==Sunday)

nweeks is number of weeks to advance (-1 means previous day of week)
Offset is added to date before the calculation.

d=ocal.gregorian(year, 11, 1)
d.next_dow(1, 1, offset=-1) # so if Nov 1 is Monday, doesn't change
d.next_dow(2)
"""
        if nweeks > 0:
            self.date += 1
            self.date += offset
            self.date = self.date+(dow-self.get_dow())%7
            self.date += (nweeks-1)*7
        elif nweeks < 0:
            self.date -= 1
            self.date += offset
            self.date = self.date - (self.get_dow()-dow) % 7
            self.date += (nweeks+1)*7
        else:
            raise ValueError, "nweeks of 0 makes no sense"
        self.sync_ymd()

def gregorian(*a, **k):
    return ocal.gregorian(*a, **k)

def julian(*a, **k):
    return ocal.julian(*a, **k)


paschacache={}

def pascha(year):
    if year in paschacache:
        return paschacache[year]

    pdate=ocal.julian(year, 3, 21)
    offset = ((year-1) % 19) + 1
    offset = (offset * 19) + 15
    offset = offset % 30
    #print("Offset is {}".format(offset))
    pdate.add_days(offset)
    #print("pdate full moon on day:{}".format(pdate.get_dow()))
    
    pdate.next_dow(1, 0)
    #print("pdate:{}".format(pdate.get_ymd_g()))
    paschacache[year]=pdate
    return pdate
