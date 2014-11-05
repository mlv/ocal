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

This package will also include a get_pascha(year) function that returns an ocal instance.
