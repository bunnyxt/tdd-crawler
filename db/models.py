from sqlalchemy import Column, Integer, String
from .basic import Base


class TddSprintVideo(Base):
    """Tdd Sprint Video"""
    __tablename__ = 'tdd_sprint_video'

    id = Column(Integer, primary_key=True, autoincrement=True)
    added = Column(Integer)  # item add time
    mid = Column(Integer)
    aid = Column(Integer, unique=True)
    tid = Column(Integer, default='')
    cid = Column(Integer)
    typename = Column(String(20), default='')
    arctype = Column(String(20), default='')
    title = Column(String(100), default='')
    pic = Column(String(100), default='')
    pages = Column(Integer)
    created = Column(Integer)
    copyright = Column(Integer)
    singer = Column(String(100), default='')  # singer(s)
    status = Column(String(20), default='processing')  # video status

    def __repr__(self):
        return "<TddSprintVideo(aid=%d,title=%s)>" % (self.aid, self.title)


class TddSprintVideoRecord(Base):
    """Tdd Sprint Video Record"""
    __tablename__ = 'tdd_sprint_video_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    added = Column(Integer)  # item add time
    aid = Column(Integer)
    view = Column(Integer)
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    like = Column(Integer)

    def __repr__(self):
        return "<TddFocusVideoRecord(aid=%d,view=%d)>" % (self.aid, self.view)


class TddMember(Base):
    """Tdd Member"""
    __tablename__ = 'tdd_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    added = Column(Integer)  # item add time
    mid = Column(Integer, unique=True)
    sex = Column(String(20))
    name = Column(String(100))
    face = Column(String(100))

    def __repr__(self):
        return "<TddMember(mid=%d,name=%s)>" % (self.mid, self.name)
