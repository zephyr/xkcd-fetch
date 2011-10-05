
# xkcd-fetch

A simple script to download all [xkcd](https://www.xkcd.com/) comics *and* theirs metadata.

## Dependencies

Python 3 and [httplib2](https://code.google.com/p/httplib2/).

## Usage

To download all xkcd comics into the subfolder `image/`, type

	$ ./xkcd-fetch.py

A renewed call will only fetch new comics.

The metadata of the comics (number/date/title/alt-text/filename) is stored into two different formats: `xkcd-db.csv` and `xkcd-db.json` – in the hope that you can use at least one of them ;).

To get the metadata for [xkcd 10](https://www.xkcd.com/10/):

	<xkcd-db.csv grep ^10,

To get the metadata for all comics from the first quarter of 2007:

	<xkcd-db.csv grep '2007-[1-3]-'

To get comics about python:

	<xkcd-db.csv grep python

To actually view [xkcd 10](https://www.xkcd.com/10/) (use the tab key for autocompletion after the `0016`!):

	eog image/0016_monty_python.jpg

## Implementation status

*The good news*: currently it supports all comics (*but* number 404 ;)).

*The bad news*: the script only downloads the *normal* images – special (that means larger oder additional) images are not (yet?) supported.

## Licence

Copyright 2011 by [Dennis Heidsiek](http://www.google.com/profiles/Dennis.Heidsiek)

This program is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/copyleft/gpl.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [here](http://www.gnu.org/licenses/).

**Please note** that the above only applies for this program! All downloaded *content from xkcd* is instead under the [Creative Commons Attribution-NonCommercial 2.5 License (CC/by-nc/2.5)](http://creativecommons.org/licenses/by-nc/2.5/)!

