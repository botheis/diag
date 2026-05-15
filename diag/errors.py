
class DiagnosticManagerError(Exception):
    pass

class DiagonalError(Exception):
    pass


class DiagnosticError(Exception):
    pass

# Manager raise messages
DIAGONAL_INVALID_NONE_ARGS = "Invalid system args : None"
DIAGONAL_INVALID_TYPE_ARGS = "Invalid system args : Incompatible type"
DIAGONAL_INVALID_NONE_MANAGER = "Invalid manager : None"
DIAGONAL_INVALID_TYPE_MANAGER = "Invalid manager : Incompatible type"
DIAGONAL_INVALID_PATH = "Invalid path name"
DIAGONAL_INVALID_NONE_PATH = "Invalid path : None or Empty"
DIAGONAL_INVALID_TYPE_PATH = "Invalid path : Incompatible type"

MANAGER_LOGGER_NOT_SET = "DiagnosticManager logger not set"
MANAGER_INVALID_EMPTY_NAME = "Invalid diagnostic register name: empty"
MANAGER_INVALID_USED_NAME = "Invalid diagnostic register name: already used"
MANAGER_INVALID_UNKNOWN_NAME = "Invalid diagnostic register name: unknown name"
MANAGER_INVALID_EMPTY_INSTANCE = "Invalid diagnostic instance : empty"
MANAGER_INVALID_TYPE_INSTANCE = "Invalid diagnostic instance : not Diagnostic"

DIAGNOSTIC_MANAGER_NOT_SET = "DiagnosticManager not set"
