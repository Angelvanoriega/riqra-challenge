import re
from src.db import DataBase
import logging

logger = logging.getLogger()


class Store(object):
    def execute(self):
        statement = self.convert_to_statement()
        db = DataBase()
        cursor = db.cursor
        try:
            cursor.execute("BEGIN")
            cursor.execute(statement)
            results_sql = cursor.fetchall()
            if len(results_sql) == 0:
                results_sql = []
            else:
                results_sql = results_sql[0][0]
                if results_sql is None:
                    results_sql = []
            cursor.execute("COMMIT")
        except Exception as error:
            return {'error': error.pgerror, 'code': error.pgcode}
        finally:
            cursor.close()
        return results_sql

    def convert_to_statement(self):
        var_names = self.get_variables_names()
        attributes = self.__dict__
        body = ""
        for var in var_names:
            body = body + "'" + str(attributes[var]).replace("'", "''") + "',"
        body = "SELECT " + self.__class__.__name__.lower() + "(" \
               + body[:-1] + ")"
        print(body)
        logger.info(body)
        return body

    def get_variables_names(self):
        attributes = self.__dict__
        var_names = []
        for var_name in attributes:
            if not (
                    var_name[0].startswith('__') and var_name[0].endswith(
                '__')):
                var_names.append(var_name)
        return var_names
