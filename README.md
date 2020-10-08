# ratestask

Steps to configure and run the project:

- Open the `.env` file and add the database credentials for accessing the ratestask together with a valid App ID from https://openexchangerates.org/
-  If Postman application is available, import the `ratestask_collection.json`. It contains the list of API samples for the ratestask.
- Install the Python dependencies listed on the `requirements.txt`. You can do so by running `pip3 install -r requirements.txt`
- Init the python API by running `python api.py`
- The application is now listening for requests on `http://127.0.0.1:5000/`