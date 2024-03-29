import argparse, csv, subprocess, json, os, re
from zipfile import ZipFile

# Parse user arguments
parser = argparse.ArgumentParser(description='Compiles and grades java assignments.')
parser.add_argument('submissions', help='The zip file downloaded from coursesite')  # Positional argument
parser.add_argument('config', help='The JSON file which contains the test cases')
parser.add_argument('-m', '--manual', help='If you want to grade in manual mode. Output for each test case must be checked manually. Useful if students have leeway with their output format and it can\'t be checked automatically.', action='store_const', const=True, default=False, required=False)
args = parser.parse_args()

# Parse the JSON file
with open(args.config, 'r') as config_json:
    json_data = json.load(config_json)
    test_suite = json_data['test_suite']
    main_file = json_data['main_file']
    compilation_points = json_data['compilation_points']
    total_points = compilation_points + sum(test['points'] for test in test_suite)

# Open & Extract the zip
with ZipFile(args.submissions, 'r') as sub_zip:
    sub_dir = sub_zip.filename[:-4]  # slice to get rid of .zip at the end.
    sub_zip.extractall(path=sub_dir)

# Move us into the directory we created
os.chdir('./{}'.format(sub_dir))
results = []

# Sorted by lastname, then firstname
for directory_name in sorted(os.listdir('.'), key=lambda d: tuple(reversed(d.split('_')[0].rsplit(' ', 1)))):
    test_results = []
    running_total = 0
    # Assuming format like "Antonio Lia_7754335_assignsubmission_file_"
    first_name, last_name = directory_name.split('_')[0].rsplit(' ', 1)
    os.chdir('./{}'.format(directory_name))  # switch into the directory
    # FIXME: This assumes javac is in your path.
    javac_proc = subprocess.run(["javac", "*.java"])

    if javac_proc.returncode != 0:
        # Compile error.
        # TODO: The csv data can be numerical values, percentages, true / false, anything really... Change later
        sub_info = {"first_name": first_name, "last_name": last_name, "compile_points": 0}
        for index, test in enumerate(test_suite):
            sub_info['test_{}_points'.format(index)] = 0
        sub_info['points_sum'] = 0
        sub_info['percentage'] = 0
        results.append(sub_info)

        if args.manual:
            print('{} failed to compile.'.format(first_name + ' ' + last_name))
            input()

    else:
        # Note that it compiled if manual mode.
        if args.manual:
            print('{} compiled successfully.'.format(first_name + ' ' + last_name))
            input()

        # Run the test suite
        sub_info = {"first_name": first_name, "last_name": last_name, "compile_points": compilation_points}
        for index, test in enumerate(test_suite):
            # FIXME: This assumes java is in your path.
            java_run_proc = subprocess.run(['java', main_file, test['args']], input=test['input'], capture_output=True)
            # FIXME: This compares the raw b'' string. Is this what we want? Needs testing...
            if str(java_run_proc.stdout).strip() == test['output'].strip():
                points = test['points']
            else:
                points = 0

            running_total += points
            sub_info['test_{}_points'.format(index)] = points

            # Manual mode check of output.
            if args.manual:
                print('Test: {} args: {} stdin: {}'.format(index, test['args'], test['input']))
                print('stdout:')
                print(java_run_proc.stdout.decode())
                print('stderr:')
                print(java_run_proc.stderr.decode())
                input()

        # add final columns
        sub_info['points_sum'] = running_total
        sub_info['percentage'] = running_total / total_points
        results.append(sub_info)
    os.chdir('..')  # Get out of the directory

# Sort the results by last name
# TODO: Could sort by other things like grade instead.
results.sort(key=lambda x: x['last_name'])

# Now format the results and put into a CSV
with open('grades.csv', 'w', newline='') as grades_csv:
    fieldnames = ['first_name', 'last_name', 'compile_points']
    for index, test in enumerate(test_suite):
        fieldnames.append('test_{}_points'.format(index))
    fieldnames.append('points_sum')
    fieldnames.append('percentage')

    writer = csv.DictWriter(grades_csv, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)