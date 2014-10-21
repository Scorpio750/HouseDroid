#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>

using namespace cv;

int main(int argc, char **argv) {
  Mat image;
  if (argc < 2) {
    printf("Please specify a device\n");
    return 1;
  }
  VideoCapture cam(argv[1]);
  if (!cam.isOpened()) {
    printf("Cannot open device\n");
    return 1;
  }
  namedWindow("display", CV_WINDOW_AUTOSIZE);
  while (true) {
    cam.read(image);
    imshow("display", image);
    waitKey(0);
  }
  cam.release();
  return 0;
}
