import os
import json
import matplotlib.pyplot as plt
import cv2


class OpenPose:
    # 骨骼节点名称，与索引一一对应
    skeleton = [
        'Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow',
        'LWrist', 'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle',
        'REye', 'LEye', 'REar', 'LEar', 'LBigToe', 'LSmallToe', 'LHeel', 'RBigToe',
        'RSmallToe', 'RHeel']

    __listOfXCoordinatePoints = list()  # 暂时存放某一节点全部帧画面的 X 坐标数据列表
    __listOfYCoordinatePoints = list()  # 暂时存放某一节点全部帧画面的 Y 坐标数据列表

    __dictOfXCoordinatePoints = dict()  # 包含所有节点的全部帧画面的的 X，Y坐标的字典
    __dictOfYCoordinatePoints = dict()  # 包含所有节点的全部帧画面的的 X，Y坐标的字典

    def __init__(self, path):
        self.path = path

    def loadFile(self):
        '''
        加载文件夹内所有文件
        '''
        listOfAllFilesPath = list()
        listOfAllFiles = os.listdir(self.path)
        for currentFileName in listOfAllFiles:
            listOfAllFilesPath.append(self.path + '/' + currentFileName)

        return listOfAllFilesPath  # 返回一个包含该文件夹内所有文件的绝对路径的列表

    def switchJsonToDict(self, currentFilePath):
        '''
        把JSON文件转换为Python字典
        '''
        with open(currentFilePath, 'r') as file:
            dictOfCurrentFileData = json.load(
                file)  # diceOfCurrentFileData是JSON文件数据里的整个数据，是一个字典
        file.close()
        return dictOfCurrentFileData

    def analyzeData(self, dictOfCurrentFileData, currentSkeleton):
        '''
        提取数据到列表（把所有帧画面的某一个节点的X,Y坐标全部放在各自的列表里，写入字典后立刻初始化清空列表，腾出空间来储存下一个节点的数据）
        '''

        self.__listOfXCoordinatePoints.append(
            (((dictOfCurrentFileData['people'])[0])[
                'pose_keypoints_2d'])[self.skeleton.index(currentSkeleton) * 3])

        self.__listOfYCoordinatePoints.append(
            (((dictOfCurrentFileData['people'])[0])[
                'pose_keypoints_2d'])[self.skeleton.index(currentSkeleton) * 3 + 1])

    def writeDataToDict(self, currentSkeleton):
        '''
        写入数据到字典
        '''
        self.__dictOfXCoordinatePoints[currentSkeleton] = self.__listOfXCoordinatePoints
        self.__dictOfYCoordinatePoints[currentSkeleton] = self.__listOfYCoordinatePoints

        self.__listOfXCoordinatePoints = []
        self.__listOfYCoordinatePoints = []

    def drawGraphics(self):
        '''
        绘制某一节点的运动轨迹
        '''
        plt.plot(self.__dictOfXCoordinatePoints['Neck'],
                 self.__dictOfYCoordinatePoints['Neck'], 'r-.o')
        # ax = plt.gca()  # 获取到当前坐标轴信息
        # ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
        # ax.invert_yaxis()  # 反转Y坐标轴
        plt.show()

    def readPictureDPI(self, currentPicturePath):
        picture = cv2.imread(currentPicturePath)
        DPI = picture.shape[0:1]


def main():
    path = 'D:/Works/json_2'  # 这里填写JSON文件的根目录，注意'/'
    OpenPoseExample = OpenPose(path)

    for currentSkeleton in OpenPoseExample.skeleton:  # 外层循环骨骼节点
        for currentFilePath in OpenPoseExample.loadFile():  # 内层循环文件
            OpenPoseExample.analyzeData(
                OpenPoseExample.switchJsonToDict(currentFilePath), currentSkeleton)
        OpenPoseExample.writeDataToDict(currentSkeleton)

    OpenPoseExample.drawGraphics()


if __name__ == '__main__':
    main()
