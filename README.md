# Shinyangtime

I've used [django](https://www.djangoproject.com/) and [Kakao's API](https://github.com/plusfriend/auto_reply) to let teachers in Shinyang middle school view timetable (or a crop of it) through Kakaotalk.

In short, Kakao provides an API which sends users' queries (in the form of kakaotalk messages) to my server. Then I process their request, send a (JSON based) timetable back and Kakao's API takes it and displays it back to the user.

<img src='example.png' alt='example image' width='400'>
