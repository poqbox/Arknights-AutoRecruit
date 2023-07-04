import sqlite3
from multipledispatch import dispatch


def commit_transactions(con):
    con.commit()


def close_connection(con):
    con.close()


def delete_from_table_where(cur, table, where_clause):
    query = "delete from " + table + " where " + where_clause
    cur.execute(query)


def update_table_set_columns_where(cur, table, set_clause, where_clause):
    query = "update " + table + " set " + set_clause + " where " + where_clause
    cur.execute(query)


def select_all_from_table(cur, table):
    query = "select * from " + table
    cur.execute(query)


@dispatch(any, any, any)
def select_columns_from_table(cur, column1, table):
    query = "select ? from " + table
    column_data = [column1]
    cur.execute(query, column_data)

@dispatch(any, any, any, any)
def select_columns_from_table(cur, column1, column2, table):
    query = "select ?, ? from " + table
    column_data = column1, column2
    cur.execute(query, column_data)

@dispatch(any, any, any, any, any)
def select_columns_from_table(cur, column1, column2, column3, table):
    query = "select ?, ?, ? from " + table
    column_data = column1, column2, column3
    cur.execute(query, column_data)


@dispatch(any, any, any)
def insert_into_table_values(cur, table, value1):
    query = "insert into " + table + " values (?)"
    insert_data = [value1]
    cur.execute(query, insert_data)

@dispatch(any, any, any, any)
def insert_into_table_values(cur, table, value1, value2):
    query = "insert into " + table + " values (?, ?)"
    insert_data = value1, value2
    cur.execute(query, insert_data)

@dispatch(any, any, any, any, any)
def insert_into_table_values(cur, table, value1, value2, value3):
    query = "insert into " + table + " values (?, ?, ?)"
    insert_data = value1, value2, value3
    cur.execute(query, insert_data)

@dispatch(any, any, any, any, any, any)
def insert_into_table_values(cur, table, value1, value2, value3, value4):
    query = "insert into " + table + " values (?, ?, ?, ?)"
    insert_data = value1, value2, value3, value4
    cur.execute(query, insert_data)
