from datetime import datetime

from flask import Blueprint, request, jsonify

from middleware import cognito_required
from models import CustomerOrder, OrderItem, Product
from models import db

order_bp = Blueprint("orders", __name__)


@order_bp.route("/", methods=["POST"])
@cognito_required
def create_order():
    try:
        # Extract data from the request
        data = request.json
        user_sub = request.user
        items = data.get("items")  # List of items, each with product_id and quantity

        if not user_sub:
            return jsonify({"error": "User identifier (user_sub) is required"}), 400

        if not items or not isinstance(items, list):
            return jsonify({"error": "Order must include a list of items"}), 400

        # Initialize total price for the order
        total_price = 0
        order_items = []

        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            if not product_id or quantity <= 0:
                return jsonify({"error": f"Invalid item details: {item}"}), 400

            # Fetch the product from the database
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": f"Product with ID {product_id} not found"}), 404

            # Check if the product is marked as deleted
            if product.deleted:
                return jsonify({"error": f"Product '{product.name}' is no longer available"}), 400

            if product.stock < quantity:
                return jsonify({"error": f"Insufficient stock for product '{product.name}'"}), 400

            # Calculate the price for this item and reduce product stock
            item_price = product.price * quantity
            total_price += item_price
            product.stock -= quantity  # Reduce stock

            # Create an OrderItem object
            order_item = OrderItem(
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            order_items.append(order_item)

        # Create the CustomerOrder object
        customer_order = CustomerOrder(
            user_sub=user_sub,
            total=total_price,
            created_at=datetime.utcnow()
        )

        # Add order items to the order
        customer_order.items = order_items  # Assuming a relationship is defined in the model

        # Save the order and associated items to the database
        db.session.add(customer_order)
        db.session.commit()

        # Build the response
        response = {
            "message": "Order created successfully",
            "order": {
                "id": customer_order.id,
                "user_sub": customer_order.user_sub,
                "total": float(customer_order.total),
                "created_at": customer_order.created_at.isoformat(),
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_name": Product.query.get(item.product_id).name,
                        "quantity": item.quantity,
                        "price": float(item.price),
                        "subtotal": float(item.quantity * item.price),
                    }
                    for item in order_items
                ],
            },
        }
        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@order_bp.route("/", methods=["GET"])
@cognito_required
def get_orders():
    try:
        user_sub = request.user

        # Query all orders for the given user
        orders = CustomerOrder.query.filter_by(user_sub=user_sub).all()

        if not orders:
            return jsonify({"message": "No orders found for this user"}), 404

        # Build the response with order details
        response = {
            "user_sub": user_sub,
            "orders": [
                {
                    "order_id": order.id,
                    "total": float(order.total),
                    "created_at": order.created_at.isoformat(),
                    "items": [
                        {
                            "product_id": item.product_id,
                            "product_name": Product.query.get(item.product_id).name,
                            "quantity": item.quantity,
                            "price": float(item.price),
                            "subtotal": float(item.quantity * item.price),
                        }
                        for item in order.items
                    ],
                }
                for order in orders
            ],
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_bp.route("/<int:order_id>", methods=["GET"])
@cognito_required
def get_order(order_id):
    try:
        # Query the specific order by its ID
        order = CustomerOrder.query.get(order_id)

        if not order:
            return jsonify({"message": "Order not found"}), 404

        # Build the order response
        response = {
            "order_id": order.id,
            "user_sub": order.user_sub,
            "total": float(order.total),
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": Product.query.get(item.product_id).name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                    "subtotal": float(item.quantity * item.price),
                }
                for item in order.items
            ],
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
