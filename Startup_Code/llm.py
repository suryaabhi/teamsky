import random
import requests
import os
from Utils.ImageUtils import get_frame
import base64
from dotenv import load_dotenv
load_dotenv()
import cv2

# Read api token from .env
API_TOKEN = os.getenv("AZ_API")
DEBUG = os.getenv("DEBUG")

API_BASE_URL = "https://roborumble-teamsky-2024.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"
headers = {"api-key": API_TOKEN}

def fallback_answer(bb_no):
    print(f"output error in bb{bb_no} returning fallback answer")
    if bb_no == 1:
        return {"found": False, "pick": {"color": "red", "shape": "square"}, "drop": {"color": "blue", "shape": "circle"}}
    elif bb_no == 2:
        return {"found": False, "path": "left"}
    elif bb_no == 3:
        return {"found": False, "characters": ["2", "T"]}

def __encode_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    success, encoded_image = cv2.imencode('.png', image)
    content2 = encoded_image.tobytes()
    return base64.b64encode(content2).decode('utf-8')

def __callAzureOpenAI(payload):
    response = requests.post(API_BASE_URL, headers=headers, json=payload)
    return response.json()

def __output_processor_bb1(res):
    answer = {}
    if len(res.split()) == 7:
            pickstmt = res.split("|")[0].strip()
            dropstmt = res.split("|")[1].strip()
            answer["found"] = True
            answer["pick"] = {
                "color": pickstmt.split()[1],
                "shape": pickstmt.split()[2]
            }
            answer["drop"] = {
                "color": dropstmt.split()[1],
                "shape": dropstmt.split()[2]
            }
    else:
        return fallback_answer(1)
    return answer

def __output_processor_bb2(res):
    answer = {}
    answer["found"] = True
    if "left" in res:
        answer["path"] = "left"
    elif "right" in res:
        answer["path"] = "right"
    elif "straight" in res:
        answer["path"] = "straight"
    else:
        return fallback_answer(2)
    return answer

def __output_processor_bb3(res):
    answer = {}
    if len(res.split()) == 2 or len(res.split()) == 1:
        answer["found"] = True
        answer["characters"] = res.split()
    else:
        return fallback_answer(3)

    return answer

def send_to_llm_bb1(image):
    image = __encode_image(image)
    payload = {
        "messages": [
            {
                "role": "system",
                "content": """you are an assisstant designed to answer which object to pick and which object to drop. you should also specify the colour and shape of the object. There are 2 types of shapes (circle, square) and 3 types of colours (red, green, blue).
                example response: pick red square | drop blue square
                example response: pick green circle | drop red square
                example response: pick red circle | drop blue circle
                now you need to analyse the image and tell which object to pick and which to drop. keep the response very short and following the pattern mentioned in the examples"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    output = __callAzureOpenAI(payload)
    
    print(output)
    
    if output.get("error"):
        return fallback_answer(1)

    airesponse = output["choices"][0]["message"]["content"]

    return __output_processor_bb1(airesponse)

def send_to_llm_bb2(image):
    image = __encode_image(image)
    payload = {
        "messages": [
            {
                "role": "system",
                "content": """you are an assisstant designed to solve path puzzles. you are shown a puzzle which asks you to choose between 'left', 'right' and 'straight'. you need to analyse the image which contains 3 options to choose from. there is an image beside 'left', an image beside 'right' and an image beside 'straight'. analyse the question asked and which image corresponds closest to the answer. keep the response very short and following the pattern mentioned in the examples. 
                example response: "left"
                example response: "right"
                example response: "straight"
                Now you need to analyse the image and tell which path to choose. 
                keep the response very short and following the pattern mentioned in the examples"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    output = __callAzureOpenAI(payload)
    
    print(output)
    
    if output.get("error"):
        return fallback_answer(2)

    airesponse = output["choices"][0]["message"]["content"]

    return __output_processor_bb2(airesponse)

def send_to_llm_bb3(image):
    image = __encode_image(image)
    payload = {
        "messages": [
            {
                "role": "system",
                "content": """You are an assisstant that solves the question asked in the image.
                You can count the number of objects in the image.
                You can identify the objects in the image.
                Keep the response short and simple. Respond in 2 characters or letters or numbers.
                Example 1: let's say image contains 9 hearts and we are asked to Idenitify the number of objects in the image. Print the number and the first letter of the object.
                Example response will be: "9 H" because the first letter of heart is h
                
                Example 2: let's say image contains 2 cats and we are asked to Identify the number of objects in the image. Print the number and the last letter of the type of object.
                Example response will be: "2 T" because the last letter of cat is t"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Identify the number of animals in the image. Count the number of animals in the image. Print the number and the first letter of the type of animal."  
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    output = __callAzureOpenAI(payload)
    
    print(output)
    
    if output.get("error"):
        return fallback_answer(3)

    airesponse = output["choices"][0]["message"]["content"]

    return __output_processor_bb3(airesponse)

if __name__ == "__main__":
    image = open("~/Downloads/billboardsampless/1.png", "rb").read()
    print(send_to_llm_bb1(image))
    pass
