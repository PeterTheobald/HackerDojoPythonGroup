Hacker Dojo Python - Rest API

Design prompt:

Design a REST API for an online discussion board similar to Reddit or Discord. The discussion board is divided into topics. Each topic has comments.
Users should be able to register, login, logout, list topics, create new topics, read comments in a topic, post new comments in a topic.

Note: Things we are skipping:
- no rate limiting,
- no 'forgot password' flows or email verification flows,
- no comment editing or deleting,
- no username password or email editing
- no search feature

Backend design prompt:

Write a Python FastAPI server to implement the following REST API. Use a SQLite file database.

## Front-end design prompt:

I have a Python FASTAPI Rest-API that implements a server for a discussion board similar to Reddit and Discord. Create a front-end for this discussion board. Use HTLM, CSS and Javascript. The user can register, login and logout. On the left side is a list of topics. On the right side is a list of comments for the selected topic. The user can select a topic, create a new topic, read comments, post a new comment.
The REST-API spec is as follows:

Discussion Board REST API Specification
...

