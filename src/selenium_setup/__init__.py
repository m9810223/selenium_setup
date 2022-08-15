import typer

from . import _drivers


def _main(
    *,
    driver: str = typer.Argument(_drivers.Driver.CHROME.value),
    ver: str = None,
    list: bool = False,
):
    if list:
        return _list_vers(driver)

    if driver.lower() == _drivers.Driver.CHROME.value:
        return _drivers.Chrome.download(ver)
    raise RuntimeError


def _list_vers(driver: str):
    if driver.lower() == _drivers.Driver.CHROME.value:
        return _drivers.Chrome.list_vers()
    raise RuntimeError


def main():
    try:
        app = typer.Typer(pretty_exceptions_enable=False)
        app.command()(_main)
        app()
        return
    except SystemExit:
        ...
    except:
        bug_report_link = 'https://github.com/m9810223/selenium_setup/issues'
        print(f'\n\n  >>> {bug_report_link = }\n')


if __name__ == '__main__':
    main()
