"""
https://selenium-python.readthedocs.io/installation.html#drivers
"""


import platform
from enum import Enum
from pathlib import Path
from zipfile import ZipFile

import httpx
import rich.progress
import xmltodict


CWD = Path.cwd()


def get_os_info():
    return platform.system(), platform.machine()


class Driver(str, Enum):
    CHROME = 'chrome'


class Chrome:
    name = 'chrome'
    latest_release_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    link = 'https://chromedriver.storage.googleapis.com/{ver}/chromedriver_{operating_system}.zip'
    os_mapping = {
        ('Linux', 'x86_64'): 'linux64',
        # (): 'mac64',
        ('Darwin', 'arm64'): 'mac64_m1',
        ('Windows', 'AMD64'): 'win32',
    }
    list_url = 'https://chromedriver.storage.googleapis.com'
    index_url = 'https://chromedriver.storage.googleapis.com/index.html'

    @classmethod
    def _download(cls, ver: str):
        _os = cls.os_mapping.get(get_os_info())
        if _os is None:
            raise RuntimeError
        print(f'{_os}')

        _url = cls.link.format(ver=ver, operating_system=_os)
        driver_file = CWD / _url.rsplit('/', 1)[-1]
        driver_file = driver_file.with_stem(f'{driver_file.stem}--{ver}')
        # return driver_file

        if driver_file.exists():
            print(f'file {driver_file.relative_to(CWD)} exists')
            return driver_file

        with driver_file.open(mode='wb') as _f:
            print(f'downloading to: {driver_file}')
            with httpx.stream("GET", _url) as response:
                total = int(response.headers["Content-Length"])
                with rich.progress.Progress(
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    rich.progress.BarColumn(bar_width=None),
                    rich.progress.DownloadColumn(),
                    rich.progress.TransferSpeedColumn(),
                ) as progress:
                    download_task = progress.add_task("Download", total=total)
                    for chunk in response.iter_bytes():
                        _f.write(chunk)
                        progress.update(
                            download_task, completed=response.num_bytes_downloaded
                        )
        return driver_file

    @classmethod
    def _unzip_driver_file(cls, driver_file: Path):
        with ZipFile(file=driver_file) as _z:
            _z.extractall(path=CWD)

    @classmethod
    def download(cls, ver: str = None, /):
        if ver is None:
            ver = httpx.get(cls.latest_release_url).text
        print(f'{cls.name} {ver = }')

        driver_file = cls._download(ver=ver)
        cls._unzip_driver_file(driver_file)

    @classmethod
    def list_vers(cls):
        xml = httpx.get(cls.list_url).text
        keys = list(
            map(
                lambda x: str(x['Key']),
                xmltodict.parse(xml)['ListBucketResult']['Contents'],
            )
        )

        _prefix = 'LATEST_RELEASE_'
        _vers = sorted(
            [
                x.split(_prefix, 1)[-1]
                for x in keys
                if x.startswith(_prefix)
                if '.' in x
            ],
            reverse=True,
            key=lambda x: tuple(map(int, x.split('.'))),
        )[:10]
        vers = [
            httpx.get(f'https://chromedriver.storage.googleapis.com/{_prefix}{x}').text
            for x in _vers
        ]

        _os = cls.os_mapping.get(get_os_info())
        ver_infos = [
            f'  {x:14} {cls.link.format(ver=x, operating_system=_os)}' for x in vers
        ]
        print(f'{cls.name} {_os}:')
        print('\n'.join(ver_infos))
