import os
import boto3
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw
import io
import base64

# Set model weights to download in /tmp
os.environ["TORCH_HOME"] = "/tmp"

weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.9)
model.eval()

# Initialize S3 client
s3_client = boto3.client('s3')

# Lambda function handler
def lambda_handler(event, context):
    try:
        # Directly decode the base64-encoded image from the body
        image_data = base64.b64decode(event["body"])

        # Decode image
        image = Image.open(io.BytesIO(image_data))
        
        # Preprocess the image
        transform = weights.transforms()
        image_tensor = transform(image).unsqueeze(0)
        
        # Perform object detection
        with torch.no_grad():
            prediction = model(image_tensor)[0]
        
        # Extract predictions
        boxes = prediction["boxes"].cpu().numpy()
        labels = prediction["labels"].cpu().numpy()
        
        # Draw bounding boxes on the image
        draw = ImageDraw.Draw(image)
        for box in boxes:
            draw.rectangle(box.tolist(), outline="red", width=3)
        
        # Save the processed image to /tmp
        processed_image_path = "/tmp/processed_image.jpg"
        image.save(processed_image_path)
        
        # Upload the processed image to an S3 bucket
        bucket_name = "object-detected-images"
        object_key = "processed_image.jpg"
        s3_client.upload_file(processed_image_path, bucket_name, object_key)
        
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        
        return {
            "statusCode": 200,
            "body": {
                "boxes": boxes.tolist(),
                "labels": labels.tolist(),
                "s3_url": s3_url
            }
        }
    
    except Exception as e:
        # Handle errors gracefully and return a 500 error with a message
        return {
            "statusCode": 500,
            "body": f"Error processing the image: {str(e)}"
        }
