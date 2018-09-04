# polynomial
Algebra system to do computations in polynomial rings

# Usage
In the command line or terminal, type

```
python main.py
```

# Current capabilities
Evaluates polynomial expressions (supports +,-,*,\/,^) correctly but negative signs are unsupported at the moment
E.g.
```
> 3 - 4
-1.0
```
works but
```
> -1 + 2
```
does not. Note all numbers are floats out of convenience currently.
Polynomial example
```
> (1 - x)^5
Polynomial: 1 - 5x + 10x^2 - 10x^3 + 5x^4 - x^5
```
