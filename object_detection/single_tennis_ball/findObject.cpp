#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include <stdio.h>

using namespace std;
using namespace cv;

double magnitude(vector<double> v) {
  double sum = 0.0;
  for (int i = 0; i < v.size(); i++)
    sum += v[i] * v[i];
  return sqrt(sum);
}

bool within(Vec3b color1, Vec3b color2, int tolerance) {
  vector<double> difference(3, 0);
  difference[0] = (double)color1[0] - (double)color2[0];
  difference[1] = (double)color1[1] - (double)color2[1];
  difference[2] = (double)color1[2] - (double)color2[2];
  return magnitude(difference) < tolerance;
}

int main(int argc, char *argv[]) {
  /* open an image */
  string name = argv[1];
  Mat old_image = imread(name);
  Mat image = old_image.clone();
  Mat ximage = image.clone(), yimage = image.clone();
  for (int y = 0; y < image.rows; y++) {
    for (int x = 0; x < image.cols; x++) {
      ximage.at<Vec3b>(y, x) = Vec3b(255, 255, 255);
      yimage.at<Vec3b>(y, x) = Vec3b(255, 255, 255);
    }
  }

  /* mask the image for the object */
  Vec3b target(29, 228, 200);
  int tolerance = 80;
  for (int y = 0; y < image.rows; y++) {
    for (int x = 0; x < image.cols; x++) {
      Vec3b pixel = old_image.at<Vec3b>(y, x);
      Vec3b white(255, 255, 255);
      if (!within(pixel, target, tolerance))
        image.at<Vec3b>(y, x) = white;
    }
  }

  /* locate the center of the ball */
  /* create a histogram for both axes */
  vector<int> histogram_x(image.cols, 0);
  vector<int> histogram_y(image.rows, 0);
  for (int y = 0; y < image.rows; y++) {
    for (int x = 0; x < image.cols; x++) {
      Vec3b pixel = image.at<Vec3b>(y, x);
      if (!(pixel[2] == 255 && pixel[1] == 255 && pixel[0] == 255)) {
        histogram_x[x] += 1;
        histogram_y[y] += 1;
      }
    }
  }

  /* find the midpoint by doing
   * sum(f(x) * x) / sum(f(x))  for each axis
   */
  unsigned long midx = 0, midy = 0;
  unsigned long countx = 0, county = 0;
  for (int i = 0; i < image.cols; i++) {
    midx += histogram_x[i] * i;
    countx += histogram_x[i];
    for (int n = 0; n < histogram_x[i]; n++)
      ximage.at<Vec3b>(image.rows - n - 1, i) = Vec3b(0, 0, 255);
  }
  for (int i = 0; i < image.rows; i++) {
    midy += histogram_y[i] * i;
    county += histogram_y[i];
    for (int n = 0; n < histogram_y[i]; n++)
      yimage.at<Vec3b>(i, n) = Vec3b(255, 0, 0);
  }
  midx /= countx;
  midy /= county;

  /* output results */
  printf("midx: %d, midy: %d\n", (int)midx, (int)midy);
  image.at<Vec3b>((int)midy-1, (int)midx-1) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy-1, (int)midx+0) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy-1, (int)midx+1) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+0, (int)midx-1) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+0, (int)midx+0) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+0, (int)midx+1) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+1, (int)midx-1) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+1, (int)midx+0) = Vec3b(0, 0, 255);
  image.at<Vec3b>((int)midy+1, (int)midx+1) = Vec3b(0, 0, 255);

  /* open a window, display it */
  namedWindow("picture", CV_WINDOW_AUTOSIZE);
  imshow("picture", old_image);
  namedWindow("xhist", CV_WINDOW_AUTOSIZE);
  imshow("xhist", ximage);
  namedWindow("yhist", CV_WINDOW_AUTOSIZE);
  imshow("yhist", yimage);
  namedWindow("new picture", CV_WINDOW_AUTOSIZE);
  imshow("new picture", image);
  waitKey(0);
  destroyAllWindows();

  return 0;
}

