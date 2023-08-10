# export-tts-devices
Script to export all devices in an The Things Stack Application. Creates a CSV file that can be imported into a different Things Stack application.

Usage:

    First use "ttn-lw-cli login" to authenticate with the browser to the 
    Things Account you want to export from. Then, use the following command, 
    substituting the appropriate command line parameters.

    ./export.py <Application ID to export> <output CSV file name>

    When importing the CSV file into Things, select "The Things Stack CSV" as the 
    file format.
