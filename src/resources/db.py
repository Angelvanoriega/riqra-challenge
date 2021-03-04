from src.procedures.procedures import Reset


class DB(object):

    def reset(self):
        store = Reset()
        return store.execute()
