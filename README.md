# SI.01

## description
This experiment is a modified posner cueing paradigm with social cues facilitating the target search.

### conditions
The demo includes two cue types:
* one arrow (as a control),
* one cartoon face as a social cue.

### condition parameters
experimental parameters are saved in the `design` folder. The script pulls parameters from the `design` .csv files. The csv file is imported as a pandas dataframe and the values are utilized for each trial.

In conjunction, the participant response is also saved as a pandas dataframe.

### output location
The entire dataframe will be saved in `data` > `sub-ID` > .csv

```
├── README.md
├── data
│   └── sub-01
│       └── practice.csv
├── design
│   └── task-pracetice.csv
├── scripts
│   └── psychopy
│       └── spatialcueing_practice.py
└── stimuli
    ├── arrow
    │   ├── left.png
    │   ├── neutral.png
    │   └── right.png
    └── practice
        ├── left.png
        ├── neutral.png
        └── right.png
```
