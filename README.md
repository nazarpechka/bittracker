# bittracker
Cryptocurrency portfolio tracker

To install, create a virtualenv with django installed.
Then run `python manage.py init`
Also add to cron `python manage.py refresh_rates` and `python manage.py refresh_balances` to update user balances periodically. 
