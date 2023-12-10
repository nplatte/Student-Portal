from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from teacher_view.models import Course, Assignment
from django.utils.timezone import datetime
import zoneinfo
from teacher_view.forms import AssignmentForm


def _add_staff_user():
    test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
    staff_group = Group.objects.create(name='staff')
    staff_group.user_set.add(test_user)
    return test_user

def _make_class(user, title='test course'):
    term = f'2023 Fall Term'
    return Course.objects.create(title=title, course_instructor = user, term=term)


class TestCreateAssignmentPage(TestCase):
    
    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.c = _make_class(self.test_user)
        self.client.force_login(self.test_user)
        self.response = self.client.get(reverse('add_assignment', kwargs={'course_id':self.c.pk}))
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'teacher_view/add_assignment.html')

    def test_sends_navbar_information(self):
        c = Course.objects.get(pk=1)
        courses = self.response.context['current_courses']
        self.assertIn(c, courses)

    def test_uses_right_form(self):
        form = self.response.context['assignment_form']
        self.assertIsInstance(form, AssignmentForm)


class TestCreateAssignmentPOST(TestCase):

    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.c = _make_class(self.test_user)
        self.data = {
            'title': 'make Google',
            'description': 'make google please',
            'due_date': datetime.now(),
            'display_date': datetime(2024, 12, 31, 12, 12, 0)
        }
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_good_form_redirects_to_course_page(self):
        response = self.client.post(reverse('add_assignment', kwargs={'course_id':self.c.pk}), data=self.data, follow=True)
        self.assertRedirects(response, '/teacher/course/1/')

    def test_good_form_makes_new_assignment(self):
        a_list = Assignment.objects.all()
        self.assertEqual(len(a_list), 0)
        self.client.post(reverse('add_assignment', kwargs={'course_id':self.c.pk}), data=self.data)
        a_list = Assignment.objects.all()
        self.assertEqual(len(a_list), 1)

    def test_bad_form_does_not_redirect(self):
        self.data = {
            'description': 'make google please',
            'due_date': datetime.now(),
            'display_date': datetime(2024, 12, 31, 12, 12, 0)
        }
        response = self.client.post(reverse('add_assignment', kwargs={'course_id':self.c.pk}), data=self.data, follow=True)
        self.assertTemplateUsed(response,'teacher_view/add_assignment.html')


class TestEditAssignmentGET(TestCase):

    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.c = _make_class(self.test_user)
        self.a = Assignment.objects.create(
            title='Make Goog',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            course=self.c
        )
        self.response = self.client.get(reverse('staff_edit_assignment_page', kwargs={'assignment_id':self.a.pk}), follow=True)
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'teacher_view/edit_assignment.html')

    def test_uses_right_form(self):
        edit_assignment_form = self.response.context['form']
        self.assertIsInstance(edit_assignment_form, AssignmentForm)

    def test_passes_courses_to_nav_bar(self):
        c = Course.objects.get(pk=1)
        courses = self.response.context['current_courses']
        self.assertIn(c, courses)


class TestEditAssignmentPOST(TestCase):

    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.c = _make_class(self.test_user)
        self.a = Assignment.objects.create(
            title='Make Goog',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            course=self.c
        )
        self.data = {
            'title': 'dont make Google',
            'description': 'its evil',
            'due_date': datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            'display_date': datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            'course': self.c.pk
        }
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_edits_assignment_on_POST(self):
        self.assertEqual(self.a.title, 'Make Goog')
        self.client.post(reverse('staff_edit_assignment_page', kwargs={'assignment_id': self.a.pk}), self.data)
        self.a = Assignment.objects.get(pk=self.a.pk)
        self.assertEqual(self.a.title, 'dont make Google')
        self.assertEqual(self.a.description, 'its evil')

    def test_redirects_course_page_on_POST(self):
        response = self.client.post(reverse('staff_edit_assignment_page', kwargs={'assignment_id': self.a.pk}), self.data)
        self.assertRedirects(response, reverse('staff_course_page', kwargs={'course_id': self.c.pk}))
