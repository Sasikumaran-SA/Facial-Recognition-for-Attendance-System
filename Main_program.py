import Program_Functions
from time import sleep


# './Photos' should have only photos format as file and any folders is allowed and name of the image file is the name of the person, also the name of the person should be less than 50 character (not necessary)
# Don't try to add or remove any file or folder in the directory while running the program
# Light environment is perferred


def Initial(known_face_encodings,known_face_names,recognised_faces):                                                  # Initializing Function
    sleep(1)
    print("\n####\nFor Registering face, Enter 1  \nFor Attendance, Enter 2 \nFor Exit, Enter 0\n####\n")             # For input
    Input = input('Give your input : ')
    print()
    if Input=='1':
        print(">> Enter 'p' on the frame to take photo <<\n")
        return_tuple = Program_Functions.Take_Photo(known_face_names)                                                 # To update the existing list of face encodings and face names
        known_face_encodings.extend(return_tuple[0])
        known_face_names.extend(return_tuple[1])
        return Initial(known_face_encodings,known_face_names,recognised_faces)
    elif Input=='2':
        recognised_faces = Program_Functions.Face_rec(known_face_encodings,known_face_names,recognised_faces)         # To get recognised names
        return Initial(known_face_encodings,known_face_names,recognised_faces)
    elif Input=='0':
        print("Thank You! See you Soon...\n")                                                                         # End<<
        exit
    else:
        print("#### Please Give The Correct Value ####")                                                              # If other than 1, 2, 0 is given
        return Initial(known_face_encodings,known_face_names,recognised_faces)


print("\n---Facial Recognition for Attendance System---")                                                             # Start<<
print("\n<< To Stop Enter 'q' at any time >>")
print("<< Please Wait for Sometime >>")


if Program_Functions.Initializing():                                                                                  # For checking the requirements
    object1 = Program_Functions.face_encodings()
    known_face_encodings,known_face_names = object1.known_face_encodings()                                            # To get the registered face encodings at the begining itself

    Initial(known_face_encodings,known_face_names,[])                                                                 # To start the function
else:
    exit
