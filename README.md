# Facial-Recognition-for-Attendance-System
It is a python program which mainly uses opencv and face_recognition module to recognise face and take attendance. This program also helps to register the faces. The attendance taken will be saved in the csv file.

>>> Features in the program:
01. It ask each time what to do
02. If any wrong input is given it will ask again, at any time
03. If required folder is not there it will create like './Photos' and './Photos/Needs to Remove', also 'haarcascade_frontalface_default.xml' is necessary file, if it is not there it will ask to download
04. 'q' can be pressed to exit the process while entering the no. of person or person name or while taking photo in registering(only in image frame), while taking attendance also(only in image frame)
05. Encodes the stored photo and store it in list, at initial itself, also if it is found to have image with no face or with more than one image it will move that photo to './Photos/Needs to Remove' folder, in that folder if same name is present it will store in different name
06. Always while encoding, only the face is encoded
07. If a person is recognised once, they will not be recognised again
08. The newly encoded image will be added to the existing list, so time is saved in this while recognising again
09. While registering if the person name is already in Photos folder it will not acccept
10. The photo is taken only if 'p' is pressed on the image frame
11. Image window will be shown while taking photo also while taking attendance
12. If taken Photo taken have no face or more than one face it will not accept, saying to retake, if only one face detected it will store in './Photos' folder
13. Creates a .csv file if it is not present in that particular date for storing data like name-data-time of the recognised face at each time, or data will append to the file if it is already created
14. output with name, date and time is shown while recognising
15. Says if no face is registered
16. Ends the recognising process if all the members in the registered list is recognised
17. A blue box will appear on the any face in the image window while taking attendance
18. Shows the name and present status in image window
