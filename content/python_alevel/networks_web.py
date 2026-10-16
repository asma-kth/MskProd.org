"""A Level Python: protocols, addressing, reliable delivery and the web."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="networks-and-the-web",
    title="Networks and the Web in Python",
    spec="A Level 22",
    icon="i-network",
    minutes=70,
    blurb="The internet as a set of rules you can program. Wrap a message in the protocol layers, do subnet arithmetic with bitwise operators, build a reliable channel over one that loses packets, write a web server that speaks HTTP and JSON, and then use real sockets and a framework on your own machine.",
    fact="The first message sent over ARPANET in 1969 was meant to be the word LOGIN. The receiving computer crashed after the first two letters, so the first message ever sent over the network that became the internet was 'LO'.",
    sections=[
        Section("Protocols, layers and packets", r"""
Two computers can only talk if they agree on the rules. Those rules are **protocols**. Since no single protocol could do everything, networks use a stack of them in **layers**, each doing one job and relying on the layer below. The internet uses the **TCP/IP model**, with four layers:

| Layer | Job | Examples |
| **Application** | the service the user wants | HTTP, HTTPS, SMTP, IMAP, FTP, DNS |
| **Transport** | breaks the data into pieces, and delivers them to the right program (the **port**) reliably or not | TCP, UDP |
| **Internet** | addresses and **routing** across networks | IP |
| **Link** | sends bits over one physical connection | Ethernet, Wi-Fi |

As data goes down the stack at the sender, each layer wraps it with its own **header**. This is **encapsulation**. At the receiver each layer strips the header off the front and passes the rest up.

```python
def application(data):
    return "GET /index.html | " + data

def transport(segment, src_port, dst_port, seq):
    return "TCP %d>%d seq=%d | " % (src_port, dst_port, seq) + segment

def internet(packet, src_ip, dst_ip):
    return "IP %s>%s ttl=64 | " % (src_ip, dst_ip) + packet

def link(frame, src_mac, dst_mac):
    return "ETH %s>%s | " % (src_mac, dst_mac) + frame

# going down the stack at the sender
message = application("Host: example.org")
segment = transport(message, 50312, 80, 1)
packet = internet(segment, "192.168.1.20", "203.0.113.7")
frame = link(packet, "aa:01", "bb:02")
print(frame)
print()

# going up the stack at the receiver
for layer in ("link", "internet", "transport", "application"):
    header, _, frame = frame.partition(" | ")
    print("the", layer, "layer reads:", header)
print("the program receives:", frame)
```

### Packet switching

A large message is not sent as one block. It is cut into **packets**, each with a header holding the source and destination **IP addresses**, a **sequence number** and a **checksum**. Each packet is passed on by **routers**, which look only at the destination and choose the next hop. Different packets of the same message may take different routes, and arrive in a different order.

```python
import random

message = "Packets can arrive out of order, so every one carries a sequence number."
size = 14
packets = [{"seq": n, "data": message[i:i + size]} for n, i in enumerate(range(0, len(message), size))]

arrived = list(packets)
random.Random(3).shuffle(arrived)                       # the network scrambles them
print("arrival order:", [p["seq"] for p in arrived])

rebuilt = "".join(p["data"] for p in sorted(arrived, key=lambda p: p["seq"]))
print(rebuilt == message)
```

The receiver puts the packets back in order using the sequence numbers. Compare it with **circuit switching**, as in an old telephone call, where a fixed path is reserved for the whole conversation, whether or not anyone is talking. Packet switching shares the links far more efficiently, and copes when a link fails.

### The domain name system

People use names such as `www.example.org`. Routers need IP addresses. **DNS** is a distributed directory that translates one into the other, by asking a chain of servers, each one knowing where to ask next:

```python
servers = {
    "root": {"org": "the .org server"},
    "the .org server": {"example.org": "the example.org name server"},
    "the example.org name server": {"www.example.org": "203.0.113.7"},
}

def resolve(name):
    server = "root"
    while True:
        answers = servers[server]
        match = next(key for key in answers if name == key or name.endswith("." + key))
        reply = answers[match]
        print(server, "says:", match, "->", reply)
        if reply[0].isdigit():
            return reply
        server = reply

print("address:", resolve("www.example.org"))
```

Real resolvers **cache** answers, so most lookups never leave your router or your internet provider.
"""),
        Section("IP addresses and subnets", r"""
An **IPv4 address** is a 32 bit number, written as four decimal bytes: `192.168.5.130`. Every address has two parts: a **network** part that identifies the network, and a **host** part that identifies the device within it. A **subnet mask** says where the split is: the 1 bits mark the network part and the 0 bits the host part.

Two devices are on the **same subnet** if the network parts of their addresses match. If they are, they talk directly. If not, the traffic must go through a **router**. The network part is found by a bitwise **AND** of the address with the mask, which is the bitwise logic from the earlier topic put to work.

```python
def to_int(dotted):
    a, b, c, d = (int(part) for part in dotted.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d

def to_dotted(number):
    return ".".join(str((number >> shift) & 255) for shift in (24, 16, 8, 0))

ip = to_int("192.168.5.130")
mask = to_int("255.255.255.192")             # also written /26: 26 one bits

network = ip & mask                           # keep only the network part
broadcast = network | (~mask & 0xFFFFFFFF)    # set every host bit to 1
host_bits = 32 - bin(mask).count("1")

print(bin(ip)[2:].zfill(32), "address")
print(bin(mask)[2:].zfill(32), "mask")
print(bin(network)[2:].zfill(32), "address AND mask")
print()
print("network address:  ", to_dotted(network))
print("broadcast address:", to_dotted(broadcast))
print("host bits:", host_bits, "-> usable hosts:", 2 ** host_bits - 2)

def same_network(a, b):
    return to_int(a) & mask == to_int(b) & mask

print(same_network("192.168.5.130", "192.168.5.140"))
print(same_network("192.168.5.130", "192.168.5.20"))
```

The first address of the range is the **network address** and the last is the **broadcast address**. Neither can be given to a device, so a subnet with `h` host bits has `2^h - 2` usable addresses.

A mask can be written in **CIDR** notation as the number of 1 bits: `255.255.255.192` is `/26`. Python's `ipaddress` module does all of this for you, and can split a network into smaller subnets:

```python
import ipaddress

network = ipaddress.ip_network("192.168.5.130/26", strict=False)
print(network, network.netmask, network.broadcast_address, network.num_addresses - 2)
print()

for subnet in ipaddress.ip_network("192.168.5.0/24").subnets(new_prefix=26):
    hosts = list(subnet.hosts())
    print(subnet, "hosts", hosts[0], "to", hosts[-1])

print()
print(ipaddress.ip_address("10.4.3.2").is_private, ipaddress.ip_address("8.8.8.8").is_private)
```

Some ranges are **private**: `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`. They are not routed on the internet, so any home can reuse them. Your router uses **network address translation** (NAT) to share its one public address between all the devices behind it.

There are only about 4.3 billion IPv4 addresses, which have run out. **IPv6** uses **128 bits**, written in hexadecimal, giving more addresses than there are grains of sand on Earth, and removes the need for NAT.
"""),
        Section("Reliable delivery over an unreliable network", r"""
The internet makes no promises. A router with a full queue simply drops packets, and wires and radio links corrupt bits. Yet when you download a file it arrives intact. The transport layer protocol **TCP** builds a reliable service on top of the unreliable one by:

- numbering every packet with a **sequence number**, so they can be put in order
- adding a **checksum**, so damaged packets can be detected and discarded
- having the receiver send an **acknowledgement** (ACK) for each packet it gets
- having the sender **resend** any packet that is not acknowledged before a **timeout**

The simplest scheme is **stop and wait**: send one packet, wait for its ACK, then send the next. This simulation uses a channel that, on set transmissions, loses a packet or damages it. A checksum catches the damage:

```python
def checksum(data):
    return sum(data.encode()) % 256

def make_channel(plan):
    count = [0]
    def channel(packet):
        count[0] += 1
        fate = plan.get(count[0])
        if fate == "lost":
            return None
        if fate == "damaged":
            seq, data, check = packet
            return (seq, "X" + data[1:], check)
        return packet
    return channel, count

def send_all(words, channel):
    delivered = []
    for seq, data in enumerate(words):
        packet = (seq, data, checksum(data))
        while True:
            print("send", seq, data)
            got = channel(packet)
            if got is None:
                print("   no ACK before the timeout: send again")
            elif checksum(got[1]) != got[2]:
                print("   arrived damaged: checksum does not match, discard it")
            else:
                print("   ACK", seq)
                delivered.append(got[1])
                break
    return delivered

channel, count = make_channel({2: "lost", 4: "damaged", 6: "lost"})
delivered = send_all(["one", "two", "three", "four"], channel)
print(delivered)
print(count[0], "transmissions to deliver", len(delivered), "packets")
```

Everything arrived, in order, at the cost of three extra transmissions. The price of reliability is time. Stop and wait spends most of its time waiting. **TCP** instead uses a **sliding window**: the sender may have several packets in flight at once, and keeps going as the ACKs return.

```python
import math

packets = 100
for window in (1, 4, 16):
    print("window of", window, "->", math.ceil(packets / window), "round trips")
```

### TCP or UDP?

| | TCP | UDP |
| Connection | set up first (the three way handshake) | none |
| Delivery | guaranteed and in order | no guarantee, any order |
| Speed | slower: acknowledgements, resending | faster: no overhead |
| Used for | web pages, email, file transfer | live video, online games, voice calls, DNS lookups |

A late packet in a live game is worthless. It is better to skip it than to stop and wait for it, so games choose UDP.
"""),
        Section("The web: URLs, HTTP and JSON", r"""
The **web** is a service that runs on the internet. A **URL** points at a resource and has several parts, which `urllib.parse` splits apart:

```python
from urllib.parse import urlparse, parse_qs

url = "https://shop.example.org:8443/products/shoes?colour=red&size=7#reviews"
parts = urlparse(url)
print("scheme:  ", parts.scheme)
print("host:    ", parts.hostname)
print("port:    ", parts.port)
print("path:    ", parts.path)
print("query:   ", parse_qs(parts.query))
print("fragment:", parts.fragment)
```

### HTTP: just text

When your browser asks for a page it sends an **HTTP request**: a request line (the **method**, the path and the version), some **headers**, a blank line, and an optional **body**. The server answers with an **HTTP response**: a status line, headers, a blank line and the body. Nothing more than text.

| Method | Meaning |
| GET | retrieve a resource |
| POST | send data to be processed, such as a form or a new record |
| PUT | replace a resource |
| DELETE | remove a resource |

The **status code** says how it went:

| Code | Meaning |
| 2xx | success: 200 OK, 201 Created |
| 3xx | redirection: 301 Moved Permanently |
| 4xx | the **client** made a mistake: 400 Bad Request, 403 Forbidden, 404 Not Found |
| 5xx | the **server** failed: 500 Internal Server Error |

The body of a modern web service is often **JSON**, a text format for structured data that looks like Python dictionaries and lists. This server is built the way real ones are, with a **routing table** that maps a method and a path to a function, and it runs entirely in memory so you can try it here:

```python
import json

scores = [{"name": "Ana", "score": 120}, {"name": "Raj", "score": 95}]

def home(request):
    return 200, "text/html", "<h1>Leaderboard</h1>"

def list_scores(request):
    return 200, "application/json", json.dumps(scores)

def add_score(request):
    try:
        entry = json.loads(request["body"])
        entry = {"name": str(entry["name"]), "score": int(entry["score"])}
    except (ValueError, KeyError, TypeError):
        return 400, "application/json", json.dumps({"error": "send a name and a score"})
    scores.append(entry)
    return 201, "application/json", json.dumps(entry)

ROUTES = {("GET", "/"): home, ("GET", "/api/scores"): list_scores, ("POST", "/api/scores"): add_score}
REASONS = {200: "OK", 201: "Created", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed"}

def parse_request(text):
    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, path, version = lines[0].split(" ")
    headers = dict(line.split(": ", 1) for line in lines[1:])
    return {"method": method, "path": path, "headers": headers, "body": body}

def serve(raw):
    request = parse_request(raw)
    handler = ROUTES.get((request["method"], request["path"]))
    if handler is not None:
        status, kind, body = handler(request)
    elif any(path == request["path"] for method, path in ROUTES):
        status, kind, body = 405, "text/plain", "That method is not allowed here"
    else:
        status, kind, body = 404, "text/plain", "Nothing at " + request["path"]
    return ("HTTP/1.1 " + str(status) + " " + REASONS[status] + "\r\n"
            "Content-Type: " + kind + "\r\n"
            "Content-Length: " + str(len(body)) + "\r\n\r\n" + body)

def ask(method, path, body=""):
    lines = [method + " " + path + " HTTP/1.1", "Host: scores.example.org"]
    if body:
        lines += ["Content-Type: application/json", "Content-Length: " + str(len(body))]
    reply = serve("\r\n".join(lines) + "\r\n\r\n" + body)
    status_line, _, rest = reply.partition("\r\n")
    print(method, path, "->", status_line, "|", rest.split("\r\n\r\n")[1])

ask("GET", "/")
ask("GET", "/api/scores")
ask("POST", "/api/scores", '{"name": "Mia", "score": 150}')
ask("POST", "/api/scores", "not json")
ask("GET", "/api/scores")
ask("GET", "/nothing")
ask("DELETE", "/api/scores")
```

Designing a service where each **URL names a thing** and the **method says what to do with it** is called **REST**. `GET /api/scores` reads the list, `POST /api/scores` adds to it. It is also **stateless**: every request carries all the information the server needs.

### Cookies and sessions

Because HTTP is stateless, the server needs another way to know that two requests came from the same person. At login it creates a long random **session identifier**, stores who it belongs to, and sends it in a **cookie**. The browser returns the cookie with every request.

```python
import secrets

sessions = {}

def log_in(user):
    token = secrets.token_hex(8)                  # long and unpredictable
    sessions[token] = user
    return "Set-Cookie: session=" + token

header = log_in("amy")
token = header.split("=")[1]
print("token length:", len(token))
print("who is that?", sessions.get(token))
print("a guessed token:", sessions.get("0123456789abcdef"))
```

### Client-side or server-side?

| | Client-side | Server-side |
| Runs | in the browser (JavaScript) | on the web server (Python, PHP, and others) |
| Good for | instant checks, animations, menus | databases, passwords, anything private |
| Trustworthy? | **No**: the user can change it | **Yes**: the user cannot see or edit it |
| Load | on the user's device | on the server |

Always check input on the server as well. A client-side check is a convenience for the user, never a security measure.
"""),
        Section("Sockets and servers on your own computer", r"""
A browser tab cannot open raw network connections or run a server, so the programs in this section need your own computer. Save each one as a file and run them in separate terminals.

A **socket** is one end of a connection, made of an IP address and a port. A **port** is a number that picks the program on that computer: 80 for HTTP, 443 for HTTPS, 25 for sending email, 53 for DNS. Run the **server** first, so that it is listening:

```pylocal
# server.py: turns whatever it is sent into upper case
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:     # TCP
    server.bind(("127.0.0.1", 5000))        # this computer, port 5000
    server.listen()
    print("waiting for a client...")
    connection, address = server.accept()
    with connection:
        print("connected to", address)
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.sendall(data.upper())
```

Then run the **client**:

```pylocal
# client.py
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 5000))
    client.sendall(b"hello server")
    print(client.recv(1024))                 # b'HELLO SERVER'
```

Python's library can speak HTTP for you. This is a complete web service, which answers requests for `/api/hello` with JSON:

```pylocal
# web.py
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/hello":
            body = json.dumps({"message": "hello from Python"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

While it runs, a second program can call it as any client would, and decode the JSON:

```pylocal
# call.py
import json
from urllib.request import urlopen

with urlopen("http://127.0.0.1:8000/api/hello") as response:
    print(response.status)
    print(json.load(response))
```

Writing a server like that by hand does not scale. A **web framework** handles the routing and the HTTP details for you. **Flask** is the most popular small one. Install it, then run the program:

```text
pip install flask
python app.py
curl http://127.0.0.1:5000/api/scores
```

```pylocal
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)
scores = [{"name": "Ana", "score": 120}]

@app.get("/api/scores")
def list_scores():
    return jsonify(scores)

@app.post("/api/scores")
def add_score():
    entry = request.get_json()
    scores.append(entry)
    return jsonify(entry), 201

if __name__ == "__main__":
    app.run(debug=True)
```

It is the same routing table you wrote above, using decorators to build it. You will meet decorators in the advanced topics.

!warn Never trust the client :: Anything arriving over a network could have been written by an attacker. Check the type, the range and the length of every value, build database queries with parameters and never by joining strings, and use HTTPS so the conversation cannot be read or changed on the way.
"""),
    ],
    keyterms=[
        ("Protocol", "A set of rules that two devices follow to communicate."),
        ("TCP/IP model", "A layered model of the internet: application, transport, internet and link layers."),
        ("Encapsulation", "Adding a header at each layer as data goes down the stack, and removing it at each layer on the way up."),
        ("Packet switching", "Splitting data into packets that are routed independently and reassembled at the destination."),
        ("Router", "A device that forwards packets between networks using the destination IP address."),
        ("Subnet mask", "A pattern of bits that separates the network part of an IP address from the host part."),
        ("DNS", "The Domain Name System, which translates domain names into IP addresses."),
        ("TCP", "A transport protocol giving reliable, ordered delivery using sequence numbers, acknowledgements and retransmission."),
        ("UDP", "A transport protocol with no guarantee of delivery or order, but low delay."),
        ("HTTP", "The protocol of the web, in which a client sends a request and a server sends a response."),
        ("JSON", "A text format for structured data using objects and arrays."),
        ("REST", "A style of web service in which URLs identify resources and HTTP methods say what to do with them."),
        ("Socket", "One end of a network connection, identified by an IP address and a port."),
    ],
    grade="""
Networking answers need the vocabulary used precisely, and a sense of what each layer or protocol is for.

+ For packet switching, name the header contents: addresses, sequence number, checksum, and say that routes can differ
+ For reliability, give all four: sequence numbers, acknowledgements, timeouts and retransmission
+ Show subnet working: write the mask and the address in binary, AND them, then count the host bits
+ For HTTP, state the method and the status code family, not just 'it sends a request'
+ Say why a server-side check is needed even when the browser has already checked
""",
    mistakes=[
        "Saying the internet and the web are the same. The web is one service that runs on the internet.",
        "Forgetting to subtract two from 2^h when counting usable hosts in a subnet.",
        "Describing TCP as faster than UDP. TCP is more reliable; UDP is faster.",
        "Treating a 404 as a server fault. It is a client error: the address does not exist.",
        "Relying on client-side validation alone for anything that matters.",
    ],
    quiz=[
        Q("What is encapsulation in the TCP/IP model?",
          ["Each layer adds its own header to the data as it goes down the stack", "Compressing data before sending it", "Encrypting data so it cannot be read", "Joining two networks together"], 0,
          "The data is wrapped in a header by the transport, internet and link layers in turn, and the receiver unwraps them."),
        Q("Why does each packet have a sequence number?",
          ["Packets can arrive out of order, so the receiver can put them back", "To show how important the packet is", "To encrypt the packet", "To tell routers which network to use"], 0,
          "Different packets may take different routes and arrive in a different order."),
        Q("What does a router use to decide where to send a packet?",
          ["The destination IP address", "The source MAC address", "The sequence number", "The packet's checksum"], 0,
          "Routers look at the destination address and forward the packet to the next hop towards it."),
        Q("The address 192.168.5.130 has a subnet mask of 255.255.255.192. What is its network address?",
          ["192.168.5.128", "192.168.5.130", "192.168.5.192", "192.168.5.0"], 0,
          "130 AND 192 = 128, because 130 is 10000010 in binary and 192 is 11000000."),
        Q("How many usable host addresses are there in a /24 network?",
          ["254", "256", "255", "24"], 0,
          "There are 8 host bits, so 2^8 = 256 addresses, minus the network and broadcast addresses."),
        Q("What does DNS do?",
          ["Translates a domain name into an IP address", "Encrypts web traffic", "Assigns IP addresses to devices", "Blocks unwanted traffic"], 0,
          "People use names, but routers need numbers, so DNS looks one up from the other."),
        Q("Which of these makes TCP reliable?",
          ["Acknowledgements and retransmission of lost packets", "Sending every packet twice", "Using a larger packet size", "Encrypting every packet"], 0,
          "A packet that is not acknowledged before the timeout is sent again."),
        Q("Why do online games usually use UDP rather than TCP?",
          ["A late packet is useless, so speed matters more than guaranteed delivery", "UDP is more secure", "TCP cannot carry game data", "UDP guarantees the order of packets"], 0,
          "Waiting for an old packet would stall the game, so it is better to carry on without it."),
        Q("A browser requests a page that does not exist. Which status code comes back?",
          ["404", "200", "301", "500"], 0,
          "404 Not Found is a client error: the address does not match anything on the server."),
        Q("Why should input be validated on the server as well as in the browser?",
          ["Client-side checks can be bypassed by the user", "Servers can validate faster", "Browsers cannot validate text", "It is required by HTTP"], 0,
          "Anyone can change the code in their browser or send requests directly, so only the server's checks can be trusted."),
    ],
    exam=[
        EQ("Describe how a large file is sent across the internet using packet switching.", 4, [
            MP("The file is split into packets", ["split", "divided", "broken", "packets"]),
            MP("Each packet has a header with the source and destination addresses and a sequence number", ["header", "address", "sequence number", "destination"]),
            MP("Routers pass each packet on separately, so packets can take different routes", ["router", "different routes", "different paths", "separately", "independently"]),
            MP("At the destination the packets are put back in order using the sequence numbers, and missing ones are requested again", ["reassembled", "put back", "order", "sequence number", "resend", "requested again", "rebuilt"]),
        ], "The file is split into small packets. Each packet has a header containing the source and destination IP addresses and a sequence number. Routers pass each packet on separately, choosing the next step towards the destination, so the packets of the same file can take different routes and arrive in a different order. At the destination the packets are put back in the correct order using their sequence numbers, and any that are missing or damaged are requested again.",
           command="Describe"),
        EQ("A computer has the IP address 192.168.5.130 and the subnet mask 255.255.255.192. Calculate the network address, and the number of usable host addresses on this subnet. Show your working.", 4, [
            MP("Writes the last byte in binary: 130 = 10000010 and 192 = 11000000", ["10000010", "11000000"]),
            MP("ANDs the address with the mask to give 10000000, which is 128, so the network address is 192.168.5.128", ["128", "192.168.5.128", "and"]),
            MP("The mask has 6 zeros, so there are 6 host bits", ["6 host bits", "six", "6 zeros", "6 bits", "26"]),
            MP("2^6 = 64 addresses, less the network and broadcast addresses gives 62 usable hosts", ["62", "64"]),
        ], "In binary the last byte of the address is 130 = 10000010 and of the mask is 192 = 11000000. ANDing them gives 10000000, which is 128, so the network address is 192.168.5.128. The mask has 26 ones, which leaves 6 bits for the host part. That gives 2^6 = 64 addresses, and since the first (the network address) and the last (the broadcast address) cannot be used by devices there are 62 usable host addresses.",
           command="Calculate"),
        EQ("Explain how the Transmission Control Protocol (TCP) makes sure that data is delivered reliably.", 4, [
            MP("Each packet is given a sequence number so the receiver can put them in order and spot missing ones", ["sequence number", "order", "numbered"]),
            MP("The receiver sends an acknowledgement for the packets that arrive", ["acknowledg", "ack", "confirmation"]),
            MP("If the sender does not receive an acknowledgement before a timeout, it resends the packet", ["timeout", "resend", "retransmit", "sent again"]),
            MP("A checksum is used to detect damaged packets, which are discarded and so resent", ["checksum", "damaged", "corrupt", "error check"]),
        ], "TCP gives each packet a sequence number, so that the receiver can put them in the right order and tell if any are missing. The receiver sends an acknowledgement for the packets that arrive. If the sender does not receive an acknowledgement before a timeout, it assumes the packet was lost and sends it again. A checksum is used to detect packets that were damaged on the way, which are discarded and so are sent again.",
           command="Explain"),
        EQ("Explain the difference between client-side processing and server-side processing, giving an example of each.", 4, [
            MP("Client-side processing is carried out on the user's device, usually by the browser", ["client", "browser", "user's device", "user's computer"]),
            MP("An example such as checking a form field as it is typed, or animating a menu", ["form", "validation", "animation", "menu", "javascript"]),
            MP("Server-side processing is carried out on the web server before the page is sent", ["server", "web server", "before"]),
            MP("An example such as checking a password, or searching a database", ["password", "database", "login", "search", "payment"]),
        ], "Client-side processing is carried out on the user's own device, usually in the browser using JavaScript. An example is checking that a form field has been filled in while the user is typing, or animating a menu. Server-side processing is carried out on the web server, which then sends the result to the browser. An example is checking a user's password against the database when they log in, which must be done on the server because the user cannot be allowed to see or change the code.",
           command="Explain"),
        EQ("A user types the address https://www.example.org/news into a web browser and presses enter. Discuss what happens, from the browser to the page appearing on the screen.", 6, [
            MP("The browser uses DNS to look up the IP address of www.example.org", ["dns", "domain name", "ip address", "look up"]),
            MP("It opens a connection to the web server using TCP, and HTTPS means the connection is encrypted", ["tcp", "connection", "https", "encrypt", "tls", "port 443"]),
            MP("It sends an HTTP request using the GET method for the path /news", ["http request", "get", "/news", "request"]),
            MP("The server finds or builds the page, perhaps using a database, and sends an HTTP response with a status code such as 200 and the HTML", ["response", "200", "status code", "html", "database"]),
            MP("The browser renders the HTML and makes further requests for linked files such as CSS, images and scripts", ["render", "css", "images", "further requests", "scripts", "display"]),
            MP("The data travels as packets, which are routed separately and reassembled at each end", ["packets", "routers", "reassembled", "routed", "split"]),
        ], "The browser first asks a DNS server to translate the domain name www.example.org into an IP address. It then opens a TCP connection to the web server at that address, and because the address starts with https the connection is encrypted. The browser sends an HTTP request using the GET method for the path /news. The web server finds or builds the page, perhaps using a database, and sends back an HTTP response with a status code such as 200 OK and the HTML of the page. The browser renders the HTML and makes further requests for files that the page links to, such as style sheets, images and scripts. All of the data travels as packets, which are routed separately across the internet and reassembled in the correct order at the other end.",
           command="Discuss"),
    ],
)
