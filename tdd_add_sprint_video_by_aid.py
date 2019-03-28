"""
tdd add sprint video by aid
"""
import sys
from biliapi import TddAddSprintVideo
from db import Session

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('error: need more args.')
    else:
        aid = sys.argv[1]
        TddAddSprintVideo.add_sprint_video(aid, Session())
