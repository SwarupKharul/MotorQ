- Clone the repository

```
git clone https://github.com/STCVIT/Flo-In.git
```

- Install the dependencies

```
pip install -r requirements.txt
```

- Make migrations

```
python manage.py makemigrations
```

- Migrate

```
python manage.py migrate
```

- Start the server

```
python manage.py runserver
```

## Tasks completed

- Events can be of multiple types - Topic A, Topic B, Workshop A etc.
- Each event has a capacity. This refers to the maximum number of attendees that can attend the
  event.
- Each event has a fixed time slot.
- Attendees can book an event if the capacity is not yet reached
- If an event is already at capacity, the system should maintain a waiting list of interested attendees.
- Registration closes at a fixed time.
- Attendees can cancel the slot before the registration closes.
