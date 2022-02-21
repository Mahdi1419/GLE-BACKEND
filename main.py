import logging
from flask import Flask, request, Response
from flask_cors import CORS
from bs4 import BeautifulSoup
import keyboard
app = Flask(__name__)
CORS(app)


def printInfo(info: dict):
  print("""
          Information received successfully
          _________________________

            Name:        =>   %s
            Description: =>   %s
            Image Link:  =>   %s

          _________________________
          """ % (info['name'].strip(), info['description'].strip(), info['img'].strip())))


def printJobs(jobs: list):
  print('\n          Best Matches Jobs')
  for index, job in enumerate(jobs):
      title=job.find("h4", {"class": "job-tile-title"}).getText()
      print(f'{" "*12}{index:02}: {title}')

  pass


# @app.route("/wait/<action>/", methods = ['GET'])
# def handleAction(action):
#     if action == "getupworkprofile":
#         os.system(
#             '"C:\Program Files\Google\Chrome\Application\chrome.exe" -new-window  getupworkprofile --no-startup-window')
#     return Response("Test")


@app.route('/page', methods = ['POST'])
def handlePage():
    """Handle account info"""

    # get page source (html dom)
    page=request.form['page']

    # parse page with bs4
    soup=BeautifulSoup(page, 'html.parser')

    # extract data from page
    name=soup.find("a", {"class": "profile-title"}).getText()
    description=soup.find("p").getText()
    img=soup.find("img", {"class": "up-avatar"})['src']

    # print info
    printInfo(
      info= {
        "name" : name,
        "description" : description,
        "img" : img,
      }
    )

    return Response("Test")


@app.route('/jobs', methods=['POST'])
def handleJobs():
    """"Handle jonbs"""
    
    # get page source (html dom)
    page=request.form['page']
    
    # parse page with bs4
    soup=BeautifulSoup(page, 'html.parser')
    
    # extract data from page
    jobs = soup.findAll("section")
    
    # print jobs
    printJobs(jobs)
    
    
    return Response("Test")


@app.route("/type/<action>/", methods=['POST'])
def type_simulate(action):

    if action in ['username', 'password']:
        print("Entering %s..." % action)
        text = request.form['text']
        keyboard.write(text)
    else:
        print('Receiving information...\n')

    return Response("Ok")


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(debug=True)
