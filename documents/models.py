from django.db import models
import datetime

# Enum for DocumentType
SINGLE_USER = 'SINGLE_USER'
ALL_USERS = 'ALL_USERS'
ADMINS_ONLY = 'ADMINS_ONLY'
RESTAURANTS_ONLY = 'RESTAURANTS_ONLY'
PROGRAMS_ONLY = 'PROGRAMS_ONLY'
COURIERS_ONLY = 'COURIERS_ONLY'
HIDDEN = 'HIDDEN'

DOCUMENT_OPTIONS = [
    (SINGLE_USER, 'single user'),
    (ALL_USERS, 'all users'),
    (ADMINS_ONLY, 'admins only'),
    (RESTAURANTS_ONLY, 'restaurants only'),
    (COURIERS_ONLY, 'couriers only'),
    (PROGRAMS_ONLY, 'programs only'),
    (HIDDEN, 'hidden'),
]

PROGRAM = 'PR'
RESTAURANT = 'RE'
BOTH = 'BOTH'
NONE = 'NONE'

OWNER_TYPES = [
    (PROGRAM, 'program'),
    (RESTAURANT, 'restaurant'),
    (NONE, 'none')
]

PERMISSION = [
    (PROGRAM, 'program'),
    (RESTAURANT, 'restaurant'),
    (BOTH, 'both')
]


class NoteManager(models.Manager):
    """Manager for Note class"""

    def create_note(self, note_name, note_content, owner_type, program_id=None, restaurant_id=None):
        new_note = Note()

        new_note.note_name = note_name
        new_note.note_content = note_content
        new_note.owner_type = owner_type

        if owner_type == 'PR':
            new_note.program_id = program_id
        elif owner_type == 'RE':
            new_note.restaurant_id = restaurant_id

        new_note.save(using=self._db)
        return new_note


class Note(models.Model):
    """Note created by users/admins"""
    created_at = models.DateTimeField(auto_now=True)
    note_name = models.CharField(max_length=15)
    note_content = models.CharField(max_length=30)
    objects = NoteManager

    owner_type = models.CharField(
        max_length=20,
        choices=OWNER_TYPES,
        default=NONE,
    )

    program_id = models.ForeignKey('profiles.Program', related_name="program_notes", on_delete=models.DO_NOTHING,
                                null=True)
    restaurant_id = models.ForeignKey('profiles.Restaurant', related_name="restaurant_notes",
                                    on_delete=models.DO_NOTHING, null=True)

    class Meta:
        """Metadata for the note class."""
        ordering = ["-created_at"]

class DocumentManager(models.Manager):
    """Manager for Note class"""

    def create_document(self, name, owner_type, size):
        new_document = Document()

        new_document.name = name
        new_document.created_at = datetime.datetime.now()
        new_document.owner_type = owner_type
        new_document.size = size
        new_document.is_deleted = False
        new_document.save(using=self._db)

        return new_document


class Document(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    size = models.CharField(max_length=50, null=True)
    owner_type = models.CharField(
        max_length=20,
        choices=PERMISSION,
        default=NONE,
    )

    is_deleted = models.BooleanField()

    def __str__(self):
        return str(self.name)
