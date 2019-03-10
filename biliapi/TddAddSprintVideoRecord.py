import json
import random
import requests
from config import get_user_agents, get_urls
from logger import bilivideolog
from db import TddSprintVideoRecord, DBOperation
from .support import get_timestamp_ms, get_timestamp_s


class TddAddSprintVideoRecord:
    """add sprint video record"""
    field_keys = ('added', 'aid', 'view', 'danmaku', 'reply', 'favorite',
                  'coin', 'share', 'like')

    def __init__(self, aid):
        self.aid = aid
        self.info = None

    def get_ajax_info(self):
        url = get_urls('url_stat')
        timestamp_ms = get_timestamp_ms()
        uas = get_user_agents()
        params = {'aid': str(self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(uas)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None

        text = json.loads(res.text)
        try:
            if text['code'] == 0:
                data = text['data']
                # ('added', 'aid', 'view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like')
                related_info = (get_timestamp_s(), self.aid, data['view'], data['danmaku'],
                                data['reply'], data['favorite'], data['coin'],
                                data['share'], data['like'])
                return related_info
            else:
                msg = 'aid({}) ajax request code return error'.format(self.aid)
                bilivideolog.info(msg)
                return None
        except TypeError:
            msg = 'aid({}) text return None'.format(self.aid)
            bilivideolog.info(msg)
            return None

    @classmethod
    def get_sprint_video_record(cls, aid):
        info_ajax = cls(aid).get_ajax_info()
        try:
            info = info_ajax
        except Exception as e:
            info = None
        return info

    @classmethod
    def add_sprint_video_record(cls, aid, session=None):
        sprint_video_record = cls.get_sprint_video_record(aid)
        if sprint_video_record:
            print(dict(zip(cls.field_keys, sprint_video_record)))
            new_sprint_video_record = TddSprintVideoRecord(**dict(zip(cls.field_keys, sprint_video_record)))
            if session:
                DBOperation.add(new_sprint_video_record, session)
                return True
            else:
                return False
        else:
            return False
