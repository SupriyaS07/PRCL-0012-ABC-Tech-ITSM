import mysql.connector
import pandas as pd
import time

# ── Try multiple connection configs ───────────────
CONFIGS = [
    # Config 1 — SSL disabled
    {
        'host'              : '18.136.157.135',
        'user'              : 'dm_team',
        'password'          : 'DM!$Team@&27920!',
        'database'          : 'project_itsm',
        'ssl_disabled'      : True,
        'connection_timeout': 60,
        'autocommit'        : True,
    },
    # Config 2 — with port explicit
    {
        'host'              : '18.136.157.135',
        'port'              : 3306,
        'user'              : 'dm_team',
        'password'          : 'DM!$Team@&27920!',
        'database'          : 'project_itsm',
        'ssl_disabled'      : True,
        'connection_timeout': 60,
        'autocommit'        : True,
        'use_pure'          : True,
    },
    # Config 3 — minimal config
    {
        'host'    : '18.136.157.135',
        'port'    : 3306,
        'user'    : 'dm_team',
        'password': 'DM!$Team@&27920!',
        'database': 'project_itsm',
        'use_pure': True,
    },
]

def get_connection():
    for i, config in enumerate(CONFIGS):
        try:
            conn = mysql.connector.connect(**config)
            if conn.is_connected():
                print(f"✅ Connected using config {i+1}")
                return conn
        except Exception as e:
            print(f"Config {i+1} failed: {e}")
            time.sleep(1)
    raise Exception("All connection configs failed")

def fetch_data(query):
    try:
        conn = get_connection()
        df   = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"DB Error: {e}")
        return pd.DataFrame()

def get_summary_stats():
    try:
        conn = get_connection()

        total = pd.read_sql(
            "SELECT COUNT(*) as total FROM dataset_list", conn)

        priority = pd.read_sql("""
            SELECT Priority, COUNT(*) as count
            FROM dataset_list
            GROUP BY Priority
            ORDER BY Priority
        """, conn)

        category = pd.read_sql("""
            SELECT Category, COUNT(*) as count
            FROM dataset_list
            GROUP BY Category
        """, conn)

        yearly = pd.read_sql("""
            SELECT YEAR(Open_Time) as year, COUNT(*) as count
            FROM dataset_list
            WHERE Open_Time IS NOT NULL
            GROUP BY YEAR(Open_Time)
            ORDER BY year
        """, conn)

        conn.close()

        return {
            'total'   : int(total['total'][0]),
            'priority': priority.to_dict(orient='records'),
            'category': category.to_dict(orient='records'),
            'yearly'  : yearly.to_dict(orient='records')
        }

    except Exception as e:
        print(f"Summary stats error: {e}")
        # Return cached static data if DB fails
        return {
            'total'   : 46606,
            'priority': [
                {'Priority': 1.0, 'count': 3},
                {'Priority': 2.0, 'count': 697},
                {'Priority': 3.0, 'count': 5323},
                {'Priority': 4.0, 'count': 24097},
                {'Priority': 5.0, 'count': 16486}
            ],
            'category': [
                {'Category': 'complaint',            'count': 11},
                {'Category': 'incident',             'count': 37748},
                {'Category': 'request for change',   'count': 1},
                {'Category': 'request for information', 'count': 8846}
            ],
            'yearly': [
                {'year': 2012, 'count': 10},
                {'year': 2013, 'count': 12246},
                {'year': 2014, 'count': 9903}
            ]
        }

def get_monthly_volume():
    try:
        conn = get_connection()

        query = """
            SELECT
                YEAR(Open_Time)  as year,
                MONTH(Open_Time) as month,
                COUNT(*)         as count
            FROM dataset_list
            WHERE Open_Time IS NOT NULL
            AND YEAR(Open_Time) != 2012
            AND NOT (YEAR(Open_Time) = 2013 AND MONTH(Open_Time) = 6)
            GROUP BY YEAR(Open_Time), MONTH(Open_Time)
            ORDER BY year, month
        """

        monthly = pd.read_sql(query, conn)
        conn.close()
        return monthly

    except Exception as e:
        print(f"Monthly volume error: {e}")
        # Return cached historical data if DB fails
        return pd.DataFrame({
            'year' : [2013,2013,2013,2013,2013,2013,2013,2013,2013,2013,2013,
                      2014,2014,2014,2014,2014,2014,2014,2014,2014,2014,2014,2014],
            'month': [1,2,3,4,5,7,8,9,10,11,12,
                      1,2,3,4,5,6,7,8,9,10,11,12],
            'count': [1086,1128,1061,1460,959,967,791,871,873,1186,910,
                      19,468,1412,954,873,1389,1193,416,391,1230,845,713]
        })