import click

from numverify.sorter.api.api import API
from numverify.sorter.local_files.local_files import LocalFiles


@click.group()
def cli():
    pass

@cli.command("phone")
@click.argument("number", default='+712345')
@click.option('-f','--file', type = click.File('r'))
def get_phone(number, file):
    number = file.read(20) if file is not None else number
    api = API()
    country = api.search_country(number)
    click.echo(country)

@cli.command("sort")
@click.argument('src',type=click.Path(exists=True, dir_okay=True))
@click.argument('dst',type=click.Path(exists=True, dir_okay=True))
def sort(src,dst):
    lf = LocalFiles(src, dst)
    lf.prepare_paths()
    lf.move_phone()

if __name__ == '__main__':
    cli()