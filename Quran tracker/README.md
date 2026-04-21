# Sprint 1 Documentation
### Quran Commitment Tracker — Web Application
> Database Design & Django Models

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Database Design](#2-database-design)
3. [Relationships & Cardinalities](#3-relationships--cardinalities)
4. [on_delete Decisions](#4-on_delete-decisions)
5. [Django Models Code](#5-django-models-code)
6. [Business Logic — Django Signals](#6-business-logic--django-signals)
7. [Key Design Decisions](#7-key-design-decisions)
8. [Project File Structure](#8-project-file-structure)
9. [Remaining Work for MVP](#9-remaining-work-for-mvp)

---

## 1. Project Overview

The Quran Commitment Tracker is a web application that helps groups of users stay committed to their daily Quran reading (Wird). The system tracks daily progress and applies agreed-upon penalties for missed days.

### 1.1 System Purpose
- Allow users to create or join reading groups (rooms)
- Track daily Quran reading per user per room
- Automatically calculate and accumulate fines for missed days
- Provide a dashboard showing progress and penalties

### 1.2 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | SQLite (Relational) |
| Frontend | Android / iOS (future) |
| API | Django REST Framework |

---

## 2. Database Design

### 2.1 Entities Overview

| Entity | Description |
|---|---|
| `USER` | Stores all registered users |
| `ROOM` | Represents a reading group/commitment room |
| `USERROOM` | Junction table — links users to rooms they joined |
| `READING` | Stores daily reading logs per user per room |
| `NOTIFICATION` | Stores notifications sent to users |
| `INVITATION` | Stores invite tokens for joining rooms |

---

### 2.2 Entity Details

#### USER

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Auto generated |
| UQ, NOT NULL | Email | Varchar(255) | Unique — no duplicate accounts |
| NOT NULL | first | Varchar(255) | First name |
| NOT NULL | last_name | Varchar(255) | Last name |
| NOT NULL | password | Varchar(255) | Hashed password |
| NULL | Image | Blob | Profile picture, optional |

---

#### ROOM

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Auto generated |
| FK, NOT NULL | AdminID | Int | References USER.ID — SET_NULL on delete |
| NOT NULL | Name | Varchar(255) | Room name |
| NOT NULL | Reading_deadline | DateTime | Changed to DateTime to include time |
| NOT NULL | Daily_fine | Decimal(10,2) | Fine amount per missed day |

---

#### USERROOM

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Added single PK for Django FK compatibility |
| FK, NOT NULL | UserID | Int | References USER.ID — CASCADE on delete |
| FK, NOT NULL | RoomID | Int | References ROOM.ID — CASCADE on delete |
| NOT NULL | IsAdmin | Boolean | Whether user is admin of this room |
| NOT NULL | Total_Fine | Decimal(10,2) | Accumulated fines for this user in this room |

---

#### READING

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Auto generated |
| FK, NOT NULL | UserID | Int | References USER.ID — CASCADE on delete |
| FK, NOT NULL | RoomID | Int | References ROOM.ID — SET_NULL on delete |
| NOT NULL | Room_name | Varchar(255) | Copied at creation — preserved if room deleted (denormalization) |
| NOT NULL | Reading_date_time | DateTime | Date and time of reading |
| NOT NULL | Amount | Decimal(10,2) | Amount of Quran read |
| NOT NULL | Fine_amount | Decimal(10,2) | Fine applied for this record if missed |
| NOT NULL | Updated_at | DateTime | Auto-updated on edit — supports same-day updates |

---

#### NOTIFICATION

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Auto generated |
| FK, NOT NULL | UserID | Int | References USER.ID — CASCADE on delete |
| FK, NULL | RoomID | Int | References ROOM.ID — SET_NULL on delete — nullable for general notifications |
| NOT NULL | Type | Varchar(50) | One of: MISSED_DAY, FINE_APPLIED, ROOM_INVITE, GENERAL |
| NOT NULL | Message | Varchar(255) | Notification text |
| NOT NULL | isRead | Boolean | Whether user has seen it — defaults to False |
| NOT NULL | CreatedAt | DateTime | Auto set at creation time |

---

#### INVITATION

| Constraint | Field | Type | Notes |
|---|---|---|---|
| PK | ID | Int | Auto generated |
| FK, NOT NULL | RoomID | Int | References ROOM.ID — CASCADE on delete |
| UQ, NOT NULL | Token | Varchar(255) | Unique token — auto generated via uuid4 |
| NOT NULL | expiresAt | DateTime | When the invite link expires |
| NOT NULL | isUsed | Boolean | Whether link has been used — defaults to False |

---

## 3. Relationships & Cardinalities

| From | To | Cardinality | Notes |
|---|---|---|---|
| `USER` | `USERROOM` | One to many | One user can join many rooms |
| `ROOM` | `USERROOM` | One to many | One room can have many members |
| `USER` | `READING` | One to many | One user can log many readings |
| `ROOM` | `READING` | One to many | One room can have many readings |
| `USER` | `NOTIFICATION` | One to many | One user can have many notifications |
| `ROOM` | `NOTIFICATION` | One to many (optional) | RoomID is nullable — general notifications have no room |
| `ROOM` | `INVITATION` | One to many | One room can have many invite links |
| `USER` | `ROOM` | One to many | One user can create many rooms via AdminID |

---

## 4. on_delete Decisions

| Table | FK Field | References | on_delete | Reason |
|---|---|---|---|---|
| USERROOM | UserID | USER.ID | CASCADE | If user deleted, remove their memberships |
| USERROOM | RoomID | ROOM.ID | CASCADE | If room deleted, remove all memberships |
| ROOM | AdminID | USER.ID | SET_NULL | If admin deleted, keep room — assign new admin via signal |
| READING | UserID | USER.ID | CASCADE | If user deleted, remove their readings |
| READING | RoomID | ROOM.ID | SET_NULL | If room deleted, keep reading history — room_name preserves the name |
| NOTIFICATION | UserID | USER.ID | CASCADE | If user deleted, remove their notifications |
| NOTIFICATION | RoomID | ROOM.ID | SET_NULL | If room deleted, keep notification but lose room FK |
| INVITATION | RoomID | ROOM.ID | CASCADE | If room deleted, remove all its invitations |

---

## 5. Django Models Code

### 5.1 Notification Model

```python
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('MISSED_DAY', 'Missed Day'),
        ('FINE_APPLIED', 'Fine Applied'),
        ('ROOM_INVITE', 'Room Invite'),
        ('GENERAL', 'General'),
    )
    user = models.ForeignKey("User.User" , on_delete= models.CASCADE)
    room = models.ForeignKey("Room.Room" , on_delete= models.SET_NULL , null=True, blank=True)
    message = models.CharField(max_length= 255)
    type = models.CharField(max_length= 255, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

```

---

### 5.2 Room Model

```python
from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        "User.User",
        related_name='admin_rooms',
        on_delete=models.SET_NULL,
        null=True,
    )
    reading_deadline = models.DateTimeField()
    daily_fine = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
```

---

### 5.3 Invitation Model

```python
from django.db import models

class Invitation(models.Model):
     room = models.ForeignKey("Room.Room", on_delete=models.CASCADE)
     token = models.CharField(max_length=255 , unique=True)
     expires_at = models.DateTimeField()
     isUsed = models.BooleanField(default=False)

     def __str__(self):
         return f"Invitation for {self.room.name} - {self.token}"
```

---

### 5.4 Reading Model — with room_name auto-copy

```python
from django.db import models

class Reading (models.Model):
    user = models.ForeignKey("User.User" , on_delete= models.CASCADE)
    room = models.ForeignKey("Room.Room" , on_delete= models.SET_NULL, null=True)
    room_name = models.CharField(max_length= 255)
    reading_date_time = models.DateTimeField()
    reading_amount = models.DecimalField(max_digits=4,decimal_places=2)
    fine_amount = models.DecimalField(max_digits= 5, decimal_places= 2)
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if self.room and not self.room_name:
            self.room_name = self.room.name
        super().save(*args , **kwargs)

```

---

## 6. Business Logic — Django Signals

### 6.1 Admin deleted → assign new admin or delete room

When an admin user is deleted, the system automatically assigns another room member as the new admin. If no members remain, the room is deleted.

```python
from django.db.models.signals import post_delete
from django.dispatch import receiver
from User.models import UserRoom
from .models import Room


@receiver(post_delete, sender=UserRoom)
def handle_admin_delete(sender , instance, **kwargs):
    members = UserRoom.objects.filter(room=instance.room)
    if not members.exists():
        instance.room.delete()
        return

    if instance.room.admin == instance.user:
        new_admin = members.first().user
        instance.room.admin = new_admin
        instance.room.save()
```


## 7. Key Design Decisions

| Decision | Choice | Reason |
|---|---|---|
| Room deletion | Hard delete | No legal/financial obligation — avoids over-engineering |
| Reading history after user leaves | Preserve via separate UserID + RoomID FKs | Financial records should never be lost |
| Room name in readings | Denormalization — copy room_name at creation | Preserves room name in history even after room is deleted |
| USERROOM primary key | Added single ID column | Django ORM does not support composite PKs as FK references natively |
| Notification room FK | Nullable RoomID | Allows both room-specific and general notifications |
| Reading deadline type | DateTime instead of Date | A deadline needs a specific time, not just a date |
| Admin deletion | SET_NULL + Django signal | Room survives admin deletion — signal reassigns a new admin automatically |
| Invitation token | uuid4 auto-generated | Guarantees uniqueness without manual management |

---

## 8. Project File Structure

```
quran_tracker/
├── manage.py
├── quran_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
├── rooms/          ← contains Room and UserRoom models
├── readings/
├── notifications/
└── invitations/
```

Each app follows the same internal structure:

```
app_name/
├── models.py       ← database table definition
├── views.py        ← business logic
├── urls.py         ← API endpoints
├── serializers.py  ← convert model to JSON
├── admin.py        ← register model in admin panel
├── signals.py      ← auto actions
├── tests.py        ← unit tests
└── apps.py         ← app configuration
```

---

## 9. Remaining Work for MVP

| Feature | Description | Priority |
|---|---|---|
| User authentication | Registration, login, logout APIs | High |
| Room management APIs | Create, join, leave room endpoints | High |
| Daily reading log API | POST endpoint to log daily reading | High |
| Fine calculation system | Celery periodic task to detect missed days and apply fines | High |
| Dashboard API | Endpoint returning user stats and room progress | Medium |
| Notification system | Auto-create notifications on missed days and fines | Medium |
| Invitation system | Generate and validate invite links | Medium |
| Expired invitation cleanup | Celery periodic task to delete expired invitations | Low |

---

*Sprint 1 — Quran Commitment Tracker | Database Design & Django Models*