from collections import defaultdict
from enum import Enum
from turtle import up
from typing import List, Tuple, Type

import typer

from database import Database
from reference_table import reference_table

app = typer.Typer()
SubTypes = Enum(
    'SubTypes', 
    {sub_type:sub_type for sub_type in reference_table.index.to_list()}
)

@app.command()
def calculate(
    slot: int = typer.Argument(...),
    rune_type: str = typer.Argument(...),
    location: str = typer.Argument('storage'),
    up_status: str = typer.Argument("+0"),
    sub_value: List[int] = typer.Option([]),
    sub_type: List[SubTypes] = typer.Option([])
):
    result = {
        'location': location,
        'slot': slot,
        'type': rune_type,
        'subs': defaultdict(dict)
    }
    for type, current_value in list(zip(sub_type, sub_value)):
        if up_status != '+12':
            min_value = reference_table.loc[type.value, "MIN START"]
            max_value = reference_table.loc[type.value, "MAX START"]
        else:
            min_value = reference_table.loc[type.value, "MIN START"]
            max_value = reference_table.loc[type.value, "MAX UP"]
        result['subs'][type.value]['value'] = current_value
        result['subs'][type.value]['quality'] = round((current_value - min_value) / (max_value - min_value), 6)

    Database().insert(result)
    typer.echo(result)


@app.command()
def verify(
    slot: int = typer.Argument(...),
    rune_type: str = typer.Argument(...),
    sub_type: SubTypes = typer.Option(...),
    location: str = typer.Argument('all'),
):
    if location == 'all':
        for rune in Database().find_among_all(slot, rune_type, sub_type.value):
            typer.echo(rune)

if __name__ == "__main__":
   app()