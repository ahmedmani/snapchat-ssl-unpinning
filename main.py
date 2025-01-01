import frida, json, os



def on_message(message, data):
    global certs, script, mode
    if message["type"] == "send":
        if message["payload"]["action"] == "init":
            script.post({"type":"send", "mode": mode})

        elif message["payload"]["action"] == "save":
            new_cert = message["payload"]
            old_cert = [cert for cert in certs if cert["hostname"] == new_cert["hostname"]]
            if not old_cert:
                print(f"new cert found for hostname {new_cert['hostname']}")
                del message["payload"]["action"]
                certs.append(message["payload"])
            else:
                print(f"certificates received are already saved for host {new_cert['hostname']}")
                        
        elif message["payload"]["action"] == "fetch":
            _certs = next((cert for cert in certs if cert["hostname"] == message["payload"]["hostname"]), None)
            if not _certs:
                print(f"host {message['payload']['hostname']} certificates have not been saved, requests will fail to this url.")
            else:
                _certs = _certs["certs"]
                print("returning certs for host " + message["payload"]["hostname"])
            script.post({"type": "send", "hostname": message["payload"]["hostname"], "certs": _certs})
        else:
            print(f"unknown action for {message['payload']['action']}")


print("""snapchat ssl pinning bypass
enter mode of operation:
    0- record certs
    1- unpin requests""")
mode = -1
while mode not in [0, 1]:
    try:
        print("mode must be either 0 or 1")
        mode = int(input())
    except:
        print("error mode must a number")
        
certs = []
certs_path = "\\".join(__file__.split("\\")[:-1]) + "\\certs.json"

if not os.path.exists(certs_path) and mode == 1:
    print("no certificates were found, run record mode first")
    exit(0)

if os.path.exists(certs_path) and mode == 0:
    input("certificates file is gonna be overwritten (hit any key to confirm)")

if os.path.exists(certs_path):
    print("saved certificates found.")
    with open(certs_path, "r") as fp:
        try:
            certs = json.loads(fp.read())
        except Exception as ex:
            print("error loading saved certificates.")
            certs = []

device = frida.get_usb_device()
pid = device.spawn(["com.snapchat.android"])
session = device.attach(pid)
script = session.create_script(open("ssl_unpinning.js").read())
script.on("message", on_message)
script.load()
device.resume(pid)

if mode == 0:
    input("Press Enter to exit and save certificates...\n")
    with open(certs_path, "w+", encoding="utf-8") as fp:
        fp.write(json.dumps(certs))
elif mode == 1:
    input("Press Enter to exit...\n")

