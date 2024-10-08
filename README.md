# Copilot for Business

Welcome to Copilot for Business. This is a student run project at the University of Cambridge, in collaboration with Cambridge Kinetics. This project is part of the second year group project in the Computer Science Tripos. The project has been created by: Samuel Jie, Isaac Lam, Izzi Millar, Mmesoma Okoro, Leo Takashige and Ram Vinjamuri.

## What is this?

Copilot for Business is an app that allows users, regardless of technical skill, to query their databases in natural language for meaningful data and insights. For more details - and answers to some FAQs - please refer to [Help](https://copilot-for-business.streamlit.app/Help)!

## Run the project

The project is currently hosted at: [Copilot For Business](https://copilot-for-business.streamlit.app).
This utilises a personal OpenAI key (which costs money), so please be mindful in its use, and email `rt590@cam.ac.uk` if you would like to use the app after the key has expired.

## Installation

To install the project, you need to have Python 3.9 or later installed. You can download it from the [Python website](https://www.python.org/downloads/).

You can then clone the repository using ``git clone https://github.com/Ryuichi-Student/Copilot-For-Business.git``

Then you should create a virtual environment using ``python -m venv venv`` or using conda if you have it installed.

You can then activate the virtual environment using ``source venv/bin/activate`` on Linux or ``venv\Scripts\activate`` on Windows.

You can then install the dependencies using ``pip install -r requirements.txt``.

Create a .env file with the template of example.env (the key must be an OpenAI key with access to the GPT4 API).

You can then run the app using ``streamlit run src/frontend/Welcome.py``.

## Using the app

To use the app, after opening up localhost:port_number, you will be greeted with the welcome page. You can then navigate to the different pages using the sidebar on the left. To start you can either go to the dashboard to upload your database or go to the main page (copilot for business) in order to start using the app.
If you need help at any point, please consult the help page.

## Testing

If you would like to test the project, you first need to install tox using ``pip install tox``.

You can then run the tests using ``tox`` from the root directory..

## Future features

- Add user accounts so that different users have different sessions
- Migrate from streamlit to a more performant frontend technology.
