#ifndef __Kinect_hpp__

#include <stdio.h>
#include <math.h>
#include <pthread.h>
#include <vector>
#include <libfreenect.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class _Kinect_Device : public Freenect::FreenectDevice {
  private:
    pthread_mutex_t depth_lock;
    pthread_mutex_t video_lock;
    std::vector<uint8_t> depth_buffer;
    std::vector<uint8_t> video_buffer;
    std::vector<uint16_t> gamma_buffer;
    bool new_depth_frame;
    bool new_video_frame;
    cv::Mat depthMat;
    cv::Mat videoMat;
  public:
    _Kinect_Device(freenect_context *_ctx, int _index) :
      Freenect::FreenectDevice(_ctx, _index),
      depth_buffer(FREENECT_DEPTH_11BIT),
      video_buffer(FREENECT_VIDEO_RGB),
      gamma_buffer(2048),
      new_depth_frame(false),
      new_video_frame(false),
      depthMat(cv::Size(640, 480), CV_16UC1),
      videoMat(cv::Size(640, 480), CV_8UC3) {
      for (uint32_t i = 0 ; i < 2048 ; i++) {
        float v = i / 2048.0;
        v = pow(v, 3) * 6;
        gamma_buffer[i] = v * 6 * 256;
      }
      pthread_mutex_init(&depth_lock, NULL);
      pthread_mutex_init(&video_lock, NULL);
    }
    ~_Kinect_Device();
    // Do not call directly even in child
    void DepthCallback(void *data, uint32_t timestamp);
    // Do not call directly even in child
    void VideoCallback(void *data, uint32_t timestamp);
    bool getDepth(cv::Mat& output);
    bool getVideo(cv::Mat& output);
};

class KinectDevice {
  private:
    _Kinect_Device *device;
    cv::Mat depthMat;
    cv::Mat videoMat;
    cv::Mat d2bgrMat;
    bool new_depth_frame;

    cv::Vec3b cd2bgr(uint16_t depth);
  public:
    KinectDevice();
    void start();
    void stop();
    cv::Mat getDepth();
    cv::Mat getVideo();
    cv::Mat getDepthAsBGR();
};

#endif
