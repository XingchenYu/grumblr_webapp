from __future__ import unicode_literals
from django.db.models import Max
from django.utils.html import escape
from django.db import models
from django.contrib.auth.models import User
import datetime

from django.contrib.auth.models import AbstractUser



class Myuser(models.Model):
    user = models.OneToOneField(User, related_name="MAIN",  on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.CharField(max_length=420, null=True, blank=True)
    photo = models.ImageField(upload_to = "user-images", null=True, blank = True)
    follow = models.ManyToManyField(User, related_name="FOLLOW")

    def __unicode__(self):
        return self.user.username

class Blog(models.Model):
    content=models.CharField(max_length=42)
    pub_date=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    last_changed=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Blog.objects.filter(last_changed__gt=time).distinct()

    @property
    def html(self):
        # return "<p id='blog_%d'>%s</p>" % (self.id, escape(self.content))
        # result = '<div class="content float-left round-border">'
        # result = result + '<div class="content-writer float-left">'
        # result = result + '<img class="float-left round-border" alt="%s %s" height="80" width="80"/>' %(self.user.first_name, self.user.last_name)
        # result = result + '<a class="stream-username" >%s</a></div>' %(escape(self.user.username))
        # result = result + '<div class="content-text float-left"><a class="stream-content changerow">%s</a></div>' %(escape(self.content))
        # result = result + '<div class="content-time float-right"><p class="steam-posttime">%s</p></div></div>' %(escape(self.pub_date))
        # return result


        result = """<div>
                        <div class='content float-left round-border'>
                            <div class='content-writer float-left'>
                                <img class='float-left round-border' src='photo%s' alt='%s %s' height='80' width='80'/>
                                <a class='stream-username' href='profile%s' >%s</a>
                            </div>
                            <div class='content-text float-left'>
                                <p class='stream-content changerow'>%s</p>
                            </div>
                            <div class='content-time float-right'>
                                <p class='steam-posttime'>%s</p>

                                <button id='comment-toggle%s' class='btn btn-default'>Comment</button>
                            </div>
                        </div>""" % (escape(self.user.id), escape(self.user.first_name), escape(self.user.last_name),
                                 escape(self.user.id), escape(self.user.username),
                                 escape(self.content), escape(self.pub_date.strftime('%b. %d, %Y %X')),escape(self.id))

        result += """<div hidden id='comment-area'>
                        <div class='form-group comment-btn'>
                            <div class='col-sm-8'>
                                <input id='commentField_%d' class='moveright-comment form-control' placeholder='Input comment...' type='text'>
                            </div>
                            <div class='col-sm-2'>
                                <button id='commentbtn' btn-id=%d class='float-left btn btn-default moveleft-text2 movetop-comment comment-button'>Comment</button>
                            </div>
                        </div>
                        <ol id='comment_list_%d'></ol>
                    </div>
                </div>""" %(self.id,self.id,self.id)
        return result

    @staticmethod
    def get_max_time():
        return Blog.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"



class Comment(models.Model):
    text = models.CharField(max_length=420)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    com_user = models.ForeignKey(User)
    com_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text + " " + self.blog.content

    @property
    def html(self):
        return """<div class='content2 float-left round-border moveright-comment2'>
                    <div class='content-writer2 float-left'>
                        <img  class='float-left round-border' src='photo%s' alt='%s %s' height='50' width='50'/>
                        <a class='comment-user' href='profile%s'>%s</a>
                    </div>
                    <div class='content-text2 float-left comment-comment'>
                        <p>%s</p>
                    </div>
                    <div class='content-time2 float-right movetop-text3 comment-time'>
                        <p>%s</p>
                    </div>
                </div>""" % (escape(self.com_user.id), escape(self.com_user.first_name), escape(self.com_user.last_name),
                             escape(self.com_user.id), escape(self.com_user.username), escape(self.text),
                             escape(self.com_time.strftime('%m/%d/%y %H:%M:%S')))