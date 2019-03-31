# Z-Score-Simulator

This project was coded to aid an analysis report/task of ECN121 Statistical Methods at Queen Mary, University of London. [BSc. Econ]

Install the required libraries before initiating the script:
```python
pip install -r requirements.txt
```

To run the script in CLI:
```python
python project_2.py
```

Select the file name without the extension (i.e. 'dataset'):
```
Select a file name: [enter filename without brackets]
```

To use the Z Score Simulator in your own project:
```python
from project_2 import generator, simulateZScores

simulateZScores(sample_mean, sample_var, n_dataset, int(input('Enter the number of trials 10^[x]: x = ')))
```
