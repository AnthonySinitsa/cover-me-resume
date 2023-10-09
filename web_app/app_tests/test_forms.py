# from django.test import TestCase
# from web_app.forms import UserRegisterForm
# from web_app.forms import ResumeUploadForm
# from django.core.files.uploadedfile import SimpleUploadedFile
# from web_app.forms import EditCoverLetterForm

# class UserRegisterFormTest(TestCase):

#     def test_form_validity(self):
#         form = UserRegisterForm(data={
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password1': 'testpassword',
#             'password2': 'testpassword'
#         })
#         self.assertTrue(form.is_valid())

#     def test_form_invalidity(self):
#         form = UserRegisterForm(data={})
#         self.assertFalse(form.is_valid())



# class ResumeUploadFormTest(TestCase):

#     def test_form_validity(self):
#         upload_file = open("path/to/your/testfile.txt", "rb")
#         file = SimpleUploadedFile(upload_file.name, upload_file.read())
#         form = ResumeUploadForm(files={'resume_file': file})
#         self.assertTrue(form.is_valid())

#     def test_form_invalidity_without_file(self):
#         form = ResumeUploadForm(files={})
#         self.assertFalse(form.is_valid())



# class EditCoverLetterFormTest(TestCase):

#     def test_form_validity(self):
#         form = EditCoverLetterForm(data={'content': 'This is a test content for the cover letter.'})
#         self.assertTrue(form.is_valid())

#     def test_form_invalidity_without_content(self):
#         form = EditCoverLetterForm(data={'content': ''})
#         self.assertFalse(form.is_valid())
