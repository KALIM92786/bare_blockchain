import logging

class IoTDevice:
    def __init__(self, device_id, blockchain):
        """
        Initialize an IoT device that interacts with the blockchain.
        :param device_id: Unique identifier for the IoT device.
        :param blockchain: Blockchain instance to interact with.
        """
        self.device_id = device_id
        self.blockchain = blockchain
        logging.info(f"IoT Device {self.device_id} initialized.")

    def trigger_contract_execution(self, contract_id, method, args):
        """
        Trigger a smart contract execution from the IoT device.
        :param contract_id: ID of the smart contract to execute.
        :param method: Method to execute within the smart contract.
        :param args: Arguments for the smart contract method.
        """
        logging.info(f"Device {self.device_id} triggering contract {contract_id} with method {method}.")
        try:
            result = self.blockchain.execute_contract(contract_id, method, args)
            logging.info(f"Contract executed successfully. Result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error executing contract from device {self.device_id}: {e}")
            raise

    def send_transaction(self, sender, recipient, amount):
        """
        Simulates an IoT device initiating a blockchain transaction.
        """
        metadata = {"device_id": self.device_id}
        self.blockchain.new_transaction(sender, recipient, amount, "signature", "public_key", metadata)

