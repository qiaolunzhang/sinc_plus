To run the ILP models select the .run file that you want to execute and check which .mod file are you executing.

The .run files are set for executing 10 data files which names are from "DataFile1.dat" to "DataFile10.dat" and which are positioned
in a folder "DatFiles". 
If you want to change the starting file, as well as the number of data files, change respectively the values of parameters "start_file" 
and "num_datafile" in the .run files.

To run different .dat files change the name of these files in the .run files.


List of all .run files and the survivability scenarios to which they correspond:

1) Test_Scenarios_1_2_6.run -> Survivability scenarios 1,2 and 6 (SVNM min Wave, SVNM max Av and One-step SINC max Av)
2) Test_Scenario3.run -> Survivability scenario 3 (Two-step SINC min Wave)
3) Test_Scenario4.run -> Survivability scenario 4 (Two-step SINC max Av)
4) Test_Scenario5.run -> Survivability scenario 5 (One-step SINC min Wave)
5) Test_Scenario7.run -> Survivability scenario 7 (One-step SINC+ min Wave)
6) Test_SVNMagainstDouble -> SVNM against double link failures

Note that in Test_Scenarios_1_2_6.run you have to select which .mod file you want to execute between the following ones:
1) SVNM_MinWave.mod (survivability scenario 1)
2) SVNM_MaxAV.mod (survivability scenario 2)
3) One-step_SINC_MaxAv.mod (survivability scenario 6)

Each .run file gives as output the following values:
1- Min, Max and Mean of total wavelength consumption
2- Min, Max and Mean number of surviving virtual networks (numerator of the formula to compute the availability)
3- Min, Max and Mean availability
4- Total execution time
