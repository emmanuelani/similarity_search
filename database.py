import asyncio
import json

# from embeddings import embeddings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData, Table, select, text, update
from sqlalchemy.orm import sessionmaker



# from logger import logger
DATABASE_URL = "mysql+aiomysql://root:Emmyboy1705#@localhost:3307/bloomzon"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)

# function to generate session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# function to fetch products
async def fetch_products():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT COUNT(*) FROM products"))
        products = result.scalars().all()
        print(products)
        return products
        

async def add_embeddings():
    async with AsyncSessionLocal() as db:
        try:
            await db.execute(text('ALTER TABLE products ADD COLUMN embeddings BLOB'))
            await db.commit()
        except Exception as e:
            print(f"{e}: Column already exists")


async def insert_embeddings():
    async with AsyncSessionLocal() as db:
        try:
            for embedding in embeddings:
                # Example: Insert the embedding as a JSON-encoded string
                embedding_json = json.dumps(embedding)

                # Update the products table to set the embeddings for all rows
                stmt = update(text("products")).values(embeddings=embedding_json)
                
                # Execute the update statement (this will update all rows)
                await db.execute(stmt)
                await db.commit()

            print(f"Updated embeddings for all products.")

        except Exception as e:
            print(f"Error updating embeddings: {e}")

async def extract_images():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT images from products"))
        images = result.scalars().all()
        first_images = [image.split(",")[0] for image in images if image]
        return first_images

async def main():
    await fetch_products()
    await add_embeddings()
    await insert_embeddings()
    await extract_images()

    # print(len(first_images))

if __name__ == "__main__":
    # If we're in an environment with a running event loop (e.g., a Jupyter notebook), we use run_until_complete
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        # If there is no existing event loop, use asyncio.run()
        asyncio.run(main())

    
