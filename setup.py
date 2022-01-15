from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="PDSUtilities",
      version="0.0.1",
      description="Utilities for data science in python",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/DrJohnWagner/PDSUtilities",
      author="Dr. John Wagner",
      author_email="Dr.John.Wagner@gmail.com",
      license="Apache-2.0",
      packages=[
          "PDSUtilities"
      ],
      install_requires=[
          "numpy",
          "xgboost",
          "plotly",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)