from client import deserializer


def test_account_blob_deserialization_account_1():
    """Test Account Blob deserialization for
    Account: 0d5c7d17fd85f19097151fba72a0ef7d6078d58feabecf1ac39db7c6e4d6f6aa
    Balance: 200000000 (200)
    """
    raw_blob = '010000002100000001217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc9744000000200000000d5c7d17fd85f19097151fba72a0ef7d6078d58feabecf1ac39db7c6e4d6f6aa00c2eb0b00000000000000000000000000000000000000000000000000000000'
    blob = bytes.fromhex(raw_blob)
    result = deserializer.AccountStateBlobDeserializer.from_bytes(blob)
    assert result['authentication_key'] == '0d5c7d17fd85f19097151fba72a0ef7d6078d58feabecf1ac39db7c6e4d6f6aa'
    assert result['balance'] == 200000000
    assert result['received_events_count'] == 0
    assert result['sent_events_count'] == 0
    assert result['sequence_number'] == 0


def test_account_blob_deserialization_account_2():
    """Test Account Blob deserialization for:
    Account: 435fc8fc85510cf38a5b0cd6595cbb8fbb10aa7bb3fe9ad9820913ba867f79d4
    Balance: 3932556404000000 (3932556404)
    """
    raw_blob = '010000002100000001217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc974400000020000000435fc8fc85510cf38a5b0cd6595cbb8fbb10aa7bb3fe9ad9820913ba867f79d4000585a3a3f80d00010000000000000000000000000000000000000000000000'
    blob = bytes.fromhex(raw_blob)
    result = deserializer.AccountStateBlobDeserializer.from_bytes(blob)
    assert result['authentication_key'] == '435fc8fc85510cf38a5b0cd6595cbb8fbb10aa7bb3fe9ad9820913ba867f79d4'
    assert result['balance'] == 3932556404000000
    assert result['received_events_count'] == 1
    assert result['sent_events_count'] == 0
    assert result['sequence_number'] == 0


