#!/usr/bin/env python3

import html.parser, json, os, re
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


if not os.path.exists('image'):
	os.mkdir('image')

archive = fetch_text('https://www.xkcd.com/archive/')

archive_pattern = r'<a href="/(\d+)/" title="(\d{4}-\d{1,2}-\d{1,2})">(.*?)</a>'

page_pattern = r'<img src="http://imgs.xkcd.com/comics/(.*?)" title="(.*?)" alt="(.*?)" /><br/>'


index = []
for a in re.finditer(archive_pattern, archive):
	entry = dict()
	entry['number']= a.group(1) # 886
	entry['date']= a.group(2)   # 2011-4-15
	entry['title']= a.group(3)  # Craigslist Apartments
	print(entry)
	
	page = fetch_text('https://www.xkcd.com/'+a.group(1)+'/')
	
	for p in re.finditer(page_pattern, page):
		
		entry['file'] = p.group(1)                  # craigslist_apartments.png
		entry['desc'] = html_unescape(p.group(2))   # $1600 / 1386153BR 3BATH, …
		#entry['title'] = p.group(3)                # Craigslist Apartments
		
		o = 'image/{:04d}_{}'.format(int(entry['number']), entry['file'])
		
		for e in entry:
			print('{:10s} = {}'.format(e, entry[e]))
		print('Filename:', o)
		
		index.append(entry)
		
		image = open(o, 'wb')
		image.write(fetch('http://imgs.xkcd.com/comics/'+entry['file']))
		image.close()
		
		

print(index)
f = open('image/index.json', 'w')
f.write(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2))
f.close()

