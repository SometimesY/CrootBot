import requests
from lxml import html

positions = {}
positions['PRO'] = 'Pro-Style Quarterback'
positions['DUAL'] = 'Dual-Threat Quarterback'
positions['APB'] = 'All Purpose Back'
positions['RB'] = 'Running Back'
positions['FB'] = 'Fullback'
positions['WR'] = 'Wide Receiver'
positions['TE'] = 'Tight End'
positions['OT'] = 'Offensive Tackle'
positions['OG'] = 'Offensive Guard'
positions['OC'] = 'Center'
positions['WDE'] = 'Weak-Side Defensive End'
positions['SDE'] = 'Strong-Side Defensive End'
positions['DT'] = 'Defensive Tackle'
positions['ILB'] = 'Inside Linebacker'
positions['OLB'] = 'Outside Linebacker'
positions['CB'] = 'Cornerback'
positions['S'] = 'Safety'
positions['ATH'] = 'Athlete'
positions['K'] = 'Kicker'
positions['LS'] = 'Long Snapper'
positions['RET'] = 'Returner'

def name(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/h1/text()')[0]

def position(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[1]/span[2]/text()')[0]

def height(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[2]/span[2]/text()')[0]

def weight(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[3]/span[2]/text()')[0]

def school(tree):
	try:
		school = tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/a/text()')[0]
	except:
		try:
			school = tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/text()')[0]
		except:
			try:
				school = tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/div/span[2]/text()')[0]
			except:
				school = ''
	return school.strip()

def hometown(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[2]/span[2]/text()')[0]

def year(tree):
	try:
		year = tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[3]/span[2]/text()')[0]
	except:
		year = tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[2]/span[2]/text()')[0]
	return year

def stars(stars_container):
	stars = 0

	for i in range (0, 5):
		if stars_container[i].get('class') == 'icon-starsolid yellow':
			stars += 1
	
	star_list = ''
	
	for i in range (1, 6):
		if i <= stars:
			star_list += '★'
		else:
			star_list += '☆'
	
	return star_list

def rankings(rankings_container):
	rankings = {}
	rankings['overall'] = ''
	rankings['position'] = ''
	rankings['state'] = ''
	
	for i in range (0, len(rankings_container)):
		category = rankings_container[i][0].text
		
		if 'Natl.' in category:
			rankings['overall'] = rankings_container[i][1][0].text
		elif category in positions.keys():
			rankings['position'] = rankings_container[i][1][0].text
		elif category != 'All-Time':
			rankings['state'] = rankings_container[i][1][0].text
	
	return rankings

def commitment_history(commit_tree):
	commitment_history = ''
	
	for i in range (1, len(commit_tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul')[0])+1):
		date = commit_tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/b/text()')[0].split(':')[0]
		school = commit_tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/p[2]/text()')[0]
		
		if 'commits to' in school:
			school = school.split('commits to ')[1]
			commitment_history += 'Committed to ' + school + ' on ' + date + '\n\n'
		elif 'decommits from' in school:
			school = school.split('decommits from ')[1]
			commitment_history += 'Decommitted from ' + school + ' on ' + date + '\n\n'
	
	return commitment_history

def commit_text(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	page = requests.get(url, headers=headers)
	tree = html.fromstring(page.content)
	
	text = '#' + name(tree) + '\n\n'
	text += '##' + positions[position(tree)] + ', Class of ' + year(tree) + '\n\n'
	text += height(tree) + ', ' + weight(tree) + ' — From ' + hometown(tree) + ' (' + school(tree) + ')\n\n'
	text += '###Rankings\n\n'
	text += '| SERVICE | RATING | POSITION | STATE | OVERALL |\n'
	text += '|:-:|:-:|:-:|:-:|:-:|\n'
	
	################################
	#         247 rankings         #
	################################
	
	star_count = stars(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/div/div[1]')[0])
	ranks = rankings(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/ul')[0])
	
	text += '| [247](' + url + ') | ' + star_count + ' | '
	
	if ranks['position'] != '' and ranks['position'] != 'N/A':
		text += '\#' + ranks['position'] + ' ' + position(tree)
	else:
		text += 'N/A'
	
	text += ' | '
	
	if ranks['state'] != '' and ranks['state'] != 'N/A':
		text += '\#' + ranks['state'] + ' in ' + hometown(tree).split(', ')[1]
	else:
		text += 'N/A'
	
	text += ' | '
	
	if ranks['overall'] != '' and ranks['overall'] != 'N/A':
		text += '\#' + ranks['overall'] + ' overall'
	else:
		text += 'N/A'
	
	text += ' |\n'
	
	################################
	#      Composite rankings      #
	################################
	
	star_count = stars(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/div/div[1]')[0])
	ranks = rankings(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/ul')[0])
	
	text += '| **Composite** | ' + star_count + ' | '
	
	if ranks['position'] != '' and ranks['position'] != 'N/A':
		text += '**\#' + ranks['position'] + ' ' + position(tree) + '**'
	else:
		text += '**N/A**'
	
	text += ' | '
	
	if ranks['state'] != '' and ranks['state'] != 'N/A':
		text += '**\#' + ranks['state'] + ' in ' + hometown(tree).split(', ')[1] + '**'
	else:
		text += '**N/A**'
	
	text += ' | '
	
	if ranks['overall'] != '' and ranks['overall'] != 'N/A':
		text += '**\#' + ranks['overall'] + ' overall**'
	else:
		text += '**N/A**'
	
	text += ' |\n\n'
	
	text += '---\n\n'
	
	################################
	#   Recent commitment history  #
	################################
	
	commit_page = requests.get(url + '/TimelineEvents', headers=headers)
	commit_tree = html.fromstring(commit_page.content)
	
	if commitment_history != '':
		text += commitment_history(commit_tree)
		
		text += '---\n\n'
	
	return text

def team_class(year, team, team_name=None):
	if team_name is None:
		team_name = team
	
	try:
		url = 'https://247sports.com/college/' + team_name.replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace('é', 'e').replace("'", '') + '/Season/' + str(year) + '-Football/Commits/'
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
		page = requests.get(url, headers=headers)
		tree = html.fromstring(page.content)
	except:
		return None
	
	team_class = '##' + team + ' ' + str(year) + ' Class\n\n'
	
	national_rank = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[1]/a/text()')[0]
	conference_rank = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[2]/a/text()')[0]
	average_rating = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[3]/span/text()')[0]
	
	team_class += '|National Rank|Conference Rank|Average Rating|\n'
	team_class += '|:-:|:-:|:-:|\n'
	team_class += '|' + national_rank + '|' + conference_rank + '|' + average_rating + '|\n\n'
	
	players = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0]
	
	for i in range (1, len(players)+1):
		try:
			player = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[2]/a/text()')[0]
			player_page = 'https:' + tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[2]/a')[0].attrib['href'] + '/'
			position = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[6]/text()')[0].strip()
			try:
				high_school = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[2]/span/text()')[0].strip()
			except:
				high_school = ''
			star_count = stars(tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[4]/div[1]')[0])
			team_class += '|[' + player + '](' + player_page + ')|' + position + '|' + high_school + '|' + star_count + '|\n'
		except:
			player_type = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/b[1]/text()')[0].split(' (')[0]
			
			team_class += '\n##' + player_type + '\n\n'
			team_class += '|Player|Position|High School|Composite Rating|\n'
			team_class += '|:--|:-:|:--|:-:|\n'
	
	return team_class

def bottom_text(post_or_comment, post_or_comment_id):
	return 'Any bugs can be submitted as a PM to me [here](https://www.reddit.com/message/compose/?to=CFBCrootBot&subject=Bug+report+on+' + post_or_comment + '+id+' + post_or_comment_id + '&message=Enter+description+of+bug)! I am still learning, so please bear with me. Rivals and ESPN rankings are hopefully coming soonish! Check out the github repository for CFBCrootBot [here](https://github.com/SometimesY/CrootBot)!'

