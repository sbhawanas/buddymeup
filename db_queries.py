"""
file with
+ connection to db for backend requirements
* sql queries
* config for variable settings per track #todo: this needs to be put into a matching-config file!
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
with open('config.json') as config_file:
    conf_data = json.load(config_file)

## DB connection
def connect():
    connection = None
    if "DATABASE_URL" in os.environ:
        DATABASE_URL = os.environ["DATABASE_URL"]
    else:
        db = conf_data["db"]
        DATABASE_URL = f"postgresql://{db['user']}@{db['host']}/{db['db_name']}"

    try:
        # connect to the PostgreSQL server
        connection = psycopg2.connect(DATABASE_URL)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    except psycopg2.DatabaseError as e:
        print(e)


def m_single_insert(conn, df):
    """
    THIS FUNCTION IS IN WORK!
    """
    cur = conn.cursor()
    try:
        # Inserting each row
        for i in df.index:
            query = """INSERT INTO matches (fk_round_id, fk_user_1_id, fk_user_2_id, algo_score_u1, algo_score_u2) 
                        VALUES('{0}','{1}','{2}','{3}','{4}') ON CONFLICT ON CONSTRAINT round_u1_u2 DO NOTHING
                        ;""".format(df['fk_round_id'][i], df['fk_user_1_id'][i], df['fk_user_2_id'][i],
                                    df['algo_score_u1'][i],
                                    df['algo_score_u2'][i])

            cur.execute(query)
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return
    conn.close()
    print("\nNew matches are inserted in db matches table")
    return












## QUERIES

# add users_round_info_id here (add find solution for .csv)
var = ['id', 'email', 'name', 'slack_name', 'gender', 'timezone', 'age',  'topic',
              'experience', 'mentor_choice', 'relation_pref', 'freq_pref', 'gender_pref',
              'timezone_pref', 'amount_buddies', 'objectives', 'personal_descr'] #todo put this into config file

#topics_python = ["data science", "mobile", "machine learning", "backend", "frontend"] #todo put this into config file


signup_info_var = "ua.{}, ua.{}, ua.{}, ua.{}, ur.{}, " \
                  "l.{}, " \
                  "ur.{}, ur.{}, ur.{}, ur.{}, ur.{}, " \
                  "ur.{}, ur.{}, ur.{}, ur.{}, " \
                  "ur.{}, ur.{}".format(*var) #*conf_data["var"]["python"]

signup_info = (f" SELECT {signup_info_var}"
               f" FROM users_rounds as ur"
               f" INNER JOIN users_all as ua"
               f" ON ur.fk_user_id = ua.id"
               f" INNER JOIN locations as l"
               f" ON ur.fk_location_id = l.id" 
               f" WHERE ur.fk_round_id = 91;") #15 is round two! 91 is sround 3




prior_part = (f"SELECT * FROM matches;")















#####################
#def many_insert(connection, matches_db):
#     """
#     THIS FUNCTION IS IN WORK!
#     Using cursor.executemany() to insert the matches dataframe
#     """
#     df = matches_db.copy()
#
#     # Create a list of tuples from the dataframe values
#     connection = connect()
#     tuples = [tuple(x) for x in df.to_numpy()]
#     # Comma-separated dataframe columns
#     cols = ','.join(list(df.columns))
#     # SQL query to execute
#     query = """INSERT INTO matches (fk_round_id, fk_user_1_id, fk_user_2_id, algo_score_u1, algo_score_u2)
#                     VALUES( %s, %s, %s, %s, %s)
#                     ON CONFLICT ON CONSTRAINT matches_fk_round_id_fkey DO NOTHING;"""
#     print(query)
#
#     cur = connection.cursor()
#     try:
#         cur.executemany(query, tuples)
#         connection.commit()
#
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error: %s" % error)
#         connection.rollback()
#         cur.close()
#         #return 1
#
#     print("execute_many() done")
#     connection.close()
#     return





