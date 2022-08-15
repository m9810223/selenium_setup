# selenium_setup

[![pypi](https://img.shields.io/pypi/v/selenium_setup?color=%2334D058)](https://pypi.org/project/selenium_setup/)

## install

```shell
pip install selenium_setup
```

## CLI

### download default version driver and unzip to CWD  

```shell
selenium_setup
# or: python3 -m selenium_setup
```

```console
chrome ver = '104.0.5112.79'
linux64
downloading to: /path/to/chromedriver_linux64--104.0.5112.79.zip
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.1/7.1 MB 200.8 kB/s
```

### list 10 links of some latest versions

```shell
selenium_setup --list
```

```console
chrome linux64:
  105.0.5195.19  https://chromedriver.storage.googleapis.com/105.0.5195.19/chromedriver_linux64.zip
  104.0.5112.79  https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
  103.0.5060.134 https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_linux64.zip
  102.0.5005.61  https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
  101.0.4951.41  https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip
  100.0.4896.60  https://chromedriver.storage.googleapis.com/100.0.4896.60/chromedriver_linux64.zip
  99.0.4844.51   https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_linux64.zip
  98.0.4758.102  https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip
  97.0.4692.71   https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip
  96.0.4664.45   https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
```

### download specific version

```shell
selenium_setup --ver ...
```
