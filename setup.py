import urllib
from setuptools import setup, find_packages

version = '1.0.0'


def parse_requirements_file(path):
    with open(path) as f:
        for line in f.read().splitlines():
            # sanitize line
            line, *_ = line.split(' ')

            # ignore comments and pip cli args
            if line.startswith('-') or line.startswith('#'):
                continue

            # convert pip git format to setuptools
            if line.startswith('git+ssh://'):
                p = urllib.parse.urlparse(line) # noqa
                # get package name
                if p.fragment:
                    _, package_name = p.fragment.split('egg=')
                else:
                    package_name = p.path.split('/')[-1].split('.git')[0]
                yield f'{package_name} @ {p.scheme}://{p.netloc}{p.path}'
            else:
                if line:
                    yield line


setup(
    name='ncscore',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=list(parse_requirements_file('requirements.txt')),
    entry_points={
        'console_scripts': [
            'runserver = manage:main',
        ]
    },
)
