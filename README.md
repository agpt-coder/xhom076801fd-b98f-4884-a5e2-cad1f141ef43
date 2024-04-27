---
date: 2024-04-27T19:31:36.675313
author: AutoGPT <info@agpt.co>
---

# xhom

Our Smart Home Central Control Dashboard is designed using the Flask web framework as its core with Python. It utilizes an application entry point named `app.py` that sets up Flask and incorporates routes from `routes.py` for mapping URL paths such as `/dashboard` for the main control panel access and `/devices/{id}/control` for specific device operations. The `dashboard_controller.py` is responsible for retrieving information about all connected devices from `device_model.py`, which interacts with MongoDB through an ORM-like mechanism allowing for flexible database interactions. Device commands and operations are managed via `device_control.py`, communicating with smart devices using a universal API adapter. The device and user settings, including automated routine scripts, are maintained in MongoDB through `device_model.py`, facilitating dynamic schema modifications. The frontend is powered by Vue.js, offering a reactive and component-based structure, enriched with Vuex for state management and Vue Router for single-page application (SPA) features. AJAX calls are implemented within Vue components to provide a seamless user experience with real-time feedback. Additionally, voice command features are incorporated through `voice_handlers.py`, leveraging voice assistant APIs like those from Google Assistant or Amazon Alexa to convert spoken commands into dashboard actions. This configuration not only streamlines home automation management for users but also lays down a strong, scalable foundation for further advancements and integrations within the Internet of Things (IoT) ecosystem.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'xhom'

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
