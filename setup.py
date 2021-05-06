from setuptools import setup, find_packages

setup(
    name='nuagelearning',
    version='1.0',
    description='A Federated Learning platform running in the cloud with Kafka',
    url='https://github.com/mcrts/nuage-learning',
    author='Martin Courtois',
    author_email='martin.courtois@protonmail.com',
    license='MIT',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=['numpy', 'confluent_kafka', 'sklearn'],
    zip_safe=False,
)