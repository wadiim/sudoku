# Sudoku

A sudoku solver and generator.

![](https://user-images.githubusercontent.com/33803413/74972761-9b56ce00-5422-11ea-94e4-04d945af2b71.png)

## Usage

```
sudoku.py [-h] [-s | -g GAPS] [--pretty]
```

When neither `-s` nor `-g` option is given, `sudoku.py` generates sudoku with random number of gaps.

### Options

Option | Meaning |
--- | ---
`-h`, `--help` | Show help message and exit.
`-s`, `--solve` | Solve sudoku.
`-g GAPS`, `--generate GAPS` | Generate sudoku with `GAPS` gaps.
`--pretty` | Pretty-print the results.

### Syntax

Sudoku is composed of digits and spaces.
Spaces indicate empty cells and are not intended to separate values.

#### Example

```
   64 2 8
76 1254
 3 8   65
  5  4 87
94 5 8  2
6 3 795
412     9
    5  24
359 82
```

## License

[MIT](https://github.com/wadiim/sudoku/blob/master/LICENSE)
