from algosdk import kmd, algod, transaction, account, encoding, auction
import json
import base64

al_token = "ef920e2e7e002953f4b29a8af720efe8e4ecc75ff102b165e0472834b25832c1"
al_address = "http://berlinhack.algodev.network:9100"


dapp = {
    "private_key": "ZmV9v1h88zd7IB7tHQbkSsbO1cVbsZ1kgtnjomhcteZTjieMuF/0sc0jOr/wRSs2CS7iVRItIlC9QEhu+3EU0w==",
    "address": "KOHCPDFYL72LDTJDHK77ARJLGYES5YSVCIWSEUF5IBEG563RCTJQLYGEGI"
}


def rewrite_events(data):
    with open("events.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data))


def read_events():
    with open("events.json", encoding="utf-8") as f:
        return json.loads(f.read())


def add_event(name):
    event = create_event(name)
    events = read_events()
    events.append(event)
    rewrite_events(events)
    return event


def store_purchase(event, user):
    note_field_bytes = json.dumps(user).encode()

    al = algod.AlgodClient(al_token, al_address)
    params = al.suggested_params()
    gh = "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI="
    txn = transaction.PaymentTxn(event["address"], 0, params.get("lastRound"), params.get("lastRound")+1000, gh, dapp["address"], 1, note=note_field_bytes)
    txn = txn.sign(event["private_key"])
    return al.send_raw_transaction(txn)


def get_tickets_amount(eid):
    address = event_by_id(eid)["address"]

    al = algod.AlgodClient(al_token, al_address)
    params = al.suggested_params()
    gh = "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI="
    return len(al.transactions_by_address(address, first=1484588, last=params.get("lastRound"))["transactions"])


def event_by_id(eid):
    eid = int(eid)
    return [n for n in read_events() if n["id"] == eid][0]


def create_event(name):
    al = algod.AlgodClient(al_token, al_address)
    key, address = account.generate_account()
    eid = len(read_events()) + 1
    return {
        "name": name,
        "id": eid,
        "private_key": key,
        "address": address
    }

