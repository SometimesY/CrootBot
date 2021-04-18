import json, requests
from datetime import datetime
from lxml import html
import get247, getRivals
from config import positions
from config import position_keys
from config import team_names

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def page_tree(url):
	page = requests.get(url, headers=headers)
	return html.fromstring(page.content)

def commit_text(url):
	tree = page_tree(url)
	
	text = '#' + get247.name(tree) + '\n\n'
	text += '##' + positions[get247.position(tree)] + ', Class of ' + get247.year(tree) + '\n\n'
	text += get247.height(tree) + ', ' + get247.weight(tree) + ' — From ' + get247.hometown(tree) + ' (' + get247.school(tree) + ')\n\n'
	text += '###Rankings\n\n'
	
	team = tree.xpath('//*[@id="page-content"]/div/section/section/div/ul/li[1]/div[1]/a[1]/text()')[0].strip()
	
	try:
		team = team_names[team]
	except:
		pass
	
	all_time_ranking_tree = page_tree('https://247sports.com/college/' + team + '/Sport/Football/AllTimeRecruits/')
	team_all_time_ranking = str(get247.all_time_ranking(all_time_ranking_tree, get247.name(tree), get247.year(tree)))
	
	if team_all_time_ranking != '' and team_all_time_ranking is not None:
		team = tree.xpath('//*[@id="page-content"]/div/section/section/div/ul/li[1]/div[1]/a[1]/text()')[0].strip()
		text += '[\#' + team_all_time_ranking + ' recruit all-time for ' + team + '](https://247sports.com/college/' + team + '/Sport/Football/AllTimeRecruits/)'
		text += '\n\n'
	
	text += '| SERVICE | RATING | POSITION | STATE | OVERALL |\n'
	text += '|:-:|:-:|:-:|:-:|:-:|\n'
	
	################################
	#      Composite rankings      #
	################################
	
	star_count = get247.stars(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/div/div[1]')[0])
	ranks = get247.rankings(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/ul')[0])
	
	text += '| **Composite** | ' + star_count + ' | '
	
	if ranks['position'] != '' and ranks['position'] != 'N/A':
		text += '**\#' + ranks['position'] + ' ' + get247.position(tree) + '**'
	else:
		text += '**N/A**'
	
	text += ' | '
	
	if ranks['state'] != '' and ranks['state'] != 'N/A':
		text += '**\#' + ranks['state'] + ' in ' + get247.hometown(tree).split(', ')[1] + '**'
	else:
		text += '**N/A**'
	
	text += ' | '
	
	if ranks['overall'] != '' and ranks['overall'] != 'N/A':
		text += '**\#' + ranks['overall'] + ' overall**'
	else:
		text += '**N/A**'
	
	text += ' |\n'
	
	################################
	#         247 rankings         #
	################################
	
	star_count = get247.stars(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/div/div[1]')[0])
	ranks = get247.rankings(tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/ul')[0])
	
	text += '| [247](' + url + ') | ' + star_count + ' | '
	
	if ranks['position'] != '' and ranks['position'] != 'N/A':
		text += '\#' + ranks['position'] + ' ' + get247.position(tree)
	else:
		text += 'N/A'
	
	text += ' | '
	
	if ranks['state'] != '' and ranks['state'] != 'N/A':
		text += '\#' + ranks['state'] + ' in ' + get247.hometown(tree).split(', ')[1]
	else:
		text += 'N/A'
	
	text += ' | '
	
	if ranks['overall'] != '' and ranks['overall'] != 'N/A':
		text += '\#' + ranks['overall'] + ' overall'
	else:
		text += 'N/A'
	
	text += ' |\n'
	
	################################
	#       Rivals rankings        #
	################################
	
	rivals_text = ''
	
	try:
		player = getRivals.matching_player(get247.name(tree), get247.year(tree), get247.hometown(tree))
		
		rivals_text += '| [Rivals](' + getRivals.url(player) + ') | ' + getRivals.stars(player) + ' | '
		
		if player['position_rank'] is not None:
			rivals_text += '\#' + str(player['position_rank']) + ' ' + get247.position(tree)
		else:
			rivals_text += 'N/A'
		
		rivals_text += ' | '
		
		if player['state_rank'] is not None:
			rivals_text += '\#' + str(player['state_rank']) + ' in ' + get247.hometown(tree).split(', ')[1]
		else:
			rivals_text += 'N/A'
		
		rivals_text += ' | '
		
		if player['national_rank'] is not None:
			rivals_text += '\#' + str(player['national_rank']) + ' overall'
		else:
			rivals_text += 'N/A'
		
		rivals_text += ' |'
	except:
		rivals_text = '| Rivals | N/A | N/A | N/A | N/A |'
	
	text += rivals_text
	text += '\n\n'
	
	text += '---\n\n'
	
	################################
	#   Recent commitment history  #
	################################
	
	if '/high-school/' in url:
		url = url.split('/high-school/')[0]
	
	commitment_tree = page_tree(url + '/TimelineEvents')
	commitment_history = get247.commitment_history(commitment_tree)
	
	if commitment_history != '':
		text += commitment_history
		text += '---\n\n'
	
	return text

def recruit_search(year, last_name, first_name, position):
	url = 'https://247sports.com/Season/' + year + '-Football/Recruits.json?&Items=15&Page=1&Player.LastName=' + last_name + '&Player.FirstName=' + first_name + '&Position.Key=' + position_keys[position]
	
	payload={}
	
	headers = {'authority': '247sports.com',
			'dnt': '1',
			'x-requested-with': 'XMLHttpRequest',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
			'content-type': 'text/html; charset=utf-8',
			'accept': '*/*',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://247sports.com/Season/' + year + '-Football/Recruits/?&Player.LastName=' + last_name + '&Player.FirstName=' + first_name,
			'accept-language': 'en-US,en;q=0.9'}
	
	response = requests.request("GET", url, headers=headers, data=payload)
	if year < str(datetime.now().year):
		return commit_text(json.loads(response.text)[0]['Player']['Url'] + 'high-school/')
	else:
		return commit_text(json.loads(response.text)[0]['Player']['Url'])

def team_class(year, team, team_name=None):
	if team_name is None:
		team_name = team
	
	try:
		url = 'https://247sports.com/college/' + team_name.replace(' ', '-').replace('&', '').replace('é', 'e').replace("'", '') + '/Season/' + str(year) + '-Football/Commits/'
		tree = page_tree(url)
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
			star_count = get247.stars(tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[4]/div[1]')[0])
			team_class += '|[' + player + '](' + player_page + ')|' + position + '|' + high_school + '|' + star_count + '|\n'
		except:
			player_type = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/b[1]/text()')[0].split(' (')[0]
			
			team_class += '\n##' + player_type + '\n\n'
			team_class += '|Player|Position|High School|Composite Rating|\n'
			team_class += '|:--|:-:|:--|:-:|\n'
	
	return team_class

def transfer(school, name):
	current_year = datetime.now().year
	
	for year in range (current_year - 6, current_year): #check the previous six years
		url = 'https://247sports.com/college/' + school.replace(' ', '-').replace('&', '').replace('é', 'e').replace("'", '') + '/Season/' + str(year) + '-Football/Commits/'
		tree = page_tree(url)
		
		# Enrollees
		for i in range (1, len(tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0])):
			try:
				player_name = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[2]/a/text()')[0]
				player_page = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul/li[' + str(i) + ']/div[1]/div[2]/a')[0].attrib['href']
				player_page = 'https:' + player_page + '/high-school/'
				
				if player_name.lower() in name.lower() or name.lower() in player_name.lower():
					return commit_text(player_page)
			except:
				pass
	

def bottom_text(post_or_comment, post_or_comment_id):
	return 'Any bugs can be submitted as a PM to me [here](https://www.reddit.com/message/compose/?to=CFBCrootBot&subject=Bug+report+on+' + post_or_comment + '+id+' + post_or_comment_id + '&message=Enter+description+of+bug)! I am still learning, so please bear with me. I now have Rivals rankings, but they are not perfect. ESPN rankings are hopefully coming soonish. Check out the github repository for CFBCrootBot [here](https://github.com/SometimesY/CrootBot)!\n\nMake sure to check out the /r/CFB recruiting tool [here](https://www.redditcfb.com/recruiting.php) for generating your own commit posts.'



