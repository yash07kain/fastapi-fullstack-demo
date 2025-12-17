from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.product import Product
from controllers.product_controller import ProductController
from data.database import SessionLocal


router = APIRouter(prefix="/products", tags=["products"])


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_all_products(db: Session = Depends(get_db)):
    """GET endpoint to fetch all products"""
    return ProductController.get_all_products(db)


@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    """GET endpoint to fetch a product by ID"""
    return ProductController.get_product_by_id(id, db)


@router.post("")
def add_product(product: Product, db: Session = Depends(get_db)):
    """POST endpoint to add a new product"""
    return ProductController.add_product(product, db)


@router.put("/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    """PUT endpoint to update an existing product"""
    return ProductController.update_product(id, product, db)


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    """DELETE endpoint to delete a product"""
    return ProductController.delete_product(id, db)
