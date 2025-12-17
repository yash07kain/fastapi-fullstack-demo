from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.product import Product
from services.product_service import ProductService


class ProductController:
    """Controller layer for product business logic"""
    
    @staticmethod
    def get_all_products(db: Session) -> List[Product]:
        """Handle request to get all products"""
        return ProductService.get_all(db)
    
    @staticmethod
    def get_product_by_id(product_id: int, db: Session):
        """Handle request to get a product by ID"""
        db_product = ProductService.get_by_id(db, product_id)
        
        if not db_product:
            return {"error": "Product not found"}
        
        return db_product
    
    @staticmethod
    def add_product(product: Product, db: Session):
        """Handle request to add a new product"""
        db_product = ProductService.create(db, product)
        return {"message": "Product created successfully", "product": db_product}
    
    @staticmethod
    def update_product(product_id: int, product: Product, db: Session):
        """Handle request to update a product"""
        db_product = ProductService.update(db, product_id, product)
        
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product updated successfully", "product": db_product}
    
    @staticmethod
    def delete_product(product_id: int, db: Session):
        """Handle request to delete a product"""
        success = ProductService.delete(db, product_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product deleted successfully"}
