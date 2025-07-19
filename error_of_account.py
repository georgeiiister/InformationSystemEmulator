from error import InformationSystemError

class AccountError(InformationSystemError):
    pass


class BalanceError(AccountError):
    pass


class RedBalanceError(BalanceError):
    pass


class ActiveBalanceError(BalanceError):
    pass


class BalanceIsNotZero(BalanceError):
    pass


class ActivationError(AccountError):
    pass


class DateActivationError(ActivationError):
    pass


class NotSetDateBeginOfAction(DateActivationError):
    pass


class NotValidDateActivationError(DateActivationError):
    pass


class CloseError(AccountError):
    pass


class DateCloseError(CloseError):
    pass


class NotValidDateCloseError(DateCloseError):
    pass


class CategoryOfAccountError(AccountError):
    pass


class AccountsError(Exception):
    pass


class AccountNotFoundError(AccountsError):
    pass


class AccountDeleteFromCollectionError(AccountsError):
    pass


class PrimaryAccountError(AccountsError):
    pass


class DeletePrimaryAccountError(PrimaryAccountError):
    pass

class PrimaryAccountNotFoundError(PrimaryAccountError):
    pass