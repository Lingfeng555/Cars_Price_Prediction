# Project Notation Guide

This repository contains iterative attempts at solving a specific problem, with each attempt building upon previous insights and progress.

## File Structure

- Files are named using the convention: `xyz_v<n>.ipynb`, where:
  - `xyz` represents the core topic or method of the notebook (e.g., `data_preprocessing`, `model_training`).
  - `<n>` is the version number, indicating the progression of attempts.
  
For example, `data_preprocessing_v1.ipynb` is the first attempt at implementing data processing steps, while `model_training_v2.ipynb` represents a second iteration in the model training process.

## Workflow

1. **Notebook Development**: Each version of the notebook (`.ipynb` files) represents a sequential iteration where we:
   - Process data to ensure it's suitable for model training.
   - Train and evaluate models directly in the notebook to understand model performance and tune parameters.
   - Test different approaches and document observations to build an optimal solution.

2. **Code Consolidation**: After validating and finalizing the data processing and model evaluation in the notebooks:
   - We translate the workflow into reusable classes and functions in Python scripts (`.py` files).
   - This modular code is designed for integration into the web server, enabling smooth deployment and efficient model use in production.

## Project Goals

- To provide a clear, iterative approach to solving data and model challenges.
- To document progress across attempts, facilitating learning and refinement of our solution.
- To streamline implementation by converting validated notebook code into structured, deployable Python classes.
