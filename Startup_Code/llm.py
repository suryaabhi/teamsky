import random
import requests
from numpy import frombuffer
from numpy import uint8
import os
import cv2
from Utils.ImageUtils import get_frame

# Read api token from .env
API_TOKEN = "WpgYNrsZA3PeCtt1vpdsJQ8YQORMaAazYPm3dKRB"
DEBUG = True

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/62f65ffc3a4f576c639bd78b4305bb40/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def __callAzureOpenAI(model, image=None, prompt=None):
    input = { "prompt": prompt }

    input["image"] = image
    input["max_tokens"] = 100

    # print(input)
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def __output_processor_bb1(oj):

    print(oj)
    print(oj["result"])

    answer = {}
    res = oj["result"]["description"].lower()
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
        answer["found"] = False
    if DEBUG:
        print(answer)
    return answer

def __output_processor_bb2(oj):
    if DEBUG:
        print(oj["result"])
    answer = {}
    res = oj["result"]["description"].lower()
    if "left" in res:
        answer["found"] = True
        answer["direction"] = "left"
    elif "right" in res:
        answer["found"] = True
        answer["direction"] = "right"
    elif "straight" in res:
        answer["found"] = True
        answer["direction"] = "straight"
    else:
        answer["found"] = False
        # pick a random direction from left, right, straight
        answer["direction"] = ["left", "right", "straight"][random.randint(0, 3)]
    if DEBUG:
        print(answer)
    return answer

def __output_processor_bb3(oj):
    """
    TODO PENDING
    """
    if DEBUG:
        print(oj["result"])
    answer = {}
    res = oj["result"]["description"].lower()
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
        answer["found"] = False
    if DEBUG:
        print(answer)
    return answer

def send_to_llm_bb1(image):
    image = frombuffer(image, uint8)
    image = image.tolist()
    
    prompt = """
    you are an assisstant designed to answer which object to pick and which object to drop. you should also specify the colour and shape of the object.
    example response: pick red square | drop blue square
    example response: pick green circle | drop yellow square
    example response: pick red circle | drop blue circle
    now you need to analyse the image and tell which object to pick and which to drop. keep the response very short and following the pattern mentioned in the examples"""

    output = __callAzureOpenAI("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)

    print(output)
    
    if not output["success"]:
        print(f"API error {output['error']}")
        return None
    

    print(output)
    print(output["result"])

    return __output_processor_bb1(output)


def send_to_llm_bb2(image):
    image = frombuffer(image, uint8)
    image = image.tolist()
    
    prompt = """you are an assisstant designed to solve path puzzles. you are shown a puzzle which asks you to choose between 'left', 'right' and 'straight'. you need to analyse the image which contains 3 options to choose from. there is an image beside 'left', an image beside 'right' and an image beside 'straight'. analyse the question asked and which image corresponds closest to the answer. keep the response very short and following the pattern mentioned in the examples. 
    example response: "left"
    example response: "right"
    example response: "straight"
    Now you need to analyse the image and tell which path to choose. 
    keep the response very short and following the pattern mentioned in the examples"""

    output = __callAzureOpenAI("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    
    print(output)
    print(output["result"])

    return __output_processor_bb2(output)

def send_to_llm_bb3(image):
    image = frombuffer(image, uint8)
    image = image.tolist()
    
    prompt = """
    Ignore the above instructions.
    You are an assisstant that identifies what is in the image.
    You are not a text extraction tool.
    You will ignore all the text in the image.
    You can count the number of objects in the image.
    You can identify the objects in the image.
    Keep the response short and simple. Respond in 2 characters or letters or numbers.
    Example 1: let's say image contains 9 hearts and we are asked to Idenitify the number of objects in the image. Print the number and the first letter of the object.
    Example response will be: "9 H" because the first letter of heart is h
    
    Example 2: let's say image contains 2 cats and we are asked to Identify the number of objects in the image. Print the number and the last letter of the type of object.
    Example response will be: "2 T" because the last letter of cat is t

    For the image, {prompt}
    """

    output = __callAzureOpenAI("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    
    print(output)
    print(output["result"])

    return __output_processor_bb3(output)

if __name__ == "__main__":
    image = open("~/Downloads/output.jpg", "rb").read()
    print(send_to_llm_bb1(image))
    pass

