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


## STEP 5 (every time)  Locate the input files
Locate the input files in `data/input`. Items: 
- **legacy**: List of legacy projects `*.xlsx`
- **projects**: 'output file from the Coding Standards process named `*-cs-prs-detail*.csv'`
- **sonar**: 'sonar report corresponding to the analysis month named `Reporte_Metricas_Sonar-*.xlsx'` 

* Multiple files can be uploaded for each item and the process will concatenate them into a single file for each item.

## STEP 6 (every time) Initialize main program
```shell
python run.py
```

## STEP 7 (every time) Read the output file
The output is a file located in `data/output` named `quality-gates_*.xlsx`.



# UNIT TESTING #

## SET 1 (every time) Execute tests
```shell
python run_tests.py
```

## SET 2 (every time) Execute coverage script 
```shell
coverage run run_tests.py
```

## SET 3 (every time) Execute coverage report
```shell
coverage report -m
```

## SET 4 (every time) Generate coverage HTML report
```shell
coverage html
```

```shell
uvicorn main:app --reload
```




