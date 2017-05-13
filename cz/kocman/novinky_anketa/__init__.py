import urllib
import json
import re
import os
import time

import novinky_tool

baseDir = 'inquiries'
if not os.path.exists(baseDir):
    os.mkdir(baseDir)

inquireId =  novinky_tool.get_last_inquire()
inquire = novinky_tool.get_inquire(inquireId)
# inquireDir = os.path.join(baseDir, str(inquireId))
novinky_tool.add_or_create_inquire(inquire)






# cislo = '16515'


