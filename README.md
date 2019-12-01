# Coursesite-Autograder
Python script to automate grading of coursesite submitted java assignments.

## Notes on usage
- Tested with python 3.7
- Expects that student submitted raw .java files with no directory structure
- The json config must be changed for every assignment.
  - main_file refers to the java file which contains the main method
  - Points are awarded if the program passes that check (successfully compiles, passes a testcase, etc..)
- Outputs a CSV of the grades

## Example
`python autograde.py --config example_config.json "CSE-017-010 Assignment 1 Submissions.zip"`
