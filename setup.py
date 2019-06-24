from setuptools import setup, find_packages

setup(name='backtrader_addons',
    version='0.17.9',
    description='Addons (analyzers, observers, indicators etc) for backtrader',
    url='https://github.com/ab-trader/backtrader_addons',
    author='ab-trader',
    author_email='',
    license='GPLv3+',
    packages=find_packages(),
    # packages=['backtrader_addons'],
	install_requires=[ 'backtrader',
	                 ],
    zip_safe=False)