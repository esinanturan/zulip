from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.db.models import OuterRef


def set_default_value_for_can_mention_many_users_group(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    Realm = apps.get_model("zerver", "Realm")
    NamedUserGroup = apps.get_model("zerver", "NamedUserGroup")

    wildcard_mention_policy_to_group_name = {
        1: "role:everyone",
        2: "role:members",
        3: "role:fullmembers",
        5: "role:administrators",
        6: "role:nobody",
        7: "role:moderators",
    }

    for id, group_name in wildcard_mention_policy_to_group_name.items():
        Realm.objects.filter(can_mention_many_users_group=None, wildcard_mention_policy=id).update(
            can_mention_many_users_group=NamedUserGroup.objects.filter(
                name=group_name, realm=OuterRef("id"), is_system_group=True
            ).values("pk")
        )


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("zerver", "0668_realm_can_mention_many_users_group"),
    ]

    operations = [
        migrations.RunPython(
            set_default_value_for_can_mention_many_users_group,
            elidable=True,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
