# CrootBot

This repository houses the code behind the automated recruit data fetching for /u/CFBCrootBot from various recruiting services, at the current time only 247sports (247) and Rivals data are included. The hope is to include ESPN, Kohls, and others in the future. The scripts include both web scraping and web API calls depending on the recruiting website.

## Getting Started

### Prerequisites

This is a set of simple Python3 scripts, a .gitignore file, a config file, and a post log file. You must first have a reddit bot account set up and must create a test script. [See reddit's OAuth2 now-archived documentation for more information.](https://github.com/reddit-archive/reddit/wiki/OAuth2) The only non-standard Python3 package this uses is the PRAW (Python Reddit API Wrapper) package. PRAW's documentation can be found [here.](https://praw.readthedocs.io/en/latest/) PRAW can be quickly installed via

```
pip3 install praw
```

If you do not have pip3 installed, it can be installed via

```
python3 -m pip install --upgrade pip
```

If you do not have python3 installed, it can be downloaded and installed via the releases [here.](https://www.python.org/downloads/)

Once you have these set up, the only step left is to insert your reddit bot account's username, password, client ID, and client secret into config.py, copied from config_sample.py and copy .gitignore_sample into .gitignore.

### Running

Once you have done the prior setup, you can run your own CrootBot via

```
python3 crootbot.py
```

You can also run the individual Python scripts in a similar fashion. If you want your CrootBot to run on a schedule, create a crontab entry via

```
crontab -e
```

Insert a record such as

```
*/5 * * * * python3 /path/to/file/crootbot.py
```

and save. This example will run every five minutes. [Check out this resource for using crontab.](https://crontab.guru/)

## Authors

* **Cameron L. Williams** - *Initial work* - [SometimesY](https://github.com/SometimesY)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* The original [CrootBot](https://www.reddit.com/u/CrootBot) which has seemingly mostly been abandoned.

