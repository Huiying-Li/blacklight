# Blacklight: Scalable Defense for Neural Networks against Query-Based Black-Box Attacks
### ABOUT

This repository contains code implementation of the paper "[Blacklight: Scalable Defense for Neural Networks against Query-Based Black-Box Attacks](https://people.cs.uchicago.edu/~huiyingli/publication/Blacklight.pdf)", at *USENIX Security 2022*. 
Blacklight is a novel defense that detects query-based black-box attacks using an efficient content-similarity engine developed by researchers at [SANDLab](https://sandlab.cs.uchicago.edu/), University of Chicago.  


### DEPENDENCIES

Our code is implemented and tested on `Python 3.6.9` and the following packages are required.

- `config==0.5.1`
- `numpy==1.19.5`
- `torchvision==0.11.2`

And the Jupyter core packages we use is:

```
IPython          : 7.16.3
ipykernel        : 5.5.6
ipywidgets       : 7.7.0
jupyter_client   : 7.1.2
jupyter_core     : 4.9.2
jupyter_server   : not installed
jupyterlab       : not installed
nbclient         : 0.5.9
nbconvert        : 6.0.7
nbformat         : 5.1.3
notebook         : 6.4.10
qtconsole        : 5.2.2
traitlets        : 4.3.3
```



### How to run detection: 

Please look into the example in `example.ipynb` as reference. Please normalize the queries into $[0,1]$ and make sure all the queries, including both attack and benign queries, are in the same format.
