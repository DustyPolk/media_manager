#!/usr/bin/env python3
"""Setup script for Media File Manager."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="media-file-manager",
        version="1.0.0",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        python_requires=">=3.8",
        install_requires=[
            "mutagen>=1.46.0",
            "Pillow>=9.0.0",
            "ffmpeg-python>=0.2.0",
            "python-magic>=0.4.27",
            "PyYAML>=6.0",
            "click>=8.0.0",
            "tqdm>=4.64.0",
            "colorama>=0.4.5",
        ],
        extras_require={
            "dev": [
                "pytest>=7.0.0",
                "pytest-cov>=4.0.0",
                "pytest-mock>=3.10.0",
                "black>=22.0.0",
                "flake8>=5.0.0",
                "mypy>=0.991",
                "pylint>=2.15.0",
            ]
        },
        entry_points={
            "console_scripts": [
                "media-manager=media_file_manager.main:main",
            ],
        },
        author="Your Name",
        author_email="your.email@example.com",
        description="Automated media file organization and metadata management",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/username/media-file-manager",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Video",
            "Topic :: Utilities",
        ],
    )
