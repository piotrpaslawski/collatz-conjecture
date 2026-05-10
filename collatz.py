import sys
import argparse
import statistics
import matplotlib.pyplot as plt


def collatz(n: int) -> int:
    """
    Calculates one step of the Collatz function.

    Args:
        n: A positive integer.

    Returns:
        n // 2 if n is even, otherwise 3 * n + 1.
    """
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_sequence(n: int) -> list[int]:
    """
    Generates the full Collatz sequence for a given number,
    starting from n until it reaches 1.

    Args:
        n: A positive integer (starting value).

    Returns:
        A list of integers representing every value in the sequence.
    """
    seq = [n]
    while n != 1:
        n = collatz(n)
        seq.append(n)
    return seq


def count_iterations(n: int) -> int:
    """
    Counts the number of steps needed to reach 1 from n.

    Args:
        n: A positive integer (starting value).

    Returns:
        The number of Collatz steps required to reach 1.
    """
    steps = 0
    while n != 1:
        n = collatz(n)
        steps += 1
    return steps


def peak_value(n: int) -> int:
    """
    Returns the maximum value reached in the Collatz sequence for a number starting from n.

    Args:
        n: A positive integer (starting value).

    Returns:
        The largest integer encountered before the sequence reaches 1.
    """
    return max(collatz_sequence(n))


def print_sequences(max_number: int):
    """
    Prints the full Collatz sequences and step counts for each integer from 1 to max_number.

    Args:
        max_number: Upper bound (inclusive) of the range to analyse.
    """
    for i in range(1, max_number + 1):
        seq = collatz_sequence(i)
        print(f"Number of iterations for {i}: {len(seq) - 1}")
        print(" -> ".join(map(str, seq)))
        print()


def print_single_sequence(n: int):
    """
    Prints the full Collatz sequence and step count for a single number n.

    Args:
        n: A positive integer.
    """
    seq = collatz_sequence(n)
    print(f"Number of iterations for {n}: {len(seq) - 1}")
    print(" -> ".join(map(str, seq)))


def print_counts(max_number: int):
    """
    Prints only the step counts for each integer from 1 to max_number.

    Args:
        max_number: Upper bound (inclusive) of the range to analyse.
    """
    for i in range(1, max_number + 1):
        print(f"Number of iterations for {i}: {count_iterations(i)}")


def plot_iterations(max_number: int):
    """
    Creates a plot of the number of Collatz steps for each integer from 1 to max_number.

    Args:
        max_number: Upper bound (inclusive) of the range to plot.
    """
    numbers = list(range(1, max_number + 1))
    iterations = [count_iterations(i) for i in numbers]

    plt.figure(figsize=(10, 5))
    plt.plot(numbers, iterations, linewidth=0.8, color="steelblue")
    plt.scatter(numbers, iterations, s=10, color="orangered", zorder=3)
    plt.xlabel("Number")
    plt.ylabel("Iterations")
    plt.title(f"Collatz iterations for numbers 1–{max_number}")
    ax = plt.gca()
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.format_coord = lambda x, y: f"x={round(x)}, y={round(y)}"
    plt.tight_layout()
    plt.show()


def plot_stats(max_number: int):
    """
    Displays statistical analysis of Collatz sequences for integers from 1 to max_number.

    Prints a text summary (mean, median, std dev, max steps, max peak) and shows
    two plots side by side: a histogram of sequence lengths and a scatter plot of
    peak values reached per starting number.

    Args:
        max_number: Upper bound (inclusive) of the range to analyse.
    """
    numbers = list(range(1, max_number + 1))
    iters = [count_iterations(i) for i in numbers]
    peaks = [peak_value(i) for i in numbers]

    max_iters = max(iters)
    max_iters_n = numbers[iters.index(max_iters)]
    max_peak = max(peaks)
    max_peak_n = numbers[peaks.index(max_peak)]

    print(f"Statistical summary for n = 1..{max_number}:")
    print(f"  Mean steps:    {statistics.mean(iters):.2f}")
    print(f"  Median steps:  {statistics.median(iters):.1f}")
    print(f"  Spread of steps: {(statistics.stdev(iters) if len(iters) > 1 else 0.0):.2f}")
    print(f"  Max steps:     {max_iters}  (n = {max_iters_n})")
    print(f"  Max peak:      {max_peak}  (n = {max_peak_n})")

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.hist(iters, bins=min(40, max_iters), color="steelblue", edgecolor="white")
    ax1.set_xlabel("Steps to reach 1")
    ax1.set_ylabel("Count")
    ax1.set_title(f"Distribution of sequence lengths (1–{max_number})")
    ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax1.format_coord = lambda x, y: f"x={round(x)}, y={round(y)}"

    ax2.scatter(numbers, peaks, s=8, color="darkorange", alpha=0.7)
    ax2.set_xlabel("Starting number n")
    ax2.set_ylabel("Peak value in sequence")
    ax2.set_title(f"Peak values for n = 1–{max_number}")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
    ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax2.format_coord = lambda x, y: f"x={round(x)}, y={round(y)}"

    plt.tight_layout()
    plt.show()


def print_records(max_number: int):
    """
    Finds and prints all integers that set a new record for sequence length or peak value.
    These correspond to OEIS sequences A006577 (step records) and A006884 (peak records).

    Args:
        max_number: Upper bound (inclusive) of the range to search.
    """
    record_steps = -1
    record_peak = -1
    step_records: list[tuple[int, int]] = []
    peak_records: list[tuple[int, int]] = []

    for n in range(1, max_number + 1):
        seq = collatz_sequence(n)
        steps = len(seq) - 1
        peak = max(seq)

        if steps > record_steps:
            record_steps = steps
            step_records.append((n, steps))
        if peak > record_peak:
            record_peak = peak
            peak_records.append((n, peak))

    print(f"Record sequence lengths (1..{max_number}):")
    print(f"  {'n':>8}  {'steps':>8}")
    print(f"  {'─' * 8}  {'─' * 8}")
    for n, s in list(reversed(step_records))[:10]:
        print(f"  {n:>8}  {s:>8}")

    print()
    print(f"Record peak values (1..{max_number}):")
    print(f"  {'n':>8}  {'peak':>16}")
    print(f"  {'─' * 8}  {'─' * 16}")
    for n, p in list(reversed(peak_records))[:10]:
        print(f"  {n:>8}  {p:>16}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog="collatz.py",
        description=(
            "Collatz conjecture explorer\n\n"
            "Analyse the Collatz sequence for integers from 1 to N.\n\n"
            "Collatz function:\n"
            "  f(n) = n / 2     if n is even\n"
            "  f(n) = 3n + 1    if n is odd\n\n"
            "The conjecture states that every positive integer eventually reaches 1\n"
            "(more precisely, it enters the cycle 4 -> 2 -> 1 -> 4 -> 2 -> 1 -> …)."
        ),
        epilog=(
            "Examples:\n"
            "  python3 collatz.py -n 20  -m sequence\n"
            "  python3 collatz.py -n 100 -m count\n"
            "  python3 collatz.py -n 500 -m plot\n"
            "  python3 collatz.py -n 500 -m stats\n"
            "  python3 collatz.py -n 500 -m records\n"
            "  python3 collatz.py -s 100"
        ),
    )

    parser.add_argument(
        "-n", "--number",
        type=int,
        required=False,
        metavar="N",
        help="analyse integers from 1 to N (must be >= 1)",
    )
    parser.add_argument(
        "-s", "--single",
        type=int,
        metavar="N",
        help="print sequence and step count for a single number N",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["sequence", "count", "plot", "stats", "records"],
        default="plot",
        metavar="MODE",
        help=(
            "output mode:\n"
            "- 'sequence'  prints full sequences with step counts\n"
            "- 'count'     prints step counts only\n"
            "- 'plot'      interactive step-count chart (default)\n"
            "- 'stats'     histogram of lengths + peak-value scatter + summary\n"
            "- 'records'   numbers with record-breaking length or peak"
        ),
    )
    return parser


def main():
    """
    Parses command-line arguments and dispatches to the
    appropriate analysis function based on the chosen mode.
    """
    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.single is not None:
        if args.single < 1:
            parser.error("N must be a positive integer (>= 1).")
        print_single_sequence(args.single)
        return

    if args.number is None:
        parser.error("one of the arguments -n/--number or -s/--single is required.")
    if args.number < 1:
        parser.error("N must be a positive integer (>= 1).")

    mode = args.mode or "plot"
    dispatch = {
        "sequence": print_sequences,
        "count":    print_counts,
        "plot":     plot_iterations,
        "stats":    plot_stats,
        "records":  print_records,
    }
    dispatch[mode](args.number)


if __name__ == "__main__":
    main()
