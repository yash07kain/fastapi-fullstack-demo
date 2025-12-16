from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.product import Product
from sqlalchemy.orm import Session
from data.database import engine, SessionLocal
import data.database_models

# Creating the needed tables based on database_models
data.database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory list
products = [
    Product(id=1, name='Pen', description='Stylish Pen', price=35, quantity=25),
    Product(id=2, name='Notebook', description='200-page ruled notebook', price=120, quantity=40),
    Product(id=3, name='Marker', description='Permanent black marker', price=50, quantity=30),
    Product(id=4, name='Pencil', description='HB graphite pencil', price=10, quantity=100),
    Product(id=5, name='Highlighter', description='Fluorescent yellow highlighter', price=45, quantity=35)
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()

    product_count = db.query(data.database_models.Product).count()

    if product_count == 0:
        for product in products:
            # Converting Pydantic object to a dict using .model_dump(),& ** used for unpacking
            db.add(data.database_models.Product(**product.model_dump()))
        db.commit()
        print("Database initialized with products.")

    db.close()


init_db()


# GET- Fetch all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(data.database_models.Product).all()
    return db_products


# GET- Fetch a product by id
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(data.database_models.Product).filter(
        data.database_models.Product.id == id
    ).first()

    if db_product:
        return db_product
    
    return {"error": "Product not found"}


# POST- Add a new product
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(data.database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product created successfully", "product": product}


# PUT- Update an existing product
@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(data.database_models.Product).filter(
        data.database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}


# DELETE - Delete a product
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(data.database_models.Product).filter(
        data.database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
