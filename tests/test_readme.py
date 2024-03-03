def readme() -> None:
    from memcrab.blocking import RawClient

    client = RawClient.tcp("127.0.0.1:9900")
    val = client.get("some-key")
    if val is None:
        print('cache miss for some-key')

    err = client.set('day', b"some data")
    assert err is None
