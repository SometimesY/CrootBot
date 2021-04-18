import requests
from lxml import html
from config import positions


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

def all_time_ranking(tree, name, year):
	rankings_container = tree.xpath('//*[@id="page-content"]/div[1]/section[2]/section/div/ul')[0]
	for i in range (0, len(rankings_container)):
		player = rankings_container[i][0][1]
		if name == player[0].text.strip() and year == player[2].text.split('Class of ')[1].strip():
			return i+1

def commitment_history(tree):
	commitment_history = ''
	
	for i in range (1, len(tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul')[0])+1):
		date = tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/b/text()')[0].split(':')[0]
		school = tree.xpath('//*[@id="page-content"]/div/section[2]/section/section/ul/li[' + str(i) + ']/div/p[2]/text()')[0]
		
		if 'commits to' in school:
			school = school.split('commits to ')[1]
			commitment_history += 'Committed to ' + school + ' on ' + date + '\n\n'
		elif 'decommits from' in school:
			school = school.split('decommits from ')[1]
			commitment_history += 'Decommitted from ' + school + ' on ' + date + '\n\n'
	
	return commitment_history

