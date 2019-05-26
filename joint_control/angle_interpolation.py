'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello, leftBackToStand, leftBellyToStand, rightBackToStand, wipe_forehead, rightBellyToStand


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.start_time = None # starttime
        self.spline = [] # spline

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        names, times, keys = keyframes
        if self.start_time == None:
            self.start_time = perception.time
        if self.spline == []:
            names, times, keys = keyframes
            for joint_i,name in enumerate(names):
                self.spline.append([])
                for frame in range(len(times[joint_i])-1):
                    self.spline[joint_i].append([])
                    P_i0 = (p0_x,p0_y) = (times[joint_i][frame], keys[joint_i][frame][0])
                    P_i1 = (p1_x,p1_y) = (times[joint_i][frame] + keys[joint_i][frame][1][1], keys[joint_i][frame][0] + keys[joint_i][frame][1][2])
                    P_i2 = (p2_x,p2_y) = (times[joint_i][frame] + keys[joint_i][frame][2][1], keys[joint_i][frame][0] + keys[joint_i][frame][2][2])
                    P_i3 = (p3_x,p3_y) = (times[joint_i][frame+1], keys[joint_i][frame+1][0])
                    t_0 = times[joint_i][frame]
                    t_4 = times[joint_i][frame+1]
                    self.spline[joint_i][frame].append(t_0)
                    self.spline[joint_i][frame].append(t_4)
                    b = bezier((p0_x,p0_y),(p1_x,p1_y),(p2_x,p2_y),(p3_x,p3_y))
                    self.spline[joint_i][frame].append(b)    
        else:
            current_time = round(perception.time - self.start_time, 2)
            for i,joint in enumerate(names):
                for t in range(len(self.spline[i])):
                    t_min =  self.spline[i][t][0]
                    t_max =  self.spline[i][t][1]
                    if t_min <= current_time and current_time <= t_max:
                        target_joints[joint] =  self.spline[i][t][2][1](current_time)
                        break
        return target_joints

def bezier((p0_x,p0_y),(p1_x,p1_y),(p2_x,p2_y),(p3_x,p3_y)):
    # i = ((t - p0_x) / (p0_x - p3_x))
    def b_x(t):
        return pow((1-((t - p0_x) / (p0_x - p3_x))),3)*p0_x+3*pow((1-((t - p0_x) / (p0_x - p3_x))),2)*((t - p0_x) / (p0_x - p3_x))*p1_x+3*(1-((t - p0_x) / (p0_x - p3_x)))*pow(((t - p0_x) / (p0_x - p3_x)),2)*p2_x+pow(((t - p0_x) / (p0_x - p3_x)),3)*p3_x
    def b_y(t):
        return pow((1-((t - p0_x) / (p0_x - p3_x))),3)*p0_y+3*pow((1-((t - p0_x) / (p0_x - p3_x))),2)*((t - p0_x) / (p0_x - p3_x))*p1_y+3*(1-((t - p0_x) / (p0_x - p3_x)))*pow(((t - p0_x) / (p0_x - p3_x)),2)*p2_y+pow(((t - p0_x) / (p0_x - p3_x)),3)*p3_y
    x = b_x
    y = b_y
    return (x,y)
        
if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    #agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.keyframes = leftBackToStand()
    agent.run()
