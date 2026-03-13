class AppError(Exception):
    """Base typed error for the app."""


class PDFEncryptedError(AppError):
    pass


class PDFNoTextError(AppError):
    pass


class IndexNotReadyError(AppError):
    pass


class ProviderUnavailableError(AppError):
    pass


class FatalLLMError(AppError):
    pass

