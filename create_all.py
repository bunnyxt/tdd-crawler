from db import Base, eng

if __name__ == '__main__':
    Base.metadata.create_all(eng)
    print('db engine created!')
