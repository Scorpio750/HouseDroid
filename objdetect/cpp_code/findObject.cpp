#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include <stdio.h>

using namespace std;
using namespace cv;

float magnitude(Vec3b vector);
bool within(Vec3b color1, Vec3b color2, int tolerance);

int main(int argc, char *argv[]) {
  /* open an image */
  string name = argv[1];
  Mat image = imread(name);

  printf("dimensions: rows=%d cols=%d\n", image.rows, image.cols);

  /* mask the image for the object */
  Vec3b target(29, 228, 200);
  int tolerance = 80;
  for (int y = 0; y < image.rows; y++) {
    for (int x = 0; x < image.cols; x++) {
      Vec3b pixel;
      Vec3b black(0, 0, 0);
      Vec3b red(0, 0, 255);
      pixel = image.at<Vec3b>(y, x);
      if (!within(pixel, target, tolerance))
        image.at<Vec3b>(y, x) = black;
    }
  }

  /* open a window, display it */
  namedWindow("picture", CV_WINDOW_AUTOSIZE);
  imshow("picture", image);
  waitKey(0);
  destroyAllWindows();

  return 0;
}

float magnitude(Vec3b vector) {
  float x = (float)vector[0];
  float y = (float)vector[1];
  float z = (float)vector[2];
  return sqrt(x * x + y * y + z * z);
}

bool within(Vec3b color1, Vec3b color2, int tolerance) {
  Vec3b difference;
  difference[0] = color1[0] - color2[0];
  difference[1] = color1[1] - color2[1];
  difference[2] = color1[2] - color2[2];
  return magnitude(difference) < (float)tolerance;
}

