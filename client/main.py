import random
import logging
import grpc
import rpc.admission_control_pb2 as admission_control_pb2
import rpc.admission_control_pb2_grpc as admission_control_pb2_grpc
import rpc.get_with_proof_pb2 as get_with_proof_pb2
from deserializer import AccountStateBlobDeserializer


class LibraClient():
    """Client to interact with Libra's gRPC functionality"""

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._current_channel = grpc.insecure_channel(f'{host}:{port}')
        self._stub = admission_control_pb2_grpc.AdmissionControlStub(
            self._current_channel)

    def get_account_state(self, account: str) -> dict:
        assert len(account) == 64, f'Wrong account length, expected 64.'
        raw_account = bytes.fromhex(account)
        acc_req = get_with_proof_pb2.GetAccountStateRequest(address=raw_account)
        items = get_with_proof_pb2.RequestItem(
            get_account_state_request=acc_req)
        req = get_with_proof_pb2.UpdateToLatestLedgerRequest(
            client_known_version=0, requested_items=[items])
        resp = self._stub.UpdateToLatestLedger(req).response_items[0]
        raw_blob = resp.get_account_state_response.account_state_with_proof.blob
        return AccountStateBlobDeserializer.from_bytes(raw_blob.blob)

    def _update_to_latest_ledger(req):
        pass


def run:
    client = LibraClient("ac.testnet.libra.org", "8000")
    account = '0d5c7d17fd85f19097151fba72a0ef7d6078d58feabecf1ac39db7c6e4d6f6aa'
    account_state = client.get_account_state(account)
    print(account_state)

if __name__ == '__main__':
    logging.basicConfig()
    run()
