from django.test import TestCase
from django.contrib.auth.models import User
from web_app.models import Resume, JobPost, CoverLetter, Job
from django.utils import timezone

class TestModels(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a job post
        self.job_post = JobPost.objects.create(
            user=self.user,
            job_title='Software Engineer',
            job_description='Develop and maintain software',
            third_party_url='http://example.com',
            scraped_at=timezone.now()
        )

        # Create a resume
        self.resume = Resume.objects.create(
            user=self.user,
            resume_file='resume.pdf',
            uploaded_at=timezone.now()
        )

        # Create a cover letter
        self.cover_letter = CoverLetter.objects.create(
            user=self.user,
            job_post=self.job_post,
            content='This is a test cover letter content',
            generated_at=timezone.now(),
            filename='Cover_Letter_Test'
        )

        # Create a job
        self.job = Job.objects.create(
            user=self.user,
            title='Data Scientist',
            company='ABC Corp',
            location='New York, NY',
            description='Analyze and interpret complex data',
            post_date=timezone.now(),
            company_overview_link='http://abc-corp.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_resume_creation(self):
        self.assertEqual(self.resume.user.username, 'testuser')

    def test_job_post_creation(self):
        self.assertEqual(self.job_post.job_title, 'Software Engineer')
        self.assertEqual(self.job_post.job_description, 'Develop and maintain software')

    def test_cover_letter_creation(self):
        self.assertEqual(self.cover_letter.user.username, 'testuser')
        self.assertEqual(self.cover_letter.job_post, self.job_post)
        self.assertEqual(self.cover_letter.content, 'This is a test cover letter content')

    def test_job_creation(self):
        self.assertEqual(self.job.title, 'Data Scientist')
        self.assertEqual(self.job.company, 'ABC Corp')
        self.assertEqual(self.job.location, 'New York, NY')
