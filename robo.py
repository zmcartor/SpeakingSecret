from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file , read_token_file
from twitter.oauth_dance import oauth_dance

import os
import time
import sys


#import any other natual processing libs

CONSUMER_KEY = 'o2EVUpU1Qn3zBRxyQ7xSxQ'
CONSUMER_SECRET = 'u46YiTorqOCF0qmgpUSdeg2hxH77Cv6epTOdP869xI'

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

	#main loop. Just keep searching anyone talking to us
	while True:
		mentions = sbird.search(q='@SpeakingSecret', since_id=last_id_replied)['results']
		if not mentions:
			print "No one talking to us now..."

		for mention in mentions:
			#cut our @SpeakingSecret out 
			message = mention['text'].replace('@SpeakingSecret' , '')
			speaker = mention['from_user']
			speaker_id = str(mention['id'])

			print "Something named "+speaker+" is saying "+message

			last_id_replied=speaker_id
		
		print "Slumber...\n\n"
		time.sleep(10)

