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
	
	archive = fetch_text('https://www.xkcd.com/archive/')
	
	archive_pattern = r'<a href="/(\d+)/" title="(\d{4}-\d{1,2}-\d{1,2})">(.*?)</a>'
	
	page_pattern = r'<img src="http://imgs.xkcd.com/comics/(.*?)" title="(.*?)" alt="(.*?)" (USEMAP="#xkcdtemp_Map")?/>'
	
	for a in re.finditer(archive_pattern, archive):
		entry = dict()
		entry['number']= a.group(1) # 886
		entry['date']= a.group(2)   # 2011-4-15
		entry['title']= a.group(3)  # Craigslist Apartments
		
		page = fetch_text('https://www.xkcd.com/'+a.group(1)+'/')
		
		for p in re.finditer(page_pattern, page):
			
			entry['file'] = p.group(1)                  # craigslist_apartments.png
			entry['desc'] = html_unescape(p.group(2))   # $1600 / 1386153BR 3BATH, …
			#entry['title'] = p.group(3)                # Craigslist Apartments
			
			o = 'image/{:04d}_{}'.format(int(entry['number']), entry['file'])
			index.append(entry)
			
			for e in entry:
				print('{:10s} = {}'.format(e, entry[e]))
			print('Downloading …')
			
			image = open(o, 'wb')
			image.write(fetch('http://imgs.xkcd.com/comics/'+entry['file']))
			image.close()
			
		
	return index;


if not os.path.exists('image'):
	os.mkdir('image')


try:
	index = read_index() # from disk
except:
	index = fetch_index([])

# Evaluate the index

found = sorted([int(entry['number']) for entry in index])
missing = [i for i in range(1, max(found)+1) if (i not in found) and (i != 404)]

print('Found {:d} comics.'.format(len(found)))
if len(missing)>0:
	print('{:d} comics are missing:\n{}'.format(len(missing), missing))
else:
	print('You are up-to-date again!')

# Finally …
write_index(index)

