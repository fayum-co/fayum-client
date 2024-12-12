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

```
<div class="job-listing container mx-auto px-4 py-8">
    <div class="job-header mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
            {{ .Title | default "Job Position" }}
        </h1>

        <div class="job-meta mt-4 text-gray-600">
            {{ if .Params.company.name }}
                <div class="company-name">
                    <strong>Company:</strong>
                    {{ with .Params.company.url }}
                        <a href="{{ . }}" target="_blank" class="text-blue-600 hover:underline">
                            {{ $.Params.company.name }}
                        </a>
                    {{ else }}
                        {{ .Params.company.name }}
                    {{ end }}
                </div>
            {{ end }}

            <div class="job-location">
                <strong>Location:</strong>
                {{ .Params.location | default "Not Specified" }}
            </div>



            <div class="company-details">
                {{ if .Params.company.size }}
                    <strong>Company Size:</strong> {{ .Params.company.size }}
                {{ end }}
                {{ if .Params.company.sector }}
                    <strong>Sector:</strong> {{ .Params.company.sector }}
                {{ end }}
            </div>
        </div>
    </div>

    <div class="job-description prose max-w-none">
        <h2 class="text-2xl font-semibold mb-4">Job Description</h2>
        {{ .Params.description | default "No description available." | markdownify }}
    </div>

    <div class="job-requirements mt-8">
        <h2 class="text-2xl font-semibold mb-4">Requirements</h2>
        {{ if .Params.requirements }}
            <ul class="list-disc list-inside">
                {{ range .Params.requirements }}
                    <li>{{ . }}</li>
                {{ end }}
            {{ else }}
                <p>No specific requirements listed.</p>
            {{ end }}
    </div>

    {{ if .Params.good_to_have_requirements }}
        <div class="good-to-have mt-6">
            <h2 class="text-2xl font-semibold mb-4">Good to Have</h2>
            <ul class="list-disc list-inside">
                {{ range .Params.good_to_have_requirements }}
                    <li>{{ . }}</li>
                {{ end }}
            </ul>
        </div>
    {{ end }}

    <div class="job-experience mt-6">
        <h2 class="text-2xl font-semibold mb-4">Experience</h2>
        <p>
            {{ if and .Params.experience.min (ne .Params.experience.min -1) }}
                Minimum {{ .Params.experience.min }} years experience
            {{ end }}

            {{ if and .Params.experience.max (ne .Params.experience.max -1) }}
                {{ if .Params.experience.min }}to{{ end }}
                {{ if ne .Params.experience.max -1 }}
                    {{ .Params.experience.max }} years
                {{ else }}
                    No upper limit
                {{ end }}
            {{ else if .Params.experience.min }}
                years and above
            {{ else }}
                Experience requirements not specified
            {{ end }}
        </p>
    </div>

salary will be here
    <div class="application-cta mt-8 text-center">
        <a href="#apply" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
            Apply for this Position
        </a>
    </div>

    <div class="additional-info mt-6 text-gray-600">
        <p>Posted on: {{ .Date.Format "January 2, 2006" }}</p>
        {{ if .Params.categories }}
            <div class="categories">
                <strong>Categories:</strong>
                {{ delimit .Params.categories ", " }}
            </div>
        {{ end }}

        {{ if .Params.tags }}
            <div class="tags mt-2">
                <strong>Tags:</strong>
                {{ range .Params.tags }}
                    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm mr-2 mb-2">
                        {{ . }}
                    </span>
                {{ end }}
            </div>
        {{ end }}
    </div>
</div>
```
