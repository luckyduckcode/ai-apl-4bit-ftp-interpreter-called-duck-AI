from setuptools import setup, Extension
import os

# Define the extension module
module = Extension(
    'apl_backend',
    sources=['src/backend/quantization.cpp'],
    extra_compile_args=['-O3'] if os.name != 'nt' else ['/O2'],
    language='c++'
)

setup(
    name='apl_backend',
    version='0.1',
    description='C++ Backend for AI-APL Interpreter',
    ext_modules=[module]
)
