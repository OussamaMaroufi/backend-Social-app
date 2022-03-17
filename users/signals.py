from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile
from django.dispatch import receiver
from chat.models import ChatRoom


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            name=instance.username,
            username=instance.username,
# email=instance.email,
        )

        print('Profile Created!')

@receiver(post_save, sender=User)
def create_chatRoom(sender, instance, created, **kwargs):
    if created:

        chatRoom = ChatRoom.objects.create(
            type="SELF",
            name=instance.username,
        )
        chatRoom.member.add(instance.id)
        print(chatRoom)
        

        print('ChatRoom Created!!')


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    user_profile, _ = UserProfile.objects.get_or_create(user=instance)
    if created == False:

        user_profile.username = instance.username

        #instance.userprofile.email = instance.email
        user_profile.save()
        print('Profile updated!')


# Here to connect between the sender and  the receiver
# the sender is the model to triger the method

post_save.connect(create_profile, sender=User)
post_save.connect(update_profile, sender=User)


#create a Room when before user signup 

