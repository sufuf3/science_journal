# science_journal  
  

1. Create API key from https://dev.elsevier.com/user/login  
2. Develop environment prepare  
```bash
$ cd science_journal
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```
3. Replace `[insert your key here]` from `science_journal.py` to API key  
4. Run program  
```bash
$ python3.6 science_journal.py
```
