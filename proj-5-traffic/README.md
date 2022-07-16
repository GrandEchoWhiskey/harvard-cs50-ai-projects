[<- Back to course](https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/dict/course/CS50-HarvardX/CS50AI/README.md)

<p align="center"><a href="https://cs50.harvard.edu/ai/2020">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/course/harvard100.png" /><br>
</a></p>
<h1 align="center">CS50’s Introduction to Artificial Intelligence with Python<br><br>Traffic</h1>

<p align="center"><a href="#">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/python.png" />
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/tensorflow.png" />
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/scikit.png" />
</a></p>

### Background:
As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

### Getting Started:
Clone this repository.
```
git clone https://github.com/GrandEchoWhiskey/harvard-cs50-ai-traffic
```
Unzip gtsrb.zip. Keep the resulting gtsrb directory inside of the traffic directory.
```
unzip gtsrb.zip
```
Inside of the traffic directory, run below command to install this project’s dependencies: opencv-python for image processing, scikit-learn for ML-related functions, and tensorflow for neural networks.
```
pip3 install -r requirements.txt
```
Now run the program.
```
python traffic.py gtsrb
```
