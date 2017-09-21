# Use an official Python runtime as a parent image
FROM python:3.6

MAINTAINER Juan Francisco Huete Verdejo

# Install esentials

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    yasm \
    pkg-config \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    libavformat-dev \
    libpq-dev \
    libgtk2.0-dev \
    pkg-config


# Install requirements necessary for opencv
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Obtain, extract and compile opencv

RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip \
&& unzip 3.2.0.zip \
&& mkdir /opencv-3.2.0/cmake_binary \
&& cd /opencv-3.2.0/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DENABLE_AVX=ON \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=$(python3.6 -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python3.6) \
  -DPYTHON_INCLUDE_DIR=$(python3.6 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3.6 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
&& make install \
&& rm /3.2.0.zip \
&& rm -r /opencv-3.2.0

# Create user, his home and add to video and audio group

ENV HOME /home/opencv
RUN useradd --create-home --home-dir $HOME opencv \
  	&& chown -R opencv:opencv $HOME \
  	&& usermod -a -G audio,video opencv

# Config opencv user

USER opencv

# Create App folder

ADD app $HOME/app

# Set the working directory to /app

WORKDIR $HOME/app

# Run main

ENTRYPOINT ["python3", "main.py"]
