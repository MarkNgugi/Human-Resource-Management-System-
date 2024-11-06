from django.db import models

class JobPost(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.job_title
