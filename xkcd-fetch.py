#!/usr/bin/env python3

import csv, html.parser, json, os, re
import httplib2


def html_unescape(s):
	p = html.parser.HTMLParser()
	return p.unescape(s)


http = httplib2.Http('.cache')

def fetch(url):
	response, content = http.request(url, 'GET')
	return content

def fetch_text(url):
	return fetch(url).decode('utf-8')


def read_index():
	''' reads the index from a json file '''
	f = open('xkcd-db.json', 'r')
	index = json.loads(f.read())
	f.close()
	return index

def write_index(index):
	''' Write the index to disk as json and csv files '''
	
	index.sort(key=lambda entry: int(entry['number']))
	
	f = open('xkcd-db.json', 'w')
	f.write(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2))
	f.close()
	
	f = open('xkcd-db.csv', 'w')
	writer = csv.DictWriter(f, ['number', 'date','title','desc','file'])#, quoting=csv.QUOTE_ALL)
	#writer.writeheader() # will arrive in Python 3.2!
	for entry in index:
		writer.writerow(entry)
	f.close()


def fetch_index(index):
	''' updates the index, returns how many new items were downloaded '''
	
	archive = fetch_text('https://www.xkcd.com/archive/')
	
	archive_pattern = r'<a href="/(\d+)/" title="(\d{4}-\d{1,2}-\d{1,2})">(.*?)</a>'
	
	page_pattern = r'<img src="http://imgs.xkcd.com/comics/(.*?)" title="(.*?)" alt="(.*?)" (USEMAP="#xkcdtemp_Map")?/>'
	
	counter = 0
	
	found = sorted([int(entry['number']) for entry in index])
	
	for a in re.finditer(archive_pattern, archive):
		entry = dict()
		entry['number'] = a.group(1) # 886
		entry['date'] = a.group(2)   # 2011-4-15
		entry['title'] = a.group(3)  # Craigslist Apartments
		
		if int(entry['number']) in found:
			continue # don’t fetch what we already have
		
		page = fetch_text('https://www.xkcd.com/'+a.group(1)+'/')
		p = re.search(page_pattern, page)
		if(p == None):
			continue
		
		entry['file'] = p.group(1)                # craigslist_apartments.png
		entry['desc'] = html_unescape(p.group(2)) # $1600 / 1386153BR 3BATH, …
		#entry['title'] = p.group(3)              # Craigslist Apartments
		
		for e in entry:
			print('{:10s} = {}'.format(e, entry[e]))
		print('Downloading …')
		
		path = os.path.join('image', '{:04d}_{}'.format(int(entry['number']), entry['file']))
		image = open(path, 'wb')
		image.write(fetch('http://imgs.xkcd.com/comics/'+entry['file']))
		image.close()
		
		index.append(entry)
		found.append(int(entry['number']))
		counter += 1
	
	# Search for errors:
	missing = [i for i in range(1, max(found)+1) if (i not in found) and (i != 404)]
	if len(missing)>0:
		print('{:d} comics are missing:\n{}'.format(len(missing), missing))
	else:
		print('You are up-to-date again!')

	return counter


if not os.path.exists('image'):
	os.mkdir('image')

try:
	index = read_index() # from disk
except:
	index = []
	print('Running the first time (this may take a while – drink some tee) …')

print('Start update …')
if fetch_index(index)>0:
	write_index(index)

print('The database now contains {:d} comics.'.format(len(index)))

