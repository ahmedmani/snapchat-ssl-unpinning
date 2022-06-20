# snapchat ssl unpinning
this was tested on a old version of snapchat it removes ssl pinning by faking the public keys used and returning the keys snapchat expects another way to do this would be to reverse the shared object library responsible of the key pinning and simply patching it with the mitm proxy keys 
