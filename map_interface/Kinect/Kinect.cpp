#include "Kinect.hpp"

using namespace cv;
using namespace std;

_Kinect_Device::~_Kinect_Device() {
  pthread_mutex_destroy(&depth_lock);
  pthread_mutex_destroy(&video_lock);
}

void _Kinect_Device::DepthCallback(void *data, uint32_t timestamp) {
  pthread_mutex_lock(&depth_lock);
  depthMat.data = (uint8_t *)(uint16_t *)data;
  new_depth_frame = true;
  pthread_mutex_lock(&depth_lock);
}

void _Kinect_Device::VideoCallback(void *data, uint32_t timestamp) {
  pthread_mutex_lock(&video_lock);
  videoMat.data = (uint8_t *)data;
  new_video_frame = true;
  pthread_mutex_unlock(&video_lock);
}

bool _Kinect_Device::getDepth(Mat& output) {
  pthread_mutex_lock(&depth_lock);
  if (new_depth_frame) {
    depthMat.copyTo(output);
    new_depth_frame = false;
    pthread_mutex_unlock(&depth_lock);
    return true;
  } else {
    pthread_mutex_unlock(&depth_lock);
    return false;
  }
}

bool _Kinect_Device::getVideo(Mat& output) {
  pthread_mutex_lock(&video_lock);
  if (new_video_frame) {
    cvtColor(videoMat, output, CV_RGB2BGR);
    new_video_frame = false;
    pthread_mutex_unlock(&video_lock);
    return true;
  } else {
    pthread_mutex_unlock(&video_lock);
    return false;
  }
}

KinectDevice::KinectDevice() {
  Freenect::Freenect freenect;
  device = &freenect.createDevice<_Kinect_Device>(0);
  depthMat.create(Size(640, 480), CV_16UC1);
  videoMat.create(Size(640, 480), CV_8UC3);
  d2bgrMat.create(Size(640, 480), CV_8UC3);
  new_depth_frame = false;
}

void KinectDevice::start() {
  device->startDepth();
  device->startVideo();
}

void KinectDevice::stop() {
  device->stopDepth();
  device->stopVideo();
}

Mat KinectDevice::getDepth() {
  new_depth_frame = device->getDepth(depthMat);
  return depthMat;
}

Mat KinectDevice::getVideo() {
  device->getVideo(videoMat);
  return videoMat;
}

Mat KinectDevice::getDepthAsBGR() {
  if (new_depth_frame) {
    for (int y = 0; y < depthMat.rows; y++)
      for (int x = 0; x < depthMat.cols; x++)
        d2bgrMat.at<Vec3b>(y, x) = cd2bgr(depthMat.at<uint16_t>(y, x));
    new_depth_frame = false;
  }
  return d2bgrMat;
}

Vec3b KinectDevice::cd2bgr(uint16_t depth) {
  Vec3b bgr;
  switch (depth / 410) {
    case 0:
      bgr[0] = depth * 255 / 410;
      break;
    case 1:
      bgr[0] = 255;
      depth -= 410;
      bgr[1] = depth * 255 / 410;
      break;
    case 2:
      bgr[1] = 255;
      depth -= 820;
      depth = 410 - depth;
      bgr[0] = depth * 255 / 410;
      break;
    case 3:
      bgr[1] = 255;
      depth -= 1230;
      bgr[2] = depth * 255 / 410;
      break;
    case 4:
      bgr[2] = 255;
      depth -= 1640;
      depth = 410 - depth;
      bgr[1] = depth * 255 / 410;
    default:
      bgr[0] = 0;
      bgr[1] = 0;
      bgr[2] = 0;
      break;
  }
  return bgr;
}
