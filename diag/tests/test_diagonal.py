from diag.diagonal import Diagonal
from diag.manager import DiagnosticManager
from diag.errors import *
import pytest

class Test_diagonal:
    app = None
    manager = None

    def test_instance_wrong_param(self):
        with pytest.raises(TypeError):
            Diagonal()
        with pytest.raises(TypeError):
            Diagonal(None)
        with pytest.raises(DiagonalError):
            Diagonal(None, None)
        with pytest.raises(DiagonalError):
            Diagonal("test", 0)

        Test_diagonal.manager = DiagnosticManager()
        assert(Test_diagonal.manager != None)
        Test_diagonal.app = Diagonal([], Test_diagonal.manager)
        assert(Test_diagonal.app != None)

    def test_configure_logger_no_param(self):
        # No parameter raise an error
        with pytest.raises(TypeError):
            Test_diagonal.app.configure_logger()

        with pytest.raises(DiagonalError):
            Test_diagonal.app.configure_logger(None)
    
        with pytest.raises(DiagonalError):
            Test_diagonal.app.configure_logger(1)

        assert(Test_diagonal.app.logger_configured == False)

        with pytest.raises(DiagonalError):
            Test_diagonal.app.configure_logger("")
        assert(Test_diagonal.app.logger_configured == False)

        Test_diagonal.app.configure_logger("./diag.log")
        assert(Test_diagonal.app.logger_configured == True)


    def test_paths(self):
        assert(isinstance(Test_diagonal.app.paths(), dict) == True)
        assert("project" in Test_diagonal.app.paths())
        assert("report" in Test_diagonal.app.paths())
        assert("diagnostics" in Test_diagonal.app.paths())

    
    def test_path(self):
        with pytest.raises(TypeError):
            Test_diagonal.app.path()
        with pytest.raises(DiagonalError):
            Test_diagonal.app.path(None)
            
        # Get mode
        assert(Test_diagonal.app.path("project") == Test_diagonal.app.paths().get("project"))
        assert(Test_diagonal.app.path("report") == Test_diagonal.app.paths().get("report"))
        assert(Test_diagonal.app.path("diagnostics") == Test_diagonal.app.paths().get("diagnostics"))

        # Set mode
        Test_diagonal.app.path("test", "test_value")
        assert(Test_diagonal.app.path("test") == "test_value")

        # OOB too much args
        with pytest.raises(TypeError):
            Test_diagonal.app.path("test", "value", None)

    def test_has_path(self):
        with pytest.raises(TypeError):
            Test_diagonal.app.has_path()
        with pytest.raises(DiagonalError):
            Test_diagonal.app.has_path(None)
        with pytest.raises(TypeError):
            Test_diagonal.app.has_path("a", "b", "c")

        assert(Test_diagonal.app.has_path("project") == True)
        assert(Test_diagonal.app.has_path("test") == True)
        assert(Test_diagonal.app.has_path("unknown") == False)

    def test_unpath(self):
        with pytest.raises(TypeError):
            Test_diagonal.app.unpath()
        with pytest.raises(DiagonalError):
            Test_diagonal.app.unpath(None)
        with pytest.raises(TypeError):
            Test_diagonal.app.unpath("a", "b", "c")

        assert(Test_diagonal.app.has_path("test") == True)
        Test_diagonal.app.unpath("test")
        assert(Test_diagonal.app.has_path("test") == False)