from django.shortcuts import render, redirect
from .models import User, Video, Review
from django.contrib import messages
import bcrypt, requests, random, math

def index(request):
    print (60* "*")

    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if errors:
        for category, message in errors.items():
            messages.error(request, message)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash)  

    new_user = User.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], password = pw_hash)
    request.session['userid'] = new_user.id
    print (60 * "*")
    print (new_user)

    return redirect('/drop_menu')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    logged_user=User.objects.get(id=request.session['userid'])
    context = {
        "logged_user" : logged_user
    }

    return render(request, "drop_menu.html", context)

def login(request):
    print (25 * "*")
    print (request.POST["email"])
    user = User.objects.filter(email = request.POST["email"])

    if not user:
        messages.error(request, "Login failed. And that's fine.")
        return redirect('/')

    if user:
        logged_user = user[0]

    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        # if we get True after checking the password, we may put the user id in session
        request.session['userid'] = logged_user.id
        # never render on a post, always redirect!
        return redirect('/drop_menu')

    messages.error(request, "Login failed. And that's fine.")
    return redirect('/')

def front_page(request):
    if 'userid' not in request.session:
        return redirect('/')
    logged_user=User.objects.get(id=request.session['userid'])
    context ={
        "logged_user" : logged_user
    }

    return render(request, "front_page.html", context)


def logout(request):
    del request.session['userid']
    return redirect('/')

def drop_menu(request):
    all_videos = []
    more_videos = []
    logged_user=User.objects.get(id=request.session['userid'])
    last_review = Review.objects.all().last()
    for i in range(3):
        rand1 = random.randint(1,math.floor((last_review.id)/2))
        temp_review = Review.objects.get(id = rand1)
        all_videos.append(temp_review.video)
    for i in range(3):
        rand1 = random.randint(math.floor((last_review.id)/2), last_review.id-1)
        temp_review = Review.objects.get(id = rand1)
        more_videos.append(temp_review.video)
    print(rand1, "$$$$$")
    context ={
        "all_videos" : all_videos,
        "more_videos" : more_videos,
        "logged_user" : logged_user

    }
    return render(request, "drop_menu.html", context)

def search_youtube(request):
    if 'userid' not in request.session:
        return redirect('/')
    logged_user=User.objects.get(id=request.session['userid']
    )
    yummyVariable = request.POST['searchParameter']
    search_term = request.POST["search"]
    print(yummyVariable)

    # part of dynamic page2 attempt
    # next_term= 13
    # request.session['next_term'] = int(next_term)

    # live search of youtube, works great, only runs if seacrh is not already in db, saving api calls.
    if Video.objects.filter(search = search_term).first():
        data = []
    else:
        url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&order=viewCount&q={search_term}%20recipe&safeSearch=none&videoCaption=any&lr=lang_en&key=" ''
        response = requests.get(url) 
        data = response.json()
        for i in range(50):
            add_id = data["items"][i]["id"]["videoId"]
            if Video.objects.filter(video_id = add_id):
                pass
            else: Video.objects.create(video_id = add_id, search = search_term)
    if yummyVariable == "none":
        all_videos = Video.objects.filter(search = search_term)[:12]
    else:
        all_videos =[]
        all_reviews = Review.objects.filter().order_by(yummyVariable).reverse()[:50]
        for i in range(50):
            temp_video = all_reviews[i].video
            if temp_video.search == search_term:
                all_videos.append(temp_video)


    # doesn't work video_id undefined
    # review_of_videos = Review.objects.filter(video=Video.objects.get(id={{video_id}}))
    context ={
        "data" : data,
        "all_videos" : all_videos,
        "logged_user" : logged_user,
        "search_term" : search_term


    }
    return render(request, "front_page.html", context)

def page2(request, search_term):
    logged_user=User.objects.get(id=request.session['userid'])

    # to make next page dynamic, can't parse int in brackets though...
    # next_term=(request.session['next_term'])
    # next_term_plus = int(next_term) +12
    # first_term = int(next_term)
    all_videos = Video.objects.filter(search = search_term)[13:25]

    # doesn't work video_id undefined
    # review_of_videos = Review.objects.filter(video=Video.objects.get(id={{video_id}}))
    context ={
        "all_videos" : all_videos,
        "logged_user" : logged_user,
        "search_term" : search_term
    }
    return render(request, "page2.html", context)

def page3(request, search_term):
    logged_user=User.objects.get(id=request.session['userid'])
    all_videos = Video.objects.filter(search = search_term)[26:38]
    context ={
        "all_videos" : all_videos,
        "logged_user" : logged_user,
        "search_term" : search_term
    }
    return render(request, "page3.html", context)

def page4(request, search_term):
    logged_user=User.objects.get(id=request.session['userid'])
    all_videos = Video.objects.filter(search = search_term)[39:50]
    context ={
        "all_videos" : all_videos,
        "logged_user" : logged_user,
        "search_term" : search_term
    }
    return render(request, "page4.html", context)    

def view_reviews(request, video_id):
    logged_user=User.objects.get(id=request.session['userid'])
    this_video = Video.objects.get(video_id=video_id) 
    y = 0
    e = 0
    h = 0
    n = 0
    count = 0
    for review in this_video.review_of_video.all():
        y = review.yummy +y
        e = review.easy + e
        h = review.healthy+ h
        n = review.entertaining + n
        count = count +1
    if count ==0:
        pass
    else:
        y = y/count
        e = e/count
        h = h/count
        n = n/count
    context ={
        "y" : y,
        "e" : e,
        "h" : h,
        "n" : n,
        "logged_user" : logged_user,
        "video_id" : video_id,
        "this_video" : this_video
    }
    return render(request, "view_reviews.html", context)

def view_write(request, video_id):
    
    logged_user=User.objects.get(id=request.session['userid'])
    video_list = Video.objects.filter(video_id = video_id)
    v_id = video_list[0].id
    reviewed_video = Video.objects.get(id = v_id)
    # this might work?
    print(logged_user.review_by_user)
    if logged_user.review_by_user:
        this_review = Review.objects.create(article = request.POST["review"],yummy = request.POST["yummy"],easy = request.POST["easy"],entertaining = request.POST["entertaining"],healthy = request.POST["healthy"], video = reviewed_video, user = logged_user)
        
    else:
        this_review_list = Review.objects.filter(user= logged_user.id)
        r_id = this_review_list[0].id
        this_review = Review.objects.get(id = r_id)
        this_review.article = request.POST["review"]
        this_review.yummy = request.POST["yummy"]
        this_review.easy = request.POST["easy"]
        this_review.entertaining = request.POST["entertaining"]
        this_review.healthy = request.POST["healthy"]
        this_review.save()
        print (50*"&")


    print(60 *"*", video_id, this_review.article, this_review.yummy)
    request.session['video_id'] = video_id
    return redirect("/display_review")

def display_review(request):
    video_id = request.session.get('video_id')
    print(50*"$", video_id)
    logged_user=User.objects.get(id=request.session['userid'])
    this_video = Video.objects.get(video_id=video_id) 
    y = 0
    e = 0
    h = 0
    n = 0
    count = 0
    for review in this_video.review_of_video.all():
        y = review.yummy +y
        e = review.easy + e
        h = review.healthy + h
        n = review.entertaining + n
        count = count +1
    y = y/count
    e = e/count
    h = h/count
    n = n/count
    context ={
        "y" : y,
        "e" : e,
        "h" : h,
        "n" : n,
        "logged_user" : logged_user,
        "video_id" : video_id,
        "this_video" : this_video
    }
    return render(request, "display_review.html", context)

def my_reviews(request):
    logged_user=User.objects.get(id=request.session['userid'])
    my_reviews = Review.objects.filter(user_id = User.objects.get(id=logged_user.id))
    context ={
        "my_reviews" : my_reviews,
        "logged_user" : logged_user
    }
    return render(request, "my_reviews.html", context)

def edit_review(request, review_id):
    logged_user=User.objects.get(id=request.session['userid'])
    this_review =Review.objects.get(id =review_id)
    this_video = Video.objects.get(video_id=this_review.video.video_id) 
    y = 0
    e = 0
    h = 0
    n = 0
    count = 0
    for review in this_video.review_of_video.all():
        y = review.yummy +y
        e = review.easy + e
        h = review.healthy + h
        n = review.entertaining + n
        count = count +1
    y = y/count
    e = e/count
    h = h/count
    n = n/count
    context ={
        "y" : y,
        "e" : e,
        "h" : h,
        "n" : n,
        "logged_user" : logged_user,
        "video_id" : this_review.video.video_id,
        "review_id" : review_id,
        "this_review" : this_review,
        "this_video" : this_video
    }
    return render(request, "edit_review.html", context)

def update_review(request, review_id):
    edit_review =Review.objects.get(id =review_id)
    edit_review.article = request.POST["review"]
    edit_review.yummy = request.POST["yummy"]
    edit_review.easy = request.POST["easy"]
    edit_review.entertaining = request.POST["entertaining"]
    edit_review.healthy = request.POST["healthy"] 
    edit_review.save()
    request.session['video_id'] = edit_review.video.video_id
    return redirect("/display_review")

def delete_review(request, review_id):
    delete_review =Review.objects.get(id =review_id)
    delete_review.delete()
    return redirect("/my_reviews")

# def advanced_search(request):
#     print (20*"^",request.Get["yummy"])
#     yummy_variable = request.Get["yummy"]
#     easy_variable = request.Get["easy"]
#     entertaing_variable = request.Get["entertaining"]
#     healthy_variable = request.Get["heathly"]
#     top_videos = Video.objects.all().order_by('{yummy_variable}')

#     return redirect("/success")

