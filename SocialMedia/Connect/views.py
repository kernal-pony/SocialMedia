
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from django.db.models import Q## only include if anything to enquire.. its query set
from .models import *


from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
# Create your views here.
def Login(request):

    if request.user.is_authenticated:
        return redirect("UserProfile", request.user.username)


    form = AddUser_Form() ### very important if i use django forms!!
    error1 = False
    if request.method == "POST":
        un = request.POST["un"]
        ps = request.POST["ps"]
        usr = authenticate(username=un, password=ps)
        if usr != None:
            login(request, usr)
            return redirect("UserProfile", usr.username)
        error1 = True
    Dict = {
        "error1": error1,
        "form": form,
    }
    return render(request, "login_register.html", Dict)

def Logout(request):
    logout(request)
    return redirect("login")



def Register(request):
    if request.user.is_authenticated:
        return redirect("UserProfile",request.user.username)

    error2 = False
    form = AddUser_Form()
    if request.method == "POST":
        form = AddUser_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            username = request.POST["un"] ## this is from html form
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                error2 = True
            else:
                ps = request.POST["ps"] ## this is from html form
                email = data.email
                usr = User.objects.create_user(username, email, ps)
                data.usr = usr
                data.save()  ## this line means we have successfully connected "UserDB" with our own "userdatabase"!
                return redirect("login")


    Dict={
        "form": form,
        "error2": error2,

    }

    return render(request,"login_register.html", Dict)

def Reset_Password(request):
    error = False
    if request.method == "POST":

        data = request.POST
        username = data.get("un")
        new_password = data.get("ps")

        # Check if the user exists
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            user = User.objects.get(username=username)
        # Update password
            user.set_password(new_password)
            user.save()
            return redirect('login')  # Redirect to the login page after successful password reset
        else:
            error = True


    Dict= {
        "error": error

    }
    return render(request, 'reset_password.html',Dict)  # Render the password reset form if GET request



def UserDetails(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")

    usr = User.objects.filter(username=Username) ## here, we implement--> if user tries gribberish username, it should direct him to logged in account
    if not usr:
        logged_in_username = request.user.username
        return redirect("UserProfile", logged_in_username)
                ###### till this point it was prev codes..

    ########################## Section to count all friends and send them ######################################
    logged_in_user = User.objects.get(username=request.user.username)
    me = userdatabase.objects.get(usr=logged_in_user)  ## details about the one who is logged in


    count_friends = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by("-date")
                        ############ Section Ends
                    ##### this code is for frnd reqst accept/reject.
    connection = None
    friend_status = None
    if request.user.username != Username: ##here, I am visiting else's profile.
        user1 = User.objects.get(username=Username) ## whom I am sending
        user2 = User.objects.get(username=request.user.username) ## its me, who is logged in. |

        UserData1 = userdatabase.objects.get(usr=user1)
        UserData2 = userdatabase.objects.get(usr=user2)
        connection = Connections.objects.filter((Q(sender=UserData1, receiver=UserData2, status="friend") | Q(sender=UserData2, receiver=UserData1, status="friend")) | (Q(sender=UserData1, receiver=UserData2, status="Sent") | Q(sender=UserData2, receiver=UserData1, status="Sent")))
        ##print(connection)

        if connection:
            connection = connection[0]


        con_status = Connections.objects.filter(Q(sender=UserData1, receiver=UserData2,status="friend") | Q(sender=UserData2, receiver=UserData1, status="friend"))

        for c in con_status:
            friend_status = c.status
    #########################################################################################################
    ## concept:- if above condition is false, then we have some data in ('usr')
    ## trying to get the unique user details to make html pages DYNAMIC!!!
    Usr = usr[0]
    User_Details = userdatabase.objects.get(usr=Usr) ## here i have extended the django's User DB,so I try to filter users using a normal user as foreign key
                                                        ## first usr is attribute of man-defined-DB 'userdatabase' and second Usr is a variable having the data of 'User' DB


    ####################################################################################################
    ########################## Collecting all posts per user and send it to front end #################################


    all_posts = Blogs_Model.objects.filter(usr=Usr).order_by("-date")  # 1st 'usr' is the foreignkey to blog model && 2nd 'usr' is the foreignkey to userdatabase !!

   ##################### This section is fro who ever liked or disliked..####################
    likedIDs = []
    dislikedIDs = []

    all_likesbypersons = BlogLiked.objects.filter(usr=request.user)
    all_dislikesbypersons = BlogDisliked.objects.filter(usr=request.user)

    for i in all_likesbypersons:
        likedIDs.append(i.blog.id)

    for i in all_dislikesbypersons:
        dislikedIDs.append(i.blog.id)

    ################################ Section Ends


    Dict={
        "Profile": User_Details, ## here, I'm passing all the details I have about any REGISTERED user.. as User_details is the bundle of all data.
        "connection": connection,
        "count_friends": count_friends,
        "friend_status": friend_status,
        "all_posts": all_posts,
        "likedIDs": likedIDs,
        "dislikedIDs": dislikedIDs,

    }
    return render(request, "user_details.html",Dict)

def Update_User_Details(request,Username):

    if not request.user.is_authenticated:
        return redirect("login")

    logged_in_username = request.user.username
    if Username != logged_in_username: ## applying security i.e others cant edit my details
        return redirect("UserProfile", logged_in_username)

    usr = User.objects.filter(username=Username) ## finding details of my user to edit

    Usr = usr[0]
    User_Details = userdatabase.objects.get(usr=Usr)



    form = Edit_User_Details(request.POST or None, request.FILES or None, instance=User_Details)## instance here relating to the usrdtails views
    if form.is_valid():
        form.save()
        return redirect("UserProfile", logged_in_username)

    Dict = {
        "Profile": User_Details,
        "form": form,
    }
    return render(request, "Update_User_Details.html", Dict)

#####################################################################################
########################  This section tells how to filter connection DB and send data to front end.########################


def All_Profession(request,what):
    if not request.user.is_authenticated:
        return redirect("login")
        ####################################################################################


    logged_in_user = User.objects.get(username=request.user.username)
    me = userdatabase.objects.get(usr=logged_in_user)  ## details about the one who is logged in

    ####################### Count sent request/ received request/  friends section ##################

    count_received_request = Connections.objects.filter(receiver=me, status="Sent")
    count_sent_request = Connections.objects.filter(sender=me, status="Sent")
    count_friends = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by("-date")

    ####################### Se ction Ends #########################################



    #################### Filtering Db according to conditions ###########
    ### here we will filter all - accept or reject requests ########
    data = ""
    All_requests_directed_to_me=""
    All_sent_requests_to_others = ""
    friends = ""

    if what == "all":
        data = userdatabase.objects.all()

    elif what == "my_received_requests":
        connection = Connections.objects.filter(receiver=me, status="Sent")
        #print(connection)
        User_Data=[]
        for c in connection:
            ud = userdatabase.objects.get(id=c.sender.id)
            User_Data.append(ud)
        data = User_Data

    elif what == "my_SENT_request":
        connection = Connections.objects.filter(sender=me, status="Sent")
        User_Data = []
        for c in connection:
            ud = userdatabase.objects.get(id=c.receiver.id)
            User_Data.append(ud)

        data = User_Data
    elif what == "friends":
        connection = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by("-date")
        Data = []

        for c in connection:
            UserData = userdatabase.objects.get(id=c.sender.id)
            if UserData.id != me.id:
                Data.append(UserData)

            UserData = userdatabase.objects.get(id=c.receiver.id)
            if UserData.id != me.id:
                Data.append(UserData)

            data = Data
    ## this was to get all registered users. and list them in front-end

    Dict = {
        "all_users": data,
        "what": what,
        "count_received_request": count_received_request,
        "count_sent_request": count_sent_request,
        "count_friends": count_friends,
     }

    return render(request,"professionals.html", Dict)


###################  CONCEPT:- UNIVERSAL FUNCTION #####################
def Manage_your_connections(request, action, u_id,):
    if not request.user.is_authenticated:
        return redirect("login")

    if action == "send_Request":
        ## in the following line,We are trying to access the person who is logged in ? and will send friend request to others to var senderUser
        senderUser = User.objects.get(username=request.user.username)
        #print((senderUser))

        ##Now, we will replace senderUser with sender because sender cant directly connect with User DB but via 'usr', as follows:-
        sender = userdatabase.objects.get(usr=senderUser)

        receiver = userdatabase.objects.get(id=u_id)##(Note:- 1.'id' is a predefined attribute when we create any model. 2. we dont need to manually pass u_id because everything is connected with 'user_details.html' page.. there we are only using Profile.id..work is done and dusted.(refer plz!!!)

        Connections.objects.create(sender=sender, receiver=receiver) ##accessing the attributes of Connections model
        return redirect("UserProfile", receiver.usr.username)

    if action == "accept_request" or action == "reject_request" :
        receiverUser = User.objects.get(username=request.user.username)
        receiver = userdatabase.objects.get(usr=receiverUser)
        sender = userdatabase.objects.get(id=u_id)
        connection = Connections.objects.filter(sender=sender, receiver=receiver)  ##accessing the attributes of Connections model
        if connection:
            for c in connection:
                if action == "accept_request":
                    c.status = "friend"
                    c.save()
                if action == "reject_request":
                    c.delete()

        return redirect("professional", 'all')



################################# Section Ends ##################################################

################################# Section to filter connection data in front end only #############################


def All_Professional_filter_in_HTML(request,what):
    if not request.user.is_authenticated:
        return redirect("login")
        ####################################################################################

    logged_in_user = User.objects.get(username=request.user.username)
    me = userdatabase.objects.get(usr=logged_in_user)  ## details about the one who is logged in

    ####################### Count sent request/ received request/  friends section ##################

    count_received_request = Connections.objects.filter(receiver=me, status="Sent")
    count_sent_request = Connections.objects.filter(sender=me, status="Sent")
    count_friends = Connections.objects.filter(Q(sender=me, status="friend") | Q(receiver=me, status="friend")).order_by("-date")

    data = ""
    if what == "all":
        data = userdatabase.objects.all()

    Dict = {
        "all_users": data,
        "me": me,
        "what": what,
        "count_received_request": count_received_request,
        "count_sent_request": count_sent_request,
        "count_friends": count_friends,
    }

    return render(request, "professionals_in_html.html", Dict)



########## Start Company ########################


def Add_Company(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = StartCompany_Form()
    if request.method == "POST":
        form = StartCompany_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            usr = request.user ## we have  directly linked our 'normal usr variable'  to the User class DB.
            data.usr = usr
            data.save()
            return redirect("login")
    Dict={
        "form": form,
    }
    return render(request,"add_company.html",Dict)


def Company_Detail(request):
    if not request.user.is_authenticated:
        return redirect("login")

    usr = request.user ## we have  directly linked our 'normal usr variable'  to the User class DB..
    company = Company_Model.objects.filter(usr=usr) ## 'usr' is the foreignkey , though which we are filtering who all have company.


    if not company:
        return redirect("login")

    Dict = {
        "company": company[0],
    }
    return render(request, "companies_details.html", Dict)

##################### Blogging Section Begins #############################
def NewPost(request):
    if not request.user.is_authenticated:
        return redirect("login")
    Usr = User.objects.get(username=request.user.username)
    persons_details = userdatabase.objects.get(usr=Usr)
    form = UserBlog_Form()
    if request.method == "POST":
        form = UserBlog_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)

            data.usr = request.user
            data.save() ## this line means we have successfully connected "UserDB" with our own "userdatabase"!
            return redirect("login")

    Dict = {
        "form": form,
        "Profile": persons_details,
    }
    return render(request, "new_post_from_user.html", Dict)


def Blogs_Liked(request, blog_id,Username): ## id of certain blog which is passed from html->url-> views!!!
    if not request.user.is_authenticated:
        return redirect("login")

    blg_id = Blogs_Model.objects.get(id=blog_id)
    BlogLiked.objects.create(usr=request.user, blog=blg_id)
    return redirect("UserProfile",Username)

def Blogs_Disliked(request, blog_id,Username): ## id of certain blog which is passed from html->url-> views!!!
    if not request.user.is_authenticated:
        return redirect("login")

    blg_id = Blogs_Model.objects.get(id=blog_id)
    BlogDisliked.objects.create(usr=request.user, blog=blg_id)
    return redirect("UserProfile", Username)


def SendMail(email, msg):
    sender = settings.EMAIL_HOST_USER
    receiver = [email]
    html = get_template("mail.html")
    sub = "Blog"
    send_mail(sub," ", sender,receiver,html_message=html)