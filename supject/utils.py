from supject.models import TestQuestion
from core.settings import MEDIA_ROOT

from django.core.files.base import ContentFile
import base64

import io

import requests
from django.utils import timezone
from PIL import Image
import mimetypes
import os


def calculate_test_ball(level, question_ball):
    total_ball = 0
    if level == TestQuestion.QuestionLevel.EASY:
        return total_ball + question_ball
    elif level == TestQuestion.QuestionLevel.MEDIUM:
        return total_ball + question_ball + 1
    else:
        return total_ball + question_ball + 2





from django.core.files.base import ContentFile
import base64

def download_image(img_url, message_id):
    try:
        file_format, file_str = img_url.split(';base64,') 
        ext = file_format.split('/')[-1]  
        decoded_file = ContentFile(base64.b64decode(file_str), name=f"upload_{message_id}.{ext}")
        
        return decoded_file
    except Exception as e:
        print("Error decoding file:", e)
        return None  

