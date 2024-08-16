class Contract:

    def __init__(self
                 , contract_id: int
                 , collection_of_accounts: object = None
                 ):

        self.__contract_id = contract_id
        self.__collection_of_accounts = collection_of_accounts

    @property
    def contract_id(self):
        return self.__contract_id