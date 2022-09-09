import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# 写入数据库
# create connection
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Huobi1234@localhost:5432/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# df = pd.read_csv(r"C:\pythonProj\data\mandatory_liquidation\origin_data\btcusdt_5min_1620748800_to_1647014400.csv")
# print(df)
# # 写入pg库
# df.to_sql(schema='public', con=engine, name='finance', if_exists='replace', index=False)


# 直接用pandas去读取，省去了转换的步骤
df = pd.read_sql('SELECT * FROM finance', engine)
print(df)


# # database，user，password，host，port分别对应要连接的 PostgreSQL 数据库的数据库名、数据库用户名、用户密码、主机、端口信息，请根据具体情况自行修改
# conn = psycopg2.connect(database="postgres", user="postgres",
# 	                    password="Huobi1234", host="localhost", port="5432")
#
# df = pd.read_csv(r"C:\pythonProj\data\mandatory_liquidation\origin_data\btcusdt_5min_1620748800_to_1647014400.csv")
# print(df)
# # 写入pg库
# df.to_sql(con=conn, name='cryptocurrency', if_exists='replace', index=False)
# #查询指令
# query = "SELECT * FROM Cryptocurrency"
# df = pd.read_sql(sql=query, con=conn)
# print(df)
#
# 关闭数据库连接
# conn.close()


if __name__ == '__main__':
    pass
