from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL

db = SQLAlchemy()


# Product model
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)  # UNSIGNED INT
    name = db.Column(db.String(255), nullable=False)  # Product name
    description = db.Column(db.Text)  # Product description
    price = db.Column(DECIMAL(10, 2), nullable=False)  # Product price
    stock = db.Column(db.Integer, nullable=False)  # Product stock quantity
    image_url = db.Column(db.String(255))  # URL to product image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp
    deleted = db.Column(db.Boolean, default=False)  # Soft delete flag

    def __repr__(self):
        return f"<Product {self.name}>"


# CustomerOrder model
class CustomerOrder(db.Model):
    __tablename__ = "customerorder"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)  # UNSIGNED INT
    user_sub = db.Column(db.String(255), nullable=False)  # User identifier
    total = db.Column(DECIMAL(10, 2), nullable=False)  # Total order price
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp

    # Relationship with OrderItem
    items = db.relationship("OrderItem", backref="customerorder", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CustomerOrder {self.id}, User {self.user_sub}>"


# OrderItem model
class OrderItem(db.Model):
    __tablename__ = "orderitem"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)  # UNSIGNED INT
    order_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("customerorder.id", ondelete="CASCADE"),
                         nullable=False)  # Foreign key to CustomerOrder
    product_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("product.id"),
                           nullable=False)  # Foreign key to Product
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the product in the order
    price = db.Column(DECIMAL(10, 2), nullable=False)  # Price of the product at the time of the order

    # Relationship with Product (optional, for back-references)
    product = db.relationship("Product", backref="orderitem", lazy=True)

    def __repr__(self):
        return f"<OrderItem Order {self.order_id}, Product {self.product_id}, Quantity {self.quantity}>"
