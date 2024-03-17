from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta
import dotenv
import os

dotenv.load_dotenv()
app = FastAPI()

# AWS S3 configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")


def upload_to_s3(file, object_name):
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY
        )

        # Upload the file
        s3.upload_fileobj(file.file, S3_BUCKET_NAME, object_name)

        # Generate the URL for the uploaded file with expiration (e.g., 1 hour)
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        file_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": object_name},
            ExpiresIn=60,  # Expiration time in seconds (adjust as needed)
        )

        return file_url
    except NoCredentialsError:
        return None


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Generate a unique object name/key for the S3 object
    object_name = f"uploads/{file.filename}"

    # Upload the file to S3 and get the file URL
    file_url = upload_to_s3(file, object_name)

    if file_url:
        return JSONResponse(
            content={"message": "File uploaded successfully", "file_url": file_url},
            status_code=200,
        )
    else:
        return JSONResponse(
            content={"message": "Failed to upload file. Check your AWS credentials."},
            status_code=500,
        )
