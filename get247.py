import requests
from lxml import html
from config import positions

########################################
#             Player data              #
########################################

def name_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/h1')[0]

def name(tree):
	return name_container(tree).text.strip()

def position_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[1]/span[2]')[0]

def position(tree):
	return position_container(tree).text.strip()

def year_container(tree):
	try:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[3]/span[2]')[0]
	except:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[2]/span[2]')[0]

def year(tree):
	return year_container(tree).text.strip()

def height_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[2]/span[2]')[0]

def height(tree):
	return height_container(tree).text.strip()

def weight_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[1]/li[3]/span[2]')[0]

def weight(tree):
	return weight_container(tree).text.strip()

def hometown_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[2]/span[2]')[0]

def hometown(tree):
	return hometown_container(tree).text.strip()

def high_school_container(tree):
	try:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]/a')[0]
	except:
		try:
			return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/span[2]')[0]
		except:
			try:
				return tree.xpath('//*[@id="page-content"]/div/section/header/div[1]/ul[3]/li[1]/div/span[2]')[0]
			except:
				return ''

def high_school(tree):
	return high_school_container(tree).text.strip()

def team_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section/section/div/ul/li[1]/div[1]/a[1]')[0]

def team(tree):
	return team_container(tree).text.strip()

def score_container(tree, row):
	if row == 'composite':
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/div/div[2]')[0]
	else:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/div/div[2]')[0]

def score(tree, row):
	score = score_container(tree, row).text.strip()
	
	if score == '':
		score = 'N/A'
	
	if row == 'composite':
		score = '**' + score + '**'

def stars_container(tree, row):
	if row == 'composite':
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/div/div[1]')[0]
	else:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/div/div[1]')[0]

def stars(tree, row):
	stars = ''

	for i in range (0, 5):
		if stars_container(tree, row)[i].get('class') == 'icon-starsolid yellow':
			stars += '★'
		else:
			stars += '☆'
	
	return stars

def position_ranking_container(tree, row):
	if row == 'composite':
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/ul/li[2]/a/strong')[0]
	else:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/ul/li[2]/a/strong')[0]

def position_ranking(tree, row):
	ranking = position_ranking_container(tree, row).text.strip()
	
	if ranking != '' and ranking != 'N/A':
		ranking = '\#' + ranking + ' ' + position(tree)
	else:
		ranking = 'N/A'
	
	if row == 'composite':
		ranking = '**' + ranking + '**'
	
	return ranking

def state_ranking_container(tree, row):
	if row == 'composite':
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/ul/li[3]/a/strong')[0]
	else:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/ul/li[3]/a/strong')[0]

def state_ranking(tree, row):
	ranking = position_ranking_container(tree, row).text.strip()
	
	if ranking != '' and ranking != 'N/A':
		ranking = '\#' + ranking + ' in ' + hometown(tree).split(', ')[1]
	else:
		ranking = 'N/A'
	
	if row == 'composite':
		ranking = '**' + ranking + '**'
	
	return ranking

def overall_ranking_container(tree, row):
	if row == 'composite':
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[1]/ul/li[1]/a/strong')[0]
	else:
		return tree.xpath('//*[@id="page-content"]/div/section/header/div[2]/section[1]/section[2]/ul/li[1]/a/strong')[0]

def overall_ranking(tree, row):
	ranking = position_ranking_container(tree, row).text.strip()
	
	if ranking != '' and ranking != 'N/A':
		ranking = '\#' + ranking + ' overall'
	else:
		ranking = 'N/A'
	
	if row == 'composite':
		ranking = '**' + ranking + '**'
	
	return ranking

def all_time_ranking_container(tree):
	return tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0]

def all_time_ranking(tree, name, year):
	rankings_container = all_time_ranking_container(tree)
	
	for i in range (0, len(rankings_container)):
		player = rankings_container[i][0][1]
		if name == player[0].text.strip() and year == player[2].text.split('Class of ')[1].strip():
			return i+1

def commitment_history_container(tree):
	return tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul')[0]

def commitment_history(tree):
	commitment_history = ''
	
	for i in range (1, len(commitment_history_container(tree))+1):
		date = tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/b/text()')[0].split(':')[0]
		school = tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/p[2]/text()')[0]
		
		if 'commits to' in school:
			school = school.split('commits to ')[1]
			commitment_history += 'Committed to ' + school + ' on ' + date + '\n\n'
		elif 'decommits from' in school:
			school = school.split('decommits from ')[1]
			commitment_history += 'Decommitted from ' + school + ' on ' + date + '\n\n'
	
	return commitment_history

########################################
#              Team data               #
########################################

def team_national_rank_container(tree):
	return tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[1]/a')[0]

def team_national_rank(tree):
	return team_national_rank_container(tree).text.strip()

def team_conference_rank_container(tree):
	return tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[2]/a')[0]

def team_conference_rank(tree):
	return team_national_rank_container(tree).text.strip()

def team_average_rating_container(tree):
	return tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/section/div[3]/span')[0]

def team_average_rating(tree):
	return team_national_rank_container(tree).text.strip()

def team_class_players_container(tree):
	return tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0]

