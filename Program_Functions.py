import face_recognition
import cv2
from numpy import argmin
from csv import writer
from os import listdir,mkdir,path,rename
from datetime import datetime


def Initializing():                                                                                      # For initializing
    dirname1=listdir('./')
    if 'Photos' not in dirname1:                                                                         # If './Photos' is not present
        mkdir('./Photos')
        mkdir('./Photos/Needs to Remove')
    else:                                                                                                # If './Photos/Needs to Remove' is not present
        dirname2=listdir('./Photos')
        if 'Needs to Remove' not in dirname2:
            mkdir('./Photos/Needs to Remove')
    
    if 'haarcascade_frontalface_default.xml' not in dirname1:                                            # If 'haarcascade_frontalface_default.xml' is not present
        print('\n>> Please download haarcascade_frontalface_default.xml from "https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml"')
        print('>> Store it in ./')
        print('>> Then try to run the program...')
        print("Thank You! See you Soon...\n")
        return 0
    return 1


class face_encodings:                                                                                    # To get the face encodings and registred names at the begining itself
    def __init__(self):
        self.face_encodings=[]
        self.face_names=[]

    def known_face_encodings(self):
        file_names_list = [f for f in listdir('./Photos') if path.isfile(path.join('./Photos', f))]
        for file_name in file_names_list:                                                                # For encoding the stored image
            name_image = face_recognition.load_image_file(f"./Photos/{file_name}")                       # Also to Remove the unwanted one
            name_locations = face_recognition.face_locations(name_image)                     
            name_encoding = face_recognition.face_encodings(name_image,name_locations)       
            if len(name_encoding)==0:
                print(f'\n>> {file_name} has no Face recognised <<')
                print('Kindly Remove it or Replace it from "Needs to Remove" folder...')
                try:
                    rename(f'./Photos/{file_name}', f'./Photos/Needs to Remove/{file_name}')
                except:
                    name=path.splitext(file_name)[0]
                    rename(f'./Photos/{file_name}', f'./Photos/Needs to Remove/{name}(1).png')
            elif len(name_encoding)>1:
                print(f'\n>> {file_name} have more than one Face <<')
                print('Kindly Remove it or Replace it from "Needs to Remove" folder...')
                try:
                    rename(f'./Photos/{file_name}', f'./Photos/Needs to Remove/{file_name}')
                except:
                    name=path.splitext(file_name)[0]
                    rename(f'./Photos/{file_name}', f'./Photos/Needs to Remove/{name}(1).png')
            else:
                self.face_encodings.append(name_encoding[0])
        
        file_names_list = [f for f in listdir('./Photos') if path.isfile(path.join('./Photos', f))]
        for file_name in file_names_list:                                                                # To get the name of the person
            name = path.splitext(file_name)[0]
            self.face_names.append(name)
        
        return self.face_encodings,self.face_names


def Take_Photo(Already_registered_Names):                                                                # Photo Taking Function
    face_encodings = []
    face_names = []
    no_of_person = input("Enter the Number of Person: ")
    if no_of_person=='q':                                                                                # Use of 'q'
        return face_encodings,face_names
    else:                                                                                                # If other than integer input is given
        try:
            no_of_person = int(no_of_person)
        except:
            print('#### Enter the correct input ####\n')
            return Take_Photo(Already_registered_Names)

    while no_of_person>0:
        cam = cv2.VideoCapture(0)
        mkr = 1
        name = input("\nEnter person's name : ")
        if name=='q':                                                                                    # Use of 'q'
            cam.release()
            cv2.destroyAllWindows()
            return face_encodings,face_names
        elif name in Already_registered_Names:                                                           # To know the person is registered or not
            print('>> The Person\'s name is already Registered <<')
            print('Give Another name...')
            no_of_person+=1
            mkr = 0
        while(1):
            if cv2.waitKey(1) & 0xFF == ord('q'):                                                        # To end Recognising the person, Use of 'q'
                cam.release()
                cv2.destroyAllWindows()
                break
            if mkr==0:
                break
            _,image = cam.read()                                                                         # To Take Photo
            cv2.imshow(name,image)
            if cv2.waitKey(1) & 0xFF == ord('p'):                                                        # If 'p' is pressed photo is taken
                cam.release()
                cv2.destroyAllWindows()
                inp_locations = face_recognition.face_locations(image)
                inp_encoding = face_recognition.face_encodings(image,inp_locations,num_jitters=2)
                if len(inp_encoding)==0:                                                                 # To Check that the taken Photo have Zero face 
                    print('>> No Face is recognised! <<')
                    print('Please Register the Person again...')
                    no_of_person+=1
                    break
                elif len(inp_encoding)>1:                                                                # To Check that the taken Photo have more than one face
                    print('>> More than one face is recognised <<')
                    print('Please Register with one Person...')
                    no_of_person+=1
                    break
                cv2.imwrite('./Photos/'+name+'.png', image)                                              # To Store the Taken Photo
                print(f"{name} is Successfully Registered")
                Already_registered_Names.append(name)
                face_names.append(name)
                face_encodings.append(inp_encoding[0])
                break
        no_of_person-=1
    cam.release()
    cv2.destroyAllWindows()
    return face_encodings,face_names                                                                     # Returning the registered person to get add in the known faces


def Face_rec(known_face_encodings,known_face_names,recognised_faces):                                    # Face Recognising Function
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_locations = []
    face_encodings = []
    mkr = 0                                                                                              # To know if there are registered face or not
    current_date = datetime.now().strftime(r"%Y-%m-%d")
    
    try:
        f = open(current_date+'.csv','a',newline = '')                                                   # To append in the csv file
        lnwriter = writer(f)
    except:
        f = open(current_date+'.csv','w+',newline = '')                                                  # To create a new csv file if it is not there
        lnwriter = writer(f)
    
    if len(known_face_names)==0 and mkr==0:                                                              # To know that if there is registered face
        print("!! The Registration is Empty, Please Enter '1' to Register !!")
        return recognised_faces
    
    while True:
        if len(recognised_faces)==len(known_face_names) and mkr==1:                                      # To end the process if all the person is taken the attendance
            print("Everyone is present! Thank You for the attendance..")
            break
        
        _,frame = video_capture.read()                                                                   # To Take Photo
        cv2.imshow("Facial Recognition for Attendance System",frame)                                     # To show the frame
        # scale_percent = 40
        # width = int(frame.shape[1]*scale_percent/100)
        # height = int(frame.shape[0]*scale_percent/100)
        # small_frame = cv2.resize(frame,(width,height))

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)                                                   # For getting box in the camera image for any face
        faces = face_cascade.detectMultiScale(gray, 1.1, 1)                                              ## Scalefactor in detectMultiscale should be min to detect face, to be max to detect with more accuracy
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face_locations = face_recognition.face_locations(frame)                                          ## Small_frame can be used, but it may or may not reduse the speed of the program
        face_encodings = face_recognition.face_encodings(frame,face_locations)                           # For encoding the captured image
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding,0.45)            # To compare face encoding and return True-False list
            face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)           # Minimum the face distance means more the matches
            best_match_index = argmin(face_distance)
            name = known_face_names[best_match_index]

            if matches[best_match_index] and name not in recognised_faces:                               # Matches if have True value for that face and not in already registered names
                current_date = datetime.now().strftime(r"%Y-%m-%d")
                present_time = datetime.now().strftime("%H:%M:%S")

                font                   = cv2.FONT_HERSHEY_SIMPLEX                                        # For getting name in camera window
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2
                cv2.putText(frame,name+' Present',
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
                
                print(f"{f'{name} is present':<50}",current_date,present_time)
                lnwriter.writerow([name,current_date,present_time])                                      # Register in csv file                                   
                recognised_faces.append(name)
                mkr = 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):                                                            # To end Recognising the person, Use of 'q'
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()
    return recognised_faces                                                                              # Return recognised faces list