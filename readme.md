<h1>SEO Research Assistant Project</h1>

This is my first independent project using Python. I 
created this program to demonstrate my ability to work 
with Python and express my interest in leveraging Python 
to create applications and software relevant to web 
development, digital marketing and Search Engine Optimization.

## Features
The program prompts the user to input a website URL and 
keywords of their choosing. Using the 'requests' module and 
BeautifulSoup, as well as general Python features, the 
program outputs the following data:
* Whether or not the URL is less than 60 characters long or 
not
* If the user-provided keywords are present or not in the 
URL.
* If the user-provided keywords are present or not on the 
  page and, if so, with how many times each keyword occurs.
* If various SEO stopwords are present in the URL or not.
* The number of broken (404) hyperlinks on the page, and 
a list of the broken links.
* An indication of the URL's page and domain authority.

The program also generates graphs of 'external pages to page'
 and 'external pages to root domain' metrics which are saved 
to a folder in the directory in which the application executable
 is located.

## Key Modules/Tech Used
* Python 3.8
* requests
* BeautifulSoup
* Matplotlib
* Tkinter
* Moz URL metrics API

## Installation Note
For the program to work fully as intended, you'll need to
 provide your own Moz API credentials as environment variables.
Your Moz ID should be a variable called `MOZ_ID` and your 
secret key should be a variable named `MOZ_SECRET`.

Without setting the above environment variables, the program
 will be unable to generate graphs on the 'external pages to page' 
and 'external pages to root domain' metrics.

## Credits
Created by me, Samuel Arnold-Parra.

Special thanks to the users of Stack Overflow and r/learnpython
 for helping me overcome some issues I faced during the 
development of this program.