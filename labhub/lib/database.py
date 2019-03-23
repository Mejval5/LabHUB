#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extensions

class Database(object):
    """
    Class taking care for all the dirty work with database.
    """
    def __init__(self, host="localhost", user=None, passwd=None, db=None, port=5432):
        """
        Create connection that will be used by all requests.
        """
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

        self.connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=passwd,
                database=db
            )
