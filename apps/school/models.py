from datetime import datetime

from django.utils.text import slugify

from django.utils import timezone
from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from apps.school.validators import validate_alphabetical
from apps.tenants.models import SchoolOwner


User = get_user_model()


def school_image_path(instance, filename):
    return f"schools/{instance.slug}/{filename}"


class School(models.Model):
    Private = "pr"
    Public = "pu"

    SCHOOL_TYPE = [
        (Private, "PRIVATE"),
        (Public, "PUBLIC"),
    ]
    name = models.CharField(max_length=125, verbose_name=_("School Name"), unique=True)
    slug = models.SlugField(blank=True, max_length=200)
    motto = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to=school_image_path, blank=True
    )  # Temporary Upload path
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE, default=Private)
    address = models.CharField(
        max_length=125, verbose_name=_("School Address"), blank=True
    )
    country = models.CharField(
        max_length=100, verbose_name=_("Country"), default="Nigeria"
    )
    state = models.CharField(max_length=100, verbose_name=_("State"))
    color = models.CharField(max_length=20, verbose_name=_("School Preferred Color"))

    class Meta:
        verbose_name_plural = _("Schools")

    def __str__(self) -> str:
        return f"{self.name}"


# Contact Address
class SchoolContact(models.Model):
    """
    Model details for collecting school Contact Reach Details
    """

    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name=_("+"))
    slug = models.SlugField(max_length=100, blank=True)
    school_email = models.EmailField(unique=True, verbose_name=_("School Email"))
    school_phone = models.CharField(max_length=20)
    technical_email = models.EmailField(unique=True)
    technical_phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.school}"


class SchoolSession(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name=_("school")
    )
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(blank=True, max_length=200)
    active = models.BooleanField(verbose_name=_("School Status"), default=False)

    class Meta:
        verbose_name = _("School Year")
        verbose_name_plural = _("School Years")

    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year}"

    @property
    def year_range(self):
        return f"{self.start_date.year}-{self.end_date.year}"

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.year_range)
        return super().save(*args, **kwargs)

    @classmethod
    def get_current_year(cls, user: User):
        """Gets the current school year of a specific user"""
        today = user.get_local_today()
        school_year = SchoolSession.objects.filter(
            school__admin=user, start_date__lte=today, end_date__gte=today
        ).first()

        if not school_year:
            school_year = SchoolSession.objects.filter(
                school__admin=user, start_date__gt=today
            ).first()
        return school_year

    @property
    def is_school(self, date: datetime.date) -> bool:
        """
        Designates if the date is in a school year
        """
        return self.start_date <= date <= self.end_date

    @property
    def grades_school(self):
        pass


class SchoolTerm(models.Model):
    class TermChoices(models.IntegerChoices):
        FIRST_TERM = (1,)
        SECOND_TERM = (2,)
        THIRD_TERM = (3,)

    TERM_UPDATE = (
        TermChoices.FIRST_TERM,
        TermChoices.SECOND_TERM,
        TermChoices.THIRD_TERM,
    )
    session = models.ForeignKey(
        SchoolSession, on_delete=models.CASCADE, related_name=_("+")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Term Name"),
        help_text=_("example -> First Tirm"),
    )
    slug = models.SlugField(blank=True)
    active = models.BooleanField(default=False)
    term = models.IntegerField(choices=TermChoices.choices)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.session} - {self.name}"

    @classmethod
    def get_total_day_school_open_count(cls, term_id):
        return cls.objects.filter(term_id=term_id, present=True).count()

    def save(self, *args, **kwargs):
        date = timezone.localdate()
        if date >= self.start_date and date <= self.end_date:
            self.active = True
        self.active = False
        if self.slug == "":
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @classmethod
    def get_term_duration(cls, term_id):
        term = (
            cls.objects.get(id=term_id)
            .exclude(start_date__week_day__in=[5, 6])
            .exclude(end_date__week_day__in=[5, 6])
        )
        return (term.end_date - term.start_date).days + 1

    @classmethod
    def filter_weekends(cls):
        return cls.objects.exclude(start_date__week_day__in=[5, 6]).exclude(
            end_date__week_day__in=[5, 6]
        )

    @property
    def breaks(self):
        today = self.user.get_local_today()
        breaks = SchoolBreak.objects.filter(
            term=self, start_date__lte=today, end_date__gte=today
        )
        return breaks


class GradingSystem(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name=_("grading_system")
    )
    low_score = models.PositiveIntegerField(verbose_name=_("score range lower"))
    high_score = models.PositiveIntegerField(verbose_name=_("score range higher"))
    level = models.ManyToManyField("Level")
    grade = models.CharField(max_length=100, verbose_name="grade name")
    remark = models.CharField(max_length=100, verbose_name=_("Grade Remark"))
    teacher_comment = models.CharField(
        max_length=250, verbose_name=_("Teacher's Comment")
    )
    principal_comment = models.CharField(
        max_length=250, verbose_name=_("Principal's Comment")
    )

    def __str__(self) -> str:
        return f"{self.grade} - {self.score}"

    class Meta:
        verbose_name_plural = "Grading Systems"


class SchoolGradeScore(models.Model):
    """
    School Grade Score -> poor 0 to 30
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name=_("+"))
    # grade = models.ForeignKey()
    score_name = models.CharField(max_length=30)
    low_range = models.PositiveIntegerField(default=0)
    upper_range = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.score_name}- {self.low_range} - {self.upper_range}"


class Skills(models.Model):
    """
    Psychomotors -> Honesty, Punctuality
    """

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name=_("psychomotors")
    )
    skill = models.CharField(
        max_length=100,
        help_text=_("Skills: E.g Psychomotors, Affective"),
    )
    rating = models.CharField(max_length=10, verbose_name=_("Skill Rating"))

    def __str__(self) -> str:
        return f"{self.school} - {self.skill}"


class SkillLevel(models.Model):
    skill = models.ForeignKey(
        Skills, on_delete=models.CASCADE, related_name=_("skill_level")
    )
    name = models.CharField(max_length=200, help_text=_("A+, A, B"))
    remark = models.CharField(
        max_length=120,
        verbose_name=_("Skill Remark"),
        help_text=_("Excellent, Very Good"),
    )
    color = models.CharField(max_length=120, verbose_name=_("color choices"))
    level = models.ManyToManyField("Level")

    def __str__(self) -> str:
        return f"{self.skill} - {self.name}"


class SchoolArms(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name=_("school_arms")
    )
    arm = models.CharField(max_length=100, help_text=_("Eg: A, Science, Gold"))

    def __str__(self) -> str:
        return f"{self.school} - {self.arm}"


class Level(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name=_("school_level")
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Level Name",
        help_text=_("Levels: Primary One"),
        validators=[validate_alphabetical],
    )

    short_name = models.CharField(
        max_length=40, verbose_name=_("Level Short name"), help_text=_("Levels: Pry1")
    )
    slug = models.SlugField(max_length=60, blank=True)

    form_teacher = models.ForeignKey(
        to="staff.Staff",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Form Teacher"),
        help_text=_("Form Teacher -> Primary 3 Class Teacher"),
    )
    ass_form_teacher = models.ForeignKey(
        to="staff.Staff",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
        verbose_name=_("Assistant Form Teacher"),
        help_text=_("Assistant Form Teacher -> Primary 3 Assistant Class Teacher"),
    )

    def __str__(self) -> str:
        return f"{self.school} - {self.short_name}"

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.short_name)
        return super().save(*args, **kwargs)


class LevelArms(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="+")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name=_("+"))
    arm = models.ForeignKey(SchoolArms, on_delete=models.CASCADE, related_name=_("+"))

    class Meta:
        verbose_name_plural = "Level Arms"


# class Grade(models.Model):
#     school = models.ForeignKey(
#         School,
#         on_delete=models.CASCADE,
#         related_name=_("school_grade"),
#     )
#     name = models.CharField(max_length=125, verbose_name=_("Grade Name"))
#     is_valid = models.BooleanField(
#         default=False, help_text=_("Designates if a grade is still valid")
#     )

#     def __str__(self) -> str:
#         return f"{self.school__name} -> {self.name}"


# class GradeLevel(models.Model):
#     """A student is in a grade level in a given school year"""

#     school_year = models.ForeignKey(
#         SchoolSession, on_delete=models.CASCADE, related_name="grade_levels"
#     )
#     grade = models.ManyToManyField(
#         "Grade", help_text=_("All Available Grades For a particular school year")
#     )

#     order_with_respect_to = "school_year"

# def get_ordered_courses(self):
# """Get the courses in their proper order.

# Since ordering is defined on the through model, this is a reasonable
# way to get the courses.
# """
# from homeschool.courses.models import GradeLevelCoursesThroughModel

# courses = [
#     gc.course
#     for gc in GradeLevelCoursesThroughModel.objects.filter(
#         grade_level=self
#     ).select_related("course")
# ]
# Eager load the school year to avoid performance hit
# of hitting the cached property on course in a loop.
# school_year = self.school_year
# for course in courses:
#     course.school_year = school_year
# return courses

# def get_active_courses(self):
#     """Get the courses that are active."""
#     return [course for course in self.get_ordered_courses() if course.is_active]

# def move_course_down(self, course):
#     """Move a course down in the grade level ordering.

#     This method assumes that the course is part of the grade level.
#     """
#     through = self.courses.through.objects.get(
#         grade_level_id=self.id, course_id=course.id
#     )
#     through.down()

# def move_course_up(self, course):
#     """Move a course up in the grade level ordering.

#     This method assumes that the course is part of the grade level.
#     """
#     through = self.courses.through.objects.get(
#         grade_level_id=self.id, course_id=course.id
#     )
#     through.up()

# def __str__(self):
#     return self.name


class SchoolBreak(models.Model):
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE, related_name=_("+"))
    break_name = models.CharField(
        max_length=100, help_text=_("Holiday name -> Independence Day")
    )
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.term} - {self.break_name}"

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.break_name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("School Breaks")


class SchoolAttributes(models.Model):
    pass


class SchoolAnnouncement(models.Model):
    pass


class SchoolSummerClass(models.Model):
    session = models.ForeignKey(
        SchoolSession, on_delete=models.CASCADE, related_name=_("summer_class")
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.session__school} - {self.start_date} - {self.end_date}"
