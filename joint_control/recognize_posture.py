'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
from keyframes import hello, leftBackToStand, leftBellyToStand, rightBackToStand, wipe_forehead
# added import
import pickle
from os import listdir
ROBOT_POSE_DATA_DIR = 'robot_pose_data'

class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = pickle.load(open('robot_pose.pkl'))  # LOAD YOUR CLASSIFIER

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        features = []
        # ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'AngleX', 'AngleY']
        features += [perception.joint['LHipYawPitch']]
        features += [perception.joint['LHipRoll']]
        features += [perception.joint['LHipPitch']]
        features += [perception.joint['LKneePitch']]
        features += [perception.joint['RHipYawPitch']]
        features += [perception.joint['RHipRoll']]
        features += [perception.joint['RHipPitch']]
        features += [perception.joint['RKneePitch']]
        features += [perception.imu[0]]
        features += [perception.imu[1]]
        
        classes = listdir(ROBOT_POSE_DATA_DIR)
        
        posture_index = self.posture_classifier.predict([features])[0]
        posture = classes[posture_index]
        print posture
        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = rightBackToStand()  # CHANGE DIFFERENT KEYFRAMES
    agent.keyframes = rightBackToStand()
    agent.run()
