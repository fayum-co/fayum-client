# Fayum website

client side listing of all the jobs listing

- sorting options
  - required experience
  - min experine
  - max experience
- listing page as per the tags. i will give a tag and render all the jobs having that tag
- company listing page - name
- location
  - will be showing all the matching jobs with the particluar location. for now, let's go with exact match
- type of jobs
  - pages for part time or full time roles
- separate pages for min and max experience
  - when we go on the page, the page should be rendering the pages with min and max experience for that.
  - same goes in the max salary too.

# Upcoming features
- make the alerts for the seekers. or like we will be sending the list of curated jobs and other lists in the inbox - email or whatsapp inbox
- resume building - making it like we make the subscription based models in which the people from industries will be giving suggestions for improving the resume
- superdm - like we can make an easy assessment tool for the user which will allow the profiles to be ranked as per the JD which will allow the recruiter to make the 
    good choices in terms of the profiles 


# tasks

- put the OG url image for all the pages
- add a sitemap file xml format
- include the json schema for this.

# improvements for the prompt

- includee the job link. where should I candidate go
- if the job has the field of the job id then include the field too. also include the helper text that it should be quite helpful if uou can search the job using the job id
- update the prompt to take the headers like 'what you will get from the role" and then put the same in the fields under the category i have told
- can we include the field of the tech stack array and then also the create the set for the tech stack which might include the tech stack.
- include the fallback for the location. so if the location is india then the value has to be in the format or something else
- include the fallback for the format of the salary too. include the cases in which this can be negotiable
- can we give the summary of the job. like on the parameters i have decided, make the job score rank between one and then and then we will have the option to sort the jobs on the order of score.
- make sure the posted date is always there. if there is no date, the date should be the present date
- include the field for the long title too which will be having the field of the title and the company and the role too. which will be having the final field and should be having the detailed info of the title
- include the prompt to highlight the important words in the requirements. make some words bold
- ask the gpt to include the company desciption too if they can do with surity. otherwise, it should be giving me the empty string.
