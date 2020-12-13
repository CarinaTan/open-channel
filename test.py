from source import OpenChannel

t_channel = OpenChannel('trapezoidal', 83700, 160, 0.0034, 2, 0.014, 1.05, 2)

yA = 15
yB = 17

print(channel1.normal_depth())
print(channel1.critical_depth())
print(channel1.distance(yA, yB))
print(channel1.step_table(yA, yB))
print(channel1.profile())
print(channel1.upstream_point(yA, yB))

r_channel = OpenChannel('rectangular', 0.40107, 0.5, 0.02, 2, 0.01, 1, 2)

yA = 0.208
yB = 0.25

print(channel2.normal_depth())
print(channel2.critical_depth())
print(channel2.distance(yA, yB))
print(channel2.step_table(yA, yB))
print(channel2.profile())
print(channel2.upstream_point(yA, yB))
