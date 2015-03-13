# Dependencies #

Installing this application is easy. Before you start, you need to fulfill a few dependencies:
  * Install Python 2.7.x. On my Mac I use macports, but to each his own.
  * Install [setuptools](http://pypi.python.org/pypi/setuptools/).
  * Install virtualenv. Again, I use macports for this.

Once that's in place, you're ready to install.

# Install Steps #

1. Clone the source code. Let's say you've done this and the code is now sitting in ./python-cmis-browser.

2. Set up a virtual environment. I use "env" in the ./python-cmis-browser directory, so the command would be:
```
cd ./python-cmis-browser
virtualenv env
```

3. Now activate your virtual environment:
```
source ./env/bin/activate
```

4. Install the application and its dependencies using setuptools, like this:
```
python setup.py develop
```

5. Edit development.ini. Change cmisbrowser.serviceUrl to match the AtomPub service URL for your repository. If you are going over the network to hit your repo and you don't want someone to know your repo credentials, I strongly suggest using HTTPS.

6. Set cmisbrowser.username and cmisbrowser.password to a valid user in your repository if your repository requires credentials. The app will authenticate as this user for all transactions.

7. Change the port you want the server to run on.

8. Launch the server:
```
pserve development.ini
```

That's it. Now you can get your CMIS on.