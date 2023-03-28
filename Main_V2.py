# importar las bibliotecas necesarias
from hashlib import sha256
import json
import time

# definir la clase Block
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

# definir la clase Blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        self.add_block(block)
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]
        print("Block mined")
        
    def create_transaction(self, sender_address, recipient_address, amount):
        self.pending_transactions.append(Transaction(sender_address, recipient_address, amount))

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.sender_address == address:
                    balance -= transaction.amount
                if transaction.recipient_address == address:
                    balance += transaction.amount
        return balance

# definir la clase Transaction
class Transaction:
    def __init__(self, sender_address, recipient_address, amount):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount

# crear una instancia de Blockchain
my_blockchain = Blockchain()

# crear transacciones
my_blockchain.create_transaction("address1", "address2", 10)
my_blockchain.create_transaction("address2", "address1", 5)

# minar un bloque
my_blockchain.mine_pending_transactions("miner_address")

# imprimir el balance de una dirección
print("Balance de address1:", my_blockchain.get_balance("address1"))
