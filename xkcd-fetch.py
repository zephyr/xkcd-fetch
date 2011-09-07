#!/usr/bin/env python3


import re, httplib2

http = httplib2.Http(".cache")

def fetch(url):
	response, content = http.request(url, 'GET')
	return content

def fetch_text(url):
	return fetch(url).decode('utf-8')

archive = fetch_text('https://www.xkcd.com/archive/')
pattern = r'href="/(\d+)/" title="(.*?)">(.*?)</a>'
img_pattern = r'<img src="http://imgs.xkcd.com/comics/(.*?)" title="(.*?)" alt="(.*?)" /><br/>'

for m in re.finditer(pattern, archive):
	print(m.groups())
	
	page = fetch_text('https://www.xkcd.com/'+m.group(1)+'/')
	for c in re.finditer(img_pattern, page):
		#print(c.groups())
		o = "image/{:04d} {}".format(int(m.group(1)), c.group(1))

		file = open(o, "wb")
		file.write(fetch("http://imgs.xkcd.com/comics/"+c.group(1)))
		file.close()

