# Imports
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.optimize import fsolve

# Main class
class OpenChannel:
    x = []
    y = []
    zy = []
    profile = ''

    def __init__(self, channel, Q, b, S0, z, n, alpha, steps):
        self.channel = channel
        self.Q = Q
        self.b = b
        self.S0 = S0
        self.z = z
        self.n = n
        self.alpha = alpha
        self.steps = steps

    def normal_depth(self):
        """ This function returns the normal depth of the channel depending on its flow.
            No argument needs to be passed into this function. The function uses the
            arguments passed when calling the class. The method of calculation for the
            normal depth is done using the scipy function fsolve, as it is an iterative
            process and can not be accurately done otherwise.
        """
        manning_constant = (self.Q * self.n) / (1.49 * (self.S0**0.5))

        if self.channel == 'trapezoidal':
            manning = lambda yn : ((self.b * yn) + self.z * (yn**2))**(5/3) / (self.b + 2 * yn * (self.z**2 + 1)**(0.5))**(2/3) - manning_constant
            return float(fsolve(manning, 1))

        elif self.channel == 'rectangular':
            manning = lambda yn : (self.b * yn)**(5/3) / (2 * yn + self.b)**(2/3) - manning_constant
            return float(fsolve(manning, 1))

    def critical_depth(self):
        """ This function returns the critical depth in the channel depending on its flow
            No argument needs to be passed into this function. The function uses the arguments
            passed when calling the class. The method of calculation, similar to that for
            calculating normal depth, is done using the scipy function fsolve, as it is an
            iterative process and can not be accurately done otherwise. Here, an approximation of
            the acceleration of gravity is used, providing accuracy for up to 16 significant digits.
        """
        critical_constant = (self.Q**2) / 32.17404855643044
        if self.channel == 'trapezoidal':
            critical = lambda yc : ((((self.b * yc) + self.z * (yc**2))**3) / (self.b + 2 * self.z * yc)) - critical_constant
            return float(fsolve(critical, 1))

        elif self.channel == 'rectangular':
            yc = (critical_constant / self.b**2)**(1/3)
            return float(yc)

    def distance(self, yA, yB):
        """ This function returns the immediate distance between two points along the channel,
            as specified by the user. 'Immediate' refers to the calculation of the distance with
            a single step, as opposed to the calculation of the distance with multiple steps,
            which would provide a more accurate distance. Within the function, the area, wetted perimeter,
            hydraulic radius, slope, and specific energy of the two designated points are used
            to determine the distance between the points. This function primarily serves to provide
            necessary intermediate values for the step table function.
        """
        if self.channel == 'trapezoidal':
            AA = (self.b * yA) + (self.z * yA**2)
            PA = self.b + (2 * ((self.z * yA)**2 + yA**2)**(1/2))
            TA = self.b + 2 * self.z * yA

            AB = (self.b * yB) + (self.z * yB**2)
            PB = self.b + (2 * ((self.z * yB)**2 + yB**2)**(1/2))
            TB = self.b + 2 * self.z * yB
        elif self.channel == 'rectangular':
            AA = self.b * yA
            PA = self.b + 2 * yA
            TA = self.b

            AB = self.b * yB
            PB = self.b + 2 * yB
            TB = self.b

        RA = AA / PA
        RB = AB / PB

        SA = ((self.Q * self.n)/(1.49 * AA * RA**(2/3)))**2
        SB = ((self.Q * self.n)/(1.49 * AB * RB**(2/3)))**2

        EA = ((self.alpha * (self.Q / AA)**2) / (2 * 32.17404855643044)) + yA
        EB = ((self.alpha * (self.Q / AB)**2) / (2 * 32.17404855643044)) + yB

        S_avg = (SA + SB) / 2

        distance = (EB - EA) / (self.S0 - S_avg)

        return distance

    def step_table(self, yA, yB):
        """ This function returns a table of distances between points of specified depths.
            The number of rows in the table corresponds to the number of steps specified
            when the class is called. The total distance between the two specified points
            is displayed below the table. The more steps provided, the more accurate this
            total distance will be.
        """
        table = [['y (ft)', 'delta x (ft)']]

        if yA < yB:
            y1 = 0
            y2 = yA
            delta_x = 0
            total_x = 0
            for i in range(self.steps + 1):
                table.append([y2, delta_x])
                y1 = y2
                y2 += (abs(yA - yB) / self.steps)

                total_x += delta_x
                delta_x = self.distance(y1, y2)
                self.x.append(total_x)
                self.y.append(y1 + (-self.S0 * total_x))
                self.zy.append(-self.S0 * total_x)

        elif yA > yB:
            y1 = 0
            y2 = yA
            delta_x = 0
            total_x = 0
            for i in range(self.steps + 1):
                table.append([y2, delta_x])
                y1 = y2
                y2 -= (abs(yA - yB) / self.steps)

                total_x += delta_x
                delta_x = self.distance(y1, y2)
                self.x.append(total_x)
                self.y.append(y1 + (-self.S0 * total_x))
                self.zy.append(-self.S0 * total_x)

        print('Total Distance = %s%s' % (total_x, 'ft'))

    return tabulate(table, headers="firstrow", tablefmt="github")

    def profile(self):
        """ This function displays a plot of the water surface profile along with
            the normal depth line, critical depth line, and channel bottom surface.
            The type of water surface profile and category of slope is shown below
            the table.
        """
        NDL_y = []
        CDL_y = []

        for depth in self.zy:
            NDL_y.append(depth + self.normal_depth())
            CDL_y.append(depth + self.critical_depth())

        ws_elev = plt.plot(self.x, self.y, label='Water Surface')
        z_elev = plt.plot(self.x, self.zy, label='Channel Bottom')
        NDL = plt.plot(self.x, NDL_y, label = 'Normal Depth Line')
        CDL = plt.plot(self.x, CDL_y, label = 'Critical Depth Line')
        plt.grid(ls='--')
        plt.legend(title ="Legend", bbox_to_anchor = (1.55, 1), loc = 'upper right')
        plt.title('Water Surface Profile')
        plt.xlabel('Distance (ft)')
        plt.ylabel('Elevation (ft)')

        plt.show()

        if NDL_y > CDL_y:
            slope = "Mild"
            if self.y > NDL_y:
                self.profile = 'M1'
            elif CDL_y < self.y < NDL_y:
                self.profile = 'M2'
            elif self.y < CDL_y:
                self.profile = 'M3'
        else:
            slope = "Steep"
            if self.y > CDL_y:
                self.profile = 'S1'
            elif NDL_y < self.y < CDL_y:
                self.profile = 'S2'
            elif self.y < NDL_y:
                self.profile = 'S3'

        self.x.clear()
        self.y.clear()
        self.zy.clear()

        print('Water surface profile: ' + self.profile + ', %s' % slope)

    def upstream_point(self, yA, yB):
        """ This function returns the point that is upstream between the two points
        of specified depths. The function will say either the 'first' or 'second' point
        is upstream. This refers to the order in which the points are passed into the function.
        """
        if self.profile == 'M1' or 'M2' or 'S2':
            if yA > yB:
                return 'The first point is upstream of the second point.'
            elif yA < yB:
                return 'The second point is upstream of the first point.'
        else:
            if yA > yB:
                return 'The second point is upstream of the first point.'
            elif yA < yB:
                return 'The first point is upstream of the second point.'

        self.profile = ''
