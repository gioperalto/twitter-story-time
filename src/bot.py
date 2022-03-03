import datetime, sys, random, os, openai, json
from requests_oauthlib import OAuth1Session
from config import *

def get_story():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    topics = open('seeds/topics.txt', 'r').read().splitlines()
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

def create_oath_session():
    twitter_api_key = os.environ.get("TWITTER_API_KEY")
    twitter_api_secret = os.environ.get("TWITTER_API_SECRET")
    oauth_token = os.environ.get("OAUTH_TOKEN")
    oauth_token_secret = os.environ.get("OAUTH_TOKEN_SECRET")

    oauth = OAuth1Session(
        twitter_api_key,
        client_secret=twitter_api_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
    )

    return oauth

def tweet_story(oauth, story):
    payload = { "text": story }

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    story = get_story()
    oauth = create_oath_session()
    tweet_story(oauth, story)