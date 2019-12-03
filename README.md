# Coursesite-Autograder
Python script to automate grading of coursesite submitted java assignments.

## Notes
- Select student submissions on coursesite, then navigate to the bottom of the page and select 

"***with selected...*** \[Download selected submissions\]"
  - This will produce the `.zip` submission file which is required for the program.
- Tested with python 3.7
- Expects that student submitted raw .java files with no directory structure
- The json config must be changed for every assignment.
  - main_file refers to the java file which contains the main method
  - Points are awarded if the program passes that check (successfully compiles, passes a testcase, etc..)
- Outputs a CSV of the grades
- `java` and `javac` must be in your path.

#### Manual mode
`-m` or `-manual` allows the grader to manually check the output of each test case for each student. 
This is ideal when students have some leeway in their output.
This is many times faster than running their java files 4 or 5 times to check their program against all input edge cases.

The autograder grades students ordered by their last name. 
This makes it easy to input grades into coursesite while running.

Press `ENTER` to advance in manual mode.

## Example
`python .\autograde.py -m '.\CSE-017-010, 011-FL19-Programming Assignment 3-1610419.zip' .\eightqueens_config.json`
