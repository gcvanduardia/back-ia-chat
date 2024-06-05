# START PROJECT #

## STEP 1 (first time) Install virtual environment (virtualenv)
```shell 
pip3 install virtualenv
```

## STEP 2 (first time) Create virtual enviroment
```shell
python -m venv venv
```

## STEP 3 (every time) activate virtual mode
MacOs:
```shell
source venv/bin/activate
```
Windows:
```shell
.\venv\Scripts\activate
```

## STEP 4 (first time) Install libraries
```shell
pip install -r requirements.txt
```
if ssl certificate problem:
```shell
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
```

## STEP 5 (first time) openai config
NOWIA--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--NOWIA

## STEP 6 (every time) run serve
```shell
uvicorn main:app --reload
```