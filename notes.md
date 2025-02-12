python3 -m venv env
source env/bin/activate

# To install WSL2 chrome driver first needs to get the stable version and then install it
# Do not forget CHOWN all the dir to can execute chromedriver and make changes

> wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
> sudo apt install ./google-chrome-stable_current_amd64.deb
