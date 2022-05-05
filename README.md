# CHIP_Analysis

This represents an open source pythonic solutions to the analysis of qPCR data during Chromatin Immunoprecipitation Assays
This generates publication quality images of ip/input inclusive of error bars (Via Standard deviation)

There are 2 main modules within main.py:
1) ChIP Analyser which initially analyses Cq Data
2) ChIP Plotter which plots the data, with an option for comparing 2 or 4 samples at the same time

### Example Graph Output
![image](https://user-images.githubusercontent.com/64132598/166897170-c988d92f-54fd-4cb1-b813-f9bebfca4490.png)

## Usage 

### Set up

Create a result input file and plotting input file in the csv format. Define the path as instructed within main.py

### Conducting the Analysis 

Take note to run only 1 input at a time (A beads or G beads)
There needs to be a space between the sample and target (ie ev SIRT1), and no other spaces. This is not capital sensitive 
Copy and paste your results from the BioRad Machine onto your input file
Take the results from the output and paste into your plotting input file 
Repeat until all inputs and IP are analysed 

### Plotting the CHIP Results

Ensure that all results to be plotted is in your plotting input file 
Answer the questions as needed
Save as the image that is output
Repeat the cells after the file upload to produce other combinations of images

## Input formatting 

The program is optimised for the Cq results file from a Biorad machine but should be able to accept other machines with minor adjustments to column names 
An example data has been provided for input to the Analyser module as well as example plotting inputs for the plotting module 
Take note that the example data is not real and are not results of actual scientific experiments.

Target Name should include the primer name 
Sample Name should include the sample name and the target gene, with a space seperating them

## Contributing
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature) 

Commit your Changes (git commit -m 'Add some AmazingFeature') 

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request
