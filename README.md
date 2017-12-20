# Shinyangtime

I used [django](https://www.djangoproject.com/) and [Kakao's API](https://github.com/plusfriend/auto_reply) to let teachers in Shinyang middle school view timetable (or a crop of it) through Kakaotalk.

The whole process consists of three steps:
1. User queries(Kakaotalk msgs) => Server
2. Query processing
3. Server => User window(Kakaotalk msgs)

Kakao's API takes care of 1 and 3, and this codebase is essentially just for the second step.

Below is an example of this actually being used in Kakaotalk.

<img src='example.png' alt='example image' width='400'>
