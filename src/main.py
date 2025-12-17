from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.product import Product
from data.database import engine, SessionLocal
from data import database_models
from routes.product_routes import router as product_router
from services.product_service import ProductService

# Creating the needed tables based on database_models
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(product_router)


# Initial products data
INITIAL_PRODUCTS = [
    Product(id=1, name='Pen', description='Stylish Pen', price=35, quantity=25),
    Product(id=2, name='Notebook', description='200-page ruled notebook', price=120, quantity=40),
    Product(id=3, name='Marker', description='Permanent black marker', price=50, quantity=30),
    Product(id=4, name='Pencil', description='HB graphite pencil', price=10, quantity=100),
    Product(id=5, name='Highlighter', description='Fluorescent yellow highlighter', price=45, quantity=35)
]


def init_db():
    """Initialize database with default products"""
    db = SessionLocal()
    try:
        ProductService.init_products(db, INITIAL_PRODUCTS)
    finally:
        db.close()


# Initialize database on startup
init_db()
