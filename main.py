import argparse
import numpy as np
import cv2 as cv
inputing = []


def morphing(img, img2):
    print("Morphing executing...")
    pts1 = np.array([[218, 240], [295, 240], [250, 383]], np.float32)
    pts2 = np.array([[248, 245], [345, 270], [281, 366]], np.float32)
    pts11 = np.zeros((3, 2), np.float32)
    pts22 = np.zeros((3, 2), np.float32)
    dis = 50.0
    piece = 1.0 / dis

    for i in range(0, int(dis)):
        for j in range(0, 3):
            disx = (pts1[j, 0] - pts2[j, 0]) * -1
            disy = (pts1[j, 1] - pts2[j, 1]) * -1

            movex1 = (disx / dis) * (i + 1)
            movey1 = (disy / dis) * (i + 1)

            movex2 = disx - movex1
            movey2 = disy - movey1

            pts11[j, 0] = pts1[j, 0] + movex1
            pts11[j, 1] = pts1[j, 1] + movey1

            pts22[j, 0] = pts2[j, 0] - movex2
            pts22[j, 1] = pts2[j, 1] - movey2

        mat1 = cv.getAffineTransform(pts1, pts11)
        mat2 = cv.getAffineTransform(pts2, pts22)

        dst1 = cv.warpAffine(img, mat1, (img.shape[1], img.shape[0]), None, None, cv.BORDER_REPLICATE)
        dst2 = cv.warpAffine(img2, mat2, (img.shape[1], img.shape[0]), None, None, cv.BORDER_REPLICATE)

        dst = cv.addWeighted(dst1, 1 - (piece * i), dst2, piece * (i + 1), 0)

        cv.imshow("Morphing", dst)
        inputing.append(dst)

        cv.waitKey(25)
    cv.waitKey(0)


def main(frame):
    img1 = cv.imread(r"./Img/mona1.jpg")
    img2 = cv.imread(r"./Img/mona2.jpg")
    morphing(img1, img2)
    print(frame)
    print("Creating the Video...")
    h, w, c = img1.shape
    size = (int(h), int(w))
    out = cv.VideoWriter("Morphing.mp4", cv.VideoWriter_fourcc(*'MJPG'), int(frame), size)
    for i in range(len(inputing)):
        out.write(inputing[i])
    out.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("FrameRate", help="Frame Rate of the Video")
    args = parser.parse_args()
    main(args.FrameRate)
