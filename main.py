from resources.login import login, check_logged_in
from resources.getdata import get_course_list, get_course_ids, check_enrollable, getMetadata
from resources.enroll import enroll, sleep_with_jitter, now, compute_interval
from config import *
import time

if not check_logged_in():
    login()

courses = get_course_list()

# ids = get_course_ids(courses, COURSE_NAMES)
ids = COURSE_IDS

if DEBUG:
    print(now())
    print(courses)
    print(getMetadata(ids))

ratelimit = 0
interval = MAX_RATE
loop_counter = 0

while ids:
    if loop_counter >= 60:
        loop_counter = 0
        if not check_logged_in():
            login()
    else:
        loop_counter+=1
    
    seconds_to_open = (OPEN_TIME - now()).total_seconds()

    if ratelimit <= 0:
        if seconds_to_open > 0:
            interval = compute_interval(seconds_to_open)
        else:
            interval = MAX_RATE

    try:
        for enrollable in check_enrollable(ids):
            enroll(enrollable)
            ids.remove(enrollable)
    except Exception as e:
        interval = min(interval * ERROR_BACKOFF, 10.0)
        ratelimit += 2
    print(f"Enrollment should start in about {seconds_to_open} seconds")
    print(f"Currently polling every {interval} seconds for course(s) {ids}")
    sleep_with_jitter(interval)
