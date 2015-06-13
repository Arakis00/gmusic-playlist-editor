gmusic-playlist-editor
=========================
This is a simple `Google music <http://music.google.com>`__ playlist creation & editing tool coded in Python.

It makes use of the following API: `https://github.com/simon-weber/Unofficial-Google-Music-API`

Notes
--------------------------
To install the API mentioned above: ``$ pip install gmusicapi``.

In order to be able to login to your Google music account, it requires enabling `Access for less secure apps <https://support.google.com/accounts/answer/6010255?hl=en>`__ within your account settings.

Login information(email/password) is hardcoded into the musicFunctions.py file currently.  You have to change this to your own account information in order to login.  This is really just something for personal use on my HTPC, so I've not bothered adding an actual login dialogue.
