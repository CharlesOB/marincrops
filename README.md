# marincrops
An interpreted esolang inspired by an enlistment in the United States Marine Corps.

marincrops is a esoteric scripting language that is designed to make you feel micromanaged, to run slowly, and to waste all its money on things that do not matter, like paint for a condemned barracks. 

# Running a script
File names end in .rah and are run with the marincrops interpreter.
```
python marincrops.py hello_world.rah
```

# Writing a script
## Variable Names
Variables names have two parts, rank and name. Currently, only enlisted ranks have been implemented. These are case-sensitive and include "Pvt", "PFC", "LCpl", "Cpl", "Sgt", "SSgt", "GySgt", "MSgt", "1stSgt", "MGySgt", and "SgtMaj". The name is also case-sensitive and must always be capitalized. Names can include any character that is not a space or double quotation mark. It is a new marincrops. Some example variable names:
```
Pvt Foo
LCpl Bar
Cpl Test1
Sgt Test-2
SSgt O'Brien
```
Variables with different rank, but the same name are different variables. `PFC Schmuckatelli` and `LCpl Schmuckatelli` are not the same variable and can have different values.
## Data Types
In marincrops, there are currently 3 data types: integers, booleans, and strings. In the future there will be an implementation of a fourth datatype, the roster (list). 
### Integers
Integer numbers in marincrops are represented as a number of crayons. Some examples of assigning integer values to variables.
```
Sgt Foo has 3 crayons
Cpl Bar has no crayons
LCpl Schmuckatelli has a crayon
Pvt FooBar has 100 crayons
```
Notice that 0 must always be represented as `no crayons` and 1 must be written `a crayon`. Also, if the plurality of the crayon keyword does not match the integer represented, the interpreter will raise a "Grammar for Marines" error.
### Booleans
Booleans are represented with `yes sir` and `no sir`. These will always be lower-case.
```
GySgt Goo has yes sir
MSgt Gar has no sir
```
### Strings
String literals are written using double quotation marks. marincrops recognizes three escaped characters: the newline, tab, escaped backslash, and escaped double quotation mark. A string containing all of these:
```
Sgt String has "\"\n\t\\"
```
## Functions
### Syntax
Function names begin with a capital letter and include only alphanumeric characters or underscores. A function is ran with the `aye sir` keyword. In the example, `Go_away` terminates the program.
```
Go_away aye sir
```
Any number of parameters can be passed to the function as a suffix before the `aye sir` keyword. In marincrops, parameters are separated with the keyword `and` instead of commas. In the example, `Scream` is a function that prints to the screen.
```
Scream "Good morning!" aye sir
Scream Sgt Foo and Sgt Bar aye sir
```
One parameter can be passed to a function call as a prefix. The two lines below are equivalent.
```
"Hello world!" Scream aye sir
Scream "Hello world!" aye sir
```
Prefix and suffix parameters can be mixed and matched, and function calls can be nested. `One_more_than` is a function that returns its parameter incremented by 1. The following program excerpt prints a "2" to the screen in multiple, equivalent ways.
```
Sgt Foo has a crayon
Scream One_more_than Sgt Foo aye sir aye sir
Scream Sgt Foo One_more_than aye sir aye sir
Sgt Foo One_more_than aye sir Scream aye sir
One_more_than Sgt Foo aye sir Scream aye sir
```
### Some Useful Built-ins
#### `Scream`
`Scream` prints its parameters to the screen. It always prints in all upper-case and accepts any number of parameters, printing without separators. The following lines print "HELLO WORLD!" 3 times.
```
Scream "Hello world!\n" aye sir
Scream "Hello " and "world!\n" aye sir

Scream "Hel" and "lo" and " " aye sir
Scream "WORLD!\n" aye sir
```
#### `Next_motivator`
`Next_motivator` takes input from the user. The excerpt takes one line of user input and then prints it to the screen in all capitals.
```
Sgt Input has Next_motivator aye sir
Scream Sgt Input aye sir
```
#### `One_more_than` and `One_less_than`
These functions take an integer and add or subtract 1 from it. There are no general addition, subtraction, multiplication, division, or modulus functions. This is to remind you that you should have chosen a different branch. If you want one of those functions, you have to write one yourself.
#### `Has`, `Has_less_than`, `Has_more_than`
Not to be confused with the assignment keyword `has`, `Has` is a function that returns a boolean if both parameters have the same value (==). `Has_more_than` and `Has_less_than` are comparative functions returning booleans. The following script excerpt prints "YES SIR" to the screen 3 times.
```
Cpl Bar has 5 crayons
Scream Cpl Bar Has 5 crayons aye sir aye sir
Scream Cpl Bar Has_less_than 6 crayons aye sir aye sir
Scream Cpl Bar Has_more_than 4 crayons aye sir aye sir
```
#### `Is`
`Is` is the lesser-known cousin of `Has`. The two functions are exactly the same in functionality; however, `Has` sometimes makes more grammatical sense. 
#### `Go_away`
`Go_away` terminates the program. If a program reaches the end of the file without being told to terminate, an error will be raised. All programs must end with `Go_away aye sir`.
#### `Louder`
When the marincrops interpreter runs into an error, it will always print an error of "SCREAM LOUDER" unless the programmer has already called the `Louder` function. If you get a "SCREAM LOUDER" error, you need to add `Louder aye sir` to your program (prefferably at the beginning).
## Key Phrases and Flow Control
### Key Phrases
Key phrases all start with lower-case letters and tell the interpreter how to run blocks of code. 
#### `attention on deck` and `good morning sir`
The key phrase `attention on deck` tells the interpreter that all code in the lines following the greeting is executable code. `attention on deck` will always be immediately followed by `good morning sir`, `good afternoon sir`, or `good evening sir` on the next line. The greeting must be a proper greeting, according to the local time on the machine running the script. Use `good morning sir` between 0000 and 1200, `good afternoon sir` between 1200 and 1800, and `good evening sir` between 1800 and 0000. 
#### `i heard through the lance corporal underground`
A comment block is started with `i heard through the lance corporal underground` on its own line and ended with the `attention on deck` key phrase. Every line in a comment block must end in " sir".
```
i heard through the lance corporal underground
This is a comment sir
This is the comment second line sir
and third line sir
attention on deck
good morning sir
```
### Flow Control
#### `trust`, `but verify`, `kill`
A conditional block is denoted by the keyword `trust` and ended with the keyword `kill`. In the future, this block will also contain a `but verify` clause, but that is currently unimplemented. The syntax is 
```
trust {boolean condition}, frickin
  {program statements}
kill
```
#### `i have a saved round`, `any more saved rounds?`, and `carry on`
These keywords are used to signal the beginning and end of a looping block and to break the loop, respectively. marincrops does not support any looping structure like a conditional while loop: only infinite loops stopped by a loop break. The following snippet prints "GOOD MORNING SIR" 5 times.
```
Cpl Count has no crayons
i have a saved round, frickin
  trust Cpl Count Has_more_than 4 crayons aye sir, frickin
    carry on
  kill
  Scream "good morning sir\n" aye sir
  Cpl Count has One_more_than Cpl Count aye sir 
any more saved rounds?
```
#### `let's break Foo down barney-style`, `BAMCIS`, and `motivate`
A function is defined with the phrase `let's break Foo down barney-style` where `Foo` is the function to define. A function definition block is ended with the keyword `BAMCIS` on its own line (the only keyword that is capitalized). To make a function return a value, use the keyword `motivate`. The excerpt defines a function to print "GOOD MORNING" to the screen and then executes it.
```
let's break Scream_good_morning down barney-style, frickin
  Scream "good morning\n" aye sir
BAMCIS

Scream_good_morning aye sir
```
Parameters are added to function definitions using a `for` clause in the `let's break Foo down barney-style` line. Parameters are separated by `and` and must be valid variable names. The following prints "HELLO WORLD!" by defining a function that prints two variables to the screen followed by a newline. 
```
let's break Scream2 down barney-style for Cpl First and Cpl Second, frickin
  Scream Cpl First and Cpl Second and "\n" aye sir
BAMCIS

Scream2 "Hello " and "world!" aye sir
```
An example that returns a value:
```
let's break Two_more_than down barney-style for PFC Int, frickin
  motivate One_more_than One_more_than PFC Int aye sir aye sir
BAMCIS
```
# Conclusion
I am sorry that this exists. 

Also check out the example scripts in this repo.
