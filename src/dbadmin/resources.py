from src.dbadmin.dao import Reset


class DB(object):

    def reset(self):
        store = Reset()
        return store.execute()
