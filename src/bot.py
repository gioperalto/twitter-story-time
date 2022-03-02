import datetime, sys, requests, random, os, openai
from requests.structures import CaseInsensitiveDict
from config import *

def get_story():
    openai.api_key = sys.argv[1]

    topics = [
        'Breakfast', 'Lunch', 'Dinner', 'Gardening', 
        'Dating', 'Sake', 'Beach', 'Soccer', 
        'Sushi', 'School', 'Smoking', 'Forests',
        'Ramen', 'Japan', 'Ninjas', 'Fishing'
    ]
    choices = [ 
        { 'genre': 'Comedy', 'length': 'Two', 'max_tokens': 60 }, 
        { 'genre': 'Narrative', 'length': 'Four', 'max_tokens': 120 }
    ]

    topic = random.choice(topics)
    choice = random.choice(choices)
    choice_dir = 'prompts/{}/'.format(choice['genre'])
    files = [f for f in os.listdir(choice_dir) if os.path.isfile(os.path.join(choice_dir, f))]
    f = random.choice(files)
    text = open('{}{}'.format(choice_dir, f), 'r').read()

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=f"{text}\n    \nTopic: {topic}\n{choice['length']}-Sentence {choice['genre']} Story:",
        temperature=0.8,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
    )
    resp = response['choices'][0]['text']
    prefix = 'Story time: ' if choice['length'] == 'Four' else ''
    story = '{}{}'.format(prefix, resp.strip()) 

    print('Topic:', topic, 'Choice:', choice, '\n')
    print('Text:', text, '\n')
    print('Response:\n', story)

    return story

def tweet_story(story):
    twitter_api_key = sys.argv[2]

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {twitter_api_key}"

    print(twitter_api['tweets'])
    print(headers['Authorization'])
    # resp = requests.post(twitter_api['tweets'], headers=headers, data={ 'text': story })
    # print('Twitter API response:\n')
    # print(resp)

if __name__ == "__main__":
    # story = get_story()
    story = ''
    tweet_story(story)