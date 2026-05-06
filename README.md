Final Software Design 

The final design for the FillBot software is user-friendly while efficiently converting inputs into an OT-2 run file. The process begins with an excel file that allows user input for: Sample ID, volume of protein solution, well of protein solution, volume of DMSO, well of DMSO, and volume to move into the NMR tube.  This file is then uploaded into the FillBot UI, where the user answers two questions before the final script is generated. The output is created by inserting these user-provided values into a predefined protocol template. 

A CSV file input was chosen because it is a simple software that many are familiar with. Additionally, CSV files can also be the output of user-designed code, allowing users to produce files encompassing large sample libraries for their experiments rather than filling it out by hand. The file is structured so that all locations in a 96-well plate are in Column A, and all variables can be filled out in the columns that follow, within the row of the desired well. It is necessary that the given template is followed, as file parsing is based on the column that the data is inputted in. For example, “Column B” will always be the input for Sample ID, regardless of what the header may be changed to.  

 

 

 

 

 

Figure 1: FillBot CSV File 

There are three primary Python scripts relevant to the FillBot. The first is one titled “FillBot_FileInput.” This script outputs the popup UI. Within this UI, there is a location to upload the user’s excel file. The values within the excel file are parsed and defined as variables in a string. Because these variables are oriented together, it is simple to use them within the FillBot System, as progressing within a loop will reach every variable in the correct order. The user then progresses through the FillBot UI, which further utilizes the tkinter package to output a graphic. This graphic includes the Sample IDs in their respective well, giving the user the opportunity to double check their samples before beginning. The FillBot UI was designed to include as few user inputs as possible. As it stands, the only user input is the type of labware desired for the protein solution and whether one or two output files are desired.  

 

Figure 2: FillBot UI before and after uploading CSV  

These user inputs are intentionally kept simple. The protein labware defaults to “opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap,” which allows the user to make modifications, if necessary, but can also keep the standard. If the user selects one output file, the entire FillBot OT-2 run file is given in bulk. This protocol includes a pause step in the middle to allow the user to attach the sleeve after the initial sample preparation stages. If the user selects two output files, one file will include the sample preparation steps, and the other will include the steps requiring the FillBot Sleeve on the arm.  

This option leads to the remaining “protocol_template” python files. These files include the exact protocol that the OT-2 will follow during the run but misses the necessary variables from the user input. Once one option, mentioned above, is selected, the variables from the input file replace the missing variable locations in the “protocol_template” file. This generates the final “FillBot_Output_File,” which is ready to be uploaded into the Opentrons API to begin the run. 
