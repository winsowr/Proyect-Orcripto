# importar las bibliotecas necesarias
from hashlib import sha256
import json
import time
import uuid


# definir la clase Block
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __str__(self):
        return f"Index: {self.index}\nTimestamp: {self.timestamp}\nData: {self.data}\nHash: {self.hash}\nPrevious Hash: {self.previous_hash}\nNonce: {self.nonce}\n"


# definir la clase Blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 0.000003
        self.difficulty = 2
        self.nodes = set()
        self.uuid = str(uuid.uuid4())
        self.transactions_pool = []

    def create_genesis_block(self):
        empty_addresses = {}
        for i in range(2000):
            empty_addresses[f"address{i}"] = 0
        initial_distribution = {'address1': 0, 'address2': 0, 'address3': 0, 'rich_address': 3000000, **empty_addresses}
        return Block(0, time.time(), {'name': 'Orcripto', 'symbol': 'ORC', 'total_supply': 3000000, 'distribution': initial_distribution}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        self.add_block(block)
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]
        print("Block mined")

    def create_transaction(self, sender_address, recipient_address, amount, private_key):
        transaction = Transaction(sender_address, recipient_address, amount)
        transaction.sign_transaction(private_key)

        if not transaction.is_valid():
            raise Exception("Transaction is not valid")

        self.transactions_pool.append(transaction)
        return True

    def process_transactions(self):
        for transaction in self.transactions_pool:
            if not transaction.is_valid():
                continue
            self.pending_transactions.append(transaction)
        self.transactions_pool = []

    def register_node(self, node):
        self.nodes.add(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def sync_nodes(self):
        for node in self.nodes:
            node.update_chain(self.chain)

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain):
            self.chain = new_chain

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.sender_address == address:
                    balance -= transaction.amount
                if transaction.recipient_address == address

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 0.000003
        self.difficulty = 4  # dificultad de minado
        self.max_block_size = 5  # tamaño máximo de bloque
        self.transactions_per_second = 10  # transacciones por segundo
        self.max_unconfirmed_blocks = 10  # número máximo de bloques sin confirmar

    # Resto del código

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.sender_address == address:
                    balance -= transaction.amount
                if transaction.recipient_address == address:
                    balance += transaction.amount
        for transaction in self.pending_transactions:
            if transaction.sender_address == address:
                balance -= transaction.amount
        return balance



