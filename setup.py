from setuptools import setup

setup(name='backtrader_addons',
    version='0.8.3',
    description='Addons (analyzers, observers, indicators etc) for backtrader',
    url='https://github.com/ab-trader/backtrader_addons',
    author='ab-trader',
    author_email='',
    license='GPLv3+',
    packages=['backtrader_addons'],
	install_requires=[ 'backtrader',
	                 ],
    zip_safe=False)