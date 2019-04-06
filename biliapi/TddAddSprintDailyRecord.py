from db import TddSprintDailyRecord, DBOperation


class TddAddSprintDailyRecord:
    """add sprint daily record"""
    field_keys = ('added', 'date', 'aid', 'view', 'viewincr', 'pday', 'lday')

    @classmethod
    def add_sprint_daily_record(cls, new_daily_record_info, session=None):
        if new_daily_record_info:
            print(dict(zip(cls.field_keys, new_daily_record_info)))
            new_daily_record = TddSprintDailyRecord(**dict(zip(cls.field_keys, new_daily_record_info)))
            if session:
                DBOperation.add(new_daily_record, session)
                return True
            else:
                return False
        else:
            return False
