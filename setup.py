from setuptools import setup, find_packages

setup(
    name='pokerlib',
    version='0.2.2',
    description='Methods for poker analytics',
    author='Kamagames Studio',
    author_email='k.sarafanov@zmeke.com',
    py_modules=['poker2/__init__', 'poker2/poker_objects', 'poker2/texas_poker', 'poker2/omaha_poker', 'poker2/old_poker', 'poker2/poker_approx'],
    packages=find_packages(),
    package_data={
        '': ['*.gz']
    }
)
