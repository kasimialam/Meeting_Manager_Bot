import datetime

import dateparser
date = dateparser.parse('Tomorrow at two pm')
datetime.datetime(2020, 10, 1, 11, 12, 27, 764201)

print(date)