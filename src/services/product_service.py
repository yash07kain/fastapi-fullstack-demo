from sqlalchemy.orm import Session
from typing import List, Optional
from data import database_models
from schemas.product import Product


class ProductService:
    """Service layer for product database operations"""
    
    @staticmethod
    def get_all(db: Session) -> List[database_models.Product]:
        """Retrieve all products from database"""
        return db.query(database_models.Product).all()
    
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[database_models.Product]:
        """Retrieve a product by ID"""
        return db.query(database_models.Product).filter(
            database_models.Product.id == product_id
        ).first()
    
    @staticmethod
    def create(db: Session, product: Product) -> database_models.Product:
        """Create a new product"""
        db_product = database_models.Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update(db: Session, product_id: int, product: Product) -> Optional[database_models.Product]:
        """Update an existing product"""
        db_product = db.query(database_models.Product).filter(
            database_models.Product.id == product_id
        ).first()
        
        if not db_product:
            return None
        
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        """Delete a product by ID"""
        db_product = db.query(database_models.Product).filter(
            database_models.Product.id == product_id
        ).first()
        
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True
    
    @staticmethod
    def init_products(db: Session, products: List[Product]) -> None:
        """Initialize database with default products"""
        product_count = db.query(database_models.Product).count()
        
        if product_count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
            print("Database initialized with products.")
