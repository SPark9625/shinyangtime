# Shinyangtime

I've used [django](https://www.djangoproject.com/) and [Kakao's API](https://github.com/plusfriend/auto_reply) to let teachers in Shinyang middle school view timetable (or a crop of it) through Kakaotalk.

In short, Kakao provides an API which sends users' queries (in the form of kakaotalk messages) to my server. Then I process their request, send a (JSON based) timetable back and Kakao's API takes it and displays it back to the user.

![example1](https://github.com/SPark9625/shinyangtime/blob/master/example1.PNG)
![example2](https://github.com/SPark9625/shinyangtime/blob/master/example2.PNG)
