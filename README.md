# MakerSpaceInventory
Tool for Organizing Inventory in MakerSpaces
Written in Python using MongoDB Cloud Database and Imgur 

Following python libraries are required to run the inventory tool and need to be installed via pip:
pip install pymongo[srv]
pip installopencv-python
pip installpillow
pip installxlsxwriter
pip installpyimgur
pip installpython-barcode
pip installqrcode


To use the tool a MongoDB Atlas Cluster is required: https://www.mongodb.com/
1) Create a new Cluster
2) Setup username and password for authentification
3) Add your IP to IP Access List and "Finish and Close"
4) click on connect --> connect your application --> Python 3.12 or later
5) Uncheck the box "Include full driver code example" and copy the provided
6) execute the python program and wait for the settings.txt to be created
7) open the settings.txt and paste the code from earlier to "connection_string= "
8) Change the copied code similar to the following snippet:"mongodb+srv://<username>:<password>@cluster0.jaa9a.mongodb.net/"
9) Enter your username and password
10) Configure the rest of the settings.txt (make sure not to leave spaces between the "=" and the entered information)
  
You can now use the MakerSpace Inventory Tool :)
  
(Save Pictures to Imgur for using the companion App)
(In order to save the item pictures online for using the app a imgur account is required)
(Create an application: https://api.imgur.com/oauth2/addclient)
 
