import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from projects.models import Project, List, Item, Event, WorkDay
User = get_user_model()


class ModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Sanek', password='qwerty12345')
        self.project = Project.objects.create(developer=self.user, name='first project', description='first description')


class ProjectModelTest(ModelTest):

    def test_str_method(self):
        self.assertEqual(str(self.project), 'first project')


    def test_date_default(self):
        self.assertEqual(self.project.start_date, datetime.date.today())
        self.assertEqual(self.project.end_date, datetime.date.today())


    def test_project_ordering(self):
        end_date1 = datetime.date.today() + datetime.timedelta(days=2)
        project1 = Project.objects.create(developer=self.user, name='second project', description='description22', end_date=end_date1)
        end_date2 = datetime.date.today() + datetime.timedelta(days=-2)
        project2 = Project.objects.create(developer=self.user, name='third project', description='description33', end_date=end_date2)
        self.assertEqual(list(Project.objects.all()), [project1, self.project, project2])


class WorkDayModelTest(ModelTest):

    def setUp(self):
        super().setUp()
        self.work_day = WorkDay.objects.create(project=self.project)


    def test_str_method(self):
        self.assertEqual(str(self.work_day), str(datetime.date.today()))


    def test_default(self):
        self.assertEqual(self.work_day.in_work, False)
        self.assertEqual(self.work_day.project, self.project)
        self.assertEqual(self.work_day.elapsed_time, datetime.timedelta(0))


    def test_start_working(self):
        self.work_day.start_working()
        self.assertEqual(self.work_day.in_work, True)
        time_delta = timezone.now() - self.work_day.start_time
        self.assertEqual(time_delta.seconds, 0)


    def test_stop_working(self):
        self.work_day.start_working()
        self.work_day.stop_working()
        self.assertEqual(self.work_day.in_work, False)
        self.assertNotEqual(self.work_day.elapsed_time, datetime.timedelta(0))


    def test_start_stop_working(self):
        self.work_day.start_working()
        self.work_day.stop_working()
        time1 = self.work_day.elapsed_time

        #another start-stop
        self.work_day.start_working()
        self.work_day.stop_working()
        time2 = self.work_day.elapsed_time - time1
        elapsed_time = WorkDay.objects.get(date=datetime.date.today()).elapsed_time
        self.assertEqual(elapsed_time, time1 + time2)
        self.assertEqual(WorkDay.objects.count(), 1)


    def test_cant_create_two_work_day_with_same_date(self):
        with self.assertRaises(Exception) as raised:
            work_day2 = WorkDay.objects.create(project=self.project)
        self.assertEqual(IntegrityError, type(raised.exception))


class ListItemModelTest(ModelTest):

    def setUp(self):
        super().setUp()
        List.objects.create(project=self.project)


    def test_str_method(self):
        list_ = List.objects.first()
        self.assertEqual(str(list_), f'{list_.id}')


    def test_list_defaults(self):
        list_ = List.objects.create(project=self.project)
        item = Item.objects.create(list=list_)
        self.assertEqual(item.text, '')


    def test_unique_together(self):
        list_ = List.objects.first()
        Item.objects.create(list=list_, text='item 1')
        with self.assertRaises(Exception) as raised:
            Item.objects.create(list=list_, text='item 1')
        self.assertEqual(IntegrityError, type(raised.exception))


    def test_cant_safe_blank_item(self):
        list_ = List.objects.first()
        item = Item.objects.create(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()


    def test_list_items_ordering(self):
        list_ = List.objects.first()
        item1 = Item.objects.create(list=list_, text='item 1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='item 3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])


class EventModelTest(ModelTest):

    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(project=self.project, name='event name', description='event description')


    def test_str_method(self):
        self.assertEqual(str(self.event), 'event name')


    def test_event_value(self):
        event = self.event
        self.assertEqual(event.is_done, False)
        self.assertEqual(event.datetime.date(), datetime.date.today())

    def test_event_ordering(self):
        event1 = Event.objects.create(project=self.project, name='event1')
        event2 = Event.objects.create(project=self.project, name='event2')
        self.assertEqual(list(Event.objects.all()), [event2, event1, self.event])
