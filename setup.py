import setuptools

setuptools.setup(
    include_package_data=True,
    name='disws',
    version='0.0.6',
    description='discord-websocket (disws)',
    url='https://github.com/howryyucks/discord-websocket',
    author='Howry Yucks',
    packages=setuptools.find_packages(),
    install_requires=['aiohttp', 'multidict', 'websockets'],
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Licence :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
