from decouple import config

ML_URL = config("ML_URL")
MONGO_URI = config("MONGO_URI") 

# S3 configuration
AWS_ACCESS_KEY_ID = config("AWSAccessKeyId")
AWS_SECRET_ACCESS_KEY = config("AWSSecretKey")
AWS_REGION_NAME = config("AWS_REGION")
AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")