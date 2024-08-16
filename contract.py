import account
import person
import legal_person

class Contract:
    """Main class for create object contract"""

    def __init__(self
                 ,contract_id: int
                 ,contract_owner: person.Person|legal_person.LegalPerson
                 ,collection_of_accounts: account.Collection
                 ):

        self.__contract_id = contract_id
        self.__collection_of_accounts = collection_of_accounts
        self.__contract_owner = contract_owner

    @property
    def contract_id(self):
        return self.__contract_id