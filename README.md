# A Beginners Guide

### Setup environment
- ensure modules listed in `requirements.txt` are loaded before starting
- use a virtual environment to load modules
```bash 
   -  python3 -m venv venv
```
- *once required modules are loaded;*
- run `setup_db.py` to initialize databases
```bash
- mv config-debug/setup_db.py {/path/to/working-directory}/setup_db.py
- python3 setup_db.py
```
***should then see `tasks.db` after setup***

### Run App
```bash
- python3 app.py
```