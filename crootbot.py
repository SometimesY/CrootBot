import json, praw, re, requests, time
from lxml import html
import config, crootbot_functions

try:
	in_file = open('posts.log', 'r')
	posts = in_file.read()
	posts = json.loads(posts)
	in_file.close()
except:
	posts = {}

# Clear 3+ day old posts to make sure that the list isn't super long
for key in list(posts.keys()):
	if posts[key] + 3*24*60*60 < int(time.time()):
		del posts[key]

reddit = praw.Reddit(username = config.username, password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = config.username + ' for /r/' + config.subreddit + ' by /u/SometimesY')

# Script runs minutely, so going back 50 posts should be more than enough
for post in reddit.subreddit(config.subreddit).new(limit=50):
	title = post.title.lower()
	
	if str(post) in posts.keys():
		continue
	
	if ('*' in title or 'star' in title) and ('commit' in title or 'decommit' in title or 'flip' in title):
		comment_text = ''
		
		try:
			url = post.selftext.lower().split('/')
			url = url[url.index('player') + 1] # get unique player URI
			url = 'https://247sports.com/player/' + re.search('.*-[0-9]+', url).group(0) + '/'
			
			comment_text = crootbot_functions.commit_text(url)
			comment_text += crootbot_functions.bottom_text('post', str(post))
			
			comment = reddit.submission(id=post.id).reply(comment_text)
			comment.disable_inbox_replies()
			
			posts[str(post)] = int(comment.created_utc)
		except:
			pass

for message in reddit.inbox.unread():
	try:
		comment = reddit.comment(message)
		subreddit = comment.subreddit # Check if PM or reddit comment
		
		if subreddit == config.subreddit:
			body = comment.body
			body = body.replace(':', '')
			comment_text = ''
			
			try:
				# Use u/ rather than /u/ since not everyone pings via /u/ these days
				year = body.split('u/' + config.username)[1].strip().split(' ')[0].strip()
				team = body.split(year)[1].strip()
				
				try:
					team_name = config.team_names[team]
				except:
					team_name = None
				
				year = int(year)
				
				comment_text = crootbot_functions.team_class(year, team, team_name) + '\n\n'
				comment_text += crootbot_functions.bottom_text('comment', str(comment))
				
				reply = comment.reply(comment_text)
				reply.disable_inbox_replies()
				comment.mark_read()
			except:
				pass
	except:
		pass

out_file = open('posts.log', 'w')
out_file.write(json.dumps(posts, indent=5))
out_file.close()



