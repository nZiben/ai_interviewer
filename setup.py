import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llm-survey-system",
    version="0.1.0",
    author="Sergey Volkov",
    # author_email="you@example.com",
    description="LLM-based Survey System with TTS and STT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/llm-survey-system",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
