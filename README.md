# Battery Charge Thresholds

A simple script to set the battery charge thresholds for certain laptops.
Either set any combination of `start` and `end` thresholds or make use of pre-defined `preset`s.

The script writes to specific files to set the thresholds.
The naming or rather the path to the files may vary across different laptops.
In addition not every laptop manufacturer supports setting charging thresholds.

## Usage
```
usage: battery.py [-h] [-s START] [-e END] [-d] [-p {full,care}]

Set battery charging thresholds. Use either the 'preset' option or any combination of 'start' and 'end'.

options:
  -h, --help            show this help message and exit
  -s START, --start START
                        Threshold when to start charging if below
  -e END, --end END     Threshold when to stop charging if above
  -d, --dump            Dump current thresholds
  -p {full,care}, --preset {full,care}
                        Select preset: 'full' to charge the battery to 100%, 'care' to take care of the battery
```
