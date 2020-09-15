# ltt

### Start project
```
$ cp .env.example .env && docker-compose up -d
```

### GIT link
https://github.com/DmytroKaminskiy/ltt

### base auth
```
username: guest
password: guest12345guest
```

### Test Coverage
http://3.134.110.47/coverage/

### Resource
http://3.134.110.47/

### Check pull Requests to see task progress by PRs
https://github.com/DmytroKaminskiy/ltt/pulls


- System design document for the backend
 
  Check ./network.jpg to see connection between instances.
  Services
    1. Nginx
    2. Wsgi (django)
    3. Postgresql
    4. Redis (cache/queue)
    5. Celery (background tasks)
    6. CeleryBeat (crontab messages)  
    
  This approach is fairly straightforward but has scalability opportunities.
  
  To see database structure check file ./public.png
  To model consists of 5 tables
  1. Django User (or just User)
     I used this model as authentication model. The functional is pretty standard for this kind of table.
  2. Category. This table is responsible to store book category name and prices.
      - price - this is regular price to be charged daily for rented books
      - days_period - For how many days special price will work
      - price_period - Price for special period
 
     Example:
        - price = 3
        - days_period = 2
        - price_period = 1
         
        First 2 days user will be charged 1 dollar, afterwards, $3 per day.
  3. Book. This is representation of which book user can rent. It has only 3 fields. id (unique identifier), category_id (Foreign Key to Category), title (book title)
  4. BookRent. This table is responsible to store information about Rented books by user.
     It has Foreign Keys to User and Book models.
     It has 4 statuses.
        - pending. This means that user created request to rent the book
        - confirmed. Admin confirms that user can rent the book
        - in use. Admin gave book physically to user. When status changed from "confirmed" to "in use" we create first record about charge, as the first day of using the book counts.
        - end. User returned the book. When status changed from "in use" to "end" we also update end field to see when the book was returned.
     
     Fields: price, days_period, price_period work the same way as in Category. Even more, they are duplicated upon BookRent creation.
     This functionality was added to commit the rent contract. Category fields might be changed during book rent and category price should not affect active rents.
  5. RentDayHistory. This table is responsible to save rent story for each day. The records are created every day handled via crontab job.
     This helps to commit the exact price which should be paid daily by user. This should not be changed manually (it should be handled by code)

  This approach gives us great flexibility in categories and prices. We do not stick to any specific name or value.
  Also, we have consistent history of rents and easy to create reports system. Even more, it can is easily scalable.

- BE - Infrastructure tools usage e.g Docker, Logging tools

  At the moment server runs all applications under docker/docker-compose
  I had an idea to use sentry for this task. But I have reached my limit on free account)

- Clean readable and well documented code and how to execute it

  To run the code it's super easy with docker. Just run
  
  `$ cp .env.example .env && docker-compose up -d`

- Good unit test coverage
  
  check ./commands/check.sh to see the current test coverage (ATM 96.45%) (http://3.134.110.47/coverage/)

- Well designed with proper folder structure
  
  Standard Django structure was used to implement this task (src).
     - images. This folder contains everything related to docker images
     - commands. Commands to start services, such as wsgi, celery, celerybeat
     - static_content. Store static which will be served via nginx
     - tmp. Store temporary files such as celery.pid

- Build scalable APIs

  All the API calls were made minimalistic (without nested serializers), which guarantees easy scaling system ATM.

- Follow version control and Git best practices

  All the stories are implemented in separate Pull Requests. To see difference better between user stories, I have created additional Pull Requests.
  https://github.com/DmytroKaminskiy/ltt/pulls

- Adherence to best practice and coding standards 

  To check code I have used flake8 with few additional modules such as flake8-builtins, flake8-import-order, flake8-print

- Great user experience

  I have used template that I bought recently. But didn't have enough time to customize forms.

- Taking time to build elaborate features rather than just getting the basic functionality job done

  Everything was build with scalability in mind and without sticking to hardcoded input values (such as category names, prices. They can be changed at any moment)
