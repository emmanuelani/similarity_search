from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
# from logger import logger


DATABASE_URL = "mysql+pymysql://root:Emmyboy1705#@localhost:3306//bloomzon"

try:
    engine = create_engine(DATABASE_URL)

    print(engine)

    metadata = MetaData()
    product_table = Table(
        "products", metadata,
        autoload_with=engine
    )

    print(product_table.columns.keys())
except Exception as e:
    print(f"Error {e}")