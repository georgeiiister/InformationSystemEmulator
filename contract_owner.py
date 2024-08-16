class ContractOwner:
    """main class for create contract owner object"""

    def __init__(self
                 , contract_owner_id: int
                 , contract_owner_name: str
                 , collection_of_contracts: object = None
                 ):

        self.__contract_owner_id = contract_owner_id
        self.__contract_owner_name = contract_owner_name
        self.__collection_of_contracts = collection_of_contracts

    @property
    def person_id(self):
        return self.__contract_owner_id

    @property
    def name_person(self):
        return self.__contract_owner_name

    def add_contract(self, collection_of_contracts):
        raise NotImplemented