# python-calculator
basic calculator using RPN (reverse Polish notation)

## Usage
Run with

```nush
python3 main.py
```

This makes a prompt appear.

Above the prompt are four blank lines. They will show you the four latest stack entries.

If you type in a number or one of the built-in constants (`pi`, `tau`, `e`) and hit <kbd>Enter</kbd>, it will be added there.

If you type in a operator, it will execute it using the latest stack entry/entries.

It is also possible to enter multiple things at the same time, separated by spaces.

`5 6 7 / *` is equivalent to `5` <kbd>Enter</kbd> `6` <kbd>Enter</kbd> `7` <kbd>Enter</kbd> `/` <kbd>Enter</kbd> `*` <kbd>Enter</kbd>

## Operators
### Operators that use the latest *two* stack entries

| Operator     | Name      | Example               |
| ------------ | --------- | --------------------- |
| `+`          | Add       | `7 4 +`   →   11      |
| `-`          | Subtract  | `7 4 -`   →    3      |
| `/`          | Divide    | `7 4 /`   →    1.75   |
| `*`          | Multiply  | `7 4 *`   →   28      |
| `**` or `^`  | Power     | `7 4 **`  → 2401      |
| `mod` or `%` | Modulo    | `7 4 mod` →    3      |
| `log`        | Logarithm | `7 4 log` →    1.404… |

### Operators that use the latest *single* stack entry

| Operator           | Name                          | Example                  |
| ------------------ | ----------------------------- | ------------------------ |
| `round`            | Round (.5 to even)            | `7.5 round` →     8      |
| `ceil`             | Round up                      | `7.1 round` →     8      |
| `floor`            | Round down                    | `8.9 round` →     8      |
| `factorial` or `!` | Factorial                     | `8 !`       → 40320      |
| `abs`              | Absolute value                | `-23.8 abs` →    23.8    |
| `exp`              | (`e x **`)                    | `3 exp`     →    20.086… |
| `sqrt`             | Square Root (`x .5 **`)       | `16 sqrt`   →     4      |
| `ln`               | Natural logarithm (`x e log`) | `16 ln`     →     2.772… |

and the trigonometric functions `cos`, `sin`, `tan`, `acos`, `asin`, `atan`, all calulated in radians

## Special commands

| Command                                | Description                          |
| -------------------------------------- | ------------------------------------ |
| `help`                                 | Show simple help menu next to prompt |
| `exit` or <kbd>Ctrl</kbd>+<kbd>D</kbd> | End program                          |
| <kbd>Ctrl</kbd>+<kbd>C</kbd>           | Erase current line                   |
| `del`                                  | Delete latest stack entry            |
| `clear`                                | Delete all stack entries             |