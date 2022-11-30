import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="joonhee Cho", # Replace with your own username
    version="0.0.1",
    author="joocho",
    author_email="packet@kakao.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjoonhee/NDFC_joocho",
    project_urls={
        "Bug Tracker": "https://github.com/jjoonhee/NDFC_joocho",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": ""},
    packages=setuptools.find_packages(where="NDFC_API"),
    python_requires=">=3.6",
)