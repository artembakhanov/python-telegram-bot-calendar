from distutils.core import setup

setup(
    name='python-telegram-bot-calendar',
    packages=['telegram_bot_calendar'],
    version='0.1',
    license='MIT',
    description='Python inline calendar for Telegram bots',
    author='Artem Bakhanov',
    author_email='artembakhanov@gmail.com',
    url='https://github.com/artembakhanov/python-telegram-bot-calendar',
    download_url='https://github.com/artembakhanov/python-telegram-bot-calendar/archive/v_01.tar.gz',
    keywords=['calendar', 'telegram', 'bot', 'telegram bot'],
    install_requires=[
        'python-dateutil',
    ],
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
