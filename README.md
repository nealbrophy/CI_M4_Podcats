# Code Institute Milestone 4 - Full Stack Frameworks with Django

## Podcat(s)

### Project Description/Goals
Podcat(s) The Podcast Catalogue(s) is a Podcast review platform where user can search for, add, review, and import podcasts from iTunes.

Podcat(s) is deployed to Heroku from the master branch and will automatically update to reflect any new changes pushed.

You can view the deployed site on [Heroku](https://podcats.herokuapp.com/)

### Technologies used
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [HTML](https://www.w3schools.com/html/), [CSS](https://www.w3schools.com/Css/), [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Bootstrap](https://getbootstrap.com/)
- [Google Fonts](https://fonts.google.com/)
- [Font Awesome](https://fontawesome.com/)
- [Material Icons](https://material.io/resources/icons/?style=baseline)
- [iTunes API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/)

 
## UX

### User Stories
| AS A                                              | I WANT                                                 | SO THAT                                 |
| ----------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------ |
| Podcast consumer     | a way to search for podcasts by genre     | I can discover new podcasts |
| Podcast consumer     | the ability to pay to unlock additional features    | I can get extra features |
| Podcast consumer | to read reviews of podcasts | I can find out if a podcast is worth my attention |
| Podcast consumer | to write reviews for podcasts I've listened to| I can help others find out if podcasts are worth listening to
| Podcast consumer| a way to easily add or import missing podcasts| I can make sure my favourite pods are included|


### Strategy
The idea here was to primarly be a place users could look up information and reviews about Podcast. A "Rotten Tomatoes or IMDb" but for podcasts.

### Scope
Initially I wanted to have multiple APIs linked in so that the app could look for podcasts on various platforms. However, some early teething problems on that front caused me to scale back and instead add just one API which would serve as a fallback should the podcast being searched for not be present (and to allow easy import of said missing podcast). The API chosen for this was iTunes API as it fit the bill and was surprisingly easy to get set-up.

### Skeleton
#### Wireframes

### Surface

### Current Features

### Future Features

## Deployment
### Instructions for running locally

### Instructions for deploying to Heroku

## Testing
### Unit Tests

### Manual Tests

## Validation

### Python validation

### HTML validation

### CSS validation

### JS validation

## Bugs

### Squashed bugs

### Open bugs

## Credits/Acknowledgements
- upload functions based on [this medium post](https://medium.com/@simathapa111/how-to-upload-a-csv-file-in-django-3a0d6295f624) by [Seema Thapa](https://medium.com/@simathapa111)
- Multiple tutorials & How-Tos from the excellent [SimpleIsBetterThanComplex](https://simpleisbetterthancomplex.com/) by Vitor Freitas.
- Pagination with help from:
    - [this StackOverflow question](https://stackoverflow.com/questions/2266554/paginating-the-results-of-a-django-forms-post-request)
    - [this CodeLoop.org tutorial](https://codeloop.org/django-pagination-complete-example/)
    - [this tutorial](https://samulinatri.com/blog/django-pagination-tutorial/) by Samuli Natri
    - [this answer](https://stackoverflow.com/a/30864681) from [Blackeagle52](https://stackoverflow.com/users/2798610/blackeagle52) on StackOverflow
- Login modal with help from [this answer](https://stackoverflow.com/questions/39197723/how-to-move-singup-signin-templates-into-dropdown-menu/39235634#39235634) on StackOverflow
- Changed Review.podcast_id from (very slow) choices to raw id field with help from [this answer](https://stackoverflow.com/questions/980405/raw-id-fields-for-modelforms) on StackOverflow