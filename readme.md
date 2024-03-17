# Upload file to S3

# Start

```
conda activate BTN
```

# Install Dependencies

```
pip install -r requirements.txt
```

# .env

- Go to AWS3 https://s3.console.aws.amazon.com/s3/home?region=ap-southeast-2#

```
S3_BUCKET_NAME =
S3_ACCESS_KEY =
S3_SECRET_KEY =
```

# Run

```
uvicorn app:app --reload
```

# Test

## POST http://127.0.0.1:8000/uploadfile/

- Body form-data:
  key = file
  value = file
