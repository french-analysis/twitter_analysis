date = 'Tue Jun 20 07:30:37 +0000 2017'

import time
from datetime import datetime

ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')) 
