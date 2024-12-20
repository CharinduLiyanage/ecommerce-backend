# E-Commerce Backend
## Pre Requisites 
- Python 3.9  or greater.
- MySQL database.
- AWS Cognito
- Amazon S3.
- AWS IAM 

## Steps to follow
1. Run database/create_DB.sql file to create database.
2. Run database/design_DB.sql file to create tables.
3. Set up AWS Cognito
   1. Create a user pool
   2. Create a client app
   3. Create user group - 'admin'
4. Set up Amazon S3
5. Set up IAM user with S3 access.
6. Install requirements using requirements.txt.
7. Set up environmental variables in .env file.
8. Run app.py.

## .env file format.
| **Environment Variable**        | **Description**                                                    | **Data Type** | **Example**                                                             |
|----------------------------------|--------------------------------------------------------------------|---------------|-------------------------------------------------------------------------|
| **COGNITO_REGION_NAME**          | AWS region where the Cognito User Pool is hosted.                  | String        | `ap-southeast-1`                                                        |
| **COGNITO_USER_POOL_ID**         | Cognito User Pool ID for managing user authentication.             | String        | `ap-southeast-1_abcd`                                                   |
| **COGNITO_CLIENT_ID**            | Cognito App Client ID for the application to access the user pool. | String        | `abc123`                                                                |
| **COGNITO_CLIENT_SECRET**        | Cognito App Client secret for secure communication with the pool.  | String        | `abc123`                                                                |
| **SQLALCHEMY_DATABASE_URI**      | URI for connecting to the MySQL database using SQLAlchemy.         | String        | `mysql+pymysql://ecommerce_user:secure_password@localhost/ecommerce_db` |
| **SQLALCHEMY_TRACK_MODIFICATIONS** | Enables or disables SQLAlchemy event tracking (set to `False`).    | Boolean       | `False`                                                                 |
| **AWS_ACCESS_KEY_ID**            | AWS Access Key ID for accessing AWS S3 resources.                  | String        | `abc123`                                                                |
| **AWS_SECRET_ACCESS_KEY**        | AWS Secret Access Key for accessing AWS S3 resources securely.     | String        | `abc123`                                                                |
| **S3_BUCKET_NAME**               | Name of the S3 bucket used for storing application data.           | String        | `ecommerce-backend-abc`                                                 |
| **S3_REGION_NAME**               | AWS region where the S3 bucket is hosted.                          | String        | `ap-southeast-1`                                                        |

## Repo File Structure 
```
ecommerce-backend/
├── database                 # SQL script.
│   ├── create_DB.sql        # Run to create database.
│   └── design_DB.sql        # Run to create tables.
├── app.py                   # Main application entry point.
├── config.py                # Configuration settings.
├── models.py                # Database models.
├── middleware.py            # Middleware for authentication.
├── s3_utils.py              # AWS S3 bucket utilities.
├── routes/                  # API routes.
│   ├── __init__.py
│   ├── auth_routes.py       # Authentication-related routes.
│   ├── product_routes.py    # Product-related routes.
│   └── order_routes.py      # Order-related routes.
└── requirements.txt         # Python dependencies.
```
