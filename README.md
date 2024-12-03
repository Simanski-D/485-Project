# Setup Instructions
- Install Python (3.9-3.12). Make sure to click the "Add python.exe to PATH" checkbox.
- The following commards should be entered into the terminal:
  - Create a virtual environment for your project: `python -m venv <your_venv_name>`
  - Navigate into the /Scripts directory: `cd <your_venv_name>/Scripts` and activate the virtual env: `./activate`. Navigate back `cd ../`
  - Clone the repo into your venv: `git clone https://github.com/Simanski-D/485-Project.git`
- When working on and running the website. Make sure to activate the virtual environment that you created (See the previous step).
- Install dependencies:
  ```
  pip install flask
  ```
  ```
  pip install flask_cors
  ```
  ```
  pip install mysql-connector-python
  ```
  ```
  pip install scikit-learn
  ```
  ```
  pip install pandas
  ```
  ```
  pip install tensorflow
  ```
- Under `pyvenv.cfg` double check that `include-system-site-packages = true`
