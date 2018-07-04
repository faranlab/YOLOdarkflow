import os
import uuid
import cv2
from lxml import etree
import xml.etree.cElementTree as ET


ANOPATH='/home/fm/Desktop/Dataset/Video_Annotation/'
VIDPATH='/home/fm/Desktop/Dataset/Videos/'
IMDIR = '/home/faran/darkflow-master/newmodeldata/images/'
ANOSAVEDIR = '/home/fm/Desktop/darkflow-master/newmodeldata/annotations/'
dirs=os.listdir(ANOPATH)

def main():
    for filename in dirs:
        filename = 'Clip_1_gt.txt'
        print(filename)
        farzaframes={}
        label='uav'
        if '.txt' not in filename:
            continue

        rawname = filename.replace("_gt.txt", "")
        with open(ANOPATH + filename) as file:
            lines=file.readlines()

        key = 1
        for line in lines:
            line = line.strip()
            uavcount=line.count('(')
            detections=line.split('(')
            farzaframes[key]=[];
            if uavcount == 0:
                continue;
            for i in range(1,len(detections)):
                xy=detections[i].split(', ')
                xy=xy[:4]
                xy[3]=xy[3].strip('),')
                for j in range(len(xy)):
                    xy[j]=int(xy[j])
                [y1, x1, y2, x2]=xy
                farzaframes[key].append(tuple([label, x1, y1, x2, y2]))
            write_xml(farzaframes,key)
        quit()
        vid = cv2.VideoCapture(VIDPATH + rawname + '.mov')
        while(True)
            ret, frame = vid.read()
            cv2.imwrite()
def write_xml(farzaframes,key):
    if not os.path.isdir(ANOSAVEDIR):
        os.mkdir(ANOSAVEDIR)

    uavcnt = len(farzaframes[key])
    data_point_name = str(uuid.uuid4())
    data_point_name = data_point_name.replace("-","")
    height, width, depth = 1080,1920,3

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = IMDIR
    ET.SubElement(annotation, 'filename').text = data_point_name + '.jpg'
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    for x in range(0,uavcnt):
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = 'uav'
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(farzaframes[key][x][1])
        ET.SubElement(bbox, 'ymin').text = str(farzaframes[key][x][2])
        ET.SubElement(bbox, 'xmax').text = str(farzaframes[key][x][3])
        ET.SubElement(bbox, 'ymax').text = str(farzaframes[key][x][4])
    rere = data_point_name + 'jpg'
    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(ANOSAVEDIR, data_point_name.replace('jpg', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)

if __name__ == '__main__':
    main()
