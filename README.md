# ULR_TO_QR
I made a small webapp that lets you convert a ULR into a QR code based on reed_solomon algorithm
1. Install the background tools
Open your command line (Command Prompt on Windows or Terminal on Mac). Type the following command and press Enter:pip install flask pillow
This quickly downloads the tools the app needs to run a local web server and generate the image files.

2. Run the background script
In the same terminal, navigate to the folder where you saved all your project files (where app.py is located). Type this command and hit Enter:python app.py
You will see a few lines of text pop up telling you the server is running. Leave this terminal window open while you use the app; it acts as the engine powering the website.

3. Open the website
Open your regular web browser, like Chrome or Edge. In the address bar at the top, type [http://127.0.0.1:5000](http://127.0.0.1:5000) and press Enter. The QR generator interface will load immediately. When you are completely finished using the tool, you can just close the terminal window to shut the server down safely.
