from django.db import models


class CustomUser(models.Model):

    PERSONALITY_TYPES = (

        (1, 'ENFJ'),
        (2, 'ENFP'),
        (3, 'ENTJ'),
        (4, 'ENTP'),
        (5, 'ESFJ'),
        (6, 'ESFP'),
        (7, 'ESTJ'),
        (8, 'ESTP'),
        (9, 'INFJ'),
        (10, 'INFP'),
        (11, 'INTJ'),
        (12, 'INTP'),
        (13, 'ISFJ'),
        (14, 'ISFP'),
        (15, 'ISTJ'),
        (16, 'ISTP'),
    )

    username = models.CharField(max_length=50)

    age = models.IntegerField(default=20)

    personality_type = models.PositiveSmallIntegerField(choices=PERSONALITY_TYPES)

    predicted_personality = models.PositiveSmallIntegerField(choices=PERSONALITY_TYPES, default=1)

    class Meta:
        verbose_name_plural = "CustomUsers"

    def __str__(self):
        return str('UserID-- ') + str(self.pk) + str(' || Actual Personality-- ') + str(self.get_personality_type_display()) + str(' || Predicted Personality-- ') + str(self.get_predicted_personality_display()) + str(' || Username--') + str(self.username) + str(' || Age--') + str(self.age)



class Posts(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    post = models.TextField()

    cleaned_post = models.TextField()

    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Posts"

    def __str__(self):
        return str('PostID-- ') + str(self.pk) + str(' UserID-- ') + str(self.user.pk) + str(' || Cleaned Post-- ') + str(self.cleaned_post)



class Friendship(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    friend = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='friend')

    class Meta:
        verbose_name_plural = "Friendships"

    def __str__(self):
        return str('User-- ') + str(self.user.pk) + str(' || Friend-- ') + str(self.friend.pk)



class TagsOfInterest(models.Model):

    tag_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Tags of Interest"

    def __str__(self):
        return str('TagID-- ') + str(self.pk) + str(' || Tag-- ') + str(self.tag_name)



class UserInterestTags(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    tag = models.ForeignKey(TagsOfInterest, on_delete=models.PROTECT, related_name='tag')

    class Meta:
        verbose_name_plural = "User Interest Tags"

    def __str__(self):
        return str('User-- ') + str(self.user.pk) + str(' || Tag-- ') + str(self.tag.tag_name)