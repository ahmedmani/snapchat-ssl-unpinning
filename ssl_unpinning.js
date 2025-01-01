


var mode;
send({"action": "init"})
recv('send', function (message) {
    mode = message.mode
}).wait();

if (mode == 0){
    Java.perform(function (){
        Java.use("android.net.http.X509TrustManagerExtensions").checkServerTrusted.overload('[Ljava.security.cert.X509Certificate;', 'java.lang.String', 'java.lang.String').implementation = function(a, b, c){
            var arr = [];
            for (var i = 0; i<a.length; i++){
                arr.push(a[i].getEncoded())
            }
            send({"hostname": c, "action": "save", "certs": arr})
            return this.checkServerTrusted(a, b, c)
        }
    })
}else if (mode == 1){
    Java.perform(function (){
        Java.use("android.net.http.X509TrustManagerExtensions").checkServerTrusted.overload('[Ljava.security.cert.X509Certificate;', 'java.lang.String', 'java.lang.String').implementation = function(a, b, c){
            try{
                var BufferedInputStream = Java.use("java.io.BufferedInputStream");
                var ByteArrayInputStream = Java.use("java.io.ByteArrayInputStream") ;
                
                send({"hostname": c, "action": "fetch"})
                var arr;
                recv('send', function (message) {
                    arr = message.certs
                }).wait();

                var cf = Java.use("java.security.cert.CertificateFactory").getInstance("X.509")
                var cert_array = []

                for (var i = 0; i < arr.length; i++) {
                    var cert_bytes = Java.array('byte', arr[i]);
                    var certificate = cf.generateCertificate(BufferedInputStream.$new(ByteArrayInputStream.$new(cert_bytes)));
                    cert_array[i] = Java.cast(certificate, Java.use("java.security.cert.X509Certificate"));
                }
                var _cert_array = Java.array('java.security.cert.X509Certificate',  cert_array);

                return this.checkServerTrusted(_cert_array, b, c)
            }catch(err){
                console.log(err)
            }
        }

    })
}
