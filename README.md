# Collatz conjecture explorer

A command-line tool for exploring the **Collatz conjecture** - one of the most famous unsolved problems in mathematics.

---

## The Conjecture

Take any positive integer $n$ and apply the following rule repeatedly:

$$f(n) = \begin{cases} \dfrac{n}{2} & \text{if } n \text{ is even} \\ 3n + 1 & \text{if } n \text{ is odd} \end{cases}$$

The conjecture states that **no matter what positive integer you start with, you will always eventually reach 1**.

For example, starting from **6**:

```
6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
```

That is 8 steps. Nobody has found a counterexample, and nobody has proven it always works - hence the mystery.

---

## Requirements

- Python 3.10+
- matplotlib

```bash
pip install matplotlib
```

---

## Usage

```
python3 collatz.py -n N [-m MODE]
python3 collatz.py -s N
```

| Flag | Long form | Description |
|------|-----------|-------------|
| `-n N` | `--number N` | Analyse integers from **1 to N** (N ≥ 1) |
| `-m MODE` | `--mode MODE` | Output mode: `sequence`, `count`, `plot`, `stats`, or `records` (default: `plot`) |
| `-s N` | `--single N` | Print sequence and step count for a single number N |

Running the script **without any arguments** displays this help message and exits.

```bash
python3 collatz.py
```

---

## Modes

### `sequence` - full sequences

Prints every value in the Collatz sequence together with the total step count.

```bash
python3 collatz.py -n 6 -m sequence
```

```
Number of iterations for 1: 0
1

Number of iterations for 2: 1
2 -> 1

Number of iterations for 3: 7
3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1

Number of iterations for 4: 2
4 -> 2 -> 1

Number of iterations for 5: 5
5 -> 16 -> 8 -> 4 -> 2 -> 1

Number of iterations for 6: 8
6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
```

Use `-s` to show the sequence for a single number only:

```bash
python3 collatz.py -s 100
```

```
Number of iterations for 100: 25
100 -> 50 -> 25 -> 76 -> 38 -> 19 -> 58 -> 29 -> 88 -> 44 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
```

---

### `count` - step counts only

Prints only the number of steps for each integer - useful for larger ranges.

```bash
python3 collatz.py -n 6 -m count
```

```
Number of iterations for 1: 0
Number of iterations for 2: 1
Number of iterations for 3: 7
Number of iterations for 4: 2
Number of iterations for 5: 5
Number of iterations for 6: 8
```

Use `-s` to show the step count for a single number only:

```bash
python3 collatz.py -s 100
```

```
Number of iterations for 100: 25
100 -> 50 -> 25 -> 76 -> 38 -> 19 -> 58 -> 29 -> 88 -> 44 -> 22 -> 11 -> 34 -> 17 -> 52 -> 26 -> 13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
```

---

### `plot` - interactive chart *(default)*

Opens an interactive matplotlib window showing a line-and-scatter chart of step counts vs. starting number.

```bash
python3 collatz.py -n 500 -m plot
# or equivalently:
python3 collatz.py -n 500
```

The chart highlights the chaotic, unpredictable nature of the sequence - nearby numbers can take wildly different numbers of steps to reach 1.

---

### `stats` - statistical analysis

Prints a text summary (mean, median, standard deviation, max steps, max peak) and opens a two-panel chart:
- **left** - histogram of sequence lengths,
- **right** - scatter plot of the peak value reached per starting number.

```bash
python3 collatz.py -n 500 -m stats
```

```
Statistical summary for n = 1..500:
  Mean steps:    52.29
  Median steps:  35.0
  Spread of steps: 39.40
  Max steps:     143  (n = 327)
  Max peak:      39364  (n = 447)
```

---

### `records` - record-breaking sequences

Prints every integer that sets a new all-time record for:
- **sequence length** - more steps than any smaller starting number (OEIS A006577),
- **peak value** - higher maximum value than any smaller starting number (OEIS A006884).

```bash
python3 collatz.py -n 500 -m records
```

```
Record sequence lengths (1..500):
         n     steps
  ────────  ────────
       327       143
       313       130
       231       127
       171       124
       129       121
        97       118
        73       115
        54       112
        27       111
        25        23

Record peak values (1..500):
         n              peak
  ────────  ────────────────
       447             39364
       255             13120
        27              9232
        15               160
         7                52
         3                16
         2                 2
         1                 1
```
