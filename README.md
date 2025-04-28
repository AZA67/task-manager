# A Beginners Guide

### Setup environment
- ensure modules listed in `requirements.txt` are loaded before starting
- run `setup_db.py` to initialize databases
```bash
- mv config-debug/setup_db.py /fam-task_manager
- python3 setup_db.py
```
***should then see `tasks.db` after setup***

### Run App
```bash
- python3 app.py
```