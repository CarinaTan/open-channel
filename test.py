from source import OpenChannel

# Example 1: trapezoidal channel
t_channel = OpenChannel('trapezoidal', 83700, 160, 0.0034, 2, 0.014, 1.05, 2)

yA = 15
yB = 17

print(t_channel.normal_depth())
print(t_channel.critical_depth())
print(t_channel.distance(yA, yB))
print(t_channel.step_table(yA, yB))
print(t_channel.profile())
print(t_channel.upstream_point(yA, yB))

# Example 2: rectangular channel
r_channel = OpenChannel('rectangular', 0.40107, 0.5, 0.02, None, 0.01, 1, 2)

yC = 0.208
yD = 0.25

print(r_channel.normal_depth())
print(r_channel.critical_depth())
print(r_channel.distance(yC, yD))
print(r_channel.step_table(yC, yD))
print(r_channel.profile())
print(r_channel.upstream_point(yC, yD))
