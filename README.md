# snapchat ssl unpinning
this is a frida hook to bypass ssl pinning protection on the snapchat android app

this hook works by returning a copy of the certificates that are normally used by snapchat, tricking the app into thinking man in the middle attack is not taking place, and allows you to inspect the requests freely.

you might need to add some certificates in the checks as this was built on a old version (v12.40.0.43), you can use the commented out code to dump the cert chain, make sure a proxy is not set when you do so, else you will dump the debugging proxy cert along them.
