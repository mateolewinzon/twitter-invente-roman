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

def check_mentions(api, since_id, frase):
  logger.info('Checking mentions')
  new_since_id = since_id
  for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
    new_since_id = max(tweet.id, new_since_id)
    logger.info(f"answerng to {tweet.user.name}")
    api.update_status(status=frase, in_reply_to_status_id=tweet.id)


  return new_since_id

def get_phrase(last):
  if random.random() < 0.8:
    frase = random.choice(frases_si)
    if frase == last:
      return get_phrase(frase)
    return frase
  else:
    frase = random.choice(frases_no)
    if frase == last:
      return get_phrase(last)
    return frase

def main():
  frase = ''

  api = create_api()
  since_id = 1
  while True:
    frase = get_phrase(frase)
    since_id = check_mentions(api, since_id, frase)
    logger.info("Waiting...")
    time.sleep(60*5)

main()