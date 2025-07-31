import account
import person
import legalperson

from object import ISObject

class Contract(ISObject):
    """Main class for create object contract"""

    def __init__(self
                 , contract_id: int
                 , number: str
                 , owner: object
                 , accounts: account.Accounts
                 ):
        ISObject.__init__(self)

        self.__contract_id = contract_id
        self.__accounts = accounts
        self.__owner = owner
        self.__number = number

    @property
    def contract_id(self):
        return self.__contract_id

    @property
    def accounts(self):
        return self.__accounts

    @property
    def owner(self):
        return self.__owner
