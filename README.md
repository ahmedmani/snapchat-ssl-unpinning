this is a python frida script to bypass certificate pinning on the snapchat android app

this script works by saving the certificates that are returned from snapchat servers and replaying them when the app traffic is passing through a debug proxy such as (mitmproxy, burpsuite etc...), tricking the app into thinking man in the middle attack is not taking place, and allows you to inspect the requests freely.

## usage

```
  python main.py
```
first make sure no proxy is set and frida is running on your device/emulator, run the script with "record" mode, use the app noramlly once you stop seeing new domains being saved, press any key to save the certificates in the "certs.json" file as a java byte array.

once certificates are saved, set a debug proxy on your device and run the script in "unpin" mode, you should see snapchat http requests popping up.

Note: if the certificates of a domain are not saved, requests going to that url will not go through.
