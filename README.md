# Pet Match  #





#### 1. What goal will your website be designed to achieve? What kind of users will visit your site?   

The goal of this website is to present the user with cats and dogs in their area that match what they are looking for. The type of user who will be vistiing my site will be
ones who want to adopt a cat or dog but do not know where to start. 

#### 2. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. ###
	
The API I am using is the [Petfinder API](https://www.petfinder.com/developers/ "Petfinder API"). The data includes details on animals that are available for adoption. I use  the animals location , personality, and physical description to help match them based on the users input.  To so, I created a survey/questionnaire for the user to complete. The feedback provided from this surveyis stored in my api. When the user is matched to a pet that will be stored as well. The user can then add indivual pets to their favorites list, which is stored as well.

#### 3. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information: ###

**a. What does your database schema look like?**   

My schema has five tables: Users, Pets, Surveys, Matches, and Favorites. All tables can be referrenced by using the user's username stored on the Users table. The Survey table only references the User table. The Matches and Favorites tables references the User and Pets Table.

**b. What kinds of issues might you run into with your API?**  

The free tier of the pet finder API has a limit to daily requests.    

**c. Is there any sensitive information you need to secure?**  

User passwords will need to be secure  

**d. What functionality will your app include?  What will the user flow look like?**  

When the user access the website they will be presented with the welcome page where they can login or signup. Once they are authenticated then they are able to take a survey, view their matches from taking the surveys (can take the survey as many times as they like), view their favorites they have saved from the matches, and change some account information. They can also delete their matches and favorties and delete their account as well.  

**e. What features make your site more than CRUD? Do you have any stretch goals?**   

Matching based on preferences and favoriting the matches make this site more than CRUD. A stretch goal would be send an email to the user with their results. Another would be to allow users to take the survey but then require they sign up to view the results.
