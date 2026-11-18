#!/usr/bin/env python3
"""
Numeric limits explorer — красиво печатает min/max для всех числовых типов Python.
"""
import sys
import math
from decimal import getcontext

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich import box
except ImportError:
    sys.exit("Установите 'rich':  pip install rich")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def fmt(x: float) -> str:
    if math.isinf(x):
        return "−∞" if x < 0 else "+∞"
    return f"{x:.6e}"


def main() -> None:
    console = Console()
    console.print(Panel.fit(
        "[bold cyan]🐍  Python Numeric Types — Min / Max[/]",
        border_style="bright_blue",
        padding=(0, 2),
    ))

    finfo = sys.float_info
    ctx = getcontext()

    # ── стандартная библиотека ─────────────────────────────────────────────
    table = Table(
        title="[bold]Standard library[/]",
        box=box.ROUNDED,
        header_style="bold magenta",
        show_lines=True,
        expand=True,
    )
    table.add_column("Type", style="bold cyan", no_wrap=True)
    table.add_column("Min", style="green")
    table.add_column("Max", style="red")
    table.add_column("Notes", style="dim")

    table.add_row(
        "int", "−∞ (unbounded)", "+∞ (unbounded)",
        f"arbitrary precision · sys.maxsize = {sys.maxsize}",
    )
    table.add_row(
        "bool", "False", "True",
        "subclass of int",
    )
    table.add_row(
        "float", fmt(-finfo.max), fmt(finfo.max),
        f"IEEE-754 binary64 · min normal = {finfo.min:.3e} · "
        f"epsilon = {finfo.epsilon:.3e} · mantissa digits = {finfo.dig}",
    )
    table.add_row(
        "complex", f"{fmt(-finfo.max)} (per part)", f"{fmt(finfo.max)} (per part)",
        "unordered · каждая часть — float",
    )
    table.add_row(
        "Decimal", "−Infinity", "Infinity",
        f"context: prec={ctx.prec}, Emax={ctx.Emax}, Emin={ctx.Emin}",
    )
    table.add_row(
        "Fraction", "−∞ (unbounded)", "+∞ (unbounded)",
        "числитель и знаменатель — int (неограничены)",
    )

    console.print(table)

    # ── NumPy (если установлен) ────────────────────────────────────────────
    if HAS_NUMPY:
        console.print()
        np_table = Table(
            title="[bold]NumPy fixed-width types[/]",
            box=box.ROUNDED,
            header_style="bold magenta",
            show_lines=True,
            expand=True,
        )
        np_table.add_column("Type", style="bold cyan", no_wrap=True)
        np_table.add_column("Min", style="green")
        np_table.add_column("Max", style="red")
        np_table.add_column("Bits", style="yellow", justify="right")

        for t in (np.int8,  np.int16,  np.int32,  np.int64,
                  np.uint8, np.uint16, np.uint32, np.uint64,
                  np.float16, np.float32, np.float64):
            info = np.iinfo(t) if np.issubdtype(t, np.integer) else np.finfo(t)
            np_table.add_row(
                t.__name__,
                str(info.min),
                str(info.max),
                str(np.dtype(t).itemsize * 8),
            )
        console.print(np_table)
    else:
        console.print()
        console.print(Panel(
            "[dim]NumPy не установлен. Поставьте его, чтобы увидеть пределы\n"
            "фиксированных целочисленных и вещественных типов:\n\n"
            "    [bold cyan]pip install numpy[/][/]",
            title="[dim]hint[/]",
            border_style="dim",
        ))

    console.print()
    console.print(Align.center(Text("✔ done", style="bold green")))


if __name__ == "__main__":
    main()