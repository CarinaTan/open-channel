# open-channel
Analysis of gradually varied open channel flow

*This program is designed to be used in a part of the analysis of flow in either a rectangular or trapezoidal open channel.*

## Contraints
* arguments passed into the program must be in imperial units
* the program outputs answers in imperial units
* distances are given and provided in units of feet
* flow rate must be given in units of cubic feet per second
* the acceleration of gravity is approximated to 32.17404855643044 feet per second squared
* trapezoidal channels must be symmetrical
* channel must slope downward

## Required external libraries:
* numpy
* matplotlib
* tabulate
  - tabulate
* scipy.optimize
  - fsolve

## Inputs
  1. **channel**: *str type*; describes the type of channel and may be either 'rectangular' or 'trapezoidal'
  2. **Q**: *numeric type*; flow rate given in units of cubic feet per second
  3. **b**: *numeric type*; length of the bottom width of the channel
  4. **S0**: *numeric type*; slope of the channel bottom given as a positive value
  5. **z**: *numeric type*; sideslope of trapezoidal channels
  6. **n**: *numeric type*; Manning's friction factor of the channel
  7. **alpha**: *numeric type*; a velocity correction factor
  8. **steps**: *numeric type*; the number of steps desired to determine the distance between two points along the channel

## Outputs
  1. **Normal depth**
  2. **Critical depth**
  3. **Immediate distance between two points along the channel**
  4. **Step table**: uses the step method to determine the distance between two points along the channel.
      The more steps that are provided, the greater the accuracy of the distance between the points.
  5. **Water surface profile**: a graphical display of the water surface profile, channel bottom, normal depth line, and critical depth line.
      The category of slope is provided (mild or steep), along with the type of profile (M1, M2, M3, S1, S2, and S3).
  6. **Upstream point**: the upstream point between two points along the channel is stated.

## How to use the program
1. Instantiate a new object of 'OpenChannel'
```python
>>> channel1 = OpenChannel('trapezoidal', 83700, 160, 0.0034, 2, 0.014, 1.05, 2)
```
or
```python
>>> channel2 = OpenChannel('rectangular', 0.40107, 0.5, 0.02, None, 0.01, 1, 2)
```
2. Specify two depths along the channel
```python
>>> yA = 15
>>> yB = 17
```
or
```python
>>> yA = 0.208
>>> yB = 0.25
```
3. Call the function *normal depth* to determine the normal depth of the channel
```python
>>> channel1.normal_depth()
```
4. Call the function *critical depth* to determine the critical depth of the channel
```python
>>> channel1.critical_depth()
```
5. Call the function *distance* to determine the immediate distance between the two specified points
```python
>>> channel1.distance(yA, yB)
```
6. Call the function *step_table* to view the use of the direct step method in determining the distance between the two specified points
```python
>>> channel1.step_table(yA, yB)
```
7. Call the function *profile* to view the water surface profile and determine the slope category and type of profile of the flow
```python
>>> channel1.profile()
```
8. Call the function *upstream_point* to determine which of the two specified points is upstream according to the profile
```python
>> >channel1.upstream_point(yA, yB)
```
