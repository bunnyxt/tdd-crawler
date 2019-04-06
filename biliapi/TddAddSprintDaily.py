from db import TddSprintDaily, DBOperation


class TddAddSprintDaily:
    """add sprint daily"""
    field_keys = ('added', 'date', 'correct', 'vidnum', 'newvids', 'millvids', 'viewincr', 'viewincrincr', 'comment')

    @classmethod
    def add_sprint_daily(cls, new_daily_info, session=None):
        if new_daily_info:
            print(dict(zip(cls.field_keys, new_daily_info)))
            new_daily = TddSprintDaily(**dict(zip(cls.field_keys, new_daily_info)))
            if session:
                DBOperation.add(new_daily, session)
                return True
            else:
                return False
        else:
            return False
