import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio-metadata-updater",
    version="0.0.1",
    author="TR33HGR",
    author_email="",
    description="Scripts to update the metadata for my audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TR33HGR/audio-metadate-updater",
    project_urls={
        "Bug Tracker": "https://github.com/TR33HGR/audio-metadate-updater/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
      "pathlib",
      "mutagen",
    ],
    python_requires=">=3.7",
)