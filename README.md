I've provided one of my OpenAI API keys - use that though don't spam the API obviously.
If you want to use your own key, just replace the field in .env (but copy the original one down so as not to replace it!).

Use pipreqs --force ./ to generate requirements.txt after new install.

Use streamlit run src/frontend/Welcome.py to run the app or streamlit run src/frontend/development.py for testing.

To test we need to run tox:
First run: install all requirements_dev and requirements (pip install -r **name**)
Then run: pytest or tox from root directory

Testing convention:
All under test directory
Add appropriate tests before every push
