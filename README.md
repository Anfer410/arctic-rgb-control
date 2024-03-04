# Arctic RGB Control Master
This is a python code to replace https://support.arctic.de/rgb-controller, 

Original software is only available for windows, so I took a stab at trying to make it more OS agnostic.

## Requirements
In order to run this code you need to get [CH431SER](https://github.com/juliagoda/CH341SER) driver.

Python 3.11

>[!IMPORTANT]
>Script asumes that device is /dev/ttyUSB0, I will add config for that in the future for now you have to edit it in utils.py -> open_port(port='/dev/ttyUSB0')


## Run
```
python -m venv arctic-rgb
source arctic-rgb/bin/activate
python -m pip -r requirements.txt
python app.py
```

Go to web browser and access http://localhost:9000



## FAQ
- Q:Can't access the device. But device number is correct.
    - A: You have insufficient permissions on device. Run  ```sudo chmod 777 /dev/ttyUSB0```