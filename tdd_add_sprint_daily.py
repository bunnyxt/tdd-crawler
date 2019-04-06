"""
tdd add sprint daily by aid
"""
import sys
import schedule
import time
import datetime
from db import TddSprintVideo, TddSprintDaily
from db import Session, DBOperation
from biliapi import TddAddSprintDaily, TddAddSprintDailyRecord
from biliapi.support import get_timestamp_s


def tdd_add_sprint_daily(date):
    # format date
    if date == -1:
        # get now time to format as date
        date = datetime.datetime.now().strftime('%Y%m%d')
        pass

    end_ts = int(time.mktime(time.strptime(date, "%Y%m%d"))) + 60 * 60 * 6
    start_ts = end_ts - 60 * 60 * 24

    # get videos
    sprint_videos = []
    new_videos = []
    million_videos = []
    items = DBOperation.query(TddSprintVideo, Session())
    for item in items:
        if item.added < end_ts:
            if item.status == 'processing':  # notice: may cause error when calc history daily
                sprint_videos.append((item.aid, item.created))
                if item.added >= start_ts and item.added < end_ts:
                    new_videos.append(item.aid)

    vidnum = len(sprint_videos)
    view_incr = 0

    # get records
    for (aid, created) in sprint_videos:
        start_record = DBOperation.query_vid_record(aid, start_ts, Session())
        if len(start_record) == 1:
            start_record = start_record[0]
        else:
            start_record = 0
        end_record = DBOperation.query_vid_record(aid, end_ts, Session())
        if len(end_record) == 1:
            end_record = end_record[0]
        else:
            million_videos.append(aid)
            vidnum -= 1
            continue
        view = end_record.view
        view_increment = end_record.view - start_record.view
        pday = int((end_ts - created) / (60 * 60 * 24))
        lday = int((1000000 - view) / view_increment)
        view_incr += view_increment
        new_daily_record_info = (get_timestamp_s(), date, aid, view, view_increment, pday, lday)
        print(new_daily_record_info)
        TddAddSprintDailyRecord.add_sprint_daily_record(new_daily_record_info, Session())

    new_videos_str = ""
    for new_video in new_videos:
        new_videos_str += (str(new_video) + ';')
    million_videos_str = ""
    for million_video in million_videos:
        million_videos_str += (str(million_video) + ';')
    view_incr_incr = 0
    all_daily = DBOperation.query(TddSprintDaily, Session())
    if len(all_daily) > 0:
        last_daily = all_daily[-1]
        i = len(all_daily) - 1
        while i >= 0:
            tmp_daily = all_daily[i]
            if tmp_daily.correct:
                last_daily = tmp_daily
                break
            else:
                i -= 1
        view_incr_incr = view_incr - last_daily.viewincr
    comment = ""
    new_daily_info = (get_timestamp_s(), date, True, vidnum, new_videos_str, million_videos_str,
                      view_incr, view_incr_incr, comment)
    print(new_daily_info)
    TddAddSprintDaily.add_sprint_daily(new_daily_info, Session())


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # schedule
        schedule.every().day.at("06:30").do(tdd_add_sprint_daily, -1)
        while True:
            schedule.run_pending()
            time.sleep(10)
    else:
        # manual
        date = sys.argv[1]
        tdd_add_sprint_daily(str(date))
