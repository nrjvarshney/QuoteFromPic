from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
from PIL import Image
from io import BytesIO
from nltk.tokenize import word_tokenize
import os
import sys
from PIL import Image, ImageDraw
import numpy as np
import math
import PIL.ImageFont as ImageFont
import base64
from PIL import Image, ImageDraw
import numpy as np
import math
import PIL.ImageFont as ImageFont
import textwrap
import random

@api_view(['GET', 'POST'])
def my_view(request):
    if request.method == 'POST':
        #return Response({"data": request.data})	
#         results = GetAllQuotes(image_path)
        return Response({"caption": GetAllQuotes(request.data)})
#        return Response({"message": "Hello, world!"})


MAX_FROM_ONE_TOPIC = 3
DEBUG = 1
MAX_QUOTE_LEN = 70
DEFAULT_QUOTES = ["\nInfuse your life with action. Don't wait for it to happen. Make it happen. Make your own future. Make your own hope. Make your own love. And whatever your beliefs, honor your creator, not by passively waiting for grace to come down from upon high, but by doing what you can to make grace happen... yourself, right now, right down here on Earth.\n\nBradley Whitford\n\n", '\nLife is 10% what happens to you and 90% how you react to it.\n\nCharles R. Swindoll\n\n', '\nBeginning today, treat everyone you meet as if they were going to be dead by midnight. Extend to them all the care, kindness and understanding you can muster, and do it with no thought of any reward. Your life will never be the same again.\n\nOg Mandino\n\n', "\nLearn to enjoy every minute of your life. Be happy now. Don't wait for something outside of yourself to make you happy in the future. Think how really precious is the time you have to spend, whether it's at work or with your family. Every minute should be enjoyed and savored.\n\nEarl Nightingale\n\n", '\nNo matter what has happened to you in the past or what is going on in your life right now, it has no power to keep you from having an amazingly good future if you will walk by faith in God. God loves you! He wants you to live with victory over sin so you can possess His promises for your life today!\n\nJoyce Meyer\n\n', '\nOnly I can change my life. No one can do it for me.\n\nCarol Burnett\n\n', '\nSecurity is mostly a superstition. It does not exist in nature, nor do the children of men as a whole experience it. Avoiding danger is no safer in the long run than outright exposure. Life is either a daring adventure, or nothing.\n\nHelen Keller\n\n', "\nChoosing to be positive and having a grateful attitude is going to determine how you're going to live your life.\n\nJoel Osteen\n\n", '\nToday I choose life. Every morning when I wake up I can choose joy, happiness, negativity, pain... To feel the freedom that comes from being able to continue to make mistakes and choices - today I choose to feel life, not to deny my humanity but embrace it.\n\nKevyn Aucoin\n\n', '\nI have seen many storms in my life. Most storms have caught me by surprise, so I had to learn very quickly to look further and understand that I am not capable of controlling the weather, to exercise the art of patience and to respect the fury of nature.\n\nPaulo Coelho\n\n', "\nYour work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. As with all matters of the heart, you'll know when you find it.\n\nSteve Jobs\n\n", '\nPeace is the beauty of life. It is sunshine. It is the smile of a child, the love of a mother, the joy of a father, the togetherness of a family. It is the advancement of man, the victory of a just cause, the triumph of truth.\n\nMenachem Begin\n\n', "\nChange your life today. Don't gamble on the future, act now, without delay.\n\nSimone de Beauvoir\n\n", "\nI cannot even imagine where I would be today were it not for that handful of friends who have given me a heart full of joy. Let's face it, friends make life a lot more fun.\n\nCharles R. Swindoll\n\n", "\nI believe that a trusting attitude and a patient attitude go hand in hand. You see, when you let go and learn to trust God, it releases joy in your life. And when you trust God, you're able to be more patient. Patience is not just about waiting for something... it's about how you wait, or your attitude while waiting.\n\nJoyce Meyer\n\n", '\nMy mission in life is not merely to survive, but to thrive; and to do so with some passion, some compassion, some humor, and some style.\n\nMaya Angelou\n\n', '\nLife is a blur when one is essaying different roles; it is so fulfilling.\n\nAmitabh Bachchan\n\n', '\nFinancial independence is paramount. My mom always says that when a woman is financially independent, she has the ability to live life on her own terms. I think that was the soundest advice that I ever got. No matter where you go in life or who you get married to, you have to be financially independent - whether you use it or not.\n\nPriyanka Chopra\n\n', "\nI do have a close circle of friends and I am very fortunate to have them as friends. I feel very close to them I think friends are everything in life after your family. You come across lots of people all the time but you only make very few friends and you have to be true to them otherwise what's the point in life?\n\nShah Rukh Khan\n\n", '\nStay true to yourself, yet always be open to learn. Work hard, and never give up on your dreams, even when nobody else believes they can come true but you. These are not cliches but real tools you need no matter what you do in life to stay focused on your path.\n\nPhillip Sweet\n\n', '\nNever stop fighting until you arrive at your destined place - that is, the unique you. Have an aim in life, continuously acquire knowledge, work hard, and have perseverance to realise the great life.\n\nA. P. J. Abdul Kalam\n\n', '\nLife consists not in holding good cards but in playing those you hold well.\n\nJosh Billings\n\n', '\nClouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky.\n\nRabindranath Tagore\n\n', "\nYou can never control who you fall in love with, even when you're in the most sad, confused time of your life. You don't fall in love with people because they're fun. It just happens.\n\nKirsten Dunst\n\n", '\nTo succeed in life, you need three things: a wishbone, a backbone and a funny bone.\n\nReba McEntire\n\n', '\nLife is short, and if we enjoy every moment of every day, then we will be happy no matter what happens or what changes along the way.\n\nGretchen Bleiler\n\n']



def GetCaption(image_path):
    subscription_key = "562b4aae17574c63b7c2896b0e9836a4"
    assert subscription_key

    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"

    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()
#     print (analysis)
    image_caption = analysis["description"]["tags"]

    image = Image.open(BytesIO(image_data))
#     plt.imshow(image)
#     plt.axis("off")
#     _ = plt.title(image_caption, size="x-large", y=-0.1)
    return image_caption


def GetQuotesByKeyword(keyword, website):
    url = ""
    if(website == "wiseoldsayings"):
        url = "https://www.wiseoldsayings.com/"+ keyword +"-quotes/"
        headers = {
        'cache-control': "no-cache",
        'postman-token': "989ae6b6-79f9-d123-a496-e1b1ad157e10"
        }

        response = requests.request("GET", url, headers=headers)


        quotes = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        mydivs = soup.findAll("div", {"class": "quote"})

        for div in mydivs:
            unwanted = div.find("p", {"class": "quote_mark"})
            unwanted.extract()
            unwanted = div.find("p", {"class": "author"})
            unwanted.extract()
            ps = div.findAll('p')
            for p in ps:
                if(len(p.string.strip()) < MAX_QUOTE_LEN):
                    quotes.append(p.string.strip())
        len_quotes = len(quotes)
#         if(len_quotes > 0):
#             print("Found for "+ keyword + " on website: " + website+ " count: "+ str(len_quotes))
            
        random.shuffle(quotes)
        return quotes
    
    elif(website == "brainyquote"):
        url = "https://www.brainyquote.com/topics/" + keyword
        
        payload = ""
        headers = {
            'cache-control': "no-cache",
            'Postman-Token': "5b19b971-0950-44d1-bac6-50a068def9d3"
            }

        response = requests.request("GET", url, data=payload, headers=headers)

        if(response.status_code == 404):        
            result =  []
        else:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            result = [n.text for n in soup.find_all("div","clearfix")]
            for quote in result:
                quote = quote.split("\n")[1]
                if(len(quote) < MAX_QUOTE_LEN):
                    answer.append(str(quote))
        return answer
    
def GetAllQuotes(image):
    image_path = "temp_data.jpg"
    imgdata = base64.b64decode(image)
    with open(image_path, 'wb') as f:
        f.write(imgdata)
    
    tags = GetCaption(image_path)
    result = []
    quotes = {}
    for tag in tags:
        quotes[tag] = GetQuotesByKeyword(tag, "wiseoldsayings")
#         if (len(quotes) == 0):
#             quotes = GetQuotesByKeyword(tag, "brainyquote")
        
    for k in sorted(quotes, key=lambda k: len(quotes[k]), reverse=True):
        len_quote = len(quotes[k])
        if(len_quote == 0):
            break
        if(len_quote > MAX_FROM_ONE_TOPIC):
            result = result + (quotes[k][:MAX_FROM_ONE_TOPIC])
        else:
            result + result + quotes[k]
        
        if(len(result) > 10):
            break
    if(len(result) == 0):
        return DEFAULT_QUOTES
    random.shuffle(result)
    return result

