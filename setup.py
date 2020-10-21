import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="video_stream_queue",
    version="0.0.1",
    author="Victor Garcia",
    author_email="vgarcia@visiona-ip.es",
    description="Video stream queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vgarcia1/video_stream_queue.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
          'opencv-python',
      ],
    zip_safe=False
)