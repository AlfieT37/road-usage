from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2', 'cv2', 'imutils', 'scikit-image', 'tqdm', 'progressbar', 'PIL'
]

setup(
    name='Webapp',
    version='0.1',
    description='A Web App built with flask',
    author='Alfie Thompson',
    author_email='alfiethompson37@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)