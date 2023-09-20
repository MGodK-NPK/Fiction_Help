import os
import openai
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

OPEN_API_KEY = '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'

os.environ['OPENAI_API_KEY'] = OPEN_API_KEY
openai.api_key = OPEN_API_KEY

def generate_everything(style,num,text):
    chat = ChatOpenAI(temperature=0.7)

    template_string = """Help write a movie or novel treatment in
    English for writers from the delimited by triple backticks. \
    Note that the user is Thai so their input would be in Thai. \
    The genre of the story is {style}. \
    Format the output as JSON with the following keys (all written in lowercase):
    title
    genre
    chapters
    summary
    characters
    treatment
    \

    title: <Title of the Movie/Fiction> \
    genre: <Genre> \
    chapters: <Number of total Chapters is {num} chapters.> \
    summary: <A brief summary of the whole plot.> \
    characters: <The value is a list of dictionary. One dictionary contains details about one character. \
    The key of each dictionary should consistently be in lowercase as followed: name (Firstname and Lastname), age, occupation, protagonist, and description. \
    Note that all of its value should be a string, except for protagonist. \
    If the character is in good side, the value should be true (boolean), else it should be false. \
    Generate at least 5-8 main characters in total of both protagonists or antagonists (at least 1 protagonist)> \
    treatment: <The total number of chapters are {num}. Thus, generate the same number of chapters 
    by giving output in a list of dictionary containing the following keys: \\
    chapter (the number of the chapter) \
    title (the title of the chapter) \
    description (a brief description of what happens in the chapter, this should be at least 100 words.) \

    ```{text}```
    """

    prompt_template = ChatPromptTemplate.from_template(template_string)

    movie_message = prompt_template.format_messages(
        style=style,
        text=text,
        num=num)
    
    response = chat(movie_message)

    dict = json.loads(response.content)
    return dict


ex_style = """Fantasy, Martial Art, Magical"""
ex_num = '3'
ex_text = '"ออกผจญจัยในโลกย้อนยุคที่เต็มไปด้วยเผ่าพันธุ์ต่าง ๆ เป็นเรื่องสั้นที่เน้นต่อสู้ มีพลังพิเศษที่สามารถต่อสู้กับเหล่าร้ายได้'

if __name__ == "__main__":
    dict = (generate_everything(ex_style,ex_num,ex_text))
    pregen = 'dict.json'
    with open(pregen, 'w') as json_file:
        json.dump(dict, json_file)