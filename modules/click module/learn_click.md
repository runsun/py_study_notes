# Learning the python Click module 

Ref:[Building commandline appplication with Click](https://pymbook.readthedocs.io/en/latest/click.html)

## Using *virtualenv*

1. Create a new folder
``` 
 ..> mkdir click
 ..> cd click
 ..\click> 
```

2. Create a *hello.py*
```python
def cli():
  print('Hello World')
```

3. Create a *setup.py* file
Recommended way to write command line tools, then directly using *shebang-based* scripts.

```python
from setuptools import setup

setup(
    name="myhello",
    version='0.1',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        myhello=hello:cli
    ''',
)
```

```python
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install --editable .
Obtaining file:///home/kdas/code/practice/yoclick
Collecting Click (from myhello==0.1)
Using cached click-6.7-py2.py3-none-any.whl
Installing collected packages: Click, myhello
Running setup.py develop for myhello
Successfully installed Click-6.7 myhello

$ myhello
Hello World
```
 
4. If convert the same script to click-bsased tool, we have:

```shell
$ myhello
Hello World
$ myhello --help
Usage: myhello [OPTIONS]

Options:
--help  Show this message and exit.
```
 
## The Click module suggests using *echo* in place of *print* 

```python
import click

@click.command()
def cli():
    click.echo("Hello World")
```

## Using boolean flags

```python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def cli(verbose):
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
```

which gives:

```shell
$ myhello --help
Usage: myhello [OPTIONS]

Options:
--verbose  Will print verbose messages.
--help     Show this message and exit.
$ myhello --verbose
We are in the verbose mode.
Hello World
```

## Standard options (take input)
```python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', default='', help='Who are you?')
def cli(verbose,name):
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    click.echo('Bye {0}'.format(name))
```

Result:

```shell
$ myhello --help
Usage: myhello [OPTIONS]

Options:
--verbose    Will print verbose messages.
--name TEXT  Who are you?
--help       Show this message and exit.
$ myhello
Hello World
Bye
$ myhello --name kushal
Hello World
Bye kushal
```

## Same option multiple times + docstring

```python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', '-n', multiple=True, default='', help='Who are you?')
def cli(verbose,name):
    """This is an example script to learn Click."""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    for n in name:
        click.echo('Bye {0}'.format(n))
```

Result:

```shell
$ myhello --help
Usage: myhello [OPTIONS]

This is an example script to learn Click.

Options:
--verbose        Will print verbose messages.
-n, --name TEXT  Who are you?
--help           Show this message and exit.
```

## Super fast way to accept password w/ confirmation

```python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', '-n', multiple=True, default='', help='Who are you?')
@click.password_option()
def cli(verbose,name, password):
    """This is an example script to learn Click."""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    for n in name:
        click.echo('Bye {0}'.format(n))
        
    # Never do this in the real situation:    
    click.echo('We received {0} as password.'.format(password))
    
```

Output:

```shell
$ myhello --help
Usage: myhello [OPTIONS]

This is an example script to learn Click.

Options:
--verbose        Will print verbose messages.
-n, --name TEXT  Who are you?
--password TEXT
--help           Show this message and exit.
$ myhello
Password:
Repeat for confirmation:
Hello World
We received hello as password.
```

## None-optional arguments

```python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', '-n', multiple=True, default='', help='Who are you?')
@click.argument('country') # default: a string
def cli(verbose,name, country):
    """This is an example script to learn Click."""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello {0}".format(country))
    for n in name:
        click.echo('Bye {0}'.format(n))
```

Output:

```shell
$ myhello
Usage: myhello [OPTIONS] COUNTRY

Error: Missing argument "country".
$ myhello India
Hello India
```

## Further reading:

[Click Project](https://palletsprojects.com/p/click/)
[Click documation](https://click.palletsprojects.com/en/7.x/)
[Author:Armin Ronacher](https://lucumr.pocoo.org/about/)

