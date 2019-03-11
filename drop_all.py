from db import Base, eng

if __name__ == '__main__':
    check = input(
        'WARNING: Are you sure to drop all tables? (y/n)')
    if check == 'Y' or check == 'y':
        Base.metadata.drop_all(eng)
        print('db tables dropped!')
