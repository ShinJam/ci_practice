# CI practice
[![codecov](https://codecov.io/gh/ShinJam/ci_practice/branch/master/graph/badge.svg)](https://codecov.io/gh/ShinJam/ci_practice)
![CI](https://github.com/ShinJam/ci_practice/workflows/CI/badge.svg)

#### Requirements
`poetry`로 install
- `coverage`
- `pytest`
- `pytest-django`
- `codecov`
- `pytest-cov`
```
$ poetry add coverage pytest pytest-django codecov pyteset-cov 
```

### File tree
```
├── README.md
├── app
│   ├── blog
│   ├── config
│   ├── db.sqlite3
│   ├── manage.py
│   └── templates
├── coverage.xml
├── db.sqlite3
├── poetry.lock
├── pyproject.toml
└── pytest.ini
```

### Django기본 테스트

```
$ python manage.py test
```

### [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.0.3/)

> 테스트 코드를 실행했을 때, 전체 소스 코드 중 몇%가 실행되었는지 확인

테스트 코드가 전체 어느 정도 커버 하는지 척도  
높다고만 꼭 좋은 것은 아님


**coverage 설정파일 (`.coveragerc`)**

```
[run]
# app폴더안의 내용을 검사
source =
    app

# 지정한 경로는 리포트에서 제외
omit =
    app/manage.py
    app/config/asgi.py
    app/config/wsgi.py
    app/*/migrations/*

[report]
exclude_lines =
    def __str__
```

```
$ coverage run app/manage.py test
$ coverage run --source='.' app/manage.py test
$ coverage report -m
```


### pytest, pytest-django
> 장고 테스트 툴 ; Django기본 테스트 대신, pytest를 사용


```
$ pytest app
$ coverage run -m pytest app
$ coverage report -m
```

** pytest 설정파일(`pytest.ini`) **

```
[pytest]
python_files = tests.py test_*.py *_test.py
DJANGO_SETTINGS_MODULE = config.settings
norecursedirs = .git */templates/* */static/*
addopts = --nomigrations --reuse-db
```

### codecov, [Coverage.io](https://codecov.io/)
> codecov.io에 테스트 리포트를 쉽게 업로드 할 수 있도록 도와주는 라이브러리
1. git repository 선택
2. repo settings > secrets에 token 추가
3. repo settings >  integrations & service 에 codecov 추가

### pytest-cov
> pytest를 사용해서 codecov.io에 업로드 할 리포트를 만들어주는 라이브러리

```
$ pytest --cov app
$ CODECOV_TOKEN=<codecov.io Token> codecov
```

## Github Action
> Travis를 대체하는 github action을 이용한 CI

```yaml
// .github/workflow/main.yml

name: CI

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
    
# set env  
env:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8]

    steps:
    - uses: actions/checkout@v2
      
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v1
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install poetry
      run: curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
      
    - name: Install Python packages
      run: ~/.poetry/bin/poetry install
      
    - name: pytest-cov
      run: ~/.poetry/bin/poetry run pytest --cov app
    
    - name: codecov
      run: ~/.poetry/bin/poetry run codecov
``` 