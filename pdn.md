## What is the program for?

The program is designed to pull content from the PDN and display it in a human/
phone readable format.

In the near future I'll add the ability to only pull the last /n/ days worth of
content. For instance, 1 day or 2 days of content.

How does the program work:

The program opens up and scrapes the homepage of the PDN for all links that
have "StoryText2" in the div tag.  The app loads these links into a list.
Once the links are loaded into the list, we iterate through the links and 
print out the page contents into an html file.

## Hmm, wonder if I should store which links have been previously pulled and
only pull the new links - Arg,

