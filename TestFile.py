import pandas as pd
from datetime import datetime, timedelta
import time

pd.set_option('max_rows', 35)
pd.set_option('max_columns', 25)
pd.set_option('display.width', 1000)

time_stamps_df = pd.read_csv('/Users/847756/Desktop/time_stamps.csv', header=None)
time_stamps_df_1 = time_stamps_df.iloc[::2].reset_index(drop=True) #grab every other row starting with index 0 from timestamp dataframe
time_stamps_df_2 = time_stamps_df.iloc[1::2].reset_index(drop=True) #grab every other row starting with index 1 from timestamp dataframe
time_stamp_diffs_pd = pd.read_csv('/Users/847756/Desktop/time_stamp_diffs.csv', header=None, names=["Diff"])
delta_test = pd.DataFrame(columns=['Diff'])
time_stamp_diffs_pd["Diff"] = time_stamp_diffs_pd["Diff"].astype(str)
delta_test["Diff"] = delta_test["Diff"].astype(str)

t = len(time_stamps_df.index)//2


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


for t_itr in range(t):
    t1 = time_stamps_df_1.iat[t_itr,0]
        #print(t1)
    t2 = time_stamps_df_2.iat[t_itr,0]
    #print(t2)
    delta = time_delta(t1, t2)
    #throw_away_df = pd.DataFrame(delta, columns = ['Diff'])
    delta_test = delta_test.append({'Diff': delta}, ignore_index=True)

"""t1 = 'Thu 16 Jul 2026 06:28:56 -0930'
t2 = 'Sun 20 Apr 2149 00:02:39 -0400'
delta = time_delta(t1, t2)
print(delta)"""

#delta_missing = delta_test[~delta_test.isin(time_stamp_diffs_pd.to_dict('l')).all(1)]
delta_missing = delta_test[~delta_test.isin(time_stamp_diffs_pd.to_dict('l')).all(1)]
print(delta_missing)
delta_missing_expected = delta_missing.join(time_stamp_diffs_pd, lsuffix='', rsuffix='_expected')
print(delta_missing_expected)
with_dft1 = delta_missing_expected.join(time_stamps_df_1)
with_dft1 = with_dft1.rename(columns={0: "ts1"})
print(with_dft1)
with_dft2 = with_dft1.join(time_stamps_df_2)
with_dft2 = with_dft2.rename(columns={0: "ts2"})
with_dft2["Diff"] = with_dft2["Diff"].astype('int64')
with_dft2["Diff_expected"] = with_dft2["Diff_expected"].astype('int64')
with_dft2['time_diff'] = with_dft2.Diff - with_dft2.Diff_expected
print(with_dft2)


