import os

class Config:
    # Cognito Configurations
    COGNITO_REGION_NAME = os.getenv("COGNITO_REGION_NAME", "")
    COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "")
    COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "")
    COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET", "")

    # SQLAlchemy Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", ""
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # S3 Configurations
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
    S3_REGION_NAME = os.getenv("S3_REGION_NAME", "")