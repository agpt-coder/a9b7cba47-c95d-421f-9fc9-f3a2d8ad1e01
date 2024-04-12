---
date: 2024-04-12T15:52:17.745153
author: AutoGPT <info@agpt.co>
---

# a

It appears there has been a consistent misunderstanding in our communication. The responses reveal a pattern where the nature of the assistance required was not clarified despite multiple attempts. The user consistently indicated a broad capability to provide support and assistance across a variety of tasks and topics, such as software development, technology guidance, and more. However, a specific query or task from the user's end was never articulated. In essence, the user communicated their readiness to offer detailed support in numerous areas, including but not limited to software application development, data analysis, web development, technology advice, and educational content, but did not specify a particular project or question that requires assistance. This cyclical communication underscores the importance of clear and precise queries when seeking assistance to ensure effective and targeted support.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'a'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
