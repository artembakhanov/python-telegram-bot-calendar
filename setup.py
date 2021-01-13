from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='python-telegram-bot-calendar',
    packages=['telegram_bot_calendar'],
    version='1.0.5',
    license='MIT',
    description='Python inline calendar for telegram bots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Artem Bakhanov',
    author_email='artembakhanov@gmail.com',
    url='https://github.com/artembakhanov/python-telegram-bot-calendar',
    download_url='https://github.com/artembakhanov/python-telegram-bot-calendar/archive/v_1.0.2.tar.gz',
    keywords=['calendar', 'telegram', 'bot', 'telegram bot'],
    install_requires=[
        'python-dateutil',
    ],
    extras_require={
        'telethon': ['telethon']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
