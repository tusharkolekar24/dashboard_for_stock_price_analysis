from sqlalchemy.engine import URL
from sqlalchemy import create_engine
class DB:
    def __init__(self):
        # Method1: For Creating URL to connect with database
        self.__db_url = URL.create(
            "postgresql+psycopg2",
            username="postgres",
            password="Tushar@24041996",  # plain (unescaped) text
            host="localhost",
            database="StockMarket",
        )

    def initiate_db(self):
        self.__engine = create_engine(self.__db_url)

        return self.__engine