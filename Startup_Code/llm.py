import requests
from numpy import frombuffer
from numpy import uint8


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/62f65ffc3a4f576c639bd78b4305bb40/ai/run/"
headers = {"Authorization": "Bearer 20v0QEuLskvG0nSnl7_cyro_3EGS-Agw-fpfyy-s"}


def run(model, image=None, prompt=None):
    input = { "prompt": prompt}

    input["image"] = image
    input["max_tokens"] = 100

    # print(input)
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def output_processor_bb1(oj):
    print(oj["result"])
    answer = {}
    res = oj["result"]["description"]
    if len(res.split()) == 7:
            pickstmt = res.split("|")[0].strip()
            dropstmt = res.split("|")[1].strip()
            answer["pick"] = {
                "color": pickstmt.split()[1],
                "shape": pickstmt.split()[2]
            }
            answer["drop"] = {
                "color": dropstmt.split()[1],
                "shape": dropstmt.split()[2]
            }
    print(answer)
    return answer

def llm_bb_1():
    prompt = "you are an assisstant designed to answer which object to pick and which object to drop. you should also specify the colour and shape of the object. example response: \npick red square | drop blue circle\nexample response:\npick green circle | drop yellow square\nexample response:\npick red circle | drop blue circle\nexample response:\nnow you need to analyse the image and tell which object to pick and which to drop. keep the response very short and following the pattern mentioned in the examples" 
     # load image from local directory
    image = open("billboardss1.png", "rb")

    # image to uint8
    image = frombuffer(image.read(), uint8)

    # convert to list
    image = image.tolist()

    # print(image)
    output = run("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    print(output)
    print(output["result"])

    # return output_processor_bb1(output)

def llm_bb_2():
    prompt = "you are an assisstant designed to solve path puzzles. you are shown a puzzle which asks you to choose between 'left', 'right' and 'straight'. you need to analyse the image which contains 3 options to choose from. there is an image beside 'left', an image beside 'right' and an image beside 'straight'. analyse the question asked and which image corresponds closest to the answer. keep the response very short and following the pattern mentioned in the examples. example response: \nleft\nexample response:\nright\nexample response:\nstraight\nexample response:\nnow you need to analyse the image and tell which path to choose. keep the response very short and following the pattern mentioned in the examples" 

    # load image from local directory
    image = open("billboardss2.png", "rb")

    # image to uint8
    image = frombuffer(image.read(), uint8)

    # convert to list
    image = image.tolist()

    # print(image)
    output = run("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    print(output)
    print(output["result"])

# not working
def llm_bb_3():
    prompt = "you are an assisstant designed to solve puzzles. in the given image understand the question asked and provide the answer. keep the response very short and limited to a maximum of 3 characters. your job is to give an answer to the question asked in the image in 3 characters or less. your answer has to be 3 characters or less. " 

    # load image from local directory
    image = open("billboardss3.png", "rb")

    # image to uint8
    image = frombuffer(image.read(), uint8)

    # convert to list
    image = image.tolist()

    # print(image)
    output = run("@cf/llava-hf/llava-1.5-7b-hf", image, prompt)
    print(output)
    print(output["result"])


# llm_bb_1()
# llm_bb_2()
llm_bb_3()
