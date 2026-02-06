from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LOGIN_URL = "https://cloud.aktivkonzepte.de/hspulm/index.html##/Home/KursListe"
IS_LOGGED_IN_URL = "https://cloud.aktivkonzepte.de/busiulm/api/IsLoggedIn"
KURSLISTE_URL = "https://cloud.aktivkonzepte.de/busiulm/LANG-DEU/Home/KursListe"
ENROLLMENT_URL = "https://cloud.aktivkonzepte.de/busiulm/LANG-DEU/Home/KursBuchen/{course_id}?Storno=False"

AUTH_STATE = "auth.json"

MAX_RATE = 0.15
MED_RATE = 1.0
MIN_RATE = 3.0
ERROR_BACKOFF = 2.0

COURSE_NAMES = [""]
OPEN_TIME = datetime(2026, 2, 6, 19, 39, 0, tzinfo=ZoneInfo("Europe/Berlin")) # Year, Month, Day, Hour, Minute, Second