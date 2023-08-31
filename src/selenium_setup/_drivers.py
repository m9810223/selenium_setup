import platform
import stat
from enum import Enum
from pathlib import Path
from zipfile import ZipFile

import httpx
import rich.progress

CWD = Path.cwd()


def get_os_info():
    return platform.system(), platform.machine()


class Driver(str, Enum):
    CHROME = 'chrome'


class Chrome:  # https://github.com/GoogleChromeLabs/chrome-for-testing
    name = 'chrome'
    latest_release_url = (
        'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE'
    )
    link = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/{operating_system}/chromedriver-{operating_system}.zip'
    os_mapping: dict[tuple[str, str], str] = {
        ('Linux', 'x86_64'): 'linux64',
        ('Darwin', 'arm64'): 'mac-arm64',
        # (): 'mac-x64',
        # (): 'win32',
        ('Windows', 'AMD64'): 'win64',
    }

    @classmethod
    def download_zip(cls, *, version: str = ''):
        version = version or httpx.get(cls.latest_release_url).text
        print(f'{cls.name} {version = }')

        operating_system = cls.os_mapping.get(get_os_info())
        if operating_system is None:
            raise RuntimeError
        print(f'{operating_system = }')

        url = cls.link.format(version=version, operating_system=operating_system)
        print(f'{url = }')
        driver_zip = CWD / url.rsplit('/', 1)[-1]
        driver_zip = driver_zip.with_stem(f'{driver_zip.stem}--{version}')
        # return driver_file

        if driver_zip.exists():
            print(f'file exists: {str(driver_zip)}')
            return driver_zip

        with driver_zip.open(mode='wb') as _f:
            print(f'downloading to: {driver_zip}')
            with httpx.stream("GET", url) as response:
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
        return driver_zip

    @classmethod
    def unzip(cls, *, driver_zip: Path):
        with ZipFile(file=driver_zip) as z:
            driver_info = [
                x for x in z.filelist if x.filename.endswith('/chromedriver')
            ][0]
            driver_file = CWD / driver_info.filename.split('/')[-1]
            driver_file.write_bytes(z.read(driver_info))
            curr_mod = driver_file.stat().st_mode
            all_x = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            driver_file.chmod(curr_mod | all_x)
