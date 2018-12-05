# Parsy

This is a messenger chat bot used for extracting text from images, so that you can copy them and can use at other places. It uses Google Cloud Vision
API for OCR (Optical Character Recognition). If you want to try it out, head over to Parsy facebook page: [Link](m.me/894199580971244)

## Steps for setting up backend server
1. Install python dependencies, assuming that you have pip already setup.
```bash
pip install -r requirements.txt
```
2. Run the flask application using
```bash
python app.py
```
Now the backend is up and ready for serving requests.

I have used `gunicorn` as my WSGI server and `nginx` as reverse proxy on top of it.

To start the WSGI server at port 8000, execute the following command:
```bash
./start.sh
``` 
This shell file start the WSGI server at port 8000, *nothing fancy*

## Steps for setting up Google Cloud Vision
Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the file path of the JSON file that contains your service account key.
```bash
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

## Resources Used
* [Secure Deployment](https://medium.com/@samuel.ngigi/deploying-python-flask-to-aws-and-installing-ssl-1216b41f8511)
* [Message Events](https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages)

## Author
* yashLadha