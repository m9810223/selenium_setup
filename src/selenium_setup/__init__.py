import typer

from . import _drivers


def _main(
    *,
    driver: str = typer.Argument(_drivers.Driver.CHROME.value),
    ver: str = '',
):
    if driver.lower() == _drivers.Driver.CHROME.value:
        driver_zip = _drivers.Chrome.download_zip(version=ver)
        return _drivers.Chrome.unzip(driver_zip=driver_zip)
    raise RuntimeError


def main():
    try:
        app = typer.Typer(pretty_exceptions_enable=False)
        app.command()(_main)
        app()
        return
    except SystemExit:
        ...
    except Exception as e:
        print(e)
        bug_report_link = 'https://github.com/m9810223/selenium_setup/issues'
        print(f'\n\n  >>> {bug_report_link = }\n')


if __name__ == '__main__':
    main()
