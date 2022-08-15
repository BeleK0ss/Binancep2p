import sqlite3
import peewee

with sqlite3.connect("db/test.db") as conn:

    crs = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS Binance_BUY(order_id INTEGER, operation TEXT, nickname TEXT, price REAL,
     payments TEXT, link TEXT, dt TEXT, symbol TEXT, limits_min TEXT, limits_max TEXT, exchange TEXT, quantity REAL,
      Rate INTEGER, sum_order INTEGER, user_id TEXT) """
    query2 = """ INSERT INTO Binance_BUY (id, operation, price, payments, link, dt, symbol, limits, exchange) 
    VALUES (1, 'BUY', 41.96, 'monobank', 'https://google.com', '5151235', 'USDT', '1000-50000', 'Binance'); """
    crs.execute(query)
    conn.commit()


