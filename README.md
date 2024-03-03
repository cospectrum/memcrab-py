# memcrab-py
Memcrab Python Client

```sh
pip install memcrab
```

## Usage

### Tcp

```py
from memcrab.blocking import RawClient

host = "127.0.0.1"
port = 9900
client = RawClient.tcp((host, port))
client.ping()

client.set("letters", b"ABC")
val = client.get("letters")
print(f"{val=}")
```
