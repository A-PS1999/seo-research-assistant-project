SEO Research Assistant Project

WHY DID YOU MAKE THIS?
This is my first proper programming project. Before this, all the programming/coding work I had done was just exercises and examples from textbooks. I created this program to demonstrate my ability to work with Python and express my desire to leverage Python and my programming experience to create a program which would help someone engaging in digital marketing work. The program has this digital marketing focus because I'm interested in obtaining work in that area.

WHAT IS THIS PROGRAM?
This program prompts the user to input a website URL and the Search Engine Optimisation (SEO) keywords of their choosing. In a log window, part of the Graphical User Interface (GUI), relevant data on the URL and the keywords is then output. This data includes:
* the length of the URL
* the presence or absence of keywords in the URL or webpage
* the presence or absence of stopwords in the URL
* the presence of broken (404) links on the webpage
* information on the URL's page and domain authority

The program connects to Moz URL metrics API and creates a JSON file of backlinks data. It also creates graphs regarding the number of external pages to the root domain and external pages to the page, saving them to a folder named 'output_files' which is created in the same directory the exe is in upon running the program for the first time.

IMPORTANT USAGE/INSTALLATION NOTES:
* In order for the program to work as intended after you download it, you'll need to provide your own Moz API credentials in the form of environment variables on your PC. Your Moz ID must be an environment variable called 'MOZ_ID', while your secret key must be under a variable called 'MOZ_SECRET'.
* This is required for the program to access the Moz API so that it can analyse the URL metrics for the URL you provide it. 

CREDITS
Created by me, Samuel Arnold-Parra
Special thanks to the users of Stack Overflow and r/learnpython for helping me overcome various obstacles I faced in the creation of this program