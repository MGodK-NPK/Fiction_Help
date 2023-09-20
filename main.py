import streamlit as st
import os
import openai
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

OPEN_API_KEY = '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'

os.environ['OPENAI_API_KEY'] = OPEN_API_KEY
openai.api_key = OPEN_API_KEY

def generate_everything(style,num,text):
    chat = ChatOpenAI(temperature=0.7)

    template_string = """Help write a movie or novel treatment in
    English for writers from the delimited idea by triple backticks. \
    Note that there might not be any idea. In that case, generate according to the remaining information you get. \
    And the user is Thai so their input could be in Thai. \
    The genre of the story is {style}. 
    Here are the genre descriptions for the novels in library:
    Action: Novels in this category are filled with excitement, fast-paced sequences, and intense physical or combat situations. Expect adrenaline-pumping adventures and heroic protagonists,
    Comedy: Expect laughter and humor in these novels. They are designed to amuse and entertain, often with witty dialogues and humorous situations,
    Drama: These novels delve into deep and emotional storytelling, focusing on the complexities of human relationships, personal struggles, and life's challenges,
    Horror: Horror novels aim to send shivers down your spine. They are filled with suspense, fear, and often supernatural elements that will keep you on the edge of your seat,
    Science Fiction: Science fiction novels transport readers to future worlds, alternate realities, or speculative futures. They often explore technology, space, and scientific concepts,
    Fantasy: Fantasy novels transport readers to magical realms with mythical creatures, epic quests, and extraordinary powers,
    Romance: Romance novels focus on love, relationships, and emotional connections. They often follow the journey of characters as they fall in love,
    Mystery: Mystery novels revolve around solving puzzles, uncovering secrets, and solving crimes. Expect suspense and intrigue as characters investigate,
    Thriller: Thriller novels are known for their suspenseful and gripping plots. They often involve danger, intrigue, and high-stakes situations,
    Animation: Animated novels bring stories to life through illustrated or animated visuals
    Adventure: Adventure novels are characterized by their thrilling and often perilous journeys and escapades. They typically feature protagonists who embark on exciting quests, exploration, or challenges, often in exotic or dangerous settings. These stories are known for their high levels of excitement, action, and a sense of discovery. Adventure novels can span a wide range of sub-genres, from swashbuckling pirate tales to expeditions into uncharted territories,
    Crime: Crime novels, also known as detective or mystery novels, revolve around the investigation and resolution of criminal activities. These stories feature detectives, investigators, or amateur sleuths who work to solve crimes such as murders, thefts, or other illicit activities. Crime novels often delve into the psychological aspects of both the criminals and the investigators, creating a sense of suspense and intrigue,
    Family: Family novels focus on the dynamics and relationships within a family unit. They explore themes related to family life, love, conflicts, and the challenges faced by various family members. These novels often provide insights into the complexities of human connections and the evolution of family bonds over time. Family novels can encompass a wide range of emotions and experiences, from heartwarming tales of love and reconciliation to stories of dysfunction and discord,
    Musical: Musical novels bring the world of music and performance to life through storytelling. These novels often center around musicians, composers, or individuals with a deep passion for music. They may explore the creative process, the struggles and triumphs of artists, and the emotional power of music to connect people. Musical novels can resonate with readers who appreciate both literature and the artistry of music,
    War: War novels depict the experiences of individuals and communities during times of armed conflict. They often explore the profound impact of war on both soldiers and civilians, delving into themes of bravery, sacrifice, trauma, and the moral complexities of warfare. These novels can be set in various historical periods and settings, shedding light on the human condition in times of crisis,
    Western: Western novels are typically set in the American Old West during the 19th century. They feature elements such as cowboys, outlaws, gunfights, and rugged landscapes. These stories often explore themes of rugged individualism, justice, and the clash between civilization and the wilderness. Western novels offer readers a glimpse into a bygone era characterized by adventure, frontier life, and a code of honor
    \
    Format the output as JSON with the following keys (all written in lowercase):
    title
    genre
    chapters
    summary
    characters
    treatment
    \

    The following is an explanation of each key: \
    first is an expected data type and followed by the description. \
    title: <string--Title of the Movie/Fiction> \
    genre: <string--Genre> \
    chapters: <integer: Number of total Chapters is {num} chapters.> \
    summary: <string: A brief summary of the whole plot.> \
    characters: <The value is a list of dictionary. One dictionary contains details about one character. 
    The key of each dictionary should consistently be in lowercase as followed: 
    name (Firstname and Lastname, you have to create a character name that relate with genre), age, occupation, pro_ant(If the character is in good side (protagonist), the value of pro_ant should be True(boolean),If the character is in bad side (Antagonist), the value of pro_ant should be False(boolean)), and description. 
    Note that all of their value should be a string, except for pro_ant. 
    Generate at least 5-8 main characters in total of both protagonists or antagonists (at least 1 protagonist is a must)
    Protagonist:
    The protagonist is the central character of a novel and typically serves as the main focus of the story. They are the character with whom the reader is meant to empathize and root for. Protagonists often face challenges, conflicts, and obstacles that they must overcome as the narrative unfolds. They are typically characterized by their development, growth, or transformation throughout the story. Protagonists can have various traits and backgrounds, but they are usually the character whose goals and actions drive the plot forward.
    Antagonist:
    The antagonist is the character or force that opposes the protagonist's goals or desires. They are the primary source of conflict in the story and act as an obstacle or adversary to the protagonist's journey. Antagonists can take many forms, including human characters, supernatural entities, societal norms, or even internal struggles within the protagonist themselves. While they are often portrayed as "villains," antagonists can be complex characters with their own motivations and justifications for their actions. Their role is to create tension and conflict in the narrative, pushing the protagonist to grow and change.)> 
    \
    treatment: <The total number of chapters are {num}. Thus, generate the same number of chapters \
    by giving output in a list of dictionary. \
    Each dictionary is one chapter. \
    Each dictionary always contains the following lowercase keys: \
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

def generate_sequal(prequal,num):
    chat = ChatOpenAI(temperature=0.7)

    #templates
    string_template_summary = """
    Summarize the following text delimited by triple backticks. \
    The summary should be at least 100 words and no longer than 300 words. \
    ```
    {text}
    ```
    """

    string_template_sequal = """
    Generate the treatment of the sequel from the triple-back-ticked summary of the prequel.
    The total episode is {num}.
    The characters from the previous story are {characters}.
    Format the output as JSON with the following keys (all written in lowercase):
        title
        chapters
        summary
        treatment

    title: <Title of the Movie/Fiction> 
    chapters: <Number of total Chapters is {num} chapters.> 
    summary: <A brief summary of the whole sequel plot.>
    treatment: <The total number of chapters are {num}. Thus, generate the same number of chapters 
    by giving output in a list of dictionary containing the following keys: 
    chapter (the number of the chapter) 
    title (the title of the chapter) 
    description (a brief description of what happens in the chapter, this should be at least 100 words.) 
    ```
    {text}
    ```
    """

    response = prequal

    #Key of dict -> str
    treatment_str = ""
    for chap in response["treatment"]:
        treatment_str += "Chapter {}: {}\n".format(str(chap["chapter"]), chap["description"])
    char_str = ""
    for char in response["characters"]:
        char_str += """Character Name: {}
        Age: {}
        Occupation: {}
        Protagonist/Antagonist: {}
        Description: {}\n\n""".format(char["name"],char["age"],char["occupation"],str(char["pro_ant"]),char["description"])

    #promt template
    prompt_template_summary = ChatPromptTemplate.from_template(string_template_summary)
    promt_template_sequal = ChatPromptTemplate.from_template(string_template_sequal)

    #format messages
    summary_message = prompt_template_summary.format_messages(
        text=treatment_str)

    sequal_message = promt_template_sequal.format_messages(
        num=num,
        characters=char_str,
        text=treatment_str)
    
    #create chains
    summary_chain = LLMChain(llm=chat, prompt=prompt_template_summary, output_key='summary')
    sequal_chain = LLMChain(llm=chat, prompt=promt_template_sequal,output_key='sequal')

    chains = SequentialChain(
        chains=[summary_chain,sequal_chain],
        input_variables=['text','num','characters'],
        output_variables=['summary','sequal'])
    
    #generate sequal&other info.
    response_sequal = chains({"text":treatment_str,"num":num,"characters":char_str})

    sequal = response_sequal['sequal']
    sequal_dict = json.loads(sequal)

    return sequal_dict


    



st.title(':rainbow[Fiction Generator] :closed_book:')
style_list = st.sidebar.multiselect('What genre(s) you would like the fiction to be?',
                            [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Science Fiction",
    "Fantasy",
    "Romance",
    "Mystery",
    "Thriller",
    "Animation",
    "Adventure",
    "Crime",
    "Family",
    "Musical",
    "War",
    "Western"])

num_int = st.sidebar.slider('How many chapter(s) would you like?',
                            1,15,7)
text = st.sidebar.text_area('What is your idea of the fiction?')

secret = st.sidebar.checkbox('Activate SECRET?')



style = ""
for item in style_list:
    style += item + ', '

num = str(num_int)

button = st.sidebar.button("Let's go!")

if button:
    response = generate_everything(style,num,text)
    st.header(":blue[Title:]")
    st.subheader(response["title"], divider=True)
    st.subheader("Genre: ")
    st.write(response['genre'])
    st.subheader("Number of Chapter(s):")
    st.subheader(str(response['chapters']))
    st.divider()
    st.header('Summary:')
    st.write(response['summary'])
    st.divider()

    st.header('Characters:',divider=True)

    for char in response['characters']:
        st.subheader("_Name:_ "+ char["name"])
        st.write("**Age:** " + str(char["age"]))
        st.write("**Occupation:** " + char["occupation"])
        if char["pro_ant"] == True:
            st.write("**Protagonist/Antagonist:** :innocent:")
        else:
            st.write("**Protagonist/Antagonist:** :smiling_imp:")
        st.write("**Description:** "+ char["description"])
    st.divider()
    
    st.header('Treatment',divider=True)

    for chap in response["treatment"]:
        chapter_no = str(chap['chapter'])
        expander = st.expander("**Chapter No.** "+ chapter_no + " : " + chap["title"])
        expander.write("**Description:**")
        expander.write(chap["description"])
    
    st.divider()
    
    #for sequal (feat. LLMChain & SequencialChains)
    if secret:
        st.title('SEASON 2!')
        response_seq = generate_sequal(response,num)
        st.header(":blue[Title:]")
        st.subheader(response_seq["title"], divider=True)
        st.subheader("Number of Chapter(s):")
        st.subheader(str(response_seq['chapters']))
        st.divider()
        st.header('Summary:')
        st.write(response_seq['summary'])
        st.divider()

        st.header('Treatment',divider=True)
        for chap in response_seq["treatment"]:
            chapter_no = str(chap['chapter'])
            expander = st.expander("**Chapter No.** "+ chapter_no + " : " + chap["title"])
            expander.write("**Description:**")
            expander.write(chap["description"])





    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write("""
        **Created by** \
        Makorn N. \
        Natchanon R. \
        Natanan L \
        """)
    
