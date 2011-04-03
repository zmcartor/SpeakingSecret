from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file , read_token_file
from twitter.oauth_dance import oauth_dance

import os
import time
import sys
import time
import cleverbot
#import any other natual processing libs

#These are the keys from the twitter tools for python library.
CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'

#make sure you authenticate using the commandline tool. This will create a file called .twitter_oauth in your ~

if __name__ == "__main__":
   	oauth_file = os.environ.get("HOME",'')+os.sep+'.twitter_oauth'
	oa_token , oa_token_secret = read_token_file(oauth_file)

	#twitter client to search
	sbird = Twitter(domain='search.twitter.com')
	#make sure this guy is a tuple
	sbird.uriparts =()

	#anyone talking to us?
	last_id_replied = ''

	#twitter client to post. Posting requires oAuth schutff
	pbird = Twitter(auth=OAuth(oa_token , oa_token_secret, CONSUMER_KEY , CONSUMER_SECRET),
			secure=True,
			api_version='1',
			domain="api.twitter.com")


	#our cleverbot instance
	cbot=cleverbot.Session()

	#main loop. Just keep searching anyone talking to us
	while True:
		mentions = sbird.search(q='@SpeakingSecret', since_id=last_id_replied)['results']
		if not mentions:
			print "No one talking to us now...", time.ctime()

		for mention in mentions:
			#cut our @SpeakingSecret out 
			message = mention['text'].replace('@SpeakingSecret' , '')
			speaker = mention['from_user']
			speaker_id = str(mention['id'])

			print "[+] Something named "+speaker+" is saying "+message
			clever_response = cbot.Ask(message)
			reply = '@%s %s' % (speaker, clever_response) 
			print "[+] Replying " , reply
			pbird.statuses.update(status=reply)
			#update last_id_replied
			last_id_replied=speaker_id
		
		print "[Zzz] Slumber...\n"
		time.sleep(10)
