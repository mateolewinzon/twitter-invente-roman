import random
import tweepy
import os
import logging
import time
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

frases_no = ['No.', 'No jugó Román.']
frases_si = ['Sí.', 'Jugó Román.', '¡Invente Román invente!']

def check_mentions(api, since_id):
  logger.info('Checking mentions')
  new_since_id = since_id
  for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
    new_since_id = max(tweet.id, new_since_id)
    logger.info(f"answerng to {tweet.user.name}")
    api.update_status(status=get_phrase(api), in_reply_to_status_id=tweet.id)
  return new_since_id

def get_phrase(api):
  if random.random() < 0.8:
    frase = random.choice(frases_si)
  else: frase =  random.choice(frases_no)
  if api.home_timeline(count=1)[0].text == frase:
    return get_phrase(api)
  else: return frase

def main():
  api = create_api()
  since_id = 1
  while True:
    since_id = check_mentions(api, since_id)
    logger.info("Waiting...")
    time.sleep(60)

main()