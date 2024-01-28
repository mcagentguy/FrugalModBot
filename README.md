# FrugalModBot: Python Reddit Bot with PRAW

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Introduction

This is a Reddit bot powered by PRAW (Python Reddit API Wrapper). The bot performs mod actions on the /r/frugal subreddit, such as the following:

- removes image/link posts that don't contain a lengthy enough description
- removes posts with the Frugal Finds Friday flair when the current day is not Friday

## Dependencies

This bot runs on the following dependencies:

- Python 3.9.6
- PRAW library 7.7.1: https://praw.readthedocs.io/en/stable/

## Setup

For setup instructions, see PRAW's Quick Start documentation: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html

NOTE: You must create the credentials.py file within the directory of the app and populate it with the below two variables. (Or simply edit these variables directly within setup.py, but be careful not to share your secrets online)

CLIENT_SECRET = 'your_client_secret'
REDDIT_PASSWORD = 'your_reddit_account_password'

## Help

For help, consider the following:

- Create a post on https://www.reddit.com/r/redditdev/
- Contact the original author on reddit, /u/mcagent
