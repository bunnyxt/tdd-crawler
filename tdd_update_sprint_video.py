"""
tdd update sprint video
"""

import time
import schedule
import datetime
import threading
from queue import Queue
from biliapi import TddAddSprintVideoRecord
from db import Session, DBOperation, TddSprintVideo
from utils import Producer3, Consumer, Timer


def get_update_aids():
    result = []
    items = DBOperation.query(TddSprintVideo, Session())
    print(items)
    for item in items:
        if item.status == 'processing':
            result.append(item.aid)
    return result


def tdd_update_sprint_video(get_session):
    print("now start update at %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    Q = Queue()
    mythreads = []
    aids = get_update_aids()
    print("try update videos with aids " + str(aids))
    pthread = Producer3(Q, video_aids=aids, func=lambda x: (x,), sleepsec=0.5)
    mythreads.append(pthread)
    consumer_num = 4  # 4个消费者线程
    sessions = [get_session() for _ in range(consumer_num)]
    for i in range(consumer_num):
        db_session = sessions[i]  # 每个线程一个session
        cthread = Consumer(Q, session=db_session, func=TddAddSprintVideoRecord.add_sprint_video_record, sleepsec=0.5)
        mythreads.append(cthread)
    with Timer() as t:
        for thread in mythreads:
            thread.start()
        for thread in mythreads:
            thread.join()
    for session in sessions:
        session.close()
    print("update finished, runtime: %s" % t.elapsed)


def tdd_update_sprint_video_task(get_session):
    threading.Thread(target=tdd_update_sprint_video, args=(get_session,)).start()


if __name__ == '__main__':

    tdd_update_sprint_video(Session)

    schedule.every(10).minutes.do(tdd_update_sprint_video_task, Session)

    while True:
        schedule.run_pending()
        time.sleep(10)
