[<- Back to course](../README.md)

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
Export this directory using SVN.
```
svn export https://github.com/GrandEchoWhiskey/harvard-cs50-ai-projects/trunk/proj-5-traffic
```
Change directory
```
cd proj-5-traffic
```
Install requirements
```
pip3 install -r requirements.txt
```
Download gtsrb data
```
wget https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip
```
Unzip gtsrb data
```
unzip gtsrb.zip
```
Now run the script
```
python traffic.py data_directory [model.h5]
```
