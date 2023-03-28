from hashlib import sha256
import json
import time
import random

class Transaction:
    def __init__(self, sender_address, receiver_address, amount):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.stake_validators = {}
        self.total_coins = 1000000  # total de monedas emitidas
        self.block_reward = 0.0000001  # cantidad de monedas a recompensar por bloque minado

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def select_stake_validators(self, num_validators):
        # Selección aleatoria de validadores basada en la participación en la red
        self.stake_validators = {}
        total_stake = sum(self.stake_validators.values())
        for i in range(num_validators):
            selected_validator = None
            while not selected_validator:
                rand = random.uniform(0, total_stake)
                for validator, stake in self.stake_validators.items():
                    if rand <= stake:
                        selected_validator = validator
                        break
                    else:
                        rand -= stake
            self.stake_validators[selected_validator] = self.stake_validators.get(selected_validator, 0) + 1

    def mine_block(self, miner_address):
        # Comprobar si hay suficientes monedas para recompensar al minero
        if self.total_coins < self.block_reward:
            return False

        # Selección de validadores de stake
        self.select_stake_validators(num_validators=3)

        # Comprobar si el minero seleccionado es uno de los validadores
        if miner_address not in self.stake_validators:
            return False

        # Recompensa al minero
        self.pending_transactions.append(Transaction(None, miner_address, self.block_reward))

        # Añadir transacciones pendientes y crear un nuevo bloque
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        self.add_block(block)

        # Actualizar el total de monedas
        self.total_coins += self.block_reward

        # Limpiar las transacciones pendientes y devolver verdadero para indicar que el bloque se ha minado con éxito
        self.pending_transactions = []
        return True
