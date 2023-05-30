CHOICES_VERSION = (
    ('1.19.4', '1.19.4'),
    ('1.18.2', '1.18.2'),
    ('1.17.1', '1.17.1'),
    ('1.16.5', '1.16.5'),
    ('1.15.2', '1.15.2'),
    ('1.14.4', '1.14.4'),
    ('1.13.2', '1.13.2'),
    ('1.12.2', '1.12.2'),
    ('1.11.2', '1.11.2'),
    ('1.10.2', '1.10.2'),
    ('1.9.4', '1.9.4'),
    ('1.8.9', '1.8.9'),
    ('1.7.10', '1.7.10'),
    ('1.6.4', '1.6.4'),
    ('1.5.2', '1.5.2'),
)
CHOICES_MODPACK = (
    ('sevtech-ages', 'sevtech-ages'),
)
CHOICES_GAMEMODE = (
    ("creative", "creative"),
    ("survival", "survival"),
    ("adventure", "adventure"),
    ("spectator", "spectator"),
)
CHOICES_DIFFICULTY = (
    ("peaceful", "peaceful"),
    ("easy", "easy"),
    ("normal", "normal"),
    ("hard", "hard"),
)
CHOICES_PLAN = (
    ('Free', 'Free'),
    ('Budget', 'Budget'),
    ('Boost', 'Boost'),
)


def user_directory_path(instance, filename):
    return 'users/user_{0}/{1}'.format(instance.id, 'logo' + filename[filename.find('.'):])
