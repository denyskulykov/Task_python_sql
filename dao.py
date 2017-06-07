import sqlite3

# Use sqlite in memory
# Not need to close
connect = sqlite3.connect(':memory:')
cursor = connect.cursor()


def _exe_raw_sql(sql):
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        raise err
    else:
        connect.commit()
    return fetchall


def create_bd_input_data():
    sql = """
    CREATE TABLE inputData(
        Locode VARCHAR(6) NOT NULL,
        Phrase VARCHAR(255) NOT NULL,
        Pr201604 INT,
        Pr201605 INT,
        Pr201606 INT,
        Pr201607 INT,
        Pr201608 INT,
        Pr201609 INT,
        Pr201610 INT,
        Pr201611 INT,
        Pr201612 INT,
        Pr201701 INT,
        Pr201702 INT,
        Pr201703 INT,
        AvgMsv INT,
        Competition REAL,
        CostPerClick REAL,
        Unestimated INT DEFAULT 1,
        Correct INT DEFAULT 1,
        Identifier TXT NOT NULL,
        CONSTRAINT unique_local UNIQUE (Identifier)
        );
    """
    _exe_raw_sql(sql)


def create_bd_top_msv_click():
    sql = """
    CREATE TABLE topClick(
        Phrase VARCHAR(255),
        AU INT DEFAULT 0,
        CA INT DEFAULT 0,
        GB INT DEFAULT 0,
        US INT DEFAULT 0,
        USNYC INT DEFAULT 0,
        Total INT DEFAULT 0);
    """
    _exe_raw_sql(sql)


def create_bd_top_msv_price():
    sql = """
    CREATE TABLE topPrice(
        Phrase VARCHAR(255),
        AU REAL DEFAULT 0,
        CA REAL DEFAULT 0,
        GB REAL DEFAULT 0,
        US REAL DEFAULT 0,
        USNYC REAL DEFAULT 0,
        MaxCostPerClick REAL DEFAULT 0);
    """
    _exe_raw_sql(sql)


def create_bd_regionality():
    sql = """
    CREATE TABLE Regionality(
        Phrase VARCHAR(255),
        AU REAL DEFAULT 0,
        CA REAL DEFAULT 0,
        GB REAL DEFAULT 0,
        US REAL DEFAULT 0,
        USNYC REAL DEFAULT 0);
    """
    _exe_raw_sql(sql)


def update_bd_input_data(data):
    """Data should be List"""

    for line in data:
        cols = ', '.join("{0}='{1}'".format(key, val) for key, val in
                         line.items() if key != "Phrase"
                         or key != "Locode" or key != 'Identifier')

        sql = """UPDATE inputdata SET {0} WHERE
              Identifier = '{1}'""".format(cols, line["Identifier"])
        try:
            cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            raise err
    connect.commit()


def delete_partly_empty_line_from_inputdata():
    sql = """
        UPDATE inputData SET Correct = 0 WHERE
            Pr201604 = '' AND
            Pr201605 = '' AND
            Pr201606 = '' AND
            Pr201607 = '' AND
            Pr201608 = '' AND
            Pr201609 = '' AND
            Pr201610 = '' AND
            Pr201611 = '' AND
            Pr201612 = '' AND
            Pr201701 = '' AND
            Pr201702 = '' AND
            Pr201703 = '' AND
            AvgMsv  = '' AND
            Correct = 1;
        """
    _exe_raw_sql(sql)


def delete_anomaly_from_inputdata(more):
    sql = """
    UPDATE inputData SET Correct = 0 WHERE
    AvgMsv > {0};""".format(more)
    _exe_raw_sql(sql)


def get_empty_competition():
    sql = """SELECT * FROM inputData WHERE
        Competition = '' AND Correct = 1;
    """
    return _exe_raw_sql(sql)


def get_empty_costPerClick():
    sql = """SELECT * FROM inputData WHERE
        CostPerClick = '' AND Correct = 1;
    """
    return _exe_raw_sql(sql)


def get_empty_cells_for_avg_less_100():
    sql = """SELECT * FROM inputData WHERE (
    Pr201604 = '' OR Pr201605 = '' OR Pr201606 = '' OR Pr201607 = '' OR
    Pr201608 = '' OR Pr201609 = '' OR Pr201610 = '' OR Pr201611 = '' OR
    Pr201612 = '' OR Pr201701 = '' OR Pr201702 = '' OR Pr201703 = '' OR
    Competition = '' OR CostPerClick = '')
    AND AvgMsv < 100 AND Correct = 1;
    """
    return _exe_raw_sql(sql)


def modify_input_data():
    sql = "UPDATE inputdata SET Locode='USNYC' WHERE Locode='US NYC';"
    return _exe_raw_sql(sql)


def get_top_phrase_by_click_with_limit(limit):
    sql = """SELECT * FROM topclick ORDER BY Total DESC
    LIMIT {0}""".format(limit)

    return _exe_raw_sql(sql)


def get_top_phrase_by_price_with_limit(limit):
    sql = """SELECT * FROM topprice ORDER BY MaxCostPerClick DESC
    LIMIT {0}""".format(limit)

    return _exe_raw_sql(sql)


def get_all_fields_instead_of_total_from_top_click():
    sql = """SELECT Phrase, AU,CA, GB, US, USNYC FROM TopClick;"""
    return _exe_raw_sql(sql)


def get_sort_regionality_by_locode_with_limit(locode, limit):
    sql = """SELECT Phrase, {0} FROM Regionality
    ORDER BY {0} DESC LIMIT {1}""".format(locode, limit)
    return _exe_raw_sql(sql)


# Common methods
def insert_into_table(table, data):
    """Data should be List"""

    for line in data:
        cols = ', '.join("'{}'".format(col) for col in line.keys())
        vals = ', '.join(':{}'.format(col) for col in line.keys())
        sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, cols, vals)
        try:
            cursor.execute(sql, line)
        except sqlite3.IntegrityError:
            # ignore duplicate
            pass
        except sqlite3.DatabaseError as err:
            raise err
    connect.commit()


def get_all_from_table(table):
    sql = "SELECT * FROM {0};".format(table)
    return _exe_raw_sql(sql)


def get_all_from_table_filter_correct(table):
    sql = "SELECT * FROM {0} WHERE Correct = 1;".format(table)
    return _exe_raw_sql(sql)


def get_request_by_phrase(table, phrase):
    sql = "SELECT * FROM {0} WHERE Phrase = '{1}';".format(table, phrase)
    return _exe_raw_sql(sql)
