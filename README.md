# ece227-course-project
Course Project for ECE 227 Big Network Data

# About

This guide provides instructions on how to set up and run the network analysis code contained in this repository. The project involves analyzing large-scale network data, including Enron email corpora and Facebook social graphs.

# How to run

Install Dependencies

```pip install -r requirements.txt```

Then to get all the figures that are in out paper run the runner.ipynb file

# Generate Results
To reproduce all figures and analysis presented in the final paper:

1. Open runner.ipynb.

2. Run all cells from top to bottom.

3. The notebook will:

    + Load or download the necessary datasets.

    + Compute centrality metrics (using JSON caches for performance).

    + Perform Louvain community detection.

    + Export all generated plots to a single file named network_analysis_results.pdf.
