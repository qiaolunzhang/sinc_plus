To run the heuristics execute the SMART_SINC_SINC.py file.
Input files are read in the "DatFiles" folder. Note that all input files ("DataFile.dat") have the same structure and this must not be changed,
since the specific data are read in specific positions in the files.

The program is initialized to run "DataFile1.dat", but you can change the number of files simply specifying a different "start_file" (from 1 to 10)
or a different "end_file" (from 1 to 10).
The specific survivability scenario to be simulated must be also specified, setting parameter "scenario":

1) scenario=1 -> Survivability scenario 1 (SVNM min Wavelengths)
2) scenario=2 -> Survivability scenario 2 (SVNM max Availability)
3) scenario=3 -> Survivability scenarios 3 and 5 (Two-step SINC min Wavelengths and One-step SINC min Wavelengths)
4) scenario=4 -> Survivability scenarios 4 and 6 (Two-step SINC max Availability and One-step SINC max Availability)
5) scenario=7 -> Survivability scenario 7 (One-step SINC+ min Wavelengths)


Output values (over the selected data files):
1- Min, Max and Mean of total wavelength consumption
2- Min, Max and Mean number of surviving virtual networks (numerator of the formula to compute the availability)
3- Min, Max and Mean availability
4- Total execution time
