import json, requests
from datetime import datetime
from lxml import html
import get247, getRivals
from config import headers
from config import headers_full
from config import positions
from config import position_keys
from config import team_names

def sanitize_team(team):
	if team in team_names:
		team = team_names[team]
	
	team = team.replace(' ', '-').replace('&', '').replace('é', 'e').replace("'", '')
	return team

def page_tree(url):
	page = requests.get(url, headers=headers)
	return html.fromstring(page.content)

def commit_text(url):
	tree = page_tree(url)
	
	name			= get247.name(tree)
	position		= get247.position(tree)
	year			= get247.year(tree)
	height		= get247.height(tree)
	weight		= get247.weight(tree)
	hometown		= get247.hometown(tree)
	state		= hometown.split(', ')[1]
	high_school	= get247.high_school(tree)
	team			= get247.team(tree)
	
	text = '#' + name + '\n\n'
	text += '##' + positions[position] + ', Class of ' + year + '\n\n'
	text += height + ', ' + weight + ' — From ' + hometown + ' (' + high_school + ')\n\n'
	text += '###Rankings\n\n'
	
	all_time_ranking_tree = page_tree('https://247sports.com/college/' + sanitize_team(team) + '/Sport/Football/AllTimeRecruits/')
	team_all_time_ranking = get247.all_time_ranking(all_time_ranking_tree, name, year)
	
	if team_all_time_ranking != '' and team_all_time_ranking is not None:
		text += '[\#' + str(team_all_time_ranking) + ' recruit all-time for ' + team + '](https://247sports.com/college/' + sanitize_team(team) + '/Sport/Football/AllTimeRecruits/)'
		text += '\n\n'
	
	text += '| SERVICE | SCORE | RATING | POSITION | STATE | OVERALL | \n'
	text += '|:-:|:-:|:-:|:-:|:-:|:-:|\n'
	
	################################
	#      Composite rankings      #
	################################
	
	text += '| **Composite** | '
	text += get247.score(tree, 'composite') + ' | '
	text += get247.stars(tree, 'composite') + ' | '
	text += get247.position_ranking(tree, 'composite') + ' | '
	text += get247.state_ranking(tree, 'composite') + ' | '
	text += get247.overall_ranking(tree, 'composite') + ' | '
	text += '\n'
	
	################################
	#         247 rankings         #
	################################
	
	text += '| [247](' + url + ') | '
	text += get247.score(tree, '247') + ' | '
	text += get247.stars(tree, '247') + ' | '
	text += get247.position_ranking(tree, '247') + ' | '
	text += get247.state_ranking(tree, '247') + ' | '
	text += get247.overall_ranking(tree, '247') + ' | '
	text += '\n'
	
	################################
	#       Rivals rankings        #
	################################
	
	rivals_text = ''
	
	try:
		player	= getRivals.matching_player(name, year, hometown)
		
		rivals_text += '| [Rivals](' + getRivals.url(player) + ') | '
		rivals_text += getRivals.score(player) + ' | '
		rivals_text += getRivals.stars(player) + ' | '
		rivals_text += getRivals.position_ranking(player) + ' | '
		rivals_text += getRivals.state_ranking(player) + ' | '
		rivals_text += getRivals.overall_ranking(player) + ' | '
	except:
		rivals_text = '| Rivals | N/A | N/A | N/A | N/A | N/A |'
	
	text += rivals_text
	text += '\n\n'
	text += '---\n\n'
	
	################################
	#   Recent commitment history  #
	################################
	
	if url.endswith('/high-school'):
		url = url[:-12]
	elif url.endswith('/high-school/'):
		url = url[:-13]
	
	if url.endswith('/'):
		url = url[:-1]
	
	commitment_tree	= page_tree(url + '/TimelineEvents')
	commitment_history	= get247.commitment_history(commitment_tree)
	
	if commitment_history != '':
		text += commitment_history
		text += '---\n\n'
	
	return text

def recruit_search(year, position, first_name, last_name):
	url = 'https://247sports.com/Season/' + year + '-Football/Recruits.json?&Items=15&Page=1&Player.LastName=' + last_name + '&Player.FirstName=' + first_name + '&Position.Key=' + position_keys[position]
	
	headers_full['referer'] = 'https://247sports.com/Season/' + year + '-Football/Recruits/?&Player.LastName=' + last_name + '&Player.FirstName=' + first_name
	
	payload	= {}
	response	= requests.request("GET", url, headers=headers_full, data=payload)
	
	# If prior year commit (i.e. active CFB or no longer CFB), go to high school profile
	# Else, use profile
	
	if year < str(datetime.now().year):
		url = json.loads(response.text)[0]['Player']['Url']
		
		# Future proofing slightly
		if not url.endswith('/'):
			url += '/'
		
		url += 'high-school/'
	else:
		url = json.loads(response.text)[0]['Player']['Url']
	
	return commit_text(url)

def team_class(year, team):
	try:
		url = 'https://247sports.com/college/' + sanitize_team(team) + '/Season/' + year + '-Football/Commits/'
		tree = page_tree(url)
	except:
		return None
	
	team_class = '##' + team + ' ' + year + ' Class\n\n'
	team_class += '|National Rank|Conference Rank|Average Rating|\n'
	team_class += '|:-:|:-:|:-:|\n'
	
	national_rank		= get247.team_national_rank(tree)
	conference_rank	= get247.team_conference_rank(tree)
	average_rating		= get247.team_average_rating(tree)
	
	team_class += '|' + national_rank + '|' + conference_rank + '|' + average_rating + '|\n\n'
	
	players_container = get247.team_class_players_container(tree)
	
	for i in range (0, len(players_container)):
		try:
			url			= 'https:' + players_container[i][0][1][0].attrib['href'] + '/high-school/'
			tree			= page_tree(url)
			
			name			= get247.name(tree)
			position		= get247.position(tree)
			hometown		= get247.hometown(tree)
			high_school	= get247.high_school(tree)
			stars		= get247.stars(tree, 'composite')
			score		= get247.score(tree, 'composite')
			
			team_class += '| [' + name + '](' + url + ') | ' + position + ' | ' + high_school + ' (' + hometown + ') | ' + stars + ' | ' + score + ' | \n'
		except:
			team_class += '\n##' + players_container[i][0].text.split('(')[0].strip() + '\n\n'
			team_class += '| Player | Position | High School | Composite | Rating | \n'
			team_class += '|:--|:-:|:--|:-:|:-:|\n'
	
	return team_class

def transfer(team, name):
	current_year = datetime.now().year
	
	for year in range (current_year - 6, current_year): #check the previous six years
		url		= 'https://247sports.com/college/' + sanitize_team(team) + '/Season/' + str(year) + '-Football/Commits/'
		tree		= page_tree(url)
		transfers	= tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0]
		
		# Enrollees
		for i in range (1, len(transfers)):
			try:
				player_name = transfers[i][0][1][0].text.strip()
				player_page = 'https:' + transfers[i][0][1][0].attrib['href'] + '/high-school/'
				
				if player_name.lower().replace("'", '') in name.lower() or name.lower() in player_name.lower().replace("'", ''):
					return commit_text(player_page)
			except:
				pass

def bottom_text(post_or_comment, post_or_comment_id):
	return 'Any bugs can be submitted as a **[PM to me](https://www.reddit.com/message/compose/?to=CFBCrootBot&subject=Bug+report+on+' + post_or_comment + '+id+' + post_or_comment_id + '&message=Enter+description+of+bug)**. I am still learning, so please bear with me. I now have Rivals rankings, but they are not perfect. ESPN rankings are hopefully coming soonish (but probably not since ESPN\'s search is broken and they don\'t seem to care). Check out the **[github repository](https://github.com/SometimesY/CrootBot)** for CFBCrootBot.\n\nYou can invoke me with, for instance:\n\n>/u/CFBCrootBot: 2017 Alabama\n\nto get Alabama\'s 2017 recruiting class, or via\n\n>/u/CFBCrootBot: 2015 PRO Joe Burrow\n\nto get Joe Burrow\'s recruit information.\n\nMake sure to check out the **[/r/CFB recruiting post generator here](https://www.redditcfb.com/recruiting.php)** for generating your own (de)commit posts.'

