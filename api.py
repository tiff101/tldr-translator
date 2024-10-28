import requests
import streamlit as st
import json
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)
message_log = []
bookshelf = []

class Book:
    def __init__(self, title: str, summary: str, **kwargs):
        self.title = title
        self.summary = summary
        self.cover = kwargs.get('cover', None)
        self.headline = kwargs.get('headline', 'This is a book')
        # todo? date_added
    

def call_grok(message, **kwargs):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a language expert who has spent the last thirty years researching literature, the arts, physical sciences and world history. You have amassed a wide range of knowledge across multiple domains, and are an excellent and empathetic communicator to any audience, whether it be a domain expert or layman. Your colleagues describe you as a polymath."
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model="llama3-8b-8192",
        temperature=kwargs.get("temp", 0.5)  # allow the 'user' to control creativity of the output on the call. Default to 0.5 if not specified
    )
    message_content = chat_completion.choices[0].message.content
    message_log.append(message_content)
    return message_content


def get_book_cover(book_title: str):
    url = "https://api.jigsawstack.com/v1/web/search"
    querystring = {"query": f"Find the book cover for {book_title}"}
    headers = {"content-type": "application/json",
               "x-api-key": st.secrets["JIGSAW_API_KEY"]}
    response = requests.request(
        "GET", url, params=querystring, headers=headers)

    # unpack response
    try:
        json_content = response.json()
        print(json_content['success'])
        imgs = json_content.get('image_urls')
        print(imgs)
        return imgs[2]  # TODO: THE IMG CHECK IS TAKING TOO LONG AND NOT WORKING LOL. FIX IT 

        # NOW FOR EACH OF THESE, UNTIL WE STOP, I KINDA WANT TO CHECK WHETHER THE COVER IS CORRECT?!?!? :D
        # we know the first one is trash... so that we actually have to keep going.
        # idx = 0
        # is_correct = False
        # while not is_correct and idx < len(imgs):
        #     print(idx)
        #     is_correct = check_correct_book_cover(imgs[idx], book_title)
        #     print('returned statement', is_correct)
        #     idx += 1
        # print("URL CHECKING DONE")

    except ValueError:
        print("Response content is not in JSON format")
    except Exception as e:
        print(e)


# Does the img URL match the book title?
def check_correct_book_cover(img_url, book_title):
    #####
    print("40", img_url)
    try:
        response = requests.request("POST",
                                "https://api.jigsawstack.com/v1/vocr",
                                data= {"url": f"{img_url}"},
                                headers={"content-type": "application/json", "x-api-key": st.secrets["JIGSAW_API_KEY"]}
                                )
        print('48', response)

        # unpack response.
        json_content = response.json()
        print('50', json_content)
        context = str(json_content['context'])
        print('CONTEXT', context)
        # is the book title in the response? Y/N
        # TODO: IT BREAKS HERE --- 50 {'message': 'Invalid JSON', 'success': False}
        response = requests.request("POST",
                                "https://api.jigsawstack.com/v1/ai/summary",
                                data= {"text": f"Can you determine if the book title {book_title} is in this {context}? Respond with True or False"},
                                headers= {"content-type": "application/json", "x-api-key": st.secrets["JIGSAW_API_KEY"]}
                                )
        if book_title in json_content['context']:
            return True
        else:
            return False
    
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return False
    
    except ValueError:
        print("Response content is not in JSON format")
        return False
    
    except Exception as e:
        print(e)
        return False
