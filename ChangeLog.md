# Version 0.3.0

- [ ] Setup diag from config instead of command params.
- [ ] Add send report method
    - [ ] Through http
    - [ ] Through ssh
    - [ ] Through reverse-ssh ?
    - [ ] Through ftp ?
- [ ] Update documentation
    - [ ] Update user doc
    - [ ] Update dev doc

# Version 0.2.0

- [x] Create an app manager (Diagonal)
- [x] Use app manager instead of loader functions
- [x] Dissociate app manager from diagnostic manager
- [x] Dissociate diagnostic manager from diagnostic
- [x] Use logger to print and write messages
- [x] DiagnosticManager.store became the unique storing source
- [x] Externalize errors in diag.errors file
- [x] Uniformize the way add logs everywhere
- [x] Update documentation
    - [x] Update sources doc
    - [x] Update user doc
    - [x] Update dev doc
- [ ] Setup unit tests
    - [x] unit tests on Diagonal
    - [ ] unit tests on DiagnosticManager
    - [ ] unit tests on Diagnostic
    - [ ] unit tests on utils

# Version 0.1.0

- [x] Init the project
- [x] Create more project structure
- [x] Separate project meta datas from code.
