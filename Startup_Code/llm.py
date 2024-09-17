import requests
from numpy import frombuffer
from numpy import uint8
import os

# Read api token from .env
API_TOKEN = os.getenv("CF_API")
DEBUG = os.getenv("DEBUG") == "True"

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
    if type(image) != list:
        image = image.tolist()
    
    prompt = "you are an assisstant designed to answer which object to pick and which object to drop. you should also specify the colour and shape of the object. example response: \npick red square | drop blue circle\nexample response:\npick green circle | drop yellow square\nexample response:\npick red circle | drop blue circle\nexample response:\nnow you need to analyse the image and tell which object to pick and which to drop. keep the response very short and following the pattern mentioned in the examples" 

    output = __callAzureOpenAI("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    
    if DEBUG:
        print(output)
        print(output["result"])

    return __output_processor_bb1(output)
