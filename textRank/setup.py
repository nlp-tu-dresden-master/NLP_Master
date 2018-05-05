from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

# Maybe it's possible to enter path to en_core_web stuff to install all shit.
setup(name='pytextrank',
      version='1.1.0',
      description='Python implimentation of TextRank for text document NLP parsing and summarization',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='textrank, parsing, automatic summarization, natural language processing, nlp, text analytics',
      url='http://github.com/ceteri/pytextrank',
      author='Paco Nathan',
      author_email='ceteri@gmail.com',
      license='Apache License 2.0',
      packages=['pytextrank'],
      install_requires=[
      ],
      zip_safe=False)
