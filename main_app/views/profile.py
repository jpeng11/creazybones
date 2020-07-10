from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models import Profile, Crazybone, Cb_Profile, TradeRequest, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'catcollector-jp'


@login_required
def user_profile(request, user_id):
    current_user = request.user
    try:
        user_profile = User.objects.get(id=user_id)
        user_cb = user_profile.profile.cb.all()
        user_cb_qty = 0
        for cbP in Cb_Profile.objects.filter(profile=user_profile.profile):
            user_cb_qty += cbP.qty
        all_cb = Crazybone.objects.all().order_by('id')

        trade = TradeRequest.objects.filter(user_from_id=request.user.id)
        return render(request,
                      'profile/detail.html', {
                          'current_user': current_user,
                          'user_profile': user_profile,
                          'user_cb_qty': user_cb_qty,
                          'user_cb': user_cb,
                          'all_cb': all_cb,
                          'trade': trade})
    except:
        user_profile = None
        return render(request,
                      'profile/detail.html', {
                          'current_user': current_user, 'user_profile': user_profile, })


class profileUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']


def add_photo(request, user_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, user_id=user_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect(f'/profile/{request.user.id}')
