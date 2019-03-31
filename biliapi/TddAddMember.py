import json
import random
import requests
from config import get_user_agents, get_urls
from logger import bilivideolog
from db import TddMember, DBOperation
from .support import get_timestamp_s


class TddAddMember:
    """add member"""
    field_keys = ('added', 'mid', 'sex', 'name', 'face')

    def __init__(self, mid):
        self.mid = mid
        self.info = None

    def get_member_info(self):
        url = get_urls('url_space')
        uas = get_user_agents()
        params = {'mid': str(self.mid)}
        headers = {'User-Agent': random.choice(uas)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            msg = 'mid({}) get error'.format(self.mid)
            bilivideolog.error(msg)
            return None

        data = json.loads(res.text)
        data = data['data']
        if 'mid' in data:
            # ('added', 'mid', 'sex', 'name', 'face')
            member_info = (get_timestamp_s(), self.mid, data['sex'],
                           data['name'], data['face'])
            return member_info

        else:
            msg = 'mid({}) info request return error'.format(self.mid)
            bilivideolog.info(msg)
            return None

    @classmethod
    def get_new_member_info(cls, mid):
        member_info = cls(mid).get_member_info()
        try:
            info = member_info
        except Exception as e:
            info = None
        return info

    @classmethod
    def add_member(cls, mid, session=None):
        new_member_info = cls.get_new_member_info(mid)
        if new_member_info:
            print(dict(zip(cls.field_keys, new_member_info)))
            new_member = TddMember(**dict(zip(cls.field_keys, new_member_info)))
            if session:
                DBOperation.add(new_member, session)
                return True
            else:
                return False
        else:
            return False
