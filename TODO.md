
## TO-DO List

### Accounts
[] Create
    Create an account. Returns reference ID to use in other operations.

[] List
    Print all accounts that were created or loaded.

[] Recover
    Recover Libra wallet from the file path.
    Parameters:
      - File Path

[] Write
    Save Libra wallet mnemonic recovery seed to disk.
    Parameters:
      - File path

[] Mint
  Mint coins to the account.
  Parameters:
    - Receiver Account Address
    - Number of coins


### Query
[] Balance
    Get the current balance of an account.
    Parameters:
      - Account Address

[] Sequence
    Get the current sequence number for an account, and reset current sequence
    number in CLI  (optional, default is false).
    Parameters:
      - Account Address
      - Reset sequence number (optional, oneof: true|false, default=false)

[] Account State
    Get the latest state for an account.
    Parameters:
      - Account Address

[] Txn Acc Seq
  Get the committed transaction by account and sequence number.Optionally also
  fetch events emitted by this transaction.
  Parameters:
    - Account Address
    - Sequence Number
    - Fetch Events (oneof: true|false)

[] Txn Range
    Get the committed transactions by version range. Optionally also fetch
    events emitted by these transactions.
    Parameters:
      - Start Version
      - Limit
      - Fetch Events (oneof: true|false)

[] Event
    Get events by account and event type (sent|received).
    Parameters:
      - Account Address
      - Event type (oneof: sent|received)
      - Start sequence number
      - Ascending (oneof=true|false)
      - Limit


### Transfer
[] Allow the user to transfer coins
  Parameters:
    - Sender account address
    - Receiver account address>
    - Number of coins
    - Gas unit price in micro libras (Default=0)
    - Max Gas amount in micro libras (Default=10000)
