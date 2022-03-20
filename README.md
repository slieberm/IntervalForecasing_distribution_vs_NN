# IntervalForecasting_distribution_vs_NN
This project accompanies the masterthesis "Interval forecasts using neural networks in presence of time-varying
skewness - better than classic distribution-based methods?" of Simon Liebermann 
at Ulm University.

The aim of the project is to validate and evaluate the in the thesis proposed 
distribution and neural network models. 

In the following the most important elements of this project are introduced briefly:

- main.py: In the main file the models are build and evaluted on the measures MPIW and PICP ('print_mean_stats'). 
Additionally inteval plots are generated.
- config.py: here the general configurations are made:
  preprocessing, configurations for NN models, configurations for data generation.
- config_models.py: all specific configurations for each model are made here.
- utility.py: Here some functions, like loading and saving, are sored and then used in other files.
- naive_model.py: the simple naive model is defined here


- module D_models:
  This module contains the files needed to build the distribution models:
  - garch.py: the GARCH model as described in the thesis is defined here.
    This file can be run by itself or the function can be included in another program.
  - garch_tv.py: the ARCD model as described in the thesis is defined here.
    In general the ARCD model is in this project reverd as GARCH time-varying (tv). 
    This file can be run by itself or the function can be included in another program.
  - my_garch.py: own implementatoin of the GARCH model. Not used for comparison.
  - evaluation.py: validation of the GARCH/ARCD models is done here.
    In this files some adjustments have to be done depending on the used data and model.
  - visualization.py: this file creates plots of the skewes student-t distribution by Hansen.
  - SkewStudent.py: Class for the skewed student-t distribution by Hansen.

    
- module NN_models:
  This module contains the files needed to build the neural network models:
  - neural_networks.py: runs the neural_network model according the in "config_models" defined NN models.
    This file can be run by itself or the function can be included in another program.
  - pinball_loss.py: contains the pinball loss function.
  - qd_loss.py: contains the quality-driven loss function.
  - model_habdling.py: contains some functions which are needed to build and use the neural networks.

For this project an additional folder structure is needed:
  - /checkpoints: for storing of the weights and biases of the NN. Subfolders: type of data.
  - /data: used raw data. Subfolder: /pickles: preprocessed data pickles or generated data pickles.
  - /outputs: all outputs generated by this project. Subfolders:
    - /intervals: generated intervals can be stored here.
    - /models: model dictionaries can be cached here.
    - /pv_data: parameter evaluation/valdiation for pv_data of distribution models
    - /simulated_data: parameter evaluation/valdiation for simulated data of distribution models
    - /scaler: data scaler used for preprocessing the data for the NN models is stored here for re-transforming.