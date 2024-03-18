# ADB_LAOPDR
ADB-climate calculator project_Lao

## Work Flow
1. The data file from OSeMOSYS GUI or ESPEX (the data file creator for the carbon calculator) should be first pre processed using the <preprocess_data.py> file. Use the following code

    `python preprocess_data.py datafile.txt datafile_p.txt osemosys.txt osemosys_p.txt`

    **datafile.txt**: The orignal data file

    **datafile_p.txt**: The pre processed data file to be used for the optimisation process

    **osemosys.txt**: original osemosys code

    **osemosys_p.txt**: Preprocessed osemosys code

2. Run GLSOl to create the *.lp file

    `glpsol -m osemosys_p.txt -d datafile_p.txt --wlp lpfile.lp`

    **lpfile.lp**: the lp file created by glpsol

3. Run CBC or CPLEX to solve the model 

     CBC code 
     ---
      `cbc lpfile.lp solve -solu res_cbc.sol`
    
     CPLEX code
     ---
     `cplex -c "read lpfile.lp" "optimize" "res_cplex.sol"`

4. Use **OTOOLE** to create result CSVs

    Create folder resuls_cbc and results_cplex. We just need to run one optoimization

    CBC code 
     ---
    `otoole -vvv results cbc csv res_cbc.sol results_cbc datafile datafile.txt laotra_config.yaml`

    CPLEX code 
     ---
    `otoole -vvv results cplex csv res_cplex.sol results_cplex datafile datafile.txt laotra_config.yaml`
