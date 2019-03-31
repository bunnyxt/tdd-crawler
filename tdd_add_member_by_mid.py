"""
tdd add member by mid
"""
import sys
from biliapi import TddAddMember
from db import Session

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('error: need more args.')
    else:
        mid = sys.argv[1]
        TddAddMember.add_member(mid, Session())
