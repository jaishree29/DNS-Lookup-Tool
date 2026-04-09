# Notes

1. Downloaded the `q` tool from `github.com/natesales/q` to run subprocess and check the support for DoT, DoH and DoQ
2. Installed the following libraries:
    - `dnspython` : does DNS queries in Python
    - `httpx` : makes HTTP/HTTPS requests (for DoH)

3. `data.txt` file contains the list of IPs and hostnames

4. To test DoT:
     - Made a DNS query to ask the type 'A' record i.e. the IP address for `google.com`
     - `to_wire` converts the request into binary format i.e. bytes so that it can be sent
     - `struct.pack('!H', len(wire)) + wire` here is used because DNS over TLS has a rule which tells that the server should know how many bytes are present in the message before we send it. So this snippet takes the length of the message and converts it into a 2-byte prefix with the help of which the server can now understand where the message starts or ends.
        - In `!H` code, the `!` tells Python to use "Network Byte Order" which is the language of internet and ensures that different computers can understand the number the same way. Whereas `H` stands for "Unsigned Short" which is 2 bytes long i.e. 16 bits.
    - Setting up the secure tunnel from line 39 to 41 where `ssl.CERT_NONE` is used because as of now not caring about trusted servers but ones who are capable of DoT
    - For connection and handshake, `wrap_socket` is used which converts the naked TCP connection into an encrypted TLS connection
    - `tls.recv(1024)` is for receiving whatever data the server sends back and "1024" is the buffer size which tells Python to grab one at a time.

