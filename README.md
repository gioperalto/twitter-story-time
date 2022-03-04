# Twitter Story Time

This service leverages Twitter automation in conjunction with OpenAI's GPT-3 to craft stories given a topic (e.g. Flowers), specific genre (e.g. Horror), and length (e.g. 2 sentences, 4 sentences).

I'm going to go over three different aspects of this service:
- tech (what exactly it does)
- setup (your prerequisites)
- use (manually running the service on-demand)
- automation (running the service on a schedule)

## Tech

So above we spoke about what this service does, but I also want to elaborate on the tech and libraries/services Twitter Story Time leverages.

Twitter Story Time is written primarily in Python. It uses OpenAI's GPT-3 API to create stories based on a set of topics. The user of this application can, through OpenAI, generate small stories. The current setup is stubbed out for two-sentence and four-sentence stories. The `prompts` and `seeds` folders are data points we use to craft the way our service will create these stories. The `Comedy` and `Narrative` subfolders are my own writings, so in a way these small stories are created in my style. I would recommend changing out the text and tailoring these sentences to your own writing style.

Aside from OpenAI, this service also uses Twitter's API to send tweets out.

## Setup

You will need to get developer access to GPT-3's API and Twitter's API:
- https://beta.openai.com/docs/api-reference
- https://developer.twitter.com/en/docs/twitter-api

After you have your API keys (saved),  you will need Python (3.8) and/or Docker to run this service.

Finally, you will need to an OAuth token and a token secret. This is how you can do that:
- Run (from the root of the repo) `python src/request_access.py` in your terminal
- You will be provided a website link to authorize the application, copy and paste it into your web browser
- Once you click "Authorize App", you will be provided a 6-digit code
- Enter that 6-digit code into the terminal and hit enter
- Your OAuth token and token secret will be displayed on the terminal screen

Your OAuth token and token secret should last you about 60 days. After that, you may need to regenerate them.

## Use

For manual use, you will need to save the following API keys as environment variables on the machine you are running from:
- OPENAI_API_KEY
- TWITTER_API_KEY
- TWITTER_API_SECRET
- OAUTH_TOKEN
- OAUTH_TOKEN_SECRET

You can set an environment variable like so: `export 'OPENAI_API_KEY'='UUUVVVWWWXXXYYYZZZ'`

Once all of your environment variables are set, you should be ready to run the application. You can manually run Twitter Story Time by typing this in your terminal (from repo root): `python src/boy.py`

If your `bot.py` file runs successfully, you should see something like this in your terminal:
```
...
Response code: 201
{
    "data": {
        "id": "XXXXXXXXXXXXX",
        "text": "Story time: I love breakfast. I could eat it every day and never get bored. I usually have a big breakfast with eggs, bacon, toast, and coffee. But sometimes I like to mix it up and have a waffle or pancakes instead."
    }
}
```

## Automation

You may notice that there is a Dockerfile in the root of the repository. This service was designed to be run from a docker container. Here's how you can do it:

**Step one**: Install Docker (Engine)

**Step two**: Once docker is running, from the root of the repository run the following:

 `docker build -t twitter-story-time .`

The command above creates the docker image that you can now build from.

**Step three**: To run a docker container (which runs the service once), put this command from your terminal (change out the letters with actual keys when you run these commands):

`docker run -e OPENAI_API_KEY="AAA" -e TWITTER_API_KEY="BBB" -e TWITTER_API_SECRET="CCC" -e OAUTH_TOKEN="DDD" -e OAUTH_TOKEN_SECRET="EEE" twitter-story-time`
 
 **Step four**: To run your docker container on a scheule, you can set up a cron job:
 1. `sudo crontab -e` (opens an editor)
 2. Add this line to your crontab: 
 `0 0 * * * docker run -e OPENAI_API_KEY="AAA" -e TWITTER_API_KEY="BBB" -e TWITTER_API_SECRET="CCC" -e OAUTH_TOKEN="DDD" -e OAUTH_TOKEN_SECRET="EEE" twitter-story-time`. 
 
**Quick cronjob overview**:

The above schedule will run your job every day at midnight.

Cronjobs are typically structured in this order:

`minute hour day-of-month month day-of-week`

## New Features

### Lottery

In order to enhance the automation of Twitter Story Time, a lottery was added for probablistic tweeting. This was done by introducing a new enviroment variable, `LOTTERY`, which can be set to an integer number.

You can set `LOTTERY=N` where `1/N` is the chance of your tweet being sent out (winning the "lottery"). `LOTTERY` defaults to `1`, so if you do not override this env variable it will behave the same as before.

However, let's say that you set `LOTTERY` to `4`. That will result in a quarter chance of your tweet being sent. So in the event that your automation is scheduled to run four times a day, your account will send (on average) a single tweet out daily.