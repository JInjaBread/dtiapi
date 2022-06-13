from import_export import resources
from .models import Products

class ProductResource(resources.ModelResource):
    class meta:
        model = Products

    def __init__(self):
        super(ProductResource, self).__init__()
        # Introduce a class variable to pass dry_run into methods that do not get it
        self.in_dry_run = False

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Set helper class method to dry_run value
        self.in_dry_run = dry_run

    def before_import_row(self, row, row_number=None, **kwargs):
        if not self.in_dry_run:
            # Get URL and split image name from import file
            image_url = row['portrait']
            image_name = image_url.split('/')[-1]

            # Generate temporary file and download image from provided URL
            tmp_file = NamedTemporaryFile(delete=True, dir=f'{settings.MEDIA_ROOT}')
            tmp_file.write(urllib.request.urlopen(image_url).read())
            tmp_file.flush()

            # Add file object to row
            row['portrait'] = File(tmp_file, image_name)
