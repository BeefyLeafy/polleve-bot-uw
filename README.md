# polleve-bot

## Functionalities
- It can help you login (but you still need to verify by 2fa on duo).
- It only handles multiple choice questions by random choice, it can't handle free response questions.

## Prerequisites
- [THIS WEBFLOW IS ONLY APPLICABLE FOR UW STUDENTS] (otherwise you need to modify the login logic accordingly)
- Before running this script, please ensure that you have a webdriver located in your PATH.
  - You can use FireFox([download](https://www.mozilla.org/en-US/firefox/new/) it if you don't have it) & download gekodriver for Firefox [at their offical github repo](https://github.com/mozilla/geckodriver/releases).
  - Or use other browsers with their matching drives (do a google search)
- Python, [offical site for download](https://www.python.org/downloads/) or search for tutorials
- Do a git clone or download a zip of this repo.


## Installation
All instructions moving forward should be done in the project's directory.

To install the required dependencies, run:

    pip install -r requirements.txt

If you have don't want to mess up your global python environment, consider using virtualenv or conda or others with similar funcionalities. Do a search for tutorials for your operating system.

## Running

Running this script requires a file called credentials.txt. To create a credentials.txt file, run:

    python main.py

You will be prompted to enter information such as the name of the polleve, your student email, student password, and more.

Here's a brief summary of each attribute:

    poll name: the name of the polleve
    email: UW student email
    netid: UW student netid
    password: UW student password
    default timeout: the amount of time the script should wait before throwing an exception if no multiple choice is found (in sec)
    interval: the interval at which to check for a multiple choice (in sec)

## Please give a Star if it helped you. Thanks a lot!
(◍•ᴗ•◍)

## Thanks

Many thanks to this [repo](https://github.com/andrewschoi/polleve-bot) by [andrewschoi](https://github.com/andrewschoi)!
This repo is modified based on it.