# find-udi-appointment
For people moving to Norway, we need an appointment with UDI. This script lets you find cancellations.

# Installation
```pip install -r requirements.txt```

# Config file format
The config file is a JSON file, with keys:

- *username* &mdash; Your UDI username 
- *password* &mdash; Likewise, your UDI password
- *wait_if_earlier_than* &mdash; An ISO formatted date, eg 2019-11-28. The script will pause if it finds an appointment before this.


It's convenient to put it in ```config.json```. Example:

```
{
    "username": "someone@somewhere.com",
    "password": "hunter2"
    "wait_if_earlier_than": "2019-02-03"
}
```

# Usage
You should make an initial appointment with UDI. Then set up the config file, as specified above. Run the script with:

```./UDIdriver.py config.json```

It will wait if it finds an appointment earlier than its configured ```wait_if_earlier_than``` date. Otherwise it will terminate. The last line of the script's output will be the ISO date of the earliest appointment that it could find.

If the script waits, you should choose the appointment that suits you best, and only close the Chromium session once you've made your rebooking.
