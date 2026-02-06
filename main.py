from resources.login import login, check_logged_in
from resources.getdata import get_course_list, get_course_ids, check_enrollable
from resources.enroll import enroll
from config import *

import sys
import time

if not check_logged_in():
    login()

ids = get_course_ids(get_course_list(), COURSE_NAMES)

while ids:
    for enrollable in check_enrollable(ids):
        print(enrollable)
        ids.remove(enrollable)

    time.sleep(0.25)

sys.exit(0)

