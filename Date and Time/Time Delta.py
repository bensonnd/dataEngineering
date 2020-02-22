from datetime import datetime, timedelta

# Complete the time_delta function below.
def time_delta(t1, t2):
    temp_t1 = t1[:24]
    temp_t2 = t2[:24]

    utc_hours_t1, utc_hours_t2 = int(t1[-5:-2]), int(t2[-5:-2])
    if utc_hours_t1 >= 0:
        utc_mins_t1 = int(t1[-2:])
    elif utc_hours_t1 < 0:
        utc_mins_t1 = -int(t1[-2:])
    if utc_hours_t2 >= 0:
        utc_mins_t2 = int(t2[-2:])
    elif utc_hours_t2 < 0:
        utc_mins_t2 = -int(t2[-2:])
    time_diff_format = '%a %d %b %Y %H:%M:%S'
    utc_time_t1 = datetime.strptime(temp_t1, time_diff_format) - timedelta(hours=utc_hours_t1, minutes=utc_mins_t1)
    utc_time_t2 = datetime.strptime(temp_t2, time_diff_format) - timedelta(hours=utc_hours_t2, minutes=utc_mins_t2)
    time_diff = utc_time_t1 - utc_time_t2
    time_diff_sec = str(abs(time_diff.total_seconds())).split('.', 1)[0] #in seconds
    return time_diff_sec