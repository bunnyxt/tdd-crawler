import json
import random
import requests
from config import get_user_agents, get_urls, get_key
from logger import bilivideolog
from db import TddSprintVideo, DBOperation
from .support import get_timestamp_ms, get_timestamp_s


class TddAddSprintVideo:
    """add sprint video"""
    field_keys = ('added', 'mid', 'aid', 'tid', 'cid', 'typename', 'arctype', 'title',
                  'pic', 'pages', 'created', 'copyright', 'singer', 'solo', 'original', 'status')

    def __init__(self, aid):
        self.aid = aid
        self.info = None

    def get_basic_info(self):
        url = get_urls('url_view')
        timestamp_ms = get_timestamp_ms()
        appkey = get_key()
        uas = get_user_agents()
        params = {'type': 'json', 'appkey': appkey, 'id': str(
            self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(uas)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None

        data = json.loads(res.text)
        if 'mid' in data:
            # ('added','mid','aid','tid','cid','typename','arctype','title','pic','pages','created')
            related_info = (get_timestamp_s(), data['mid'], self.aid, data['tid'],
                            data['cid'], data['typename'], data['arctype'],
                            data['title'], data['pic'],
                            data['pages'], data['created'])
            return related_info

        else:
            msg = 'aid({}) basic info request  return error'.format(self.aid)
            bilivideolog.info(msg)
            return None

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
                # （'copyright'）
                related_info = (data['copyright'],)
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
    def get_sprint_video_info(cls, aid):
        info_basic = cls(aid).get_basic_info()
        info_ajax = cls(aid).get_ajax_info()
        try:
            info = info_basic + info_ajax
        except Exception as e:
            info = None
        return info

    @classmethod
    def add_sprint_video(cls, aid, session=None):
        new_video_info = cls.get_sprint_video_info(aid)
        new_video_info = new_video_info + ('',)  # add singer
        new_video_info = new_video_info + (True,)  # add solo
        new_video_info = new_video_info + (True,)  # add original
        new_video_info = new_video_info + ('processing',)  # add status
        if new_video_info:
            print(dict(zip(cls.field_keys, new_video_info)))
            new_sprint_video = TddSprintVideo(**dict(zip(cls.field_keys, new_video_info)))
            if session:
                DBOperation.add(new_sprint_video, session)
                return True
            else:
                return False
        else:
            return False
