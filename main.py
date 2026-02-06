from resources.login import login, check_logged_in
from resources.getdata import get_course_list, get_course_ids, check_enrollable
from resources.enroll import enroll, sleep_with_jitter, now, compute_interval
from config import *

if not check_logged_in():
    login()

ids = get_course_ids(get_course_list(), COURSE_NAMES)

print(now())
ratelimit = 0
interval = MIN_RATE

while ids:
    seconds_to_open = (OPEN_TIME - now()).total_seconds()

    if ratelimit <= 0:
        if seconds_to_open > 0:
            interval = compute_interval(seconds_to_open)
        else:
            interval = MIN_RATE

    try:
        for enrollable in check_enrollable(ids):
            enroll(enrollable)
            ids.remove(enrollable)
    except Exception as e:
        interval = min(interval * ERROR_BACKOFF, 10.0)
        ratelimit += 2
    print("Enrollment should start in about ", seconds_to_open, " seconds")
    print("Currently polling every ", interval, " seconds for course(s) ", ids)
    sleep_with_jitter(interval)
