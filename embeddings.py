import torch
import requests
import asyncio

from database import extract_images
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms
from torchvision import models
from warnings import filterwarnings
from requests import RequestException

filterwarnings("ignore")

# Load ResNet50 Pretrained Model
resnet50 = models.resnet50(pretrained=True)
resnet50 = torch.nn.Sequential(*list(resnet50.children())[:-1])  # Remove the last FC layer
resnet50.eval()  # Set to evaluation mode

# Define Image Transformations (Required for ResNet50)
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to ResNet50 input size
    transforms.ToTensor(),           # Convert to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
])

# Function to Get Image from URL and Extract Embedding
def get_image_embedding(image_url):
    # Fetch image from URL
    try:
        # Fetch image from URL with timeout
        response = requests.get(image_url, timeout=5)  
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Open image and convert to RGB
        image = Image.open(BytesIO(response.content)).convert("RGB")
        image = transform(image).unsqueeze(0)  # Add batch dimension
        
        # Extract features
        with torch.no_grad():
            embedding = resnet50(image).squeeze().numpy()  # Remove extra dimensions
        
        return embedding  # 2048-dimensional feature vector

    except RequestException as e:
        print(f"Error processing {image_url}: {e}")
        return None  # Return None for failed images

embeddings = []

first_images = asyncio.run(extract_images())

# embedding the images
for image in first_images:
    embedding = get_image_embedding(image)
    if embedding is None:
        embeddings.append("NULL")
        print("Appending NULL...")
        continue
    else:
        embeddings.append(embedding)
        print("Appending embedding...")
    
    print(len(embeddings))
    
# print(embeddings)