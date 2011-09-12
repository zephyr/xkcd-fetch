
# xkcd-fetch
A simple script to download all [xkcd](https://www.xkcd.com/) comics *and* its metadata.

Usage:

	./xkcd-fetch.py
	grep python xkcd-db.csv
	eog image/0016_monty_python.jpg

To fetch new comics, just rerun the script:

	./xkcd-fetch.py

## Dependencies
Python 3 and [httplib2](https://code.google.com/p/httplib2/).

## Implementation status
*The good news*: currently it support all comics (*but* number 404 ;)).

*The bad news*: the script only downloads the *normal* images – special (that means larger oder additional) images are not (yet?) supported.

## Licence

This work is licensed under the ?.

**Please note** that all downloaded work from xkcd is instead under the [Creative Commons Attribution-NonCommercial 2.5 License](http://creativecommons.org/licenses/by-nc/2.5/)!

