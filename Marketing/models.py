from django.db import models


class ImagesAdds(models.Model):
    IMAGECATEGORY = (
        ('Top-Banner', 'Top-Banner'),
        ('Blog-Post', 'Blog-Post'),
        ('Testimonials', 'Testimonials'),
        ('Card-Banner', 'Card-Banner'),

    )
    header = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(blank=True, upload_to='addimages/')
    image_category = models.CharField(max_length=20, choices=IMAGECATEGORY, default='None')
    

    def __str__(self):
        return self.title
    
    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""
        