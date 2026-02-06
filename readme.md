## Course enrollment bot for Hochschulsport Uni Ulm
This project allows you to automatically enroll in a Hochschulsport course, specifically for Ulm University. It works by first manually logging in, saving the login state and then regularly checking if the courses have opened yet. If the selected course is available, the script instantly enrolls the logged in user.

## Getting started
This Bot is written for Linux. To set up the environment, you can run `setup.sh` once. Then you'll just have to run `main.py` from inside the venv, created by `setup.sh`. You can run this on windows aswell, you'll just have to replicate what `setup.sh` does (creating a venv, installing requirements.txt and installing chromium in playwright)

## Config
To select a course you want to enroll into, just take the name of the course and paste it into the `COURSE_NAME` variable inside `config.py`.

# This is for educational purposes only!