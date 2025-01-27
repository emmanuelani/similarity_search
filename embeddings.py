import torch
from torchvision.models import resnet50, ResNet50_Weights, resnet152, ResNet152_Weights
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from logger import set_logger

import sys

logger = set_logger(__name__)

# load pre-trained ResNet
logger.info("Loading model ....")
model = resnet152(weights=ResNet152_Weights.DEFAULT)

# save model
logger.info("Saving model ...")
torch.save(model.state_dict(), "resnet_152.pth")
