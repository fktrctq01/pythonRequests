## 🏁 Get started

- Install python version 3.9.13 or +
- Install pytest framework
```
$ pip3 install pytest
```

- Install other frameworks
```
$ pip3 install requests
$ pip3 install jsonschema
$ pip3 install pydantic

```
- Install allure framework
```
$ brew install allure
$ pip3 install allure-pytest
```

## 🚀 For run autotests:
```
$  pytest -s -v tests/{file_name}.py --alluredir=allure_result
or
$  pytest -s -v tests --alluredir=allure_result
```

## 📊 For create report:
```
$ allure serve allure_result/
```