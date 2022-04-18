from collections import defaultdict
from enum import Enum
from turtle import up
from typing import List, Tuple, Type

import typer

from reference_table import reference_table

app = typer.Typer()
SubTypes = Enum(
    'SubTypes', 
    {sub_type:sub_type for sub_type in reference_table.index.to_list()}
)

@app.command()
def calculate(
    location: str = typer.Argument('storage'),
    slot: int = typer.Argument(...),
    up_status: str = typer.Argument("+0"),
    sub_value: List[int] = typer.Option([]),
    sub_type: List[SubTypes] = typer.Option([])
):
    result = {
        'location': location,
        'slot': slot,
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

    typer.echo(result)


if __name__ == "__main__":
    typer.run(calculate)