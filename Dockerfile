# Start with the official AWS Lambda Python runtime image
FROM public.ecr.aws/lambda/python:3.8

# Install necessary dependencies
RUN pip install torch==2.4.1 torchvision==0.19.1 --index-url https://download.pytorch.org/whl/cpu

# Copy the Lambda function code 
COPY lambda_function.py .

# Set the handler to function 
CMD ["lambda_function.lambda_handler"]
