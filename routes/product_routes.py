from flask import Blueprint, jsonify, request

from middleware import admin_required, cognito_required
from models import Product, db
from s3_utils import upload_file_to_s3, delete_file_from_s3

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
def get_products():
    try:
        # Query only products that are not flagged as deleted
        products = Product.query.filter_by(deleted=False).all()
        return jsonify([
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock": product.stock,
                "image_url": product.image_url
            }
            for product in products
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        # Query the product by ID
        product = Product.query.get(product_id)

        # If product not found, return 404
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Build the response
        response = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "image_url": product.image_url,
            "deleted": product.deleted,
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/", methods=["POST"])
@cognito_required
@admin_required
def create_product():
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files["file"]

    try:
        # Upload the file to S3 and get the URL
        image_url = upload_file_to_s3(file)

        # Create a new product
        data = request.form
        product = Product(
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            stock=int(data["stock"]),
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()

        # Build detailed response
        response = {
            "message": "Product created successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock": product.stock,
                "image_url": product.image_url,
            }
        }
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_bp.route("/<int:product_id>", methods=["PUT"])
@cognito_required
@admin_required
def edit_product(product_id):
    try:
        # Start a database transaction
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Parse request data
        data = request.form
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        # Update fields if provided
        if "name" in data:
            product.name = data["name"]
        if "description" in data:
            product.description = data["description"]
        if "price" in data:
            product.price = data["price"]
        if "stock" in data:
            product.stock = data["stock"]

        # Handle file upload for product image
        new_image_url = None
        if "file" in request.files:
            file = request.files["file"]
            if file:
                # Step 1: Upload the new image
                new_image_url = upload_file_to_s3(file)

                # Step 2: Delete the old image if the new one was uploaded successfully
                if product.image_url:
                    old_file_key = product.image_url.split("/")[-1]
                    delete_file_from_s3(old_file_key)

                # Update product image URL
                product.image_url = new_image_url

        # Commit database changes only after successful operations
        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock": product.stock,
                "image_url": product.image_url
            }
        }), 200

    except Exception as e:
        # Roll back database changes if an error occurs
        db.session.rollback()

        # If the new image was uploaded but the operation failed, clean it up
        if new_image_url:
            new_file_key = new_image_url.split("/")[-1]
            try:
                delete_file_from_s3(new_file_key)
            except Exception as cleanup_error:
                # Log the cleanup error if needed
                print(f"Failed to clean up new image: {cleanup_error}")

        return jsonify({"error": str(e)}), 500


@product_bp.route("/<int:product_id>", methods=["DELETE"])
@cognito_required
@admin_required
def delete_product(product_id):
    try:
        # Fetch the product to delete
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Mark the product as deleted
        product.deleted = True
        db.session.commit()

        return jsonify({"message": "Product flagged as deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
