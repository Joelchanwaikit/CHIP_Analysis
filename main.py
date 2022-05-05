import pandas as pd
import numpy as np
import math
import os
import matplotlib.pyplot as plt

def chip_analyser():
    # 1 Determine Dilution Factor

    variable1 = int(input("Total volume of IP buffer per cell line in ul (Typically 1500)"))
    variable2 = int(input("Total volume of Input buffer taken per cell line in ul (Typically 50)"))
    variable3 = variable2 / variable1
    splitter = int(input("How many different antibodies were used for this input (Assuming Even split)"))
    variable4 = 1 / splitter
    dilutionfactor = math.log(variable4 / variable3, 2)
    print(f"Dilution Factor Calculated: {dilutionfactor}")

    # 2 Read CSV Files - User to set up a CSV file and enter their own path
    print("Please only use 1 input at a time! Thanks")
    dfread = pd.read_csv(r"C:\Users\joelc\OneDrive\Desktop\Input\CHIP_results.csv")

    # Ignore null columns and combine the target and sample columns to create a unique identifer
    df = dfread[dfread.Cq.notnull()]
    col_sampletype = list(' ' + df.Target + ' ' + df.Sample + ' ')
    for z in range(len(col_sampletype)):
        col_sampletype[z] = col_sampletype[z].lower()
    col_cqvalues = list(df.Cq)

    # 3 Sort by sample type and the cq values. Replicates are put in the same list
    Clean_data = {}
    for i in range(len(col_cqvalues)):
        if col_sampletype[i] in Clean_data.keys():
            if abs(Clean_data[col_sampletype[i]][0] - col_cqvalues[i]) > 1:
                print(f"Warning, More than 1 Cq diff between {col_sampletype[i]}")
            Clean_data[col_sampletype[i]] = Clean_data[col_sampletype[i]] + [col_cqvalues[i]]
        else:
            Clean_data[col_sampletype[i]] = [col_cqvalues[i]]

    # 4 Calculate the Cq Mean and Cq Standard deviation for each sample type
    Analysed_data = {}
    for key in Clean_data:
        Values = np.array(Clean_data[key])
        Cq_mean = np.mean(Values)
        Cq_std = np.std(Values)
        Analysed_data[key] = [Cq_mean, Cq_std]

    # 5 Split into input and IP samples through the presence of the str "input" in the sampletype variable
    Input_details = {}
    IP_details = {}

    for key in Analysed_data:

        if "input" in key.lower():
            Input_details[key] = Analysed_data[key]
        else:
            IP_details[key] = Analysed_data[key]

    # 6 Minus dilution factor from the cq values for the inputs
    for key in Input_details:
        Input_details[key][0] = Input_details[key][0] - dilutionfactor

    # 7 Obtain information on Targets, Primers and Samples and format with a space before and after
    TargetsID_input = list(input("Name of target genes, separated by comma").lower().split(','))
    PrimerID_input = list(set(list(df.Target)))
    SamplesID_input = list(input("Name of Samples , separated by comma").lower().split(','))
    TargetsID = [x.center(len(x) + 2) for x in TargetsID_input]
    PrimerID = [x.center(len(x) + 2) for x in PrimerID_input]
    SamplesID = [x.center(len(x) + 2) for x in SamplesID_input]

    # 8 create IP - Input table
    ipminusinput = {}
    for key in IP_details:
        for i in range(len(TargetsID)):
            if TargetsID[i].lower() in key.lower():
                target = TargetsID[i]

        for i in range(len(SamplesID)):
            if SamplesID[i].lower() in key.lower():
                sample = SamplesID[i]
                print("Sample Check " + sample)

        for k in range(len(PrimerID)):
            if PrimerID[k].lower() in key.lower():
                primer = PrimerID[k]

        for j in Input_details:
            if sample.lower() in j.lower() and primer.lower() in j.lower():
                input_info = j

        IPminusIN_dCq = IP_details[key][0] - Input_details[input_info][0]

        IPminusIN_SD = IP_details[key][1] + Input_details[input_info][1]
        IPminusIN_Name = sample + target + primer
        print(IPminusIN_Name)
        print(IPminusIN_dCq)
        ipminusinput[IPminusIN_Name] = [IPminusIN_dCq, IPminusIN_SD, sample, target, primer]

    # 9 create IP/IN

    percentofip = {}
    for key in ipminusinput:
        ipoverin = 100 * math.pow(2, -ipminusinput[key][0])
        lower_bound = 100 * math.pow(2, -(ipminusinput[key][0] + ipminusinput[key][1]))
        upper_bound = 100 * math.pow(2, -(ipminusinput[key][0] - ipminusinput[key][1]))
        percentofip[key] = [ipoverin, lower_bound, upper_bound]

    # 10 Data Export

    # Export dCq and ip/in(%) Data
    sample = []
    dCq = []
    Std = []
    ipinpercent = []
    uperr = []
    low_err = []
    sample_output = []
    target_output = []
    primer_output = []
    for keys in ipminusinput:
        sample.append(keys)
        dCq.append(ipminusinput[keys][0])
        Std.append(ipminusinput[keys][1])
        ipinpercent.append(percentofip[keys][0])
        uperr.append(percentofip[keys][2])
        low_err.append(percentofip[keys][1])
        sample_output.append(ipminusinput[keys][2])
        target_output.append(ipminusinput[keys][3])
        primer_output.append(ipminusinput[keys][4])

    data = {"Samples": sample, "dCQ": dCq, "Std": Std, 'IP/IN (%)': ipinpercent, "upper_bound": uperr,
            'lower_bound': low_err, 'sample': sample_output, 'target': target_output, 'primer': primer_output}
    dfexport = pd.DataFrame(data)
    path = "C:\\Users\\joelc\\OneDrive\\Desktop\\Output"  # User to define own Path
    dfexport.to_csv(os.path.join(path, F"Python_CHIP_output_{TargetsID}.csv"))

    # If only 1 input type, you can use the file directly as input for the plotter
    # If you have 2 or more input types, aggregate the data on a singular CSV file for the plotter

def chip_plotter():

    # 1 Read the file, user to define path on set up
    df = pd.read_csv(r"C:\Users\joelc\OneDrive\Desktop\Input\CHIP_Plottinginputs.csv")

    # 2 Ask for which 2 to compare
    pre_comparison_plot = list(input("What 2 samples to compare, seperated by comma").lower().split(','))
    comparison_plot = [x.center(len(x) + 2) for x in pre_comparison_plot]
    pre_comparison_target = list(input("What target to compare").lower().split(','))
    comparison_target = [x.center(len(x) + 2) for x in pre_comparison_target]

    # 3 Process the data to plot which is the ip/in and error bars
    sample1df = df[(df['sample'] == comparison_plot[0]) & (df['target'] == comparison_target[0])]
    sample2df = df[(df['sample'] == comparison_plot[1]) & (df['target'] == comparison_target[0])]
    sample1 = list(sample1df.loc[:, 'IP/IN (%)'])
    lowerbound1 = list(sample1df.loc[:, 'lower_bound'])
    upperbound1 = list(sample1df.loc[:, 'upper_bound'])
    sample2 = list(sample2df.loc[:, 'IP/IN (%)'])
    lowerbound2 = list(sample2df.loc[:, 'lower_bound'])
    upperbound2 = list(sample2df.loc[:, 'upper_bound'])
    x = list(sample2df.primer)
    w = 0.4
    bar1 = np.arange(len(x))
    bar2 = [i + w for i in bar1]

    # 4 Process length of error bars
    upper1 = []
    lower1 = []
    upper2 = []
    lower2 = []
    for i in range(len(sample1)):
        upper1.append(upperbound1[i] - sample1[i])
        lower1.append(sample1[i] - lowerbound1[i])
        upper2.append(upperbound2[i] - sample2[i])
        lower2.append(sample2[i] - lowerbound2[i])

    asymmetric_error1 = np.array(list(zip(lower1, upper1))).T
    asymmetric_error2 = np.array(list(zip(lower2, upper2))).T

    # 5 Plotting

    plt.bar(bar1, sample1, width=w, label=F"{comparison_plot[0]}")
    plt.errorbar(x=bar1, y=sample1, yerr=asymmetric_error1, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.bar(bar2, sample2, width=w, label=F"{comparison_plot[1]}")
    plt.errorbar(x=bar2, y=sample2, yerr=asymmetric_error2, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.xticks(bar1 + w / 2, x)
    plt.title(F"Comparison of IP/IN % for{comparison_target[0]}between{comparison_plot[0]}and{comparison_plot[1]}")
    plt.xlabel("Primers")
    plt.ylabel("IP/IN Percentage")
    plt.legend()

    plt.show()

    repeat = input("Another Graph? (y/n)")
    if repeat == 'y':
        chip_plotter()

def chip_combined_plotter():

    # 1 Read the file, user to define path on set up
    df = pd.read_csv(r"C:\Users\joelc\OneDrive\Desktop\Input\CHIP_Plottinginputs.csv")

    # 2 Get information on what to plot
    pre_comparison_plot = list(input("What 4 samples to compare, seperated by comma").lower().split(','))
    comparison_plot = [x.center(len(x) + 2) for x in pre_comparison_plot]
    pre_comparison_target = list(input("What target to compare").lower().split(','))
    comparison_target = [x.center(len(x) + 2) for x in pre_comparison_target]

    # 3 Read info on what to plot
    sample1df = df[(df['sample'] == comparison_plot[0]) & (df['target'] == comparison_target[0])]
    sample2df = df[(df['sample'] == comparison_plot[1]) & (df['target'] == comparison_target[0])]
    sample3df = df[(df['sample'] == comparison_plot[2]) & (df['target'] == comparison_target[0])]
    sample4df = df[(df['sample'] == comparison_plot[3]) & (df['target'] == comparison_target[0])]
    sample1 = list(sample1df.loc[:, 'IP/IN (%)'])
    lowerbound1 = list(sample1df.loc[:, 'lower_bound'])
    upperbound1 = list(sample1df.loc[:, 'upper_bound'])
    sample2 = list(sample2df.loc[:, 'IP/IN (%)'])
    lowerbound2 = list(sample2df.loc[:, 'lower_bound'])
    upperbound2 = list(sample2df.loc[:, 'upper_bound'])
    sample3 = list(sample3df.loc[:, 'IP/IN (%)'])
    lowerbound3 = list(sample3df.loc[:, 'lower_bound'])
    upperbound3 = list(sample3df.loc[:, 'upper_bound'])
    sample4 = list(sample4df.loc[:, 'IP/IN (%)'])
    lowerbound4 = list(sample4df.loc[:, 'lower_bound'])
    upperbound4 = list(sample4df.loc[:, 'upper_bound'])
    x = list(sample2df.primer)
    w = 0.2
    bar1 = np.arange(len(x))
    bar2 = [i + w for i in bar1]
    bar3 = [i + w + w for i in bar1]
    bar4 = [i + w + w + w for i in bar1]

    # 4 Calculate error bar sizes
    upper1 = []
    lower1 = []
    upper2 = []
    lower2 = []
    lower3 = []
    upper3 = []
    lower4 = []
    upper4 = []
    for i in range(len(sample1)):
        upper1.append(upperbound1[i] - sample1[i])
        lower1.append(sample1[i] - lowerbound1[i])
        upper2.append(upperbound2[i] - sample2[i])
        lower2.append(sample2[i] - lowerbound2[i])
        upper3.append(upperbound3[i] - sample3[i])
        lower3.append(sample3[i] - lowerbound3[i])
        upper4.append(upperbound4[i] - sample4[i])
        lower4.append(sample4[i] - lowerbound4[i])
    asymmetric_error1 = np.array(list(zip(lower1, upper1))).T
    asymmetric_error2 = np.array(list(zip(lower2, upper2))).T
    asymmetric_error3 = np.array(list(zip(lower3, upper3))).T
    asymmetric_error4 = np.array(list(zip(lower4, upper4))).T

    # 5 Plot the graph

    plt.bar(bar1, sample1, width=w, label=F"{comparison_plot[0]}")
    plt.errorbar(x=bar1, y=sample1, yerr=asymmetric_error1, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.bar(bar2, sample2, width=w, label=F"{comparison_plot[1]}")
    plt.errorbar(x=bar2, y=sample2, yerr=asymmetric_error2, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.bar(bar3, sample3, width=w, label=F"{comparison_plot[2]}")
    plt.errorbar(x=bar3, y=sample3, yerr=asymmetric_error3, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.bar(bar4, sample4, width=w, label=F"{comparison_plot[3]}")
    plt.errorbar(x=bar4, y=sample4, yerr=asymmetric_error4, c='k', fmt=' ', elinewidth=1, capsize=3)
    plt.xticks(bar1 + w + w / 2, x)
    plt.title(F"Comparison of IP/IN % for{comparison_target[0]}")
    plt.xlabel("Primers")
    plt.ylabel("IP/IN Percentage")
    plt.legend()

    plt.show()

    repeat = input("Another Graph? (y/n)")
    if repeat == 'y':
        chip_combined_plotter()


if __name__ == '__main__':
    print("a: Analyser , b: Plotter")
    program = input("Which module would you like to use? (a/b)")
    if program == 'a':
        chip_analyser()
    elif program == 'b':
        to_plot = int(input("Number of comparisons to plot? (2 or 4)"))
        if to_plot == 2:
            chip_plotter()
        elif to_plot == 4:
            chip_combined_plotter()
        else:
            print("Invalid Input")
    else:
        print("Invalid input")


